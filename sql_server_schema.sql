-- SQL Server Database Schema for Performance Review System
-- Run this script to create the database and tables

-- Create database (run this as SA or database admin)
-- CREATE DATABASE performance_review;
-- GO

USE kedaara;
GO

-- Create Users table
CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    email NVARCHAR(255) UNIQUE NOT NULL,
    name NVARCHAR(255) NOT NULL,
    role NVARCHAR(50) NOT NULL, -- Employee, Mentor, HR Lead, System Administrator, People Committee
    department NVARCHAR(100),
    position NVARCHAR(100),
    password_hash NVARCHAR(255) NOT NULL,
    is_active BIT DEFAULT 1,
    created_at DATETIME2 DEFAULT GETUTCDATE(),
    updated_at DATETIME2 DEFAULT GETUTCDATE()
);
GO

-- Create Performance Cycles table
CREATE TABLE performance_cycles (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(255) NOT NULL,
    start_date DATETIME2 NOT NULL,
    end_date DATETIME2 NOT NULL,
    status NVARCHAR(50) NOT NULL, -- active, inactive, completed
    description NVARCHAR(MAX),
    created_at DATETIME2 DEFAULT GETUTCDATE(),
    updated_at DATETIME2 DEFAULT GETUTCDATE()
);
GO

-- Create Reviewer Selections table
CREATE TABLE reviewer_selections (
    id INT IDENTITY(1,1) PRIMARY KEY,
    performance_cycle_id INT NOT NULL,
    mentee_id INT NOT NULL,
    status NVARCHAR(50) NOT NULL, -- pending, approved, sent_back
    submitted_at DATETIME2,
    mentor_feedback NVARCHAR(MAX),
    created_at DATETIME2 DEFAULT GETUTCDATE(),
    updated_at DATETIME2 DEFAULT GETUTCDATE(),
    FOREIGN KEY (performance_cycle_id) REFERENCES performance_cycles(id),
    FOREIGN KEY (mentee_id) REFERENCES users(id)
);
GO

-- Create Reviewer Selection Details table
CREATE TABLE reviewer_selection_details (
    id INT IDENTITY(1,1) PRIMARY KEY,
    selection_id INT NOT NULL,
    reviewer_id INT NOT NULL,
    created_at DATETIME2 DEFAULT GETUTCDATE(),
    FOREIGN KEY (selection_id) REFERENCES reviewer_selections(id),
    FOREIGN KEY (reviewer_id) REFERENCES users(id)
);
GO

-- Create Feedback Forms table
CREATE TABLE feedback_forms (
    id INT IDENTITY(1,1) PRIMARY KEY,
    employee_id INT NOT NULL,
    reviewer_id INT NOT NULL,
    performance_cycle_id INT NOT NULL,
    strengths NVARCHAR(MAX) NOT NULL,
    improvements NVARCHAR(MAX) NOT NULL,
    overall_rating NVARCHAR(50) NOT NULL, -- tracking_below, tracking_expected, tracking_above
    status NVARCHAR(50) NOT NULL, -- draft, submitted
    created_at DATETIME2 DEFAULT GETUTCDATE(),
    updated_at DATETIME2 DEFAULT GETUTCDATE(),
    FOREIGN KEY (employee_id) REFERENCES users(id),
    FOREIGN KEY (reviewer_id) REFERENCES users(id),
    FOREIGN KEY (performance_cycle_id) REFERENCES performance_cycles(id)
);
GO

