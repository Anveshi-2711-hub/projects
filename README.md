# Customer Feedback System

A RESTful API for managing customer feedback built with Node.js, Express, and SQLite.

## Prerequisites

- Node.js (v14 or higher)
- npm (comes with Node.js)

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start the server:
```bash
npm start
```

The server will start on http://localhost:3000

## API Endpoints

### Submit Feedback
- **POST** `/api/feedback`
- Body: 
  ```json
  {
    "customer_name": "string (max 100 chars)",
    "feedback_text": "string (max 1000 chars)",
    "rating": "integer (1-5)"
  }
  ```

### Get All Feedback (Admin Only)
- **GET** `/api/feedback`
- Headers: `Authorization: Bearer supersecretkey123`

### Get Feedback by ID
- **GET** `/api/feedback/:id`

### Delete Feedback (Admin Only)
- **DELETE** `/api/feedback/:id`
- Headers: `Authorization: Bearer supersecretkey123` 