# Copyright 2021 The DDSP Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""Library of base Processor and ProcessorGroup.

ProcessorGroup exists as an alternative to manually specifying the forward
propagation in python. The advantage is that a variety of configurations can be
programmatically specified via external dependency injection, such as with the
`gin` library.
"""

from typing import Dict, Text

from ddsp import core
from ddsp import dags
import gin
import tensorflow as tf

tfkl = tf.keras.layers

# Define Types.
TensorDict = Dict[Text, tf.Tensor]


# Processor Base Class ---------------------------------------------------------
class Processor(tfkl.Layer):
  """Abstract base class for signal processors.

  Since most effects / synths require specificly formatted control signals
  (such as amplitudes and frequenices), each processor implements a
  get_controls(inputs) method, where inputs are a variable number of tensor
  arguments that are typically neural network outputs. Check each child class
  for the class-specific arguments it expects. This gives a dictionary of
  controls that can then be passed to get_signal(controls). The
  get_outputs(inputs) method calls both in succession and returns a nested
  output dictionary with all controls and signals.
  """

  def __init__(self, name: Text, trainable: bool = False):
    super().__init__(name=name, trainable=trainable, autocast=False)

  def call(self,
           *args: tf.Tensor,
           return_outputs_dict: bool = False,
           **kwargs) -> tf.Tensor:
    """Convert input tensors arguments into a signal tensor."""
    # Don't use `training` or `mask` arguments from keras.Layer.
    for k in ['training', 'mask']:
      if k in kwargs:
        _ = kwargs.pop(k)

    controls = self.get_controls(*args, **kwargs)
    signal = self.get_signal(**controls)
    if return_outputs_dict:
      return dict(signal=signal, controls=controls)
    else:
      return signal

  def get_controls(self, *args: tf.Tensor, **kwargs: tf.Tensor) -> TensorDict:
    """Convert input tensor arguments into a dict of processor controls."""
    raise NotImplementedError

  def get_signal(self, *args: tf.Tensor, **kwargs: tf.Tensor) -> tf.Tensor:
    """Convert control tensors into a signal tensor."""
    raise NotImplementedError


@gin.configurable
class ProcessorGroup(dags.DAGLayer):
  """String Proccesor() objects together into a processor_group."""

  def __init__(self, dag: dags.DAG, **kwarg_processors):
    """Constructor, completely configurable via gin.

    Args:
      dag: A directed acyclical graph in the form of a list of nodes. Each node
        has the form

        ['module', ['input_key', ...], ['output_key', ...]]

        'module': Module instance or string name of module. For example,
          'reverb' woud access the attribute `processor_group.reverb`.
        'input_key': List of strings, nested keys in dictionary of dag outputs.
          For example, 'inputs/f0_hz' would access `outputs[inputs]['f0_hz']`.
          Inputs to the dag are wrapped in a `inputs` dict as shown in the
          example. This list is ordered and has one key per a module input
          argument. Each node's outputs are prefixed by their module name.
        'output_key': List of strings, keys for each return value of the module.
          For example, ['amps', 'freqs'] would have the module return a dict
          {'module_name': {'amps': return_value_0, 'freqs': return_value_1}}.
          If the module returns a dictionary, the keys of the dictionary will be
          used and these values (if provided) will be ignored.

        The graph is read sequentially and must be topologically sorted. This
        means that all inputs for a module must already be generated by earlier
        modules (or in the input dictionary).
      **kwarg_processors: Processor instances to add to ProcessorGroup. Each
        kwarg Processor will be added as a property of the layer, so that it
        will be accessible as `processor_group.kwarg`. Also, other keras kwargs
        such as 'name' are split off before adding modules.
    """
    super().__init__(dag, **kwarg_processors)
    self.processor_names = self.module_names

  @property
  def processors(self):
    """Processor getter."""
    return [getattr(self, name) for name in self.processor_names]

  def call(self,
           inputs: TensorDict,
           return_outputs_dict: bool = False,
           **kwargs) -> tf.Tensor:
    """Convert input tensors arguments into a signal tensor."""
    controls = self.get_controls(inputs, **kwargs)
    signal = self.get_signal(controls)
    if return_outputs_dict:
      return dict(signal=signal, controls=controls)
    else:
      return signal

  def get_controls(self, inputs: TensorDict, **kwargs) -> TensorDict:
    """Run the DAG and get complete outputs dictionary for the processor_group.

    Args:
      inputs: A dictionary of input tensors fed to the signal processing
        processor_group.
      **kwargs: Other kwargs for all the modules in the dag.

    Returns:
      A nested dictionary of all the output tensors.
    """
    # Also build layer on get_controls(), instead of just __call__().
    self.built = True
    return super().call(inputs, **kwargs)

  def get_signal(self, outputs: TensorDict) -> tf.Tensor:
    """Extract the output signal from the dag outputs.

    Args:
      outputs: A dictionary of tensors output from self.get_controls().

    Returns:
      Signal tensor.
    """
    # Get output signal from last processor.
    return outputs['out']['signal']


# Routing processors for manipulating signals in a processor_group -------------
@gin.register
class Add(Processor):
  """Sum two signals."""

  def __init__(self, name: Text = 'add'):
    super().__init__(name=name)

  def get_controls(self, signal_one: tf.Tensor,
                   signal_two: tf.Tensor) -> TensorDict:
    """Just pass signals through."""
    return {'signal_one': signal_one, 'signal_two': signal_two}

  def get_signal(self, signal_one: tf.Tensor,
                 signal_two: tf.Tensor) -> tf.Tensor:
    return signal_one + signal_two


@gin.register
class Mix(Processor):
  """Constant-power crossfade between two signals."""

  def __init__(self, name: Text = 'mix'):
    super().__init__(name=name)

  def get_controls(self, signal_one: tf.Tensor,
                   signal_two: tf.Tensor,
                   nn_out_mix_level: tf.Tensor) -> TensorDict:
    """Standardize inputs to same length, mix_level to range [0, 1].

    Args:
      signal_one: 2-D or 3-D tensor.
      signal_two: 2-D or 3-D tensor.
      nn_out_mix_level: Tensor of shape [batch, n_time, 1] output of the network
        determining relative levels of signal one and two.

    Returns:
      Dict of control parameters.

    Raises:
      ValueError: If signal_one and signal_two are not the same length.
    """
    n_time_one = int(signal_one.shape[1])
    n_time_two = int(signal_two.shape[1])
    if n_time_one != n_time_two:
      raise ValueError('The two signals must have the same length instead of'
                       '{} and {}'.format(n_time_one, n_time_two))

    mix_level = tf.nn.sigmoid(nn_out_mix_level)
    mix_level = core.resample(mix_level, n_time_one)
    return {
        'signal_one': signal_one,
        'signal_two': signal_two,
        'mix_level': mix_level
    }

  def get_signal(self, signal_one: tf.Tensor, signal_two: tf.Tensor,
                 mix_level: tf.Tensor) -> tf.Tensor:
    """Constant-power cross fade between two signals.

    Args:
      signal_one: 2-D or 3-D tensor.
      signal_two: 2-D or 3-D tensor.
      mix_level: Tensor of shape [batch, n_time, 1] determining relative levels
        of signal one and two. Must have same number of time steps as the other
        signals and be in the range [0, 1].

    Returns:
      Tensor of mixed output signal.
    """
    mix_level_one = tf.sqrt(tf.abs(mix_level))
    mix_level_two = 1.0 - tf.sqrt(tf.abs(mix_level - 1.0))
    return mix_level_one * signal_one + mix_level_two * signal_two
