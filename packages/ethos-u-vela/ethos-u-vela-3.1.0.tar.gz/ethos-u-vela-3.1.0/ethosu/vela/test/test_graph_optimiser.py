# Copyright (C) 2020-2021 Arm Limited or its affiliates. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the License); you may
# not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an AS IS BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Description:
# Unit tests for tflite_graph_optimiser
import numpy as np
import pytest

from ethosu.vela.data_type import DataType
from ethosu.vela.graph_optimiser import optimise_graph
from ethosu.vela.nn_graph import Graph
from ethosu.vela.nn_graph import NetworkType
from ethosu.vela.operation import Op
from ethosu.vela.operation import Padding
from ethosu.vela.rewrite_graph import verify_graph_health
from ethosu.vela.tensor import create_const_tensor
from ethosu.vela.tensor import Shape4D
from ethosu.vela.tensor import Tensor
from ethosu.vela.test import testutil
from ethosu.vela.tflite_graph_optimiser import calc_explicit_padding
from ethosu.vela.tflite_graph_optimiser import convert_batched_fc_shape
from ethosu.vela.tflite_graph_optimiser import replace_pad_by_hw_pad
from ethosu.vela.tflite_graph_optimiser import rewrite_fully_connected_input


def test_convert_batched_fc():
    """Tests shape conversion of batched fully connected"""
    ifm_shape = [4, 8]
    ifm = create_const_tensor("test_in", ifm_shape, np.uint8, np.zeros(ifm_shape))
    w_shape = [8, 4]
    weights = create_const_tensor("weight_in", w_shape, np.uint8, np.zeros(w_shape))
    ofm = Tensor(ifm.shape, np.uint8, "test_out")
    op = testutil.create_op(Op.FullyConnected, [ifm, weights], ofm)

    ifm.consumer_list.append(op)

    prev_op = op.clone()
    prev_op.ifm_shapes = op.ifm_shapes.copy()
    prev_op.ofm_shapes = op.ofm_shapes.copy()

    rewrite_fully_connected_input(op, None, None)
    conv_op = convert_batched_fc_shape(op, None, None)
    assert conv_op.ifm == prev_op.ifm
    assert conv_op.ofm == prev_op.ofm
    assert op.ifm_shapes[0] == Shape4D([1, 2, 2, 8])
    assert op.ofm_shapes[0] == Shape4D([1, 2, 2, 8])
    assert conv_op.type == Op.FullyConnected
    assert len(conv_op.ifm.shape) == 2
    assert len(conv_op.ofm.shape) == 2
    assert conv_op.ifm.shape == conv_op.ofm.shape

    ifm.shape = [1, 8]
    weights.shape = [8, 1]
    ofm.shape = [1, 8]
    op = testutil.create_op(Op.FullyConnected, [ifm, weights], ofm)
    ifm.consumer_list.append(op)

    prev_op = op.clone()
    prev_op.ifm_shapes = op.ifm_shapes.copy()
    prev_op.ofm_shapes = op.ofm_shapes.copy()

    rewrite_fully_connected_input(op, None, None)
    conv_op = convert_batched_fc_shape(op, None, None)

    assert conv_op.ifm == prev_op.ifm
    assert conv_op.ofm == prev_op.ofm
    assert op.ifm_shapes[0] == prev_op.ifm_shapes[0]
    assert op.ofm_shapes[0] == prev_op.ofm_shapes[0]
    assert conv_op.type == Op.FullyConnected
    assert len(conv_op.ifm.shape) == 2
    assert len(conv_op.ofm.shape) == 2
    assert conv_op.ifm.shape == conv_op.ofm.shape


