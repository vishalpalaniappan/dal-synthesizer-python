import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";
import path from "node:path";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SYNTHESIZER_PATH = path.resolve(__dirname, "../dal_ast_synthesizer.py");

function synthesisRunner(synthPackage, args = []) {
    return new Promise((resolve, reject) => {
        const process = spawn("python3", [SYNTHESIZER_PATH]);
                let settled = false;

        const stdoutChunks = [];
        let stderr = "";

        process.stdout.on("data", (data) => {
            stdoutChunks.push(data);
        });

        process.stderr.on("data", (data) => {
            stderr += data.toString();
        });

        process.on("error", (err) => {
            if (settled) return;
            settled = true;
            reject(err);
        });

        process.on("close", async (code) => {
            if (settled) return;
            settled = true;
            if (code !== 0) {
                reject(new Error(stderr || `Process exited with code ${code}`));
            } else {
                resolve(Buffer.concat(stdoutChunks));
            }
        });

        process.stdin.write(synthPackage);
        process.stdin.end();
    });
}

export default synthesisRunner;