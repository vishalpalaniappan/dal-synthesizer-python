import ast

def getRunBlockDesign(startingBehavior):
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


def getRunBlockCompositeBehavior(startingBehavior, behaviorName):
    '''
        Returns the run block for composite behavior. For composite
        behaviors, it provides a function with the name of the
        composite behavior. This can be invoked by other behaviors that
        import it. 

        Args:
            startingBehavior (string): First behavior to exhibit.
            behaviorName (string): Name of the behavior (function name)

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

    return ast.FunctionDef(
        name=behaviorName,
        args=ast.arguments(
            posonlyargs=[],
            args=[],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]
        ),
        body=[
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
            )
        ],
        decorator_list=[]
    )