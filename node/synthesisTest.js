import path from 'path';
import synthesisRunner from "./synthesisRunner.js"
import fs from 'fs/promises';
import { writeFile } from "node:fs/promises";
import { json } from 'stream/consumers';
import unzipper from "unzipper";


const testStreamMode = async (pathToAst, behavior) => {    
    const data = await fs.readFile(pathToAst);

    try {
        const synthesizedOutput = await synthesisRunner(data);
        const output = JSON.parse(synthesizedOutput);
        console.log("Synthesizer output:", output);
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