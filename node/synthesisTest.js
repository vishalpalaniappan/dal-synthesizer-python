import path from 'path';
import synthesisRunner from "./synthesisRunner.js"
import fs from 'fs/promises';
import { writeFile } from "node:fs/promises";
import { json } from 'stream/consumers';
import unzipper from "unzipper";
import {DalAstGenerator} from "dal-ast-js";
import { copyFile, rm, mkdir } from "fs/promises";

const testStreamMode = async (pathToDesign, behavior) => {    

    // Create an asts object with all the necessary designs to send
    // to the synthesizer (currently not connected to the synth)
    const designFolder = path.dirname(pathToDesign);
    const filesToProcess = [path.basename(pathToDesign)]
    const asts = {};

    while (filesToProcess.length > 0) {
        for (const _file of filesToProcess) {
            const compositeImport = filesToProcess.pop();
            const importPath = path.join(designFolder, compositeImport);
            const data = await fs.readFile(importPath);
            const ast = new DalAstGenerator().run(data.toString());
            asts[compositeImport] = ast;

            // If the ast has imports, add it so we can process it
            if (!ast?.imports) continue
            for (const _import of ast?.imports) {
                // Don't add twice
                if (filesToProcess.includes(_import[0])) continue
                // Don't reprocess same file
                if (_import[0] in asts) continue
                // Add file to be processed
                filesToProcess.push(_import[0]);
            }
        }
    }

    // Write AST to file
    const astPath = path.join(process.cwd(), "node", "ast", path.basename(pathToDesign)+".json");
    await fs.writeFile(astPath, JSON.stringify(asts));

    // TODO: Detect circular dependencies

    // Synthesize the design at the provided path
    const data = await fs.readFile(pathToDesign);
    const ast = new DalAstGenerator().run(data.toString());

    try {
        const synthesizedOutput = await synthesisRunner(JSON.stringify(asts));

        const synthObj = JSON.parse(synthesizedOutput.toString());
        const synthPath = path.join(process.cwd(), "node", "output");
        await rm(synthPath, { recursive: true, force: true });
        await mkdir(synthPath, { recursive: true });

        for (const [name, value] of Object.entries(synthObj)) {
            const filePath = path.join(process.cwd(), "node", "output", name);
            await fs.writeFile(filePath, value);
        }
    } catch (err) {
        console.error("Error during synthesis execution:");
        console.error(err);
        process.exit(1);
    }
}

const args = process.argv;
if (args.length < 3) {
    console.error("Please provide the path to the design file as an argument.");
    process.exit(1);
}

const pathToAst = args[2];
testStreamMode(pathToAst).catch((err) => {
    console.error("Error during test execution:", err);
    process.exit(1);
});