explicit_padding_test_data = [
    # Kernel size 2
    [(17, 1, 2, 1, 1), (1, 1)],
    [(18, 1, 2, 0, 1), (0, 1)],
    [(18, 1, 2, 1, 0), (1, 0)],
    # Kernel size 3
    [(18, 2, 3, 1, 1), (1, 0)],
    [(25, 2, 3, 1, 1), (1, 1)],
    # Kernel size 4
    [(18, 1, 4, 1, 2), (1, 2)],
    [(18, 1, 4, 2, 1), (2, 1)],
    [(19, 1, 4, 2, 2), (2, 2)],
    # Kernel size 5
    [(19, 1, 5, 1, 2), (1, 2)],
    [(19, 1, 5, 0, 2), (0, 2)],
    [(19, 1, 5, 1, 0), (1, 0)],
    # Kernel size 21
    [(41, 2, 21, 8, 10), (8, 10)],
    [(41, 3, 21, 10, 10), (10, 9)],
    [(42, 3, 21, 10, 10), (10, 8)],
    [(42, 3, 21, 9, 10), (9, 9)],
    [(41, 3, 21, 10, 6), (10, 6)],
]


@pytest.mark.parametrize("test_input, expected_result", explicit_padding_test_data)
def test_calc_explicit_padding(test_input, expected_result):
    input_size, stride, filter_size, explicit_pad_before, explicit_pad_after = test_input
    before, after = calc_explicit_padding(input_size, stride, filter_size, explicit_pad_before, explicit_pad_after)
    assert (before, after) == expected_result


def create_pad_and_conv2d(
    in_shape,
    out_shape,
    padding,
    in_dtype=DataType.int8,
    out_dtype=DataType.int8,
    pad_dtype=DataType.int32,
    pad_setting=Padding.VALID,
    kernel_size=3,
):
    """Creates Pad operator followed by a conv2d operator"""
    qp = testutil.default_quant_params()
    in0 = Tensor(in_shape, in_dtype, "in")
    in0.quantization = qp
    pad_tensor = create_const_tensor(name="pad", shape=list(np.shape(padding)), values=padding, dtype=pad_dtype)
    out = Tensor(out_shape, out_dtype, "out")
    out.quantization = qp.clone()
    op = testutil.create_op(Op.Pad, [in0, pad_tensor], out)
    op.run_on_npu = True
    conv_out_tens = Tensor(in_shape, in_dtype, "output")
    conv_out_tens.quantization = qp.clone()
    weight_tens = Tensor([kernel_size, kernel_size, in_shape[-1], out_shape[-1]], in_dtype, "weights")
    weight_tens.values = np.zeros(weight_tens.shape, in_dtype.as_numpy_type())
    weight_tens.quantization = qp.clone()
    bias_tens = Tensor(out_shape, pad_dtype, "biases")
    attrs = {"padding": pad_setting, "stride_w": 2, "stride_h": 2, "dilation_w_factor": 1, "dilation_h_factor": 1}
    attrs["strides"] = (1, attrs["stride_h"], attrs["stride_w"], 1)
    conv2d_op = testutil.create_op(Op.Conv2DBias, [out, weight_tens, bias_tens], conv_out_tens, attrs)
    conv2d_op.add_input_tensor(out)
    conv2d_op.run_on_npu = True
    return op, conv2d_op


def test_pad_followed_by_conv_is_removed():
    """
    Tests that the PAD operator is bypassed when followed by a convolution operator,
    and that the padding of the convolution operation is correctly updated
    """
    pad_op, conv2d_op = create_pad_and_conv2d(
        in_shape=[1, 76, 75, 64], out_shape=[1, 76, 75, 64], padding=[[0, 0], [2, 1], [1, 1], [0, 0]], kernel_size=4
    )
    nng = testutil.create_graph([pad_op, conv2d_op])
    arch = testutil.create_arch()

    replace_pad_by_hw_pad(conv2d_op, nng, arch)

    op = nng.subgraphs[0].output_tensors[0].ops[0]
    assert op.type == Op.Conv2DBias
    assert op.attrs["padding"] == Padding.EXPLICIT
    assert op.attrs["explicit_padding"] == (2, 1, 1, 1)
    assert op.ifm.shape == [1, 76, 75, 64]
    assert pad_op not in op.ifm.ops


leading_pad_test_data = [
    (2, 2, 11, True),
    (1, 2, 11, False),
    (2, 1, 11, False),
    (5, 2, 11, True),
]


