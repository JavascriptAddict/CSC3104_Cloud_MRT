const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 80;

// Serve the React app's static files
app.use(express.static(path.join(__dirname, 'build')));

// Serve model files for face-api
app.get('/models/:filename', (req, res) => {
    const filePath = path.join(__dirname, 'build', 'models', 'weights', req.params.filename);
    res.sendFile(filePath, (err) => {
        if (err) {
            res.status(err.status).end();
        }
    });
});

// Serve the React app for any other route
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'build', 'index.html'));
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
