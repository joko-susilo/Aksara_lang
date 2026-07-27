# Copyright 2026 Joko Susilo
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

import argparse
from aksara.lexer.tokenizer import tokenize
from aksara.parser.parser import Parser
from aksara.interpreter.evaluator import evaluate
from aksara.interpreter.environment import Environment

def main():
    parser = argparse.ArgumentParser(description="Aksara - Bahasa Pemrograman Indonesia")
    parser.add_argument("file", help="File .ak yang akan dijalankan")
    parser.add_argument("-t", "--tokens", action="store_true", help="Tampilkan token")
    parser.add_argument("-a", "--ast", action="store_true", help="Tampilkan AST")
    parser.add_argument("-v", "--version", action="store_true", help="Versi")
    args = parser.parse_args()

    if args.version:
        from aksara import __version__
        print(f"Aksara v{__version__}")
        return

    with open(args.file, 'r', encoding='utf-8') as f:
        kode = f.read()

    tokens = tokenize(kode)
    if args.tokens:
        for t in tokens:
            print(t)
        return

    parser_obj = Parser(tokens)
    ast = parser_obj.parse_program()
    if args.ast:
        for node in ast:
            print(node)
        return

    env = Environment()
    for node in ast:
        evaluate(node, env)

if __name__ == "__main__":
    main()
