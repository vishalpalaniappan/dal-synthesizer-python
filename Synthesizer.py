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
        '''
        self.getActors()

        if self.designName == None:
            raise RuntimeError("No design name provided")

        self.clearOutputFolder()
        metadata = {}

        for actor in self.actors:
            if not self.stream:
                print("Processing Actor:", actor["actorName"])

            self.pythonAst = ast.Module(body=[],type_ignores=[])
            
            # Process each node in the DAL ast.
            for node in actor["body"]:
                self.processTree(node, self.pythonAst, 0)

            self.pythonAst.body.insert(0, ast.parse("from LoggingHelper import semanticLogger").body[0])
            self.pythonAst.body.insert(0, ast.parse("from registered import *").body[0])
            self.pythonAst.body.insert(0, ast.parse("from WorldState import WorldState").body[0])

            synthSrc = ast.unparse(self.pythonAst)

            if self.stream:
                metadata[f'{actor[f"actorName"]}.py'] = synthSrc
            else:
                self.writeToOutputFolder(synthSrc, actor["actorName"])

        # If stream mode, write the synth output package through stdout
        if self.stream:
            with open(Path(__file__).parent / "output_helpers" / "LoggingHelper.py","r") as f:
                metadata["LoggingHelper.py"] = f.read()

            with open(Path(__file__).parent / "output_helpers" / "WorldState.py","r") as f:
                metadata["WorldState.py"] = f.read()

            sys.stdout.buffer.write(json.dumps(metadata).encode("utf-8"))

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

        designFolder = Path(__file__).parent / "output" / self.designName
        designFolder.mkdir(parents=True, exist_ok=True)

        # Copyt logging helper
        src = Path(__file__).parent / "output_helpers" / "LoggingHelper.py"
        dst = Path(__file__).parent / "output" / self.designName / "LoggingHelper.py"
        shutil.copy(src, dst)

        # Copyt worldState
        src = Path(__file__).parent / "output_helpers" / "WorldState.py"
        dst = Path(__file__).parent / "output" / self.designName / "WorldState.py"
        shutil.copy(src, dst)

    def writeToOutputFolder(self, synthSrc, actorName):
        '''
            Writes the synthesized output to output folder and
            also adds the logging helper.

            If the output folder has files, clear it.
        '''
        designFolder = Path(__file__).parent / "output" / self.designName
        designFolder.mkdir(parents=True, exist_ok=True)

        # Write the synthesized output
        outputFile = Path(__file__).parent / "output" / self.designName / f'{actorName}.py'
        with open(outputFile,"w+") as f:
            f.write(synthSrc)


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