import ast

def getVariableNameWithKeys(name, keys):
    '''
        TODO:
        This was is a legacy function that I used
        when I was supporting special commands like
        set and get from the AST. However, since then
        I've moved the implementation to a much more
        scalable solution by letting the user define
        the transformations. So this will be removed
        after I make that change.
    '''
    current = ast.Name(id=name, ctx=ast.Load())

    for key in keys:
        current = ast.Subscript(
            value=current,
            slice=ast.Constant(value=key),
            ctx=ast.Store()
        )

    return current

def getRunBlock(startingBehavior, loggingMode):
    '''
        Returns the run block used to execute a design.     

        Args:
            startingBehavior (string): First behavior to exhibit.
            loggingMode (boolean): Verbose or minimal logging mode.

        Returns:
            ast: Returns the AST node that was generated using the
            metadata.
    '''
    tryBlock = ast.Try(
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
        handlers=[
            ast.ExceptHandler(
                type=ast.Name(id="Exception", ctx=ast.Load()),
                name="e",
                body=[
                    ast.Expr(
                        value=ast.Call(
                            func=ast.Attribute(
                                value=ast.Name(id="worldStateManager", ctx=ast.Load()),
                                attr="setFailure",
                                ctx=ast.Load(),
                            ),
                            args=[],
                            keywords=[],
                        )
                    ),
                    ast.Raise(
                        exc=ast.Name(id="e", ctx=ast.Load()),
                        cause=None
                    )
                ]
            )
        ],
        orelse=[],
        finalbody=[]
    )

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
                    ast.Name(id="worldStateManager", ctx=ast.Store())
                ],
                value=ast.Call(
                    func=ast.Name(id="WorldState", ctx=ast.Load()),
                    args=[
                        ast.Constant(value=loggingMode)
                    ],
                    keywords=[]
                )
            ),
            ast.Assign(
                targets=[
                    ast.Name(id="nextBehavior", ctx=ast.Store())
                ],
                value=ast.Constant(value=startingBehavior),
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
                body=[tryBlock],
                orelse=[],
            ),
        ],
        orelse=[],
    )