import path from 'path';
import synthesisRunner from "./synthesisRunner.js"
import fs from 'fs/promises';
import { writeFile } from "node:fs/promises";
import { json } from 'stream/consumers';
import unzipper from "unzipper";
import {DalAstGenerator} from "dal-ast-js";
import { copyFile, rm, mkdir } from "fs/promises";

const testStreamMode = async (pathToDesign, behavior) => {    
    const data = await fs.readFile(pathToDesign);

    const ast = new DalAstGenerator().run(data.toString());

    try {
        const synthesizedOutput = await synthesisRunner(JSON.stringify(ast));

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