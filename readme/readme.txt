Plugin for CudaText.
Adds support for Language Server Protocol (LSP) servers.
For each language server needs to be installed separately.

For each LSP server, add config to the folder "settings" (folder of user.json CudaText config).
Config file must be named lsp_*.json ("lsp_" prefix and ".json" suffix).
See Wiki information about many ready configurations:
https://wiki.freepascal.org/CudaText_plugins

"Hover" dialog feature: dialog appears when you stop moving the mouse cursor, over some
identifier, with Ctrl-key pressed (on macOS: with Command-key).
"Hover" dialog gives several buttons to call other features of LSP:
* Definition
* References
* Implementation
* Declaration
* Type definition
All these features can also be called from menu "Plugins / LSP Client" or from editor's
Command Palette (menu "Help / Command palette").


Example for Python
------------------
Python LSP server can be installed in the Linux by command:
$ pip3 install python-language-server
It creates the script "~/.local/bin/pyls". Basic config would look like this:

  {
    "lexers": {
        "Python": "python"
    },
    "cmd_unix": ["~/.local/bin/pyls"]
  }


Server common options
---------------------
Plugin supports 3 keys for running commands:
- "cmd_windows" for Windows,
- "cmd_macos" for macOS,
- "cmd_unix" for all other OS.

Each cmd-key must be a list of strings, e.g.
  "cmd_windows": ["C:\\Python_folder\\pyls.exe", "--param", "param"],

The config key "lexers" contains mapping between CudaText lexer names and LSP language names.
For example, while CudaText lexer name is "C#", LSP language name is "csharp", so you need
  "lexers": {
     "C#": "csharp"
  }
This mapping is needed also when you have some renamed/changed lexer, e.g. "MyPython".
Some list of LSP language names can be seen here:
https://microsoft.github.io/language-server-protocol/specifications/specification-current/#-textdocumentitem-

Option to fill "Code tree" from the LSP server:
  "enable_code_tree": true

Which document symbols to show in the tree can also be configured with a comma-separated list of symbol kinds:
  "tree_types_show": "file,module,namespace,package,class,method,property,field,constructor,enum,interface,function,variable,constant,string,number,boolean,array,object,key,null,enummember,struct,event,operator,typeparameter" 
Default value is: "namespace,class,method,constructor,interface,function,struct"

Format document on every save (off by default). Server needs to support document formatting.
  "format_on_save": true

Log 'stderr' of server's process to log-panel (off by default):
  "log_stderr": true

Disable autocompletion in comment and/or string context for this server. overrides same global option. ('cs' by default):
  "disabled_contexts": "cs"
User must set it to empty value ("") for LSP servers that can autocomplete inside quotes (class attribute in HTML, etc).
  

Server-specific options
-----------------------
Some servers can be additionally configured, this configuration can be placed
a) in the server config file settings/lsp_*.json
b) or in the project config file *.cuda-proj-lsp, near the project file *.cuda-proj
Use command "Plugins / LSP Client / Configure server for current project".

For example, Golang server "gopls" has docs about its options:
https://github.com/golang/tools/blob/master/gopls/doc/settings.md
Options can be written to:

a) settings/lsp_go.json
  ...
  "settings": {
    "gopls": {
        "hoverKind": "NoDocumentation"
    }
  }
  ...

b) project config myname.cuda-proj-lsp
  {
    "gopls": {
      "hoverKind": "NoDocumentation"
    }
  }

You can also use dot-path notation to specify sections in simple format:
  ...
  "settings": {
    "python.analysis.typeCheckingMode": "off",
  }
  ...
 

Plugin options
--------------
Plugin has the config file, which can be opened in CudaText by:
"Options / Settings-plugins / LSP Client / Config".
The possible options are listed in another text file in the LSP Client folder.


Semantic tokens
---------------
Semantic Tokens according to LSP specification is providing information about ID's kind
(class/var/param/macro/etc) and modifiers (global/static/readonly/etc).
For example, you want all 'classes' to be painted green, or all 'readonly vars' be painted
in teal color, etc.

Some servers provide the support for this feature, some don't. Tested with C++ (clangd), Java,
Lua, JS, TypeScript, Markdown, Rust.
Example .cpp file is located in the "readme" folder (cuda_lsp\readme\test_semantic_tokens.cpp).

To enable and configure this, call "LSP Client / Config" command and see the following options:
- "enable_semantic_tokens"
- "semantic_colors_light"
- "semantic_colors_dark"


About
-----
Authors:
- Shovel, https://github.com/halfbrained/
- Yuriy Balyuk, https://github.com/veksha/
- snippet.py by Alexey Torgashin (CudaText) & helpers

License: MIT
