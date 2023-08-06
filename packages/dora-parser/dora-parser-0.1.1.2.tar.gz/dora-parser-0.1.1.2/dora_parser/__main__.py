# -*- coding: utf-8 -*-
#
# Copyright 2021 Compasso UOL
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Dora Parser Command Line interface"""
import fire
from dora_parser.parser import Parser
from dora_parser.transpiler import Transpiler

def translate(from_dialect:str='impala', to_dialect:str='spark', query:str=None):
    transpiler = Transpiler(from_dialect='impala', to_dialect='spark')
    result, errors = transpiler.translate(Parser(query))
    return result

if __name__ == '__main__':
  fire.Fire(translate)