@pytest.mark.parametrize("top, left, kernel_size, expect_pad_removed", leading_pad_test_data)
def test_leading_pad_size(top, left, kernel_size, expect_pad_removed):
    # Tests PAD operator with big kernel size; top and left pad must be multiple of stride
    out_shape = [1, 11 + left, 11 + top, 1]
    padding = [[0, 0], [top, 0], [left, 0], [0, 0]]
    pad_op, conv2d_op = create_pad_and_conv2d(
        in_shape=[1, 11, 11, 1], out_shape=out_shape, padding=padding, kernel_size=kernel_size
    )
    nng = testutil.create_graph([pad_op, conv2d_op])
    arch = testutil.create_arch()
    replace_pad_by_hw_pad(conv2d_op, nng, arch)
    op = nng.subgraphs[0].output_tensors[0].ops[0]
    if expect_pad_removed:
        assert op.attrs["padding"] == Padding.EXPLICIT
        assert "explicit_padding" in op.attrs
        assert op.ifm.shape == op.ofm.shape
        assert pad_op not in op.ifm.ops
    else:
        assert pad_op in op.ifm.ops
        assert op.attrs["padding"] == Padding.VALID
        assert "explicit_padding" not in op.attrs


def test_optimise_pad_followed_by_avg_pool():
    """
    Tests that the PAD operator is bypassed when followed by a average pool operator,
    and that the average pool is converted to a depthwise
    """
    # Create Pad operation followed by AvgPool
    quant = testutil.default_quant_params()
    in_tens = Tensor([1, 76, 75, 64], DataType.uint8, "input")
    in_tens.quantization = quant
    # Test with 3x2 input tensor
    pad_input = create_const_tensor("pad_input", [3, 2], DataType.int32, [[2, 2], [1, 1], [0, 0]])
    temp_tens = Tensor([1, 79, 77, 64], DataType.uint8, "pad_out")
    temp_tens.quantization = quant.clone()
    out_tens = Tensor([1, 76, 75, 64], DataType.uint8, "output")
    out_tens.quantization = quant.clone()

    pad_op = testutil.create_op(Op.Pad, [in_tens, pad_input], temp_tens)
    attrs = {
        "padding": Padding.VALID,
        "ksize": [1, 5, 3, 1],
        "stride_w": 2,
        "stride_h": 2,
        "dilation_w_factor": 1,
        "dilation_h_factor": 1,
    }
    attrs["strides"] = (1, attrs["stride_h"], attrs["stride_w"], 1)
    pad_op.run_on_npu = True
    conv2d_op = testutil.create_op(Op.AvgPool, [temp_tens], out_tens, attrs)
    conv2d_op.run_on_npu = True
    nng = testutil.create_graph([pad_op, conv2d_op])
    arch = testutil.create_arch()

    replace_pad_by_hw_pad(conv2d_op, nng, arch)

    op = nng.subgraphs[0].output_tensors[0].ops[0]
    assert op.type == Op.DepthwiseConv2DBias
    assert op.attrs["padding"] == Padding.EXPLICIT
    assert op.attrs["explicit_padding"] == (2, 1, 2, 1)
    assert op.ifm.shape == [1, 76, 75, 64]
    assert pad_op not in op.ifm.ops
    # Check that bias and weight tensors have been added
    assert op.bias.shape == [64]
    assert op.weights.shape == [5, 3, 1, 64]


pad_avg_pool_test_data = [
    ((3, 3), (1, 1, 1, 1), True),
    ((3, 3), (2, 1, 1, 1), False),
    ((3, 3), (1, 2, 1, 1), False),
    ((3, 3), (1, 1, 2, 1), False),
    ((3, 3), (1, 1, 1, 2), False),
    ((2, 4), (1, 2, 1, 2), True),
    ((5, 3), (2, 1, 2, 1), True),
    ((5, 3), (0, 1, 2, 1), True),
    ((5, 3), (2, 0, 2, 1), True),
    ((5, 3), (2, 1, 0, 1), True),
    ((5, 3), (2, 1, 0, 1), True),
    ((4, 4), (2, 2, 2, 2), True),
    ((4, 4), (1, 2, 2, 2), False),
    ((4, 4), (2, 1, 2, 2), False),
    ((4, 4), (2, 2, 1, 2), False),
    ((4, 4), (2, 2, 2, 1), False),
]


