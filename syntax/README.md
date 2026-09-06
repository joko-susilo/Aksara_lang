# Sintaks Highlight untuk Bahasa Aksara

Grammar TextMate `aksara.tmLanguage.json` untuk file `.ak` / `.aksara`.

## VSCode / VS Codium

Buat ekstensi lokal sederhana (atau jalankan lewat "Developer: Install Extension
from Location...") dengan struktur:

```
ekstensi-aksara/
├── package.json
└── syntaxes/
    └── aksara.tmLanguage.json
```

`package.json` minimal:

```json
{
  "name": "aksara-syntax",
  "version": "0.1.0",
  "engines": { "vscode": "^1.60.0" },
  "contributes": {
    "languages": [
      {
        "id": "aksara",
        "aliases": ["Aksara", "aksara"],
        "extensions": [".ak", ".aksara"],
        "configuration": "./language-configuration.json"
      }
    ],
    "grammars": [
      {
        "language": "aksara",
        "scopeName": "source.aksara",
        "path": "./syntaxes/aksara.tmLanguage.json"
      }
    ]
  }
}
```

## Neovim (tree-sitter/TextMate via nvim-treesitter "textobjects")

Salin `aksara.tmLanguage.json` ke `~/.config/nvim/after/queries/` dan muat lewat
plugin yang mendukung TextMate grammar, atau pakai `:setf` + standalone
highlight dengan `vim.api.nvim_buf_add_highlight`.

## GitHub

Prompt GitHub (linguist) belum terdaftar untuk `.ak`. Sementara ini `.ak` akan
dianggap file Coccinelle/SML dll. Registrasi folding/language di
github/linguist bisa diajukan via PR ke repo linguist (contoh daftar
keywords/gag).