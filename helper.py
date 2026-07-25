import ast

def getVariableNameWithKeys(name, keys):
    current = ast.Name(id=name, ctx=ast.Load())

    for key in keys:
        current = ast.Subscript(
            value=current,
            slice=ast.Constant(value=key),
            ctx=ast.Store()
        )

    return current