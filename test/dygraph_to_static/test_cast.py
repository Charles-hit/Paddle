# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
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

import unittest

import numpy as np
from dy2st_test_utils import test_and_compare_with_new_ir

from paddle import fluid
from paddle.jit.api import to_static

SEED = 2020
np.random.seed(SEED)


@to_static
def test_bool_cast(x):
    x = fluid.dygraph.to_variable(x)
    x = bool(x)
    return x


@to_static
def test_int_cast(x):
    x = fluid.dygraph.to_variable(x)
    x = int(x)
    return x


@to_static
def test_float_cast(x):
    x = fluid.dygraph.to_variable(x)
    x = float(x)
    return x


@to_static
def test_not_var_cast(x):
    x = int(x)
    return x


@to_static
def test_mix_cast(x):
    x = fluid.dygraph.to_variable(x)
    x = int(x)
    x = float(x)
    x = bool(x)
    x = float(x)
    return x


class TestCastBase(unittest.TestCase):
    def setUp(self):
        self.place = (
            fluid.CUDAPlace(0)
            if fluid.is_compiled_with_cuda()
            else fluid.CPUPlace()
        )
        self.prepare()
        self.set_func()

    def prepare(self):
        self.input_shape = (16, 32)
        self.input_dtype = 'float32'
        self.input = (
            np.random.binomial(4, 0.3, size=np.product(self.input_shape))
            .reshape(self.input_shape)
            .astype(self.input_dtype)
        )
        self.cast_dtype = 'bool'

    def set_func(self):
        self.func = test_bool_cast

    def do_test(self):
        with fluid.dygraph.guard():
            res = self.func(self.input)
            return res

    @test_and_compare_with_new_ir(False)
    def test_cast_result(self):
        res = self.do_test().numpy()
        self.assertTrue(
            res.dtype == self.cast_dtype,
            msg='The target dtype is {}, but the casted dtype is {}.'.format(
                self.cast_dtype, res.dtype
            ),
        )
        ref_val = self.input.astype(self.cast_dtype)
        np.testing.assert_allclose(
            res,
            ref_val,
            rtol=1e-05,
            err_msg='The casted value is {}.\nThe correct value is {}.'.format(
                res, ref_val
            ),
        )


class TestIntCast(TestCastBase):
    def prepare(self):
        self.input_shape = (1,)
        self.input_dtype = 'float32'
        self.input = (
            np.random.normal(loc=6, scale=10, size=np.product(self.input_shape))
            .reshape(self.input_shape)
            .astype(self.input_dtype)
        )
        self.cast_dtype = 'int32'

    def set_func(self):
        self.func = test_int_cast


class TestFloatCast(TestCastBase):
    def prepare(self):
        self.input_shape = (8, 16)
        self.input_dtype = 'bool'
        self.input = (
            np.random.binomial(2, 0.5, size=np.product(self.input_shape))
            .reshape(self.input_shape)
            .astype(self.input_dtype)
        )
        self.cast_dtype = 'float32'

    def set_func(self):
        self.func = test_float_cast


class TestMixCast(TestCastBase):
    def prepare(self):
        self.input_shape = (8, 32)
        self.input_dtype = 'float32'
        self.input = (
            np.random.normal(loc=6, scale=10, size=np.product(self.input_shape))
            .reshape(self.input_shape)
            .astype(self.input_dtype)
        )
        self.cast_int = 'int'
        self.cast_float = 'float32'
        self.cast_bool = 'bool'
        self.cast_dtype = 'float32'

    def set_func(self):
        self.func = test_mix_cast

    @test_and_compare_with_new_ir(False)
    def test_cast_result(self):
        res = self.do_test().numpy()
        self.assertTrue(
            res.dtype == self.cast_dtype,
            msg='The target dtype is {}, but the casted dtype is {}.'.format(
                self.cast_dtype, res.dtype
            ),
        )
        ref_val = (
            self.input.astype(self.cast_int)
            .astype(self.cast_float)
            .astype(self.cast_bool)
            .astype(self.cast_dtype)
        )
        np.testing.assert_allclose(
            res,
            ref_val,
            rtol=1e-05,
            err_msg='The casted value is {}.\nThe correct value is {}.'.format(
                res, ref_val
            ),
        )


class TestNotVarCast(TestCastBase):
    def prepare(self):
        self.input = 3.14
        self.cast_dtype = 'int'

    def set_func(self):
        self.func = test_not_var_cast

    @test_and_compare_with_new_ir(False)
    def test_cast_result(self):
        res = self.do_test()
        self.assertTrue(type(res) == int, msg='The casted dtype is not int.')
        ref_val = int(self.input)
        self.assertTrue(
            res == ref_val,
            msg='The casted value is {}.\nThe correct value is {}.'.format(
                res, ref_val
            ),
        )


if __name__ == '__main__':
    unittest.main()
