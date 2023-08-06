# Copyright 2021, The TensorFlow Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""`DPQuery`s for differentially private tree aggregation protocols.

`TreeCumulativeSumQuery` and `TreeResidualSumQuery` are `DPQuery`s for continual
online observation queries relying on `tree_aggregation`. 'Online' means that
the leaf nodes of the tree arrive one by one as the time proceeds. The core
logic of tree aggregation is implemented in `tree_aggregation.TreeAggregator`
and `tree_aggregation.EfficientTreeAggregator`.
"""
import distutils
import math

import attr
import tensorflow as tf
from tensorflow_privacy.privacy.analysis import dp_event
from tensorflow_privacy.privacy.dp_query import distributed_discrete_gaussian_query
from tensorflow_privacy.privacy.dp_query import dp_query
from tensorflow_privacy.privacy.dp_query import gaussian_query
from tensorflow_privacy.privacy.dp_query import tree_aggregation

# TODO(b/193679963): define `RestartQuery` and move `RestartIndicator` to be
# in the same module.


class TreeCumulativeSumQuery(dp_query.SumAggregationDPQuery):
  """Returns private cumulative sums by clipping and adding correlated noise.

  Consider calling `get_noised_result` T times, and each (x_i, i=0,2,...,T-1) is
  the private value returned by `accumulate_record`, i.e. x_i = sum_{j=0}^{n-1}
  x_{i,j} where each x_{i,j} is a private record in the database. This class is
  intended to make multiple queries, which release privatized values of the
  cumulative sums s_i = sum_{k=0}^{i} x_k, for i=0,...,T-1.
  Each call to `get_noised_result` releases the next cumulative sum s_i, which
  is in contrast to the GaussianSumQuery that releases x_i. Noise for the
  cumulative sums is accomplished using the tree aggregation logic in
  `tree_aggregation`, which is proportional to log(T).

  Example usage:
    query = TreeCumulativeSumQuery(...)
    global_state = query.initial_global_state()
    params = query.derive_sample_params(global_state)
    for i, samples in enumerate(streaming_samples):
      sample_state = query.initial_sample_state(samples[0])
      # Compute  x_i = sum_{j=0}^{n-1} x_{i,j}
      for j,sample in enumerate(samples):
        sample_state = query.accumulate_record(params, sample_state, sample)
      # noised_cumsum is privatized estimate of s_i
      noised_cumsum, global_state, event = query.get_noised_result(
        sample_state, global_state)

  Attributes:
    clip_fn: Callable that specifies clipping function. `clip_fn` receives two
      arguments: a flat list of vars in a record and a `clip_value` to clip the
        corresponding record, e.g. clip_fn(flat_record, clip_value).
    clip_value: float indicating the value at which to clip the record.
    record_specs: `Collection[tf.TensorSpec]` specifying shapes of records.
    tree_aggregator: `tree_aggregation.TreeAggregator` initialized with user
      defined `noise_generator`. `noise_generator` is a
      `tree_aggregation.ValueGenerator` to generate the noise value for a tree
      node. Noise stdandard deviation is specified outside the `dp_query` by the
      user when defining `noise_fn` and should have order
      O(clip_norm*log(T)/eps) to guarantee eps-DP.
  """

  @attr.s(frozen=True)
  class GlobalState(object):
    """Class defining global state for Tree sum queries.

    Attributes:
      tree_state: Current state of noise tree keeping track of current leaf and
        each level state.
      clip_value: The clipping value to be passed to clip_fn.
      samples_cumulative_sum: Noiseless cumulative sum of samples over time.
    """
    tree_state = attr.ib()
    clip_value = attr.ib()
    samples_cumulative_sum = attr.ib()

  def __init__(self,
               record_specs,
               noise_generator,
               clip_fn,
               clip_value,
               use_efficient=True):
    """Initializes the `TreeCumulativeSumQuery`.

    Consider using `build_l2_gaussian_query` for the construction of a
    `TreeCumulativeSumQuery` with L2 norm clipping and Gaussian noise.

    Args:
      record_specs: A nested structure of `tf.TensorSpec`s specifying structure
        and shapes of records.
      noise_generator: `tree_aggregation.ValueGenerator` to generate the noise
        value for a tree node. Should be coupled with clipping norm to guarantee
        privacy.
      clip_fn: Callable that specifies clipping function. Input to clip is a
        flat list of vars in a record.
      clip_value: Float indicating the value at which to clip the record.
      use_efficient: Boolean indicating the usage of the efficient tree
        aggregation algorithm based on the paper "Efficient Use of
        Differentially Private Binary Trees".
    """
    self._clip_fn = clip_fn
    self._clip_value = clip_value
    self._record_specs = record_specs
    if use_efficient:
      self._tree_aggregator = tree_aggregation.EfficientTreeAggregator(
          noise_generator)
    else:
      self._tree_aggregator = tree_aggregation.TreeAggregator(noise_generator)

  def initial_global_state(self):
    """Implements `tensorflow_privacy.DPQuery.initial_global_state`."""
    initial_tree_state = self._tree_aggregator.init_state()
    initial_samples_cumulative_sum = tf.nest.map_structure(
        lambda spec: tf.zeros(spec.shape), self._record_specs)
    return TreeCumulativeSumQuery.GlobalState(
        tree_state=initial_tree_state,
        clip_value=tf.constant(self._clip_value, tf.float32),
        samples_cumulative_sum=initial_samples_cumulative_sum)

  def derive_sample_params(self, global_state):
    """Implements `tensorflow_privacy.DPQuery.derive_sample_params`."""
    return global_state.clip_value

  def preprocess_record(self, params, record):
    """Implements `tensorflow_privacy.DPQuery.preprocess_record`.

    Args:
      params: `clip_value` for the record.
      record: The record to be processed.

    Returns:
      Structure of clipped tensors.
    """
    clip_value = params
    record_as_list = tf.nest.flatten(record)
    clipped_as_list = self._clip_fn(record_as_list, clip_value)
    return tf.nest.pack_sequence_as(record, clipped_as_list)

  def get_noised_result(self, sample_state, global_state):
    """Implements `tensorflow_privacy.DPQuery.get_noised_result`.

    Updates tree state, and returns noised cumulative sum and updated state.

    Computes new cumulative sum, and returns its noised value. Grows tree state
    by one new leaf, and returns the new state.

    Args:
      sample_state: Sum of clipped records for this round.
      global_state: Global state with current sample's cumulative sum and tree
        state.

    Returns:
      A tuple of (noised_cumulative_sum, new_global_state).
    """
    new_cumulative_sum = tf.nest.map_structure(
        tf.add, global_state.samples_cumulative_sum, sample_state)
    cumulative_sum_noise, new_tree_state = self._tree_aggregator.get_cumsum_and_update(
        global_state.tree_state)
    noised_cumulative_sum = tf.nest.map_structure(tf.add, new_cumulative_sum,
                                                  cumulative_sum_noise)
    new_global_state = attr.evolve(
        global_state,
        samples_cumulative_sum=new_cumulative_sum,
        tree_state=new_tree_state)
    event = dp_event.UnsupportedDpEvent()
    return noised_cumulative_sum, new_global_state, event

  def reset_state(self, noised_results, global_state):
    """Returns state after resetting the tree.

    This function will be used in `restart_query.RestartQuery` after calling
    `get_noised_result` when the restarting condition is met.

    Args:
      noised_results: Noised cumulative sum returned by `get_noised_result`.
      global_state: Updated global state returned by `get_noised_result`, which
        has current sample's cumulative sum and tree state for the next
        cumulative sum.

    Returns:
      New global state with current noised cumulative sum and restarted tree
        state for the next cumulative sum.
    """
    new_tree_state = self._tree_aggregator.reset_state(global_state.tree_state)
    return attr.evolve(
        global_state,
        samples_cumulative_sum=noised_results,
        tree_state=new_tree_state)

  @classmethod
  def build_l2_gaussian_query(cls,
                              clip_norm,
                              noise_multiplier,
                              record_specs,
                              noise_seed=None,
                              use_efficient=True):
    """Returns a query instance with L2 norm clipping and Gaussian noise.

    Args:
      clip_norm: Each record will be clipped so that it has L2 norm at most
        `clip_norm`.
      noise_multiplier: The effective noise multiplier for the sum of records.
        Noise standard deviation is `clip_norm*noise_multiplier`.
      record_specs: A nested structure of `tf.TensorSpec`s specifying structure
        and shapes of records.
      noise_seed: Integer seed for the Gaussian noise generator. If `None`, a
        nondeterministic seed based on system time will be generated.
      use_efficient: Boolean indicating the usage of the efficient tree
        aggregation algorithm based on the paper "Efficient Use of
        Differentially Private Binary Trees".
    """
    if clip_norm <= 0:
      raise ValueError(f'`clip_norm` must be positive, got {clip_norm}.')

    if noise_multiplier < 0:
      raise ValueError(
          f'`noise_multiplier` must be non-negative, got {noise_multiplier}.')

    gaussian_noise_generator = tree_aggregation.GaussianNoiseGenerator(
        noise_std=clip_norm * noise_multiplier,
        specs=record_specs,
        seed=noise_seed)

    def l2_clip_fn(record_as_list, clip_norm):
      clipped_record, _ = tf.clip_by_global_norm(record_as_list, clip_norm)
      return clipped_record

    return cls(
        clip_fn=l2_clip_fn,
        clip_value=clip_norm,
        record_specs=record_specs,
        noise_generator=gaussian_noise_generator,
        use_efficient=use_efficient)


class TreeResidualSumQuery(dp_query.SumAggregationDPQuery):
  """Implements DPQuery for adding correlated noise through tree structure.

  Clips and sums records in current sample x_i = sum_{j=0}^{n-1} x_{i,j};
  returns the current sample adding the noise residual from tree aggregation.
  The returned value is conceptually equivalent to the following: calculates
  cumulative sum of samples over time s_i = sum_{k=0}^i x_i (instead of only
  current sample) with added noise by tree aggregation protocol that is
  proportional to log(T), T being the number of times the query is called; r
  eturns the residual between the current noised cumsum noised(s_i) and the
  previous one noised(s_{i-1}) when the query is called.

  This can be used as a drop-in replacement for `GaussianSumQuery`, and can
  offer stronger utility/privacy tradeoffs when aplification-via-sampling is not
  possible, or when privacy epsilon is relativly large.  This may result in
  more noise by a log(T) factor in each individual estimate of x_i, but if the
  x_i are used in the underlying code to compute cumulative sums, the noise in
  those sums can be less. That is, this allows us to adapt code that was written
  to use a regular `SumQuery` to benefit from the tree aggregation protocol.

  Combining this query with a SGD optimizer can be used to implement the
  DP-FTRL algorithm in
  "Practical and Private (Deep) Learning without Sampling or Shuffling".

  Example usage:
    query = TreeResidualSumQuery(...)
    global_state = query.initial_global_state()
    params = query.derive_sample_params(global_state)
    for i, samples in enumerate(streaming_samples):
      sample_state = query.initial_sample_state(samples[0])
      # Compute  x_i = sum_{j=0}^{n-1} x_{i,j}
      for j,sample in enumerate(samples):
        sample_state = query.accumulate_record(params, sample_state, sample)
      # noised_sum is privatized estimate of x_i by conceptually postprocessing
      # noised cumulative sum s_i
      noised_sum, global_state, event = query.get_noised_result(
        sample_state, global_state)

  Attributes:
    clip_fn: Callable that specifies clipping function. `clip_fn` receives two
      arguments: a flat list of vars in a record and a `clip_value` to clip the
        corresponding record, e.g. clip_fn(flat_record, clip_value).
    clip_value: float indicating the value at which to clip the record.
    record_specs: A nested structure of `tf.TensorSpec`s specifying structure
      and shapes of records.
    tree_aggregator: `tree_aggregation.TreeAggregator` initialized with user
      defined `noise_generator`. `noise_generator` is a
      `tree_aggregation.ValueGenerator` to generate the noise value for a tree
      node. Noise stdandard deviation is specified outside the `dp_query` by the
      user when defining `noise_fn` and should have order
      O(clip_norm*log(T)/eps) to guarantee eps-DP.
  """

  @attr.s(frozen=True)
  class GlobalState(object):
    """Class defining global state for Tree sum queries.

    Attributes:
      tree_state: Current state of noise tree keeping track of current leaf and
        each level state.
      clip_value: The clipping value to be passed to clip_fn.
      previous_tree_noise: Cumulative noise by tree aggregation from the
        previous time the query is called on a sample.
    """
    tree_state = attr.ib()
    clip_value = attr.ib()
    previous_tree_noise = attr.ib()

  def __init__(self,
               record_specs,
               noise_generator,
               clip_fn,
               clip_value,
               use_efficient=True):
    """Initializes the `TreeCumulativeSumQuery`.

    Consider using `build_l2_gaussian_query` for the construction of a
    `TreeCumulativeSumQuery` with L2 norm clipping and Gaussian noise.

    Args:
      record_specs: A nested structure of `tf.TensorSpec`s specifying structure
        and shapes of records.
      noise_generator: `tree_aggregation.ValueGenerator` to generate the noise
        value for a tree node. Should be coupled with clipping norm to guarantee
        privacy.
      clip_fn: Callable that specifies clipping function. Input to clip is a
        flat list of vars in a record.
      clip_value: Float indicating the value at which to clip the record.
      use_efficient: Boolean indicating the usage of the efficient tree
        aggregation algorithm based on the paper "Efficient Use of
        Differentially Private Binary Trees".
    """
    self._clip_fn = clip_fn
    self._clip_value = clip_value
    self._record_specs = record_specs
    if use_efficient:
      self._tree_aggregator = tree_aggregation.EfficientTreeAggregator(
          noise_generator)
    else:
      self._tree_aggregator = tree_aggregation.TreeAggregator(noise_generator)

  def _zero_initial_noise(self):
    return tf.nest.map_structure(lambda spec: tf.zeros(spec.shape),
                                 self._record_specs)

  def initial_global_state(self):
    """Implements `tensorflow_privacy.DPQuery.initial_global_state`."""
    initial_tree_state = self._tree_aggregator.init_state()
    return TreeResidualSumQuery.GlobalState(
        tree_state=initial_tree_state,
        clip_value=tf.constant(self._clip_value, tf.float32),
        previous_tree_noise=self._zero_initial_noise())

  def derive_sample_params(self, global_state):
    """Implements `tensorflow_privacy.DPQuery.derive_sample_params`."""
    return global_state.clip_value

  def preprocess_record(self, params, record):
    """Implements `tensorflow_privacy.DPQuery.preprocess_record`.

    Args:
      params: `clip_value` for the record.
      record: The record to be processed.

    Returns:
      Structure of clipped tensors.
    """
    clip_value = params
    record_as_list = tf.nest.flatten(record)
    clipped_as_list = self._clip_fn(record_as_list, clip_value)
    return tf.nest.pack_sequence_as(record, clipped_as_list)

  def get_noised_result(self, sample_state, global_state):
    """Implements `tensorflow_privacy.DPQuery.get_noised_result`.

    Updates tree state, and returns residual of noised cumulative sum.

    Args:
      sample_state: Sum of clipped records for this round.
      global_state: Global state with current samples cumulative sum and tree
        state.

    Returns:
      A tuple of (noised_cumulative_sum, new_global_state).
    """
    tree_noise, new_tree_state = self._tree_aggregator.get_cumsum_and_update(
        global_state.tree_state)
    noised_sample = tf.nest.map_structure(lambda a, b, c: a + b - c,
                                          sample_state, tree_noise,
                                          global_state.previous_tree_noise)
    new_global_state = attr.evolve(
        global_state, previous_tree_noise=tree_noise, tree_state=new_tree_state)
    event = dp_event.UnsupportedDpEvent()
    return noised_sample, new_global_state, event

  def reset_state(self, noised_results, global_state):
    """Returns state after resetting the tree.

    This function will be used in `restart_query.RestartQuery` after calling
    `get_noised_result` when the restarting condition is met.

    Args:
      noised_results: Noised cumulative sum returned by `get_noised_result`.
      global_state: Updated global state returned by `get_noised_result`, which
        records noise for the conceptual cumulative sum of the current leaf
        node, and tree state for the next conceptual cumulative sum.

    Returns:
      New global state with zero noise and restarted tree state.
    """
    del noised_results
    new_tree_state = self._tree_aggregator.reset_state(global_state.tree_state)
    return attr.evolve(
        global_state,
        previous_tree_noise=self._zero_initial_noise(),
        tree_state=new_tree_state)

  @classmethod
  def build_l2_gaussian_query(cls,
                              clip_norm,
                              noise_multiplier,
                              record_specs,
                              noise_seed=None,
                              use_efficient=True):
    """Returns `TreeResidualSumQuery` with L2 norm clipping and Gaussian noise.

    Args:
      clip_norm: Each record will be clipped so that it has L2 norm at most
        `clip_norm`.
      noise_multiplier: The effective noise multiplier for the sum of records.
        Noise standard deviation is `clip_norm*noise_multiplier`.
      record_specs: A nested structure of `tf.TensorSpec`s specifying structure
        and shapes of records.
      noise_seed: Integer seed for the Gaussian noise generator. If `None`, a
        nondeterministic seed based on system time will be generated.
      use_efficient: Boolean indicating the usage of the efficient tree
        aggregation algorithm based on the paper "Efficient Use of
        Differentially Private Binary Trees".
    """
    if clip_norm <= 0:
      raise ValueError(f'`clip_norm` must be positive, got {clip_norm}.')

    if noise_multiplier < 0:
      raise ValueError(
          f'`noise_multiplier` must be non-negative, got {noise_multiplier}.')

    gaussian_noise_generator = tree_aggregation.GaussianNoiseGenerator(
        noise_std=clip_norm * noise_multiplier,
        specs=record_specs,
        seed=noise_seed)

    def l2_clip_fn(record_as_list, clip_norm):
      clipped_record, _ = tf.clip_by_global_norm(record_as_list, clip_norm)
      return clipped_record

    return cls(
        clip_fn=l2_clip_fn,
        clip_value=clip_norm,
        record_specs=record_specs,
        noise_generator=gaussian_noise_generator,
        use_efficient=use_efficient)


# TODO(b/197596864): Remove `TreeRangeSumQuery` from this file after the next
# TFP release


@tf.function
def _build_tree_from_leaf(leaf_nodes: tf.Tensor, arity: int) -> tf.RaggedTensor:
  """A function constructs a complete tree given all the leaf nodes.

  The function takes a 1-D array representing the leaf nodes of a tree and the
  tree's arity, and constructs a complete tree by recursively summing the
  adjacent children to get the parent until reaching the root node. Because we
  assume a complete tree, if the number of leaf nodes does not divide arity, the
  leaf nodes will be padded with zeros.

  Args:
    leaf_nodes: A 1-D array storing the leaf nodes of the tree.
    arity: A `int` for the branching factor of the tree, i.e. the number of
      children for each internal node.

  Returns:
    `tf.RaggedTensor` representing the tree. For example, if
    `leaf_nodes=tf.Tensor([1, 2, 3, 4])` and `arity=2`, then the returned value
    should be `tree=tf.RaggedTensor([[10],[3,7],[1,2,3,4]])`. In this way,
    `tree[layer][index]` can be used to access the node indexed by (layer,
    index) in the tree,
  """

  def pad_zero(leaf_nodes, size):
    paddings = [[0, size - len(leaf_nodes)]]
    return tf.pad(leaf_nodes, paddings)

  leaf_nodes_size = tf.constant(len(leaf_nodes), dtype=tf.float32)
  num_layers = tf.math.ceil(
      tf.math.log(leaf_nodes_size) /
      tf.math.log(tf.cast(arity, dtype=tf.float32))) + 1
  leaf_nodes = pad_zero(
      leaf_nodes, tf.math.pow(tf.cast(arity, dtype=tf.float32), num_layers - 1))

  def _shrink_layer(layer: tf.Tensor, arity: int) -> tf.Tensor:
    return tf.reduce_sum((tf.reshape(layer, (-1, arity))), 1)

  # The following `tf.while_loop` constructs the tree from bottom up by
  # iteratively applying `_shrink_layer` to each layer of the tree. The reason
  # for the choice of TF1.0-style `tf.while_loop` is that @tf.function does not
  # support auto-translation from python loop to tf loop when loop variables
  # contain a `RaggedTensor` whose shape changes across iterations.

  idx = tf.identity(num_layers)
  loop_cond = lambda i, h: tf.less_equal(2.0, i)

  def _loop_body(i, h):
    return [
        tf.add(i, -1.0),
        tf.concat(([_shrink_layer(h[0], arity)], h), axis=0)
    ]

  _, tree = tf.while_loop(
      loop_cond,
      _loop_body, [idx, tf.RaggedTensor.from_tensor([leaf_nodes])],
      shape_invariants=[
          idx.get_shape(),
          tf.RaggedTensorSpec(dtype=leaf_nodes.dtype, ragged_rank=1)
      ])

  return tree


class TreeRangeSumQuery(dp_query.SumAggregationDPQuery):
  """Implements dp_query for accurate range queries using tree aggregation.

  Implements a variant of the tree aggregation protocol from. "Is interaction
  necessary for distributed private learning?. Adam Smith, Abhradeep Thakurta,
  Jalaj Upadhyay." Builds a tree on top of the input record and adds noise to
  the tree for differential privacy. Any range query can be decomposed into the
  sum of O(log(n)) nodes in the tree compared to O(n) when using a histogram.
  Improves efficiency and reduces noise scale.
  """

  @attr.s(frozen=True)
  class GlobalState(object):
    """Class defining global state for TreeRangeSumQuery.

    Attributes:
      arity: The branching factor of the tree (i.e. the number of children each
        internal node has).
      inner_query_state: The global state of the inner query.
    """
    arity = attr.ib()
    inner_query_state = attr.ib()

  def __init__(self,
               inner_query: dp_query.SumAggregationDPQuery,
               arity: int = 2):
    """Initializes the `TreeRangeSumQuery`.

    Args:
      inner_query: The inner `DPQuery` that adds noise to the tree.
      arity: The branching factor of the tree (i.e. the number of children each
        internal node has). Defaults to 2.
    """
    self._inner_query = inner_query
    self._arity = arity

    if self._arity < 1:
      raise ValueError(f'Invalid arity={arity} smaller than 2.')

  def initial_global_state(self):
    """Implements `tensorflow_privacy.DPQuery.initial_global_state`."""
    return TreeRangeSumQuery.GlobalState(
        arity=self._arity,
        inner_query_state=self._inner_query.initial_global_state())

  def derive_sample_params(self, global_state):
    """Implements `tensorflow_privacy.DPQuery.derive_sample_params`."""
    return (global_state.arity,
            self._inner_query.derive_sample_params(
                global_state.inner_query_state))

  def preprocess_record(self, params, record):
    """Implements `tensorflow_privacy.DPQuery.preprocess_record`.

    This method builds the tree, flattens it and applies
    `inner_query.preprocess_record` to the flattened tree.

    Args:
      params: Hyper-parameters for preprocessing record.
      record: A histogram representing the leaf nodes of the tree.

    Returns:
      A `tf.Tensor` representing the flattened version of the preprocessed tree.
    """
    arity, inner_query_params = params
    preprocessed_record = _build_tree_from_leaf(record, arity).flat_values
    # The following codes reshape the output vector so the output shape of can
    # be statically inferred. This is useful when used with
    # `tff.aggregators.DifferentiallyPrivateFactory` because it needs to know
    # the output shape of this function statically and explicitly.
    preprocessed_record_shape = [
        (self._arity**(math.ceil(math.log(record.shape[0], self._arity)) + 1) -
         1) // (self._arity - 1)
    ]
    preprocessed_record = tf.reshape(preprocessed_record,
                                     preprocessed_record_shape)
    preprocessed_record = self._inner_query.preprocess_record(
        inner_query_params, preprocessed_record)

    return preprocessed_record

  def get_noised_result(self, sample_state, global_state):
    """Implements `tensorflow_privacy.DPQuery.get_noised_result`.

    This function re-constructs the `tf.RaggedTensor` from the flattened tree
    output by `preprocess_records.`

    Args:
      sample_state: A `tf.Tensor` for the flattened tree.
      global_state: The global state of the protocol.

    Returns:
      A `tf.RaggedTensor` representing the tree.
    """
    # The [0] is needed because of how tf.RaggedTensor.from_two_splits works.
    # print(tf.RaggedTensor.from_row_splits(values=[3, 1, 4, 1, 5, 9, 2, 6],
    #                                       row_splits=[0, 4, 4, 7, 8, 8]))
    # <tf.RaggedTensor [[3, 1, 4, 1], [], [5, 9, 2], [6], []]>
    # This part is not written in tensorflow and will be executed on the server
    # side instead of the client side if used with
    # tff.aggregators.DifferentiallyPrivateFactory for federated learning.
    sample_state, inner_query_state, _ = self._inner_query.get_noised_result(
        sample_state, global_state.inner_query_state)
    new_global_state = TreeRangeSumQuery.GlobalState(
        arity=global_state.arity, inner_query_state=inner_query_state)

    row_splits = [0] + [
        (self._arity**(x + 1) - 1) // (self._arity - 1) for x in range(
            math.floor(math.log(sample_state.shape[0], self._arity)) + 1)
    ]
    tree = tf.RaggedTensor.from_row_splits(
        values=sample_state, row_splits=row_splits)
    event = dp_event.UnsupportedDpEvent()
    return tree, new_global_state, event

  @classmethod
  def build_central_gaussian_query(cls,
                                   l2_norm_clip: float,
                                   stddev: float,
                                   arity: int = 2):
    """Returns `TreeRangeSumQuery` with central Gaussian noise.

    Args:
      l2_norm_clip: Each record should be clipped so that it has L2 norm at most
        `l2_norm_clip`.
      stddev: Stddev of the central Gaussian noise.
      arity: The branching factor of the tree (i.e. the number of children each
        internal node has). Defaults to 2.
    """
    if l2_norm_clip <= 0:
      raise ValueError(f'`l2_norm_clip` must be positive, got {l2_norm_clip}.')

    if stddev < 0:
      raise ValueError(f'`stddev` must be non-negative, got {stddev}.')

    if arity < 2:
      raise ValueError(f'`arity` must be at least 2, got {arity}.')

    inner_query = gaussian_query.GaussianSumQuery(l2_norm_clip, stddev)

    return cls(arity=arity, inner_query=inner_query)

  @classmethod
  def build_distributed_discrete_gaussian_query(cls,
                                                l2_norm_bound: float,
                                                local_stddev: float,
                                                arity: int = 2):
    """Returns `TreeRangeSumQuery` with central Gaussian noise.

    Args:
      l2_norm_bound: Each record should be clipped so that it has L2 norm at
        most `l2_norm_bound`.
      local_stddev: Scale/stddev of the local discrete Gaussian noise.
      arity: The branching factor of the tree (i.e. the number of children each
        internal node has). Defaults to 2.
    """
    if l2_norm_bound <= 0:
      raise ValueError(
          f'`l2_clip_bound` must be positive, got {l2_norm_bound}.')

    if local_stddev < 0:
      raise ValueError(
          f'`local_stddev` must be non-negative, got {local_stddev}.')

    if arity < 2:
      raise ValueError(f'`arity` must be at least 2, got {arity}.')

    inner_query = distributed_discrete_gaussian_query.DistributedDiscreteGaussianSumQuery(
        l2_norm_bound, local_stddev)

    return cls(arity=arity, inner_query=inner_query)


def _get_add_noise(stddev, seed: int = None):
  """Utility function to decide which `add_noise` to use according to tf version."""
  if distutils.version.LooseVersion(
      tf.__version__) < distutils.version.LooseVersion('2.0.0'):

    # The seed should be only used for testing purpose.
    if seed is not None:
      tf.random.set_seed(seed)

    def add_noise(v):
      return v + tf.random.normal(
          tf.shape(input=v), stddev=stddev, dtype=v.dtype)
  else:
    random_normal = tf.random_normal_initializer(stddev=stddev, seed=seed)

    def add_noise(v):
      return v + tf.cast(random_normal(tf.shape(input=v)), dtype=v.dtype)

  return add_noise
