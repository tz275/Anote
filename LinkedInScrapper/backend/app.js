import express from "express";
import { spawn } from "child_process";
import { resolve } from "path";

const app = express()
app.use(express.json());

const executePython = (script, args, res) => {
    const _arguments = args.map(arg => arg.toString())
    const py = spawn('python', [script, ..._arguments])
    let success = true;

    py.stdout.on("data", (data) => {
        const lines = data.toString().trim().split("\n");
        for (const line of lines) {
            console.log(line)
            if (line === "wrong username or password") {
                res.status(500).send("wrong username or password")
            }
            if (line) {
                res.write(`data: ${line}\n\n`); // Send each print statement as a server-sent event
            }
        }
    });

    py.stderr.on("data", (data) => {
        console.error(`stderr: ${data}`);
        success = false;
    });

    py.on("close", (code) => {
        if (code !== 0) {
            console.error(`Python script exited with code ${code}`);
            success = false;
        }
        res.end();
        if (success) {
            res.status(200);
        } else {
            res.status(500);
        }
    });

}

app.get('/run-script', async (req, res) => {
    // Get the arguments from the query string or request body
    const username = req.body.username;
    const password = req.body.password;
    const save_csv = req.body.save_csv;
    const send_message = req.body.send_message;

    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');

    executePython("./python/scrapper.py", [username, password, save_csv, send_message], res);
})

export default app;