@pytest.mark.parametrize("k_size, padding, expect_pad_removed", pad_avg_pool_test_data)
def test_pad_followed_by_avg_pool(k_size, padding, expect_pad_removed):
    # Tests PAD followed by AvgPool
    k_w, k_h = k_size
    top, left, bottom, right = padding
    pad_values = [[0, 0], [top, bottom], [left, right], [0, 0]]
    dtype = DataType.int8
    qp = testutil.default_quant_params()
    in_shape = [1, 15, 17, 8]
    out_shape = [1, in_shape[1] + top + bottom, in_shape[2] + left + right, in_shape[3]]
    in0 = Tensor(in_shape, dtype, "in")
    in0.quantization = qp
    pad_tensor = create_const_tensor(
        name="pad", shape=list(np.shape(pad_values)), values=pad_values, dtype=DataType.int32
    )
    out = Tensor(out_shape, dtype, "out")
    out.quantization = qp.clone()
    pad_op = testutil.create_op(Op.Pad, [in0, pad_tensor], out)
    pool_out_tens = Tensor(in_shape, dtype, "output")
    pool_out_tens.quantization = qp.clone()
    attrs = {
        "padding": Padding.VALID,
        "ksize": [1, k_w, k_h, 1],
        "stride_w": 1,
        "stride_h": 1,
        "dilation_w_factor": 1,
        "dilation_h_factor": 1,
    }
    pool_op = testutil.create_op(Op.AvgPool, [out], pool_out_tens, attrs)
    pad_op.run_on_npu = True
    pool_op.run_on_npu = True
    nng = testutil.create_graph([pad_op, pool_op])
    arch = testutil.create_arch()
    nng = optimise_graph(nng, arch, NetworkType.TFLite)
    sg = nng.subgraphs[0]
    all_ops = sg.get_all_ops()
    print("all_ops: ", all_ops)
    # Pad should not be in the graph anymore, it should either have been removed or rewritten
    assert not any(op.type == Op.Pad for op in all_ops)
    op = nng.subgraphs[0].output_tensors[0].ops[0]
    if expect_pad_removed:
        # Expect rewrite to depthwise, PAD is removed
        assert op.type == Op.DepthwiseConv2DBias
        assert op.attrs["padding"] == Padding.EXPLICIT
        assert any(pad > 0 for pad in op.attrs["explicit_padding"])
        assert op.ifm.shape == op.ofm.shape
        # Check that bias and weight tensors have been added
        assert len(op.bias.shape) > 0
        assert op.weights.shape is not None
    else:
        # Pad should have been rewritten to a number of average pool operations
        assert all(op.type in (Op.AvgPool, Op.Const) for op in all_ops)
        assert pool_op.type == Op.AvgPool
        assert pool_op.attrs["padding"] == Padding.VALID


