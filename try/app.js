const express = require('express');
const {spawn} = require("child_process")

const app = express();

const executePython = (script, args, res) => {
    const arguments = args.map(arg => arg.toString())
    const py = spawn("python", [script, ...arguments])
    let success = true;

    py.stdout.on("data", (data) => {
        const lines = data.toString().trim().split("\n");
        for (const line of lines) {
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

// Server-Sent Events (SSE)
app.get('/', (req, res) => {
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');
    executePython('python/hi.py', [], res);
});


const port = 3001; // You can change the port number if desired

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});

module.exports = app;