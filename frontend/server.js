const express = require('express');
const serveStatic = require("serve-static")
const history = require('connect-history-api-fallback')
const path = require('path');

app = express();

app.use(history({
    index: '/index.html'
}))
app.use(serveStatic(path.join(__dirname, 'dist')));

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
    console.log('Server started: ', 'http://127.0.0.1:' + PORT)
});


