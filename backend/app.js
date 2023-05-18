import express from "express";
import { spawn } from "child_process";

const app = express()
app.use(express.json());

const executePython = async(script, args) => {
    const _arguments = args.map(arg => arg.toString())
    const py = spawn('python', [script, ..._arguments])

    const result = await new Prormise(() => {
        let output;

        py.stdout.on('data', (data) => {
            output = JSON.parse;
        }) 
    })
    return result
}

app.get('/run-script', async (req, res) => {
    // Get the arguments from the query string or request body
    const username = req.body.username;
    const password = req.body.password;
    const save_csv = req.body.save_csv;
    const send_email = req.body.send_email;

    const result = await executePython("./python/scrapper.py", [username, password, save_csv, send_email])

    // res.status(201).send("run successfully!")
    res.status(200).send({output: result})
})

export default app;