# FastAPI Backend Specification for Performance Review System

## Overview
This document outlines all the required FastAPI endpoints for the performance review system based on the frontend functionality implemented.

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication
All endpoints (except login) require JWT authentication via Authorization header:
```
Authorization: Bearer <jwt_token>
```

---

## 1. Authentication Endpoints

### 1.1 Login
```http
POST /auth/login
```

**Request Body:**
```json
{
  "email": "user@company.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@company.com",
    "name": "John Doe",
    "role": "Employee",
    "department": "Engineering",
    "position": "Software Engineer"
  }
}
```

### 1.2 Refresh Token
```http
POST /auth/refresh
```

**Request Body:**
```json
{
  "refresh_token": "refresh_token_here"
}
```

### 1.3 Logout
```http
POST /auth/logout
```

---

## 2. Performance Cycle Management

### 2.1 Get Active Performance Cycle
```http
GET /performance-cycles/active
```

**Response:**
```json
{
  "id": 1,
  "name": "Q4 2024 Performance Review",
  "start_date": "2024-10-01",
  "end_date": "2024-12-31",
  "status": "active",
  "description": "Quarterly performance review cycle"
}
```

### 2.2 Get All Performance Cycles (Admin/HR)
```http
GET /performance-cycles
```

**Query Parameters:**
- `status`: Filter by status (active, inactive, completed)
- `page`: Page number for pagination
- `limit`: Items per page

### 2.3 Create Performance Cycle (Admin/HR)
```http
POST /performance-cycles
```

**Request Body:**
```json
{
  "name": "Q1 2025 Performance Review",
  "start_date": "2025-01-01",
  "end_date": "2025-03-31",
  "description": "Q1 performance review cycle"
}
```

### 2.4 Update Performance Cycle (Admin/HR)
```http
PUT /performance-cycles/{cycle_id}
```

### 2.5 Delete Performance Cycle (Admin/HR)
```http
DELETE /performance-cycles/{cycle_id}
```

---

## 3. User Management

### 3.1 Get Current User Profile
```http
GET /users/profile
```

### 3.2 Get All Users (Admin)
```http
GET /users
```

**Query Parameters:**
- `role`: Filter by role
- `department`: Filter by department
- `page`: Page number
- `limit`: Items per page

### 3.3 Get Available Reviewers
```http
GET /users/reviewers
```

**Query Parameters:**
- `department`: Filter by department
- `exclude_current_user`: Boolean to exclude current user

**Response:**
```json
[
  {
    "id": 1,
    "name": "John Smith",
    "email": "john.smith@company.com",
    "department": "Engineering",
    "position": "Senior Engineer",
    "is_available": true
  }
]
```

### 3.4 Create User (Admin)
```http
POST /users
```

**Request Body:**
```json
{
  "email": "newuser@company.com",
  "name": "New User",
  "role": "Employee",
  "department": "Engineering",
  "position": "Software Engineer",
  "password": "password123"
}
```

### 3.5 Update User (Admin)
```http
PUT /users/{user_id}
```

### 3.6 Delete User (Admin)
```http
DELETE /users/{user_id}
```

---

## 4. Reviewer Selection (Mentee Functionality)

### 4.1 Submit Reviewer Selection
```http
POST /reviewer-selections
```

**Request Body:**
```json
{
  "performance_cycle_id": 1,
  "selected_reviewers": [1, 2, 3],
  "comments": "Optional comments about selection"
}
```

### 4.2 Get Current User's Reviewer Selection
```http
GET /reviewer-selections/my-selection
```

**Response:**
```json
{
  "id": 1,
  "performance_cycle_id": 1,
  "mentee_id": 1,
  "selected_reviewers": [
    {
      "id": 1,
      "name": "John Smith",
      "email": "john.smith@company.com",
      "department": "Engineering",
      "position": "Senior Engineer"
    }
  ],
  "status": "pending",
  "submitted_at": "2024-10-15T10:30:00Z",
  "mentor_feedback": null,
  "created_at": "2024-10-15T10:30:00Z",
  "updated_at": "2024-10-15T10:30:00Z"
}
```

### 4.3 Update Reviewer Selection
```http
PUT /reviewer-selections/{selection_id}
```

**Request Body:**
```json
{
  "selected_reviewers": [1, 2, 4],
  "comments": "Updated selection"
}
```

### 4.4 Delete Reviewer Selection
```http
DELETE /reviewer-selections/{selection_id}
```

---

## 5. Mentor Approval Management

### 5.1 Get Pending Approvals (Mentor)
```http
GET /mentor/approvals/pending
```

