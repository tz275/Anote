const express = require('express');
const app = express();
const port = process.env.PORT || 3001;

app.get("/api", (req, res) => {
    res.json({ message: "Hello from server!" });
  });
  
app.listen(PORT, () => {
    console.log(`Server listening on ${PORT}`);
  });
