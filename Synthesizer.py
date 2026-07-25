import ast
from pathlib import Path
from getSynthesizedNode import getSynthesizedNode
import shutil

class Synthesizer:
    
    def __init__(self, dalAst):
        self.dalAst = dalAst
        self.pythonAst = ast.Module(
            body=[],
            type_ignores=[]
        )

    def run(self):
        '''
            Run the synthesizer
        '''
        # Process each node in the DAL ast.
        for node in self.dalAst["body"]:
            self.processTree(node, self.pythonAst, 0)

        importNode = ast.parse("from LoggingHelper import semanticLogger").body[0]
        self.pythonAst.body.insert(0, importNode)

        self.writeToOutputFolder()


    def writeToOutputFolder(self):
        '''
            Writes the synthesized output to output folder and
            also adds the logging helper.

            If the output folder has files, clear it.
        '''
        outputFolder = Path(__file__).parent / "output"

        # Make folder if it doesn't exist
        outputFolder.mkdir(parents=True, exist_ok=True)

        # Clear the output folder (assuming it existed)
        for item in outputFolder.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()

        # Write the synthesized output
        outputFile = Path(__file__).parent / "output" / "synthesized.py"
        with open(outputFile,"w+") as f:
            f.write(ast.unparse(self.pythonAst))

        # Copyt logging helper
        src = Path(__file__).parent / "output_helpers" / "LoggingHelper.py"
        dst = Path(__file__).parent / "output" / "LoggingHelper.py"
        shutil.copy(src, dst)


    def processTree(self, dalAstNode, pythonAstNode, indent):
        '''
            Process the tree node. If there is a body, process
            each node in the body.

            Writes the synthesized ast node to the ast tree.
        '''
        # self.printTree(indent, dalAstNode["type"])
        astNodeBody = getSynthesizedNode(dalAstNode)

        if astNodeBody is None:
            if dalAstNode['type'] == "cmd":
                type = dalAstNode['type'] + "," + dalAstNode['command']
            else:
                type = dalAstNode['type']
            print(f"Unable to synthesize node of type {type}")
        else:
            ast.fix_missing_locations(astNodeBody)
            pythonAstNode.body.append(astNodeBody)
        
            if "body" in dalAstNode:
                for node in dalAstNode["body"]:
                    self.processTree(node, astNodeBody, indent + 1)

    def printTree(self, indent, value):
        '''
            Prints Tree with indentation for inspection.
        '''
        spaces = (indent * 4) * " "
        print(f"{spaces}{value}")