**Response:**
```json
[
  {
    "id": 1,
    "mentee": {
      "id": 1,
      "name": "Alice Johnson",
      "email": "alice.johnson@company.com",
      "department": "Engineering",
      "position": "Software Engineer"
    },
    "selected_reviewers": [
      {
        "id": 1,
        "name": "John Smith",
        "email": "john.smith@company.com",
        "department": "Engineering",
        "position": "Senior Engineer"
      }
    ],
    "status": "pending",
    "submitted_at": "2024-10-15T10:30:00Z",
    "performance_cycle": {
      "id": 1,
      "name": "Q4 2024 Performance Review"
    }
  }
]
```

### 5.2 Get All Approvals (Mentor)
```http
GET /mentor/approvals
```

**Query Parameters:**
- `status`: Filter by status (pending, approved, sent_back)
- `page`: Page number
- `limit`: Items per page

### 5.3 Approve Reviewer Selection
```http
POST /mentor/approvals/{selection_id}/approve
```

**Request Body:**
```json
{
  "comments": "Optional approval comments"
}
```

### 5.4 Send Back Reviewer Selection
```http
POST /mentor/approvals/{selection_id}/send-back
```

**Request Body:**
```json
{
  "feedback": "Please add at least one more reviewer for comprehensive feedback",
  "required_changes": ["add_more_reviewers"]
}
```

### 5.5 Get Approval Details
```http
GET /mentor/approvals/{selection_id}
```

---

## 6. Feedback Management (Reviewer Functionality)

### 6.1 Get Assigned Employees (Reviewer)
```http
GET /reviewer/assignments
```

**Response:**
```json
[
  {
    "id": 1,
    "employee": {
      "id": 1,
      "name": "Alice Johnson",
      "email": "alice.johnson@company.com",
      "department": "Engineering",
      "position": "Software Engineer"
    },
    "performance_cycle": {
      "id": 1,
      "name": "Q4 2024 Performance Review"
    },
    "assignment_date": "2024-10-15T10:30:00Z",
    "feedback_status": "pending"
  }
]
```

### 6.2 Get Feedback Forms (Reviewer)
```http
GET /reviewer/feedback-forms
```

**Query Parameters:**
- `status`: Filter by status (draft, submitted)
- `employee_id`: Filter by employee
- `page`: Page number
- `limit`: Items per page

### 6.3 Create Feedback Form
```http
POST /reviewer/feedback-forms
```

**Request Body:**
```json
{
  "employee_id": 1,
  "performance_cycle_id": 1,
  "strengths": "Alice shows excellent problem-solving skills and is a great team player.",
  "improvements": "Could improve time management and documentation skills.",
  "overall_rating": "tracking_expected",
  "status": "draft"
}
```

### 6.4 Update Feedback Form
```http
PUT /reviewer/feedback-forms/{form_id}
```

**Request Body:**
```json
{
  "strengths": "Updated strengths feedback",
  "improvements": "Updated improvements feedback",
  "overall_rating": "tracking_above",
  "status": "submitted"
}
```

### 6.5 Get Feedback Form Details
```http
GET /reviewer/feedback-forms/{form_id}
```

### 6.6 Delete Feedback Form
```http
DELETE /reviewer/feedback-forms/{form_id}
```

---

## 7. Dashboard Statistics

### 7.1 Get Dashboard Stats (Role-based)
```http
GET /dashboard/stats
```

**Response (Employee):**
```json
{
  "reviewers_selected": 2,
  "submission_status": "pending",
  "performance_cycle": {
    "id": 1,
    "name": "Q4 2024 Performance Review",
    "start_date": "2024-10-01",
    "end_date": "2024-12-31"
  }
}
```

**Response (Mentor):**
```json
{
  "pending_approvals": 3,
  "approved_today": 1,
  "total_mentees": 5,
  "performance_cycle": {
    "id": 1,
    "name": "Q4 2024 Performance Review",
    "start_date": "2024-10-01",
    "end_date": "2024-12-31"
  }
}
```

**Response (Reviewer):**
```json
{
  "pending_reviews": 2,
  "completed_reviews": 1,
  "draft_reviews": 1,
  "performance_cycle": {
    "id": 1,
    "name": "Q4 2024 Performance Review",
    "start_date": "2024-10-01",
    "end_date": "2024-12-31"
  }
}
```

---

## 8. Admin/HR Management

### 8.1 Get System Overview (Admin/HR)
```http
GET /admin/overview
```

