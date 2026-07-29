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

class AksaraCompiler:
    def __init__(self):
        self.indent = 0
    
    def compile_program(self, ast_list):
        lines = []
        for node in ast_list:
            lines.append(self.compile(node))
        return "\n".join(lines)
    
    def compile(self, node):
        tipe = type(node).__name__
        
        if tipe == "Assign":
            return f"{node.target.nama} = {self.compile(node.nilai)}"
        
        elif tipe == "Angka":
            return str(node.nilai)
        
        elif tipe == "String":
            return repr(node.nilai)
        
        elif tipe == "NamaVariabel":
            return node.nama
        
        elif tipe == "Cetak":
            return f"print({self.compile(node.ekspresi)})"
        
        elif tipe == "OperasiBiner":
            return f"({self.compile(node.kiri)} {node.op} {self.compile(node.kanan)})"
        
        elif tipe == "Jika":
            test = self.compile(node.kondisi)
            body = "\n".join([f"    {self.compile(s)}" for s in node.blok_jika])
            orelse = ""
            if node.cabang_lain:
                else_body = "\n".join([f"    {self.compile(s)}" for s in node.cabang_lain[-1]])
                orelse = f"\nelse:\n{else_body}"
            return f"if {test}:\n{body}{orelse}"
        
        elif tipe == "Ulangi":
            body = "\n".join([f"    {self.compile(s)}" for s in node.blok])
            return f"for _ in range({self.compile(node.jumlah)}):\n{body}"
        
        elif tipe == "DefinisiFungsi":
            params = ", ".join(node.parameter)
            body = "\n".join([f"    {self.compile(s)}" for s in node.blok])
            return f"def {node.nama}({params}):\n{body}"
        
        elif tipe == "Balik":
            return f"return {self.compile(node.ekspresi)}"
        elif tipe == "PanggilFungsi":
            args = ", ".join([self.compile(a) for a in node.argumen])
            return f"{self.compile(node.fungsi)}({args})"
        
        else:
            return f"# TODO: {tipe}"
