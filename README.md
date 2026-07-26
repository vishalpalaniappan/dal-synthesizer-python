# dal-synthesizer-python
This tool synthesizes an executable python program given an AST generated from a DAL script. In addition to synthesizing computable primitives, it also synthesizes developer registered realization of semantics.

It is written in python because the AST library is very convenient to use and I will invoke it from the workbench using the nodejs runner.

## Overview

The language itself is very simple in its current state:
- Structural Blocks: behavior, if, while
- Reserved Commands: design, select
- Command structure: cmd(args)

The blocks establish the basic structure, for example, behavior becomes def:
```
behavior getName {
    ...
}

def getName():
    ...
```

The commands establish the transformations. There are computable synthesis and registered synthesis and this implementation synthesizes them in python3.

## Computable Synthesis
```
insert(<participant>, <value>, <index>)

<participant>.insert(<index>,<value>)
```
## Registered Synthesis
```
getInput(<participant>,<prompt>)

<participant> = input(<prompt>)
```

Likewise, the other blocks and commands are synthesized into the implementation that realizes their meaning. You can find these AST nodes in the  [`commands.json`](docs/commands.json) file. 

The synthesizer itself traverses the AST and builds the synthesized implementation. It is a very simple program since it is just realizing the design as an implementation that realizes its meaning.

## Python Usage
```bash
python3 dal_ast_synthesizer.py --ast ./asts/lib_manager_ast.json
```

## NodeJS Runner Usage
```bash
node node/synthesisTest.js asts/lib_manager_ast.json
```

# Providing feedback

You can use GitHub issues to [report a bug][bug-report] or [request a feature][feature-req].

[bug-report]: https://github.com/vishalpalaniappan/dal-synthesizer-python/issues
[feature-req]: https://github.com/vishalpalaniappan/dal-synthesizer-python/issues