-- Create Notifications table
CREATE TABLE notifications (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NOT NULL,
    title NVARCHAR(255) NOT NULL,
    message NVARCHAR(MAX) NOT NULL,
    type NVARCHAR(50) NOT NULL,
    is_read BIT DEFAULT 0,
    created_at DATETIME2 DEFAULT GETUTCDATE(),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
GO

-- Create indexes for better performance
CREATE INDEX IX_users_email ON users(email);
CREATE INDEX IX_users_role ON users(role);
CREATE INDEX IX_performance_cycles_status ON performance_cycles(status);
CREATE INDEX IX_reviewer_selections_mentee_id ON reviewer_selections(mentee_id);
CREATE INDEX IX_reviewer_selections_cycle_id ON reviewer_selections(performance_cycle_id);
CREATE INDEX IX_reviewer_selection_details_selection_id ON reviewer_selection_details(selection_id);
CREATE INDEX IX_feedback_forms_employee_id ON feedback_forms(employee_id);
CREATE INDEX IX_feedback_forms_reviewer_id ON feedback_forms(reviewer_id);
CREATE INDEX IX_feedback_forms_cycle_id ON feedback_forms(performance_cycle_id);
CREATE INDEX IX_notifications_user_id ON notifications(user_id);
CREATE INDEX IX_notifications_is_read ON notifications(is_read);
GO

-- Create triggers to update the updated_at column
CREATE TRIGGER TR_users_updated_at ON users
AFTER UPDATE AS
BEGIN
    UPDATE users 
    SET updated_at = GETUTCDATE()
    FROM users u
    INNER JOIN inserted i ON u.id = i.id;
END;
GO

CREATE TRIGGER TR_performance_cycles_updated_at ON performance_cycles
AFTER UPDATE AS
BEGIN
    UPDATE performance_cycles 
    SET updated_at = GETUTCDATE()
    FROM performance_cycles pc
    INNER JOIN inserted i ON pc.id = i.id;
END;
GO

CREATE TRIGGER TR_reviewer_selections_updated_at ON reviewer_selections
AFTER UPDATE AS
BEGIN
    UPDATE reviewer_selections 
    SET updated_at = GETUTCDATE()
    FROM reviewer_selections rs
    INNER JOIN inserted i ON rs.id = i.id;
END;
GO

CREATE TRIGGER TR_feedback_forms_updated_at ON feedback_forms
AFTER UPDATE AS
BEGIN
    UPDATE feedback_forms 
    SET updated_at = GETUTCDATE()
    FROM feedback_forms ff
    INNER JOIN inserted i ON ff.id = i.id;
END;
GO

-- Insert sample data (optional)
-- Sample Performance Cycle
INSERT INTO performance_cycles (name, start_date, end_date, status, description)
VALUES ('Q4 2024 Performance Review', '2024-10-01', '2024-12-31', 'active', 'Quarterly performance review cycle');
GO

-- Sample Users (passwords are hashed versions of 'password123')
INSERT INTO users (email, name, role, department, position, password_hash)
VALUES 
('admin@company.com', 'System Administrator', 'System Administrator', 'IT', 'System Admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5uO.G'),
('hr@company.com', 'HR Manager', 'HR Lead', 'Human Resources', 'HR Manager', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5uO.G'),
('mentor@company.com', 'John Mentor', 'Mentor', 'Engineering', 'Senior Engineer', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5uO.G'),
('employee@company.com', 'Alice Employee', 'Employee', 'Engineering', 'Software Engineer', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5uO.G'),
('reviewer@company.com', 'Bob Reviewer', 'People Committee', 'Engineering', 'Tech Lead', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5uO.G');
GO

-- Create stored procedures for common operations
-- Get active performance cycle
CREATE PROCEDURE GetActivePerformanceCycle
AS
BEGIN
    SELECT * FROM performance_cycles WHERE status = 'active';
END;
GO

-- Get available reviewers
CREATE PROCEDURE GetAvailableReviewers
    @ExcludeUserId INT = NULL
AS
BEGIN
    SELECT * FROM users 
    WHERE is_active = 1 
    AND (@ExcludeUserId IS NULL OR id != @ExcludeUserId)
    AND role IN ('Mentor', 'People Committee');
END;
GO

-- Get user's reviewer selection
CREATE PROCEDURE GetUserReviewerSelection
    @UserId INT
AS
BEGIN
    SELECT rs.*, 
           STRING_AGG(u.name, ', ') as reviewer_names
    FROM reviewer_selections rs
    LEFT JOIN reviewer_selection_details rsd ON rs.id = rsd.selection_id
    LEFT JOIN users u ON rsd.reviewer_id = u.id
    WHERE rs.mentee_id = @UserId
    GROUP BY rs.id, rs.performance_cycle_id, rs.mentee_id, rs.status, 
             rs.submitted_at, rs.mentor_feedback, rs.created_at, rs.updated_at;
END;
GO

-- Get pending approvals for mentor
CREATE PROCEDURE GetPendingApprovalsForMentor
    @MentorId INT
AS
BEGIN
    -- This would need to be customized based on your mentor-mentee relationship logic
    SELECT rs.*, u.name as mentee_name, u.email as mentee_email
    FROM reviewer_selections rs
    JOIN users u ON rs.mentee_id = u.id
    WHERE rs.status = 'pending';
    -- Add mentor-mentee relationship filter here
END;
GO

-- Get assigned employees for reviewer
CREATE PROCEDURE GetAssignedEmployeesForReviewer
    @ReviewerId INT
AS
BEGIN
    SELECT DISTINCT u.*, rs.id as selection_id, rs.status as selection_status
    FROM users u
    JOIN reviewer_selection_details rsd ON u.id = rsd.reviewer_id
    JOIN reviewer_selections rs ON rsd.selection_id = rs.id
    WHERE rsd.reviewer_id = @ReviewerId
    AND rs.status = 'approved';
END;
GO

-- Create views for common queries
-- Dashboard stats for employees
CREATE VIEW EmployeeDashboardStats AS
SELECT 
    u.id as user_id,
    u.name,
    COUNT(rsd.reviewer_id) as reviewers_selected,
    rs.status as submission_status,
    pc.name as performance_cycle_name
FROM users u
LEFT JOIN reviewer_selections rs ON u.id = rs.mentee_id
LEFT JOIN reviewer_selection_details rsd ON rs.id = rsd.selection_id
LEFT JOIN performance_cycles pc ON rs.performance_cycle_id = pc.id
WHERE u.role = 'Employee'
GROUP BY u.id, u.name, rs.status, pc.name;
GO

-- Dashboard stats for mentors
CREATE VIEW MentorDashboardStats AS
SELECT 
    u.id as mentor_id,
    u.name as mentor_name,
    COUNT(CASE WHEN rs.status = 'pending' THEN 1 END) as pending_approvals,
    COUNT(CASE WHEN rs.status = 'approved' AND CAST(rs.updated_at AS DATE) = CAST(GETUTCDATE() AS DATE) THEN 1 END) as approved_today,
    COUNT(DISTINCT rs.mentee_id) as total_mentees
FROM users u
LEFT JOIN reviewer_selections rs ON 1=1 -- Add mentor-mentee relationship logic here
WHERE u.role = 'Mentor'
GROUP BY u.id, u.name;
GO

-- Dashboard stats for reviewers
CREATE VIEW ReviewerDashboardStats AS
SELECT 
    u.id as reviewer_id,
    u.name as reviewer_name,
    COUNT(CASE WHEN ff.status = 'draft' THEN 1 END) as draft_reviews,
    COUNT(CASE WHEN ff.status = 'submitted' THEN 1 END) as completed_reviews,
    COUNT(CASE WHEN ff.id IS NULL THEN 1 END) as pending_reviews
FROM users u
LEFT JOIN reviewer_selection_details rsd ON u.id = rsd.reviewer_id
LEFT JOIN reviewer_selections rs ON rsd.selection_id = rs.id
LEFT JOIN feedback_forms ff ON u.id = ff.reviewer_id AND rs.mentee_id = ff.employee_id
WHERE u.role = 'People Committee'
GROUP BY u.id, u.name;
GO

PRINT 'Database schema created successfully!';
PRINT 'Sample data inserted.';
PRINT 'Stored procedures and views created.';
PRINT '';
PRINT 'Default login credentials:';
PRINT 'Admin: admin@company.com / password123';
PRINT 'HR: hr@company.com / password123';
PRINT 'Mentor: mentor@company.com / password123';
PRINT 'Employee: employee@company.com / password123';
PRINT 'Reviewer: reviewer@company.com / password123';
