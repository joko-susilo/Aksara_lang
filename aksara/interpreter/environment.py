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



class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent  # scope luar (untuk fungsi)

    def define(self, name, value):
        """Mendefinisikan variabel baru di scope ini."""
        self.vars[name] = value

    def assign(self, name, value):
        """Mengubah nilai variabel yang sudah ada (bisa di scope ini atau parent)."""
        if name in self.vars:
            self.vars[name] = value
        elif self.parent:
            self.parent.assign(name, value)
        else:
            raise NameError(f"Variabel '{name}' belum didefinisikan")

    def get(self, name, default=None):
        if name in self.vars:
            return self.vars[name]
        elif self.parent:
            
            return self.parent.get(name, default)
        else:
            if default is not None:
                return default
            raise NameError(f"Variabel '{name}' tidak ditemukan")