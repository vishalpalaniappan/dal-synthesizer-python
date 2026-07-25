import ast
from helper import getVariableNameWithKeys

def getSynthesizedNode(node):
    '''
        Get the AST node given the dalAST metadata.

        DAL Identifiers: get<Identifier>Ast
        Commands: getCmd<CommandName>Ast
    '''
    type = node["type"]
    if (type == "cmd"):
        cmd = node["command"]
        funcName = f"getCmd{cmd[0].upper() +cmd[1:]}Ast"
    else:
        funcName = f"get{type[0].upper() +type[1:]}Ast"

    if (funcName in globals()):
        return globals()[funcName](node)

def getCmdLogAst(node):
    '''
        log(<behavior>, <name>, <type>, <value>)

        semanticLogger.logParticipant(<behavior>, <name>, <type>, <value>)
    
    '''
    behavior = node["args"][0]["value"]
    name = node["args"][1]["value"]
    type = node["args"][2]["value"]
    value = node["args"][3]["value"]
    return ast.Expr(
        value=ast.Call(
            func=ast.Attribute(
                value=ast.Name(id="semanticLogger", ctx=ast.Load()),
                attr="logParticipant",
                ctx=ast.Load(),
            ),
            args=[
                ast.Constant(value=behavior),
                ast.Constant(value=name),
                ast.Constant(value=type),
                ast.Name(id=value, ctx=ast.Load()),
            ],
            keywords=[],
        )
    )

def getBehaviorAst(node):
    '''
        def <behaviorName>():
            global worldState
    '''
    return ast.FunctionDef(
        name=node["behaviorName"],
        args=ast.arguments(
            posonlyargs=[],
            args=[],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
            vararg=None,
            kwarg=None
        ),
        body=[
            ast.Global(
                names=["worldState"]
            )
        ],
        decorator_list=[]
    )

def getDesignAst(node):
    '''
        design = <design_Name>
    '''
    return ast.Assign(
        targets=[
            ast.Name(id="design", ctx=ast.Store())
        ],
        value=ast.Constant(value=node["design_name"][0]["value"])
    )

def getWhileAst(node):
    '''
        while <condition>:
            <body>
    '''
    return ast.While(
        test=ast.Name(id=node["args"][0]["value"], ctx=ast.Load()),
        body=[],
        orelse=[]
    )

def getIfAst(node):
    '''
        if <condition>:
            <body>
    '''
    condition = node["args"][0]["value"]
    return ast.If(
        test=ast.Name(id=condition, ctx=ast.Load()),
        body=[],
        orelse=[],
    )

def getCmdGetInputAst(node):
    '''
        This is a registered synthesis. I am claiming
        that input() realises the meaning of the behavior
        defined by getInput()

        <output> = input()
    '''
    name = node["args"][0]["value"]
    prompt = node["args"][1]["value"]
    return  ast.Assign(
        targets=[
            ast.Name(id=name, ctx=ast.Store())
        ],
        value=ast.Call(
            func=ast.Name(id="input", ctx=ast.Load()),
            args=[ast.Constant(value=prompt)],
            keywords=[]
        )
    )

def getCmdSetAst(node):
    '''
        <name>[<keys>] = <value>
    '''
    name = node["args"][0]["value"]
    keys = node["args"][1]["value"]
    rawValue = node["args"][2]["value"]

    if (node["args"][2]["type"] == "name"):
        value = ast.Name(id=rawValue, ctx=ast.Load())
    else:
        value = ast.Constant(value=rawValue)

    return ast.Assign(
        targets=[
            getVariableNameWithKeys(name, keys)
        ],
        value=value,
    )

def getCmdInsertAst(node):
    '''
        Command: insert(<target>, <keys>,  <value>, <index>)

        Synthesized: <target>[<keys>].insert(<index>, <value>)
    '''
    target = node["args"][0]["value"]
    keys = node["args"][1]["value"]
    value = node["args"][2]["value"]
    index = node["args"][3]["value"]
    return ast.Expr(
        value=ast.Call(
            func=ast.Attribute(
                value= getVariableNameWithKeys(target, keys),
                attr="insert",
                ctx=ast.Load()
            ),
            args=[
                ast.Constant(index),
                ast.Name(id=value, ctx=ast.Load()),
            ],
            keywords=[]
        )
    )

def getCmdGetAst(node):
    '''
        Command: get(<target>, <source>, <keys>)

        Synthesized: <target> = <source>[<keys>]
    '''
    target = node["args"][0]["value"]
    source = node["args"][1]["value"]
    keys = node["args"][2]["value"]
    return ast.Assign(
        value=getVariableNameWithKeys(source, keys),
        targets=[ast.Name(id=target, ctx=ast.Store())]
    )