# Setup network to test removal of op with op_type Op.Reshape or Op.Squeeze
# op_type should be Op.Reshape or Op.Squeeze
def setup_network(op_type):
    assert op_type == Op.Reshape or op_type == Op.Squeeze
    if op_type == Op.Reshape:
        op_str = "reshape"
    elif op_type == Op.Squeeze:
        op_str = "squeeze"

    quant = testutil.default_quant_params()
    # create reshape1 op
    ifm_shape = [64, 16]
    reshape1_ofm_shape = [1, 4, 16, 16]
    reshape1_ifm = create_const_tensor(f"{op_str}1_in", ifm_shape, DataType.uint8, np.zeros(ifm_shape))
    reshape1_ifm.quantization = quant
    reshape1_ofm = create_const_tensor(
        f"{op_str}1_out", reshape1_ofm_shape, DataType.uint8, np.zeros(reshape1_ofm_shape)
    )
    reshape1_ofm.quantization = quant
    shape_tens = create_const_tensor(f"{op_str}1_shape", [1], DataType.int32, reshape1_ofm_shape)
    reshape1_op = testutil.create_op(op_type, [reshape1_ifm, shape_tens], reshape1_ofm, set_ifm_ofm_shapes=False)
    reshape1_op.attrs["new_shape"] = reshape1_ofm_shape
    reshape1_op.run_on_npu = True

    # create conv op
    conv_ofm = Tensor([1, 8, 8, 16], DataType.uint8, "output")
    conv_ofm.quantization = quant.clone()
    weight_tens = Tensor([1, 1, 16, 16], DataType.uint8, "weights")
    weight_tens.values = np.zeros(weight_tens.shape, np.uint8)
    weight_tens.quantization = quant.clone()
    bias_tens = Tensor([16], DataType.int32, "biases")

    attrs = {"padding": Padding.SAME, "stride_w": 1, "stride_h": 1, "dilation_w_factor": 1, "dilation_h_factor": 1}
    attrs["strides"] = (1, attrs["stride_h"], attrs["stride_w"], 1)

    conv2d_op = testutil.create_op(
        Op.Conv2D, [reshape1_ofm, weight_tens, bias_tens], conv_ofm, attrs=attrs, set_ifm_ofm_shapes=False
    )
    conv2d_op.run_on_npu = True

    # create reshape2 op
    ofm_shape = [8, 8, 16]
    reshape2_ofm = create_const_tensor(f"{op_str}2_out", ofm_shape, DataType.uint8, np.zeros(ofm_shape))
    reshape2_ofm.quantization = quant
    shape_tens = create_const_tensor(f"{op_str}2_shape", [1], DataType.int32, ofm_shape)
    reshape2_op = testutil.create_op(op_type, [conv_ofm, shape_tens], reshape2_ofm, set_ifm_ofm_shapes=False)
    reshape2_op.attrs["new_shape"] = ofm_shape
    reshape2_op.run_on_npu = True
    nng = Graph()
    sg = testutil.create_subgraph([reshape1_op, conv2d_op, reshape2_op])
    nng.subgraphs.append(sg)

    return nng, reshape1_op, conv2d_op, reshape2_op


def test_remove_reshape():
    """
    Tests that the expected reshape are removed in graph_optimisation
    """

    # Test1 no Reshape op is expected to remain in the NPU subgrapgh
    # but first one will be put on CPU
    # Network is Reshape-Conv-Reshape
    # Result is Conv
    nng, reshape1_op, conv2d_op, reshape2_op = setup_network(Op.Reshape)
    arch = testutil.create_arch()
    assert verify_graph_health(nng)
    nng = optimise_graph(nng, arch, NetworkType.TFLite)
    assert verify_graph_health(nng)

    # Test2 reshape1 with different quantisation, this Reshape op is expected to remain
    # Network is Reshape-Conv-Reshape
    # expected is Reshape-Conv
    nng, reshape1_op, conv2d_op, reshape2_op = setup_network(Op.Reshape)
    quant_zp32 = testutil.default_quant_params()
    quant_zp32.zero_point = 32
    reshape1_op.ofm.quantization = quant_zp32
    assert verify_graph_health(nng)
    nng = optimise_graph(nng, arch, NetworkType.TFLite)
    assert verify_graph_health(nng)


def test_remove_squeeze():
    """
    Tests that the expected squeeze are removed in graph_optimisation
    """

    # Test1 no Squeeze op is expected to remain in the NPU subgrapgh
    # but first one will be put on CPU
    # Network is Squeeze-Conv-Squeeze
    # Result is Conv
    nng, squeeze1_op, conv2d_op, squeeze2_op = setup_network(Op.Squeeze)
    arch = testutil.create_arch()
    assert verify_graph_health(nng)
    nng = optimise_graph(nng, arch, NetworkType.TFLite)
    assert verify_graph_health(nng)

    # Test2 squeeze1 with different quantisation, this Squeeze op is expected to remain
    # Network is Squeeze-Conv-Squeeze
    # expected is Squeeze-Conv
    nng, squeeze1_op, conv2d_op, squeeze2_op = setup_network(Op.Squeeze)
    quant_zp32 = testutil.default_quant_params()
    quant_zp32.zero_point = 32
    squeeze1_op.ofm.quantization = quant_zp32
    assert verify_graph_health(nng)
    nng = optimise_graph(nng, arch, NetworkType.TFLite)
    assert verify_graph_health(nng)
