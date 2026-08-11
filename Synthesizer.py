import ast
import os
import io
import sys
import json
from pathlib import Path
from SynthesizeNode import SynthesizeNode
import shutil

class Synthesizer:
    
    def __init__(self, dalAst, mode, stream):
        self.dalAst = dalAst
        self.stream = stream
        self.mode = mode
        self.designName = None
        self.actors = []
        self.pythonAst = ast.Module(
            body=[],
            type_ignores=[]
        )
        self.nodeSynthesizer = SynthesizeNode(mode)

    def run(self):
        '''
            Run the synthesizer
            -------------------------------------
            - Processes AST to extract each actor
            - Processes each actors AST and synthesizes each node
            - Creates metadata file that has the necessary files to include
              and the commands to run the design
            - Includes the synthesizer defined files (logging helper, world state manager)
            - Streams output or writes it to folder.
        '''
        self.getActors()

        if self.designName == None:
            raise RuntimeError("No design name provided")

        output = {}

        with open(Path(__file__).parent / "output_helpers" / "LoggingHelper.py","r") as f:
            output["LoggingHelper.py"] = f.read()

        with open(Path(__file__).parent / "output_helpers" / "WorldState.py","r") as f:
            output["WorldState.py"] = f.read()

        required = []
        for actor in self.actors:
            if not self.stream:
                print("Processing Actor:", actor["actorName"])

            self.pythonAst = ast.Module(body=[],type_ignores=[])
            
            # Process each node in the DAL ast.
            for node in actor["body"]:
                self.processTree(node, self.pythonAst, 0)

            self.pythonAst.body.insert(0, ast.parse("from LoggingHelper import semanticLogger").body[0])
            self.pythonAst.body.insert(0, ast.parse("from WorldState import WorldState").body[0])

            if "includes" in actor:
                for inc in actor["includes"]:
                    required.append(inc[0])
                    if inc[0].endswith(".py"):
                        name = os.path.splitext(inc[0])[0] 
                        self.pythonAst.body.insert(0, ast.parse(f"from {name} import *").body[0])

            synthSrc = ast.unparse(self.pythonAst)
            output[f'{actor[f"actorName"]}.py'] = synthSrc

        metadata = {
            "designName": self.designName,
            "actors": [],
            "commands":[],
            "required": required
        }
        for actor in self.actors:
            metadata["actors"].append(actor["actorName"])
            metadata["commands"].append(f"python3 {actor['actorName']}.py")

        output["metadata.json"] = json.dumps(metadata)

        # Stream through stdout or write to output folder
        if self.stream:
            sys.stdout.buffer.write(json.dumps(output).encode("utf-8"))
        else:
            self.clearOutputFolder()
            for file in output:
                self.writeToOutputFolder(output[file], file)

    def clearOutputFolder(self):
        '''
            Clears the output folder and loads the helper files used
            across all the applications.
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

        # Make traces folder if it doesn't exist
        tracesFolder = Path(__file__).parent / "output" / "traces"
        tracesFolder.mkdir(parents=True, exist_ok=True)

        designFolder = Path(__file__).parent / "output" / self.designName
        designFolder.mkdir(parents=True, exist_ok=True)

    def writeToOutputFolder(self, src, name):
        '''
            Writes the synthesized output to output folder and
            also adds the logging helper.

            If the output folder has files, clear it.
        '''
        designFolder = Path(__file__).parent / "output" / self.designName
        designFolder.mkdir(parents=True, exist_ok=True)

        # Write the synthesized output
        outputFile = Path(__file__).parent / "output" / self.designName / f'{name}'
        with open(outputFile,"w+") as f:
            f.write(src)


    def processTree(self, dalAstNode, pythonAstNode, indent):
        '''
            Process the tree node. If there is a body, process
            each node in the body.

            Writes the synthesized ast node to the ast tree.
        '''
        # self.printTree(indent, dalAstNode["type"])
        astNodeBody = self.nodeSynthesizer.run(dalAstNode)

        if astNodeBody is None:
            if dalAstNode['type'] == "cmd":
                type = dalAstNode['type'] + "," + dalAstNode['command']
            else:
                type = dalAstNode['type']

            if not self.stream:
                print(f"Unable to synthesize node of type {type}")

        elif astNodeBody == "render_body":
            if "body" in dalAstNode:
                for node in dalAstNode["body"]:
                    self.processTree(node, pythonAstNode, indent + 1)
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

    def getActors(self):
        '''
            Gets all the actors from the design file.
        '''
        self.actors = []
        for node in self.dalAst["body"]:
            if node["type"] == "design":
                self.designName = node["design_name"][0]["value"]
            elif node["type"] == "actor":
                self.actors.append(node)