**Response:**
```json
{
  "total_users": 150,
  "active_performance_cycle": {
    "id": 1,
    "name": "Q4 2024 Performance Review",
    "participants": 120,
    "completed_reviews": 85,
    "pending_reviews": 35
  },
  "recent_activities": [
    {
      "id": 1,
      "action": "reviewer_selection_submitted",
      "user": "Alice Johnson",
      "timestamp": "2024-10-15T10:30:00Z"
    }
  ]
}
```

### 8.2 Get Performance Review Reports
```http
GET /admin/reports/performance-reviews
```

**Query Parameters:**
- `cycle_id`: Performance cycle ID
- `department`: Filter by department
- `status`: Filter by review status
- `start_date`: Start date filter
- `end_date`: End date filter

### 8.3 Export Performance Data
```http
GET /admin/export/performance-data
```

**Query Parameters:**
- `cycle_id`: Performance cycle ID
- `format`: Export format (csv, excel, pdf)

---

## 9. Notifications

### 9.1 Get User Notifications
```http
GET /notifications
```

**Query Parameters:**
- `unread_only`: Boolean to get only unread notifications
- `page`: Page number
- `limit`: Items per page

### 9.2 Mark Notification as Read
```http
PUT /notifications/{notification_id}/read
```

### 9.3 Mark All Notifications as Read
```http
PUT /notifications/read-all
```

---

## 10. Data Models (Pydantic Schemas)

### 10.1 User Model
```python
class User(BaseModel):
    id: int
    email: str
    name: str
    role: str
    department: str
    position: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
```

### 10.2 Performance Cycle Model
```python
class PerformanceCycle(BaseModel):
    id: int
    name: str
    start_date: date
    end_date: date
    status: str
    description: str
    created_at: datetime
    updated_at: datetime
```

### 10.3 Reviewer Selection Model
```python
class ReviewerSelection(BaseModel):
    id: int
    performance_cycle_id: int
    mentee_id: int
    selected_reviewers: List[User]
    status: str
    submitted_at: datetime
    mentor_feedback: Optional[str]
    created_at: datetime
    updated_at: datetime
```

### 10.4 Feedback Form Model
```python
class FeedbackForm(BaseModel):
    id: int
    employee_id: int
    reviewer_id: int
    performance_cycle_id: int
    strengths: str
    improvements: str
    overall_rating: str
    status: str
    created_at: datetime
    updated_at: datetime
```

---

## 11. Error Responses

### 11.1 Standard Error Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "field": "email",
      "issue": "Invalid email format"
    }
  }
}
```

### 11.2 Common HTTP Status Codes
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `422`: Validation Error
- `500`: Internal Server Error

---

## 12. Database Schema (SQLAlchemy Models)

### 12.1 Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    department VARCHAR(100),
    position VARCHAR(100),
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 12.2 Performance Cycles Table
```sql
CREATE TABLE performance_cycles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(50) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 12.3 Reviewer Selections Table
```sql
CREATE TABLE reviewer_selections (
    id SERIAL PRIMARY KEY,
    performance_cycle_id INTEGER REFERENCES performance_cycles(id),
    mentee_id INTEGER REFERENCES users(id),
    status VARCHAR(50) NOT NULL,
    submitted_at TIMESTAMP,
    mentor_feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 12.4 Reviewer Selection Details Table
```sql
CREATE TABLE reviewer_selection_details (
    id SERIAL PRIMARY KEY,
    selection_id INTEGER REFERENCES reviewer_selections(id),
    reviewer_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 12.5 Feedback Forms Table
```sql
CREATE TABLE feedback_forms (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES users(id),
    reviewer_id INTEGER REFERENCES users(id),
    performance_cycle_id INTEGER REFERENCES performance_cycles(id),
    strengths TEXT NOT NULL,
    improvements TEXT NOT NULL,
    overall_rating VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 12.6 Notifications Table
```sql
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(50) NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 13. Implementation Notes

### 13.1 Authentication
- Use JWT tokens for authentication
- Implement refresh token mechanism
- Store password hashes using bcrypt

### 13.2 Authorization
- Implement role-based access control (RBAC)
- Use decorators for endpoint protection
- Validate user permissions for each operation

### 13.3 Database
- Use PostgreSQL for production
- Implement database migrations
- Use connection pooling

### 13.4 Validation
- Use Pydantic for request/response validation
- Implement custom validators for business logic
- Add comprehensive error handling

### 13.5 Performance
- Implement caching for frequently accessed data
- Use database indexing for better query performance
- Implement pagination for large datasets

### 13.6 Security
- Implement rate limiting
- Use HTTPS in production
- Sanitize all user inputs
- Implement audit logging

This specification provides a complete foundation for implementing the FastAPI backend for the performance review system.
