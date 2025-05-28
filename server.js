const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const cors = require('cors');
const path = require('path');

const app = express();
const port = 3001;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Database setup
const db = new sqlite3.Database(path.join(__dirname, 'db', 'feedback.db'), (err) => {
    if (err) {
        console.error('Error opening database:', err);
    } else {
        console.log('Connected to SQLite database');
        // Create feedback table if it doesn't exist
        db.run(`CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL CHECK(length(customer_name) <= 100),
            feedback_text TEXT NOT NULL CHECK(length(feedback_text) <= 1000),
            rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
            submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )`, (err) => {
            if (err) {
                console.error('Error creating table:', err);
            } else {
                // Insert test data
                const testData = [
                    ['Alice Smith', 'Excellent service! The staff was very helpful.', 5],
                    ['Bob Johnson', 'Good experience overall, but could be faster.', 4],
                    ['Carol White', 'Average service, nothing special.', 3]
                ];
                
                const insert = 'INSERT OR IGNORE INTO feedback (customer_name, feedback_text, rating) VALUES (?, ?, ?)';
                testData.forEach(data => {
                    db.run(insert, data, (err) => {
                        if (err) console.error('Error inserting test data:', err);
                    });
                });
                console.log('Test data initialized');
            }
        });
    }
});

// Middleware to check admin token
const checkAdminToken = (req, res, next) => {
    const authHeader = req.headers.authorization;
    if (!authHeader || authHeader !== 'Bearer supersecretkey123') {
        return res.status(401).json({ error: 'Unauthorized' });
    }
    next();
};

// POST /api/feedback - Submit new feedback
app.post('/api/feedback', (req, res) => {
    const { customer_name, feedback_text, rating } = req.body;

    // Input validation
    if (!customer_name || !feedback_text || !rating) {
        return res.status(400).json({ error: 'All fields are required' });
    }

    if (customer_name.length > 100) {
        return res.status(400).json({ error: 'Customer name must be 100 characters or less' });
    }

    if (feedback_text.length > 1000) {
        return res.status(400).json({ error: 'Feedback text must be 1000 characters or less' });
    }

    if (!Number.isInteger(rating) || rating < 1 || rating > 5) {
        return res.status(400).json({ error: 'Rating must be an integer between 1 and 5' });
    }

    const sql = `INSERT INTO feedback (customer_name, feedback_text, rating) VALUES (?, ?, ?)`;
    db.run(sql, [customer_name, feedback_text, rating], function(err) {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.status(201).json({
            id: this.lastID,
            customer_name,
            feedback_text,
            rating,
            submitted_at: new Date().toISOString()
        });
    });
});

// GET /api/feedback - Get all feedback (admin only)
app.get('/api/feedback', checkAdminToken, (req, res) => {
    const sql = 'SELECT * FROM feedback ORDER BY submitted_at DESC';
    db.all(sql, [], (err, rows) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json(rows);
    });
});

// GET /api/feedback/:id - Get feedback by ID
app.get('/api/feedback/:id', (req, res) => {
    const sql = 'SELECT * FROM feedback WHERE id = ?';
    db.get(sql, [req.params.id], (err, row) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        if (!row) {
            return res.status(404).json({ error: 'Feedback not found' });
        }
        res.json(row);
    });
});

// DELETE /api/feedback/:id - Delete feedback (admin only)
app.delete('/api/feedback/:id', checkAdminToken, (req, res) => {
    const sql = 'DELETE FROM feedback WHERE id = ?';
    db.run(sql, [req.params.id], function(err) {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        if (this.changes === 0) {
            return res.status(404).json({ error: 'Feedback not found' });
        }
        res.json({ message: 'Feedback deleted successfully' });
    });
});

// 404 handler
app.use((req, res) => {
    res.status(404).json({ error: 'Not found' });
});

// Error handler
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Something broke!' });
});

// Start server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
}); 