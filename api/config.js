const express = require('express');
const router = express.Router();
require('dotenv').config();

router.get('/config', (req, res) => {
    res.json({
        apiKey: process.env.OPENAI_API_KEY
    });
});

module.exports = router; 