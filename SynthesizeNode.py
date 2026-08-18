import ast
from helper import getRunBlockDesign
from helper import getRunBlockCompositeBehavior

class SynthesizeNode:

    def __init__(self, mode, ):
        self.mode = mode

    def setFileType(self, type, name):
        '''
            Sets the file type (design or composite behavior)

            Sets the name (used to choose the method name in
            synthesized composite behaviors so that it can be
            invoked from other behaviors)
        '''
        self.fileType = type
        self.name = name

    def run(self, node):
        '''
            Get the AST node given the dalAST metadata.

            DAL Identifiers: get<Identifier>Ast
            Commands: getCmd<CommandName>Ast
            Registered: getRegisteredCall
        '''
        type = node["type"]
        if (type == "cmd"):
            cmd = node["command"]
            funcName = f"getCmd{cmd[0].upper() + cmd[1:]}Ast"
        elif (type == "registeredCmd"):
            funcName = f"getRegisteredCall"
        else:
            funcName = f"get{type[0].upper() +type[1:]}Ast"

        method = getattr(self, funcName, None)

        if (callable(method)):
            return getattr(self, funcName)(node)

    def getRegisteredCall(self,node):
        '''
            Invokes a custom opaque transformation and stores the result in store_name.
            If store name is null, it simply calls the transformtion.

            _customCall(<store_name>, <arg1>, <arg2>, <arg3>)
            <store_name> = customCall(<arg1>, <arg2>, <arg3>)

            _customCall(null, <arg1>, <arg2>, <arg3>)
            customCall(<arg1>, <arg2>, <arg3>)
        '''

        # Create the call node
        argsAsType = []
        for arg in node["args"][1:]:
            if (arg["type"] == "name"):
                argsAsType.append(ast.Name(id=arg["value"], ctx=ast.Load()))
            else:
                argsAsType.append(ast.Constant(value=arg["value"]))
        
        callNode = ast.Call(
            func=ast.Name(id=node["command"][1:], ctx=ast.Load()),
            args=argsAsType,
            keywords=[]
        )

        # Create the AST output
        if node["args"][0]["type"] == "null":
            return ast.Expr(value=callNode)
        else:
            return ast.Assign(
                targets=[ast.Name(id=node["args"][0]["value"], ctx=ast.Store())],
                value=callNode
            )

    def getCmdRunCompositeBehaviorAst(self, node):
        '''
            Calls the composite behavior

            runCompositeBehavior(<Behavior>)

            <behavior>()
        '''
        behavior = node["args"][0]["value"]
        
        return ast.Expr(
            value=ast.Call(
                func=ast.Name(id=behavior, ctx=ast.Load()),
                args=[],
                keywords=[]
            )
        )
            
    def getCmdWorldStateManagerAst(self, node):
        '''
            Command structure:
            worldStateManager(<cmd>, <arg>)

            Usage Example:
            worldStateManager(null, "add", "bucket", [])
            worldStateManager.add(bucket, [])

            worldStateManager(uid, "getUid", "bucket")
            uid = worldStateManager.getUid("bucket")
        '''
        cmd = node["args"][1]["value"]

        argList = []
        for arg in node["args"][2:]:
            if (arg["type"] == "name"):
                value = ast.Name(id=arg["value"], ctx=ast.Load())
            else:
                value = ast.Constant(value=arg["value"])
            argList.append(value)

        call = ast.Call(
            func=ast.Attribute(
                value=ast.Name(id="worldStateManager", ctx=ast.Load()),
                attr=cmd,
                ctx=ast.Load(),
            ),
            args=argList,
            keywords=[],
        )

        if (node["args"][0]["type"] == "null"):
            return ast.Expr(value=call)
        else:
            return ast.Assign(
                targets=[
                    ast.Name(id=node["args"][0]["value"], ctx=ast.Store())
                ],
                value=call
            )
 
    def getBehaviorAst(self, node):
        '''
            def <behaviorName>():
                global worldState
        '''
        logBehavior = ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="worldStateManager", ctx=ast.Load()),
                    attr="setBehavior",
                    ctx=ast.Load(),
                ),
                args=[
                    ast.Constant(value=node["behaviorName"]),
                ],
                keywords=[],
            )
        )

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
            body= [logBehavior],
            decorator_list=[]
        )

    def getDesignAst(self, node):
        '''
            design = <design_Name>
        '''
        return ast.Assign(
            targets=[
                ast.Name(id="design", ctx=ast.Store())
            ],
            value=ast.Constant(value=node["design_name"][0]["value"])
        )

    def getWhileAst(self, node):
        '''
            while <condition>:
                <body>
        '''
        return ast.While(
            test=ast.Name(id=node["args"][0]["value"], ctx=ast.Load()),
            body=[],
            orelse=[]
        )

    def getInvariantAst(self, node):
        '''
            In verbose mode, tell synthesizer to show
            the body of the invariant.
        '''
        if self.mode == "verbose":
            return "render_body"
        else:
            return None

    def getSelectAst(self, node):
        '''
            Returning render body to tell synthesizer
            to synthesize body of node even though I am
            not returning a valid ast.
        '''
        return "render_body"

    def getIfAst(self, node):
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

    def getCmdGoToBehaviorAst(self, node):
        '''
            Command: select(<nextBehavior>)

            Synthesized: return <nextBehavior>
        '''
        returnValue = node["args"][0]["value"]
        return ast.Return(
            value=ast.Constant(value=returnValue)
        )

    def getCmdRunAstV2(self,node):
        '''
            I'm moving the run command to a new version so that
            it can run a design and a composite behavior. It will
            be specified in the following way:

            design(<design_name>)
            compositeBehavior(<composite_behavior>)

            Then the run command will synthesize the relevant structure
            neeed. Below, I show the example of a composite behavior, it
            exposes a method that other behaviors can use to invoke it.

            Command: 
                run(<startBehavior>)

            Synthesized:
                def <composite_behavior>():
                    nextBehavior = (<startBehavior>
                    
                    nextBehavior = <startBehavior>
                    while nextBehavior:
                        try:
                            nextBehavior = globals()[nextBehavior]()
                        except Exception as e:
                            worldStateManager.setFailure(nextBehavior)

                if __name__ == "__main__":
                    <composite_behavior>(args...)    

            Invoking composite behavior:
                runCompositeBehavior(<compositeBehavior>)
                
            Synthesized:                
                <compositeBehavior>()

            This is being done to establish a boundary between a 
            composite behavior and its environment. In this case,
            the meaning  is being invoked by another behavior while
            providing the necessary participants to realize the
            meaning. 

            Since all the behaviors are accessing the same world 
            state module, the behavior can access the necessary
            participants directly.

            If I wanted to test the behavior locally, I can simply
            provide a world state but it will be ultimatly used as
            part of a larger design that will provide the necessary
            world state.
            
            The higher level meaning will contain a library world and
            this is then operated on by the behavior. In order to add
            a book to the library, you need a library world with the
            basket.
        '''
        pass

    def getCmdRunAst(self, node):
        '''
            Command: run(<startBehavior>)

            Synthesized:

            if __name__ == "__main__":
                nextBehavior = <startBehavior>
                while nextBehavior:
                    try:
                        nextBehavior = globals()[nextBehavior]()
                    except Exception as e:
                        worldStateManager.setFailure(nextBehavior)
        '''
        startingBehavior = node["args"][0]["value"]
        loggingMode = self.mode
        if self.fileType == "design":
            return getRunBlockDesign(startingBehavior, loggingMode)
        elif self.fileType == "compositeBehavior":
            return getRunBlockCompositeBehavior(startingBehavior, self.name)