def getCmdSelectAst(node):
    '''
        Command: select(<nextBehavior>)

        Synthesized: return <nextBehavior>
    '''
    returnValue = node["args"][0]["value"]
    return ast.Return(
        value=ast.Constant(value=returnValue)
    )

def getCmdDisplayAst(node):
    '''
        Command: display(<prompt>)

        Synthesized: print(<prompt>)
    '''
    display = node["args"][0]["value"]
    
    return ast.Expr(
        value=ast.Call(
            func=ast.Name(id="print", ctx=ast.Load()),
            args=[
                ast.parse(display, mode="eval").body
            ],
            keywords=[]
        )
    )

def getCmdIsEqualAst(node):
    '''
        Command: isEqual(<cmp1>, <cmp2>, <result>)

        Synthesized: isAdd = choice == "a"
    '''
    output = node["args"][2]["value"]

    if (node["args"][0]["type"] == "name"):
        cmp1 = ast.Name(id=node["args"][0]["value"], ctx=ast.Load())
    else:
        cmp1 = ast.Constant(value=node["args"][0]["value"])

    if (node["args"][1]["type"] == "name"):
        cmp2 = ast.Name(id=node["args"][1]["value"], ctx=ast.Load())
    else:
        cmp2 = ast.Constant(value=node["args"][1]["value"])

    return ast.Assign(
        targets=[
            ast.Name(id=output, ctx=ast.Store())
        ],
        value=ast.Compare(
            left=cmp1,
            ops=[ast.Eq()],
            comparators=[cmp2],
        ),
    )

def getCmdGetFromPosAst(node):
    '''
        Command: getFromPos(book, basket, 0)

        Synthesized:
        book = basket[0]
    '''
    target = node["args"][0]["value"]
    source = node["args"][1]["value"]
    index = node["args"][2]["value"]

    return ast.Assign(
        targets=[
            ast.Name(id=target, ctx=ast.Store())
        ],
        value=ast.Subscript(
            value=ast.Name(id=source, ctx=ast.Load()),
            slice=ast.Constant(value=index),
            ctx=ast.Load()
        )
    )

def getCmdRemoveFromPosAst(node):
    '''
        Command: removeFromPos(book, basket, 0)

        Synthesized:
        book = basket.pop(0)
    '''
    target = node["args"][0]["value"]
    source = node["args"][1]["value"]
    index = node["args"][2]["value"]

    return ast.Assign(
        targets=[
            ast.Name(id=target, ctx=ast.Store())
        ],
        value=ast.Call(
            func=ast.Attribute(
                value=ast.Name(id=source, ctx=ast.Load()),
                attr="pop",
                ctx=ast.Load()
            ),
            args=[ast.Constant(value=index)],
            keywords=[]
        )
    )


def getCmdRunAst(node):
    '''
        Command: run(<startBehavior>)

        Synthesized:

        if __name__ == "__main__":
            nextBehavior = <startBehavior>
            while nextBehavior:
                nextBehavior = globals()[nextBehavior]()
    '''
    nextBehavior = node["args"][0]["value"]
    return ast.If(
        test=ast.Compare(
            left=ast.Name(id="__name__", ctx=ast.Load()),
            ops=[ast.Eq()],
            comparators=[
                ast.Constant(value="__main__")
            ],
        ),
        body=[
            ast.Assign(
                targets=[
                    ast.Name(id="nextBehavior", ctx=ast.Store())
                ],
                value=ast.Constant(value=nextBehavior),
            ),
            ast.Assign(
                targets=[
                    ast.Name(id="worldState", ctx=ast.Store())
                ],
                value=ast.Dict(
                    keys=[],
                    values=[]
                )
            ),
            ast.While(
                test=ast.Name(id="nextBehavior", ctx=ast.Load()),
                body=[
                    ast.Assign(
                        targets=[
                            ast.Name(id="nextBehavior", ctx=ast.Store())
                        ],
                        value=ast.Call(
                            func=ast.Subscript(
                                value=ast.Call(
                                    func=ast.Name(
                                        id="globals",
                                        ctx=ast.Load(),
                                    ),
                                    args=[],
                                    keywords=[],
                                ),
                                slice=ast.Name(
                                    id="nextBehavior",
                                    ctx=ast.Load(),
                                ),
                                ctx=ast.Load(),
                            ),
                            args=[],
                            keywords=[],
                        ),
                    )
                ],
                orelse=[],
            ),
        ],
        orelse=[],
    )