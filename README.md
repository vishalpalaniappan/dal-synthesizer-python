# dal-synthesizer-python
This tool synthesizes an executable python program given an AST generated from a DAL script. In addition to synthesizing computable primitives, it also synthesizes developer registered realization of semantics.

I am writing it in python because the AST library is very convenient and I will invoke it from the workbench using the nodejs runner.

# Example Usage
```bash
python3 dal_ast_synthesizer.py --ast ./asts/lib_manager_ast.json
```


