// Copyright (c) 2023 PaddlePaddle Authors. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <math.h>
#include <vector>

#include "paddle/ir/core/value.h"
#include "paddle/primitive/rule/vjp/vjp_dispatch.h"
#include "paddle/primitive/type/desc_tensor.h"

namespace ir {
namespace api {
std::vector<std::vector<ir::OpResult>> tanh_grad(
    ir::OpResult out,
    ir::OpResult grad_out,
    const std::vector<std::vector<int>>& stop_gradients) {
  std::vector<std::vector<ir::OpResult>> res;

  return res;
}
}  // namespace api
}  // namespace ir

namespace paddle {
namespace primitive {
namespace experimental {
// std::vector<std::vector<ir::OpResult> interface(vector<vector<int>> argnums,
// vector<vector<opresult>){

//     return vector<vector<opresult>> res ;
// }

std::vector<std::vector<Tensor>> tanh_vjp(
    const Tensor& out,
    const Tensor& grad_out,
    const std::vector<std::vector<int>>& stop_gradients) {
  // 1.constuct out and grad_out OpResult
  std::vector<std::vector<Tensor>> res;
  ir::OpResult out_opres = std::static_pointer_cast<DescTensor>(out.impl())
                               ->getValue()
                               .dyn_cast<ir::OpResult>();
  ir::OpResult grad_out_opres =
      std::static_pointer_cast<DescTensor>(grad_out.impl())
          ->getValue()
          .dyn_cast<ir::OpResult>();

  // 2.tanh_grad
  return res;
}
}  // namespace experimental
}  // namespace primitive
}  // namespace paddle
