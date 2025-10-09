## **Database Schema**

This section provides the complete and definitive SQL Data Definition Language (DDL) for creating the MariaDB/MySQL database schema. The schema is organized into logical groups that mirror the `Data Models` section, ensuring a clear and traceable path from conceptual design to physical implementation.

All tables use the `InnoDB` storage engine to support transactions and foreign key constraints. Character sets are defined as `utf8mb4` with `utf8mb4_unicode_ci` collation to provide full Unicode support.

***

### **Group 1: Core Identity & Tenancy Tables**

This group of tables forms the foundational layer for multi-tenancy and user identity management. It includes the core entities for universities (tenants), user accounts, roles, and the university registration process.

```sql
-- =================================================================
-- Group 1: Core Identity & Tenancy Tables (Refined)
-- =================================================================

-- -----------------------------------------------------------------
-- Table: universities
-- Purpose: Represents a single, isolated tenant institution.
-- -----------------------------------------------------------------
CREATE TABLE `universities` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL COMMENT 'The official name of the university.',
    `street` VARCHAR(255),
    `city` VARCHAR(100),
    `country` VARCHAR(100),
    `postal_code` VARCHAR(20),
    `status` ENUM('pending', 'active', 'inactive') NOT NULL DEFAULT 'pending' COMMENT 'The current state of the university''s account.',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX `idx_universities_name` (`name`),
    INDEX `idx_universities_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------
-- Table: university_registration_requests
-- Purpose: Tracks the application process for a new university.
-- -----------------------------------------------------------------
CREATE TABLE `university_registration_requests` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `university_name` VARCHAR(255) NOT NULL,
    `contact_person_name` VARCHAR(255) NOT NULL,
    `contact_person_email` VARCHAR(255) NOT NULL,
    `status` ENUM('submitted', 'in_review', 'approved', 'rejected') NOT NULL DEFAULT 'submitted',
    `rejection_reason` TEXT COMMENT 'Stores the reason for rejection, if applicable.',
    `details` JSON COMMENT 'Flexible JSON field for additional, non-critical metadata.',
    `university_id` INT NULL COMMENT 'Link to the created university record upon approval.',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY `uk_contact_person_email` (`contact_person_email`),
    CONSTRAINT `fk_requests_university_id` FOREIGN KEY (`university_id`) REFERENCES `universities` (`id`) ON DELETE SET NULL,
    INDEX `idx_requests_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------
-- Table: documents
-- Purpose: Stores metadata for uploaded files, primarily for registration.
-- -----------------------------------------------------------------
CREATE TABLE `documents` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `request_id` INT NOT NULL COMMENT 'Foreign key to the registration request.',
    `filename` VARCHAR(255) NOT NULL,
    `storage_path` VARCHAR(1024) NOT NULL UNIQUE COMMENT 'The unique path to the file in storage.',
    `mime_type` VARCHAR(100) NOT NULL,
    `file_size` BIGINT NOT NULL COMMENT 'File size in bytes.',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_documents_request_id` FOREIGN KEY (`request_id`) REFERENCES `university_registration_requests` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------
-- Table: roles
-- Purpose: A static, seeded table defining user roles within the system.
-- -----------------------------------------------------------------
CREATE TABLE `roles` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(50) NOT NULL UNIQUE COMMENT 'e.g., Student, Faculty, Department Head, Admin, Super Admin'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------
-- Table: super_admins
-- Purpose: Manages platform-level administrator accounts.
-- -----------------------------------------------------------------
CREATE TABLE `super_admins` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `email` VARCHAR(255) NOT NULL UNIQUE,
    `password_hash` VARCHAR(255) NOT NULL,
    `pin_hash` VARCHAR(255) NOT NULL COMMENT 'Hashed 6-digit PIN for MFA.',
    `status` ENUM('active', 'locked') NOT NULL DEFAULT 'active',
    `token_version` INT NOT NULL DEFAULT 1 COMMENT 'Incremented to invalidate all active JWTs for this user.',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------
-- Table: registration_codes
-- Purpose: Manages codes for controlled user self-registration.
-- -----------------------------------------------------------------
CREATE TABLE `registration_codes` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `university_id` INT NOT NULL,
    `role_id` INT NOT NULL,
    `code_value` VARCHAR(50) NOT NULL UNIQUE,
    `max_uses` INT NOT NULL DEFAULT 1,
    `current_uses` INT NOT NULL DEFAULT 0,
    `status` ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
    `expires_at` TIMESTAMP NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_reg_codes_university_id` FOREIGN KEY (`university_id`) REFERENCES `universities` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_reg_codes_role_id` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE CASCADE,
    INDEX `idx_reg_codes_university_id` (`university_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------
-- Table: users
-- Purpose: Represents an individual user account within a university.
-- -----------------------------------------------------------------
CREATE TABLE `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `university_id` INT NOT NULL,
    `school_id` VARCHAR(100) NOT NULL COMMENT 'The university-issued ID.',
    `first_name` VARCHAR(100) NOT NULL,
    `last_name` VARCHAR(100) NOT NULL,
    `email` VARCHAR(255) NOT NULL UNIQUE,
    `password_hash` VARCHAR(255) NOT NULL,
    `status` ENUM('active', 'inactive', 'unverified') NOT NULL DEFAULT 'unverified',
    `program_id` INT NULL COMMENT 'Foreign key to programs table; for students.',
    `registration_code_id` INT NULL COMMENT 'The registration code used to sign up, if any.',
    `token_version` INT NOT NULL DEFAULT 1 COMMENT 'Incremented to invalidate all active JWTs for this user.',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY `uk_university_school_id` (`university_id`, `school_id`),
    CONSTRAINT `fk_users_university_id` FOREIGN KEY (`university_id`) REFERENCES `universities` (`id`) ON DELETE CASCADE,
    -- Note: fk_users_program_id will be added after Group 2 tables are defined.
    CONSTRAINT `fk_users_reg_code_id` FOREIGN KEY (`registration_code_id`) REFERENCES `registration_codes` (`id`) ON DELETE SET NULL,
    INDEX `idx_users_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------
-- Table: user_roles (Junction Table)
-- Purpose: Assigns roles to users, enabling many-to-many relationship.
-- -----------------------------------------------------------------
CREATE TABLE `user_roles` (
    `user_id` INT NOT NULL,
    `role_id` INT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`user_id`, `role_id`),
    CONSTRAINT `fk_user_roles_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_user_roles_role_id` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

```

***

### **Group 2: Academic Structure Tables**

This group of tables defines the core academic hierarchy and relationships within an institution. It includes departments, programs, subjects, and the specific offerings for each term, forming the backbone of the evaluation system.

```sql
-- =================================================================
-- Group 2: Academic Structure Tables (Refined)
-- =================================================================

-- -----------------------------------------------------------------
-- Table: departments
-- Purpose: Represents a major academic division within a university.
-- -----------------------------------------------------------------
CREATE TABLE `departments` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `university_id` INT NOT NULL,
    `parent_department_id` INT NULL COMMENT 'Self-referencing key for sub-departments.',
    `name` VARCHAR(255) NOT NULL,
    `short_name` VARCHAR(50),
    `head_user_id` INT NULL COMMENT 'Foreign key to the user who is the Department Head.',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_departments_university_id` FOREIGN KEY (`university_id`) REFERENCES `universities` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_departments_parent_id` FOREIGN KEY (`parent_department_id`) REFERENCES `departments` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_departments_head_user_id` FOREIGN KEY (`head_user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL,
    UNIQUE KEY `uk_university_department_name` (`university_id`, `name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------
-- Table: programs
-- Purpose: Represents a specific academic program or degree.
-- -----------------------------------------------------------------
CREATE TABLE `programs` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `university_id` INT NOT NULL,
    `department_id` INT NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `program_code` VARCHAR(50) NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_programs_university_id` FOREIGN KEY (`university_id`) REFERENCES `universities` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_programs_department_id` FOREIGN KEY (`department_id`) REFERENCES `departments` (`id`) ON DELETE CASCADE,
    UNIQUE KEY `uk_university_program_code` (`university_id`, `program_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------
-- Table: subjects
-- Purpose: Represents a specific course or subject template.
-- -----------------------------------------------------------------
CREATE TABLE `subjects` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `university_id` INT NOT NULL,
    `department_id` INT NOT NULL,
    `edp_code` VARCHAR(50) NOT NULL COMMENT 'Official, unique university code for the subject.',
    `subject_code` VARCHAR(50) NOT NULL COMMENT 'Common, abbreviated code for the subject.',
    `name` VARCHAR(255) NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_subjects_university_id` FOREIGN KEY (`university_id`) REFERENCES `universities` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_subjects_department_id` FOREIGN KEY (`department_id`) REFERENCES `departments` (`id`) ON DELETE CASCADE,
    UNIQUE KEY `uk_university_edp_code` (`university_id`, `edp_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------
-- Table: school_years
-- Purpose: Defines academic years.
-- -----------------------------------------------------------------
CREATE TABLE `school_years` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `year_start` SMALLINT NOT NULL,
    `year_end` SMALLINT NOT NULL,
    UNIQUE KEY `uk_school_year` (`year_start`, `year_end`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------
-- Table: school_terms
-- Purpose: Defines a specific term within a school year.
-- -----------------------------------------------------------------
CREATE TABLE `school_terms` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `school_year_id` INT NOT NULL,
    `semester` ENUM('1st Semester', '2nd Semester', 'Summer') NOT NULL,
    CONSTRAINT `fk_terms_school_year_id` FOREIGN KEY (`school_year_id`) REFERENCES `school_years` (`id`) ON DELETE CASCADE,
    UNIQUE KEY `uk_school_term` (`school_year_id`, `semester`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------
-- Table: assessment_periods
-- Purpose: A static, seeded table for evaluation windows (e.g., Midterm).
-- -----------------------------------------------------------------
CREATE TABLE `assessment_periods` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` ENUM('Midterm', 'Finals') NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------
-- Table: modalities
-- Purpose: A static, seeded table for mode of instruction.
-- -----------------------------------------------------------------
CREATE TABLE `modalities` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` ENUM('Online', 'Face-to-Face', 'Hybrid', 'Modular') NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------
-- Table: faculty_department_affiliations
-- Purpose: Manages the term-based relationship between a faculty and departments.
-- -----------------------------------------------------------------
CREATE TABLE `faculty_department_affiliations` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `faculty_id` INT NOT NULL,
    `department_id` INT NOT NULL,
    `school_term_id` INT NOT NULL,
    `is_home_department` BOOLEAN NOT NULL DEFAULT FALSE,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_affiliations_faculty_id` FOREIGN KEY (`faculty_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_affiliations_department_id` FOREIGN KEY (`department_id`) REFERENCES `departments` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_affiliations_school_term_id` FOREIGN KEY (`school_term_id`) REFERENCES `school_terms` (`id`) ON DELETE CASCADE,
    UNIQUE KEY `uk_faculty_department_term` (`faculty_id`, `department_id`, `school_term_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------
-- Table: subject_offerings
-- Purpose: Represents a specific "class" instance of a subject.
-- -----------------------------------------------------------------
CREATE TABLE `subject_offerings` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `university_id` INT NOT NULL,
    `subject_id` INT NOT NULL,
    `faculty_id` INT NOT NULL,
    `school_term_id` INT NOT NULL,
    `modality_id` INT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_offerings_university_id` FOREIGN KEY (`university_id`) REFERENCES `universities` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_offerings_subject_id` FOREIGN KEY (`subject_id`) REFERENCES `subjects` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_offerings_faculty_id` FOREIGN KEY (`faculty_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_offerings_school_term_id` FOREIGN KEY (`school_term_id`) REFERENCES `school_terms` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_offerings_modality_id` FOREIGN KEY (`modality_id`) REFERENCES `modalities` (`id`) ON DELETE SET NULL,
    INDEX `idx_faculty_term` (`faculty_id`, `school_term_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------
-- Table: enrollments
-- Purpose: Enrolls a student in a specific subject offering.
-- -----------------------------------------------------------------
CREATE TABLE `enrollments` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `university_id` INT NOT NULL,
    `student_id` INT NOT NULL,
    `subject_offering_id` INT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_enrollments_university_id` FOREIGN KEY (`university_id`) REFERENCES `universities` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_enrollments_student_id` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_enrollments_subject_offering_id` FOREIGN KEY (`subject_offering_id`) REFERENCES `subject_offerings` (`id`) ON DELETE CASCADE,
    UNIQUE KEY `uk_student_offering` (`student_id`, `subject_offering_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

```

***

### **Group 3: Evaluation Configuration Tables**

This group of tables provides the necessary structure for university administrators to create, configure, and schedule evaluation periods. It defines the reusable templates for forms, criteria, and questions.

```sql
-- =================================================================
-- Group 3: Evaluation Configuration Tables (Final & Verified)
-- =================================================================

-- -----------------------------------------------------------------
-- Table: likert_scale_templates
-- Purpose: A static, seeded table defining predefined Likert scales.
-- -----------------------------------------------------------------
CREATE TABLE `likert_scale_templates` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL UNIQUE COMMENT 'e.g., Standard 5-Point Scale (1-5)',
    `point_values` JSON NOT NULL COMMENT 'Defines the labels for each point, e.g., {"1": "Poor", "5": "Excellent"}',
    `min_value` TINYINT NOT NULL COMMENT 'The lowest possible score on the scale.',
    `max_value` TINYINT NOT NULL COMMENT 'The highest possible score on the scale.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------
-- Table: evaluation_form_templates
-- Purpose: The master template for an evaluation form.
-- -----------------------------------------------------------------
CREATE TABLE `evaluation_form_templates` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `university_id` INT NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `likert_scale_template_id` INT NOT NULL,
    `intended_for` ENUM('Students', 'Department Heads', 'Both') NOT NULL COMMENT 'Organizational label for the form''s target audience.',
    `status` ENUM('draft', 'active', 'assigned', 'archived') NOT NULL DEFAULT 'draft',
    `version` INT NOT NULL DEFAULT 1 COMMENT 'Used for optimistic locking to prevent concurrent edits.',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_forms_university_id` FOREIGN KEY (`university_id`) REFERENCES `universities` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_forms_likert_scale_id` FOREIGN KEY (`likert_scale_template_id`) REFERENCES `likert_scale_templates` (`id`),
    UNIQUE KEY `uk_university_form_name` (`university_id`, `name`),
    INDEX `idx_forms_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------
-- Table: evaluation_criteria
-- Purpose: Represents a weighted, thematic section within a form.
-- -----------------------------------------------------------------
CREATE TABLE `evaluation_criteria` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `form_template_id` INT NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `weight` DECIMAL(5, 2) NOT NULL COMMENT 'The numerical weight of this criterion, e.g., 25.50 for 25.5%',
    `order` SMALLINT NOT NULL DEFAULT 0 COMMENT 'Controls the display order of criteria within the form.',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_criteria_form_template_id` FOREIGN KEY (`form_template_id`) REFERENCES `evaluation_form_templates` (`id`) ON DELETE CASCADE,
    UNIQUE KEY `uk_form_criterion_name` (`form_template_id`, `name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------
-- Table: evaluation_questions
-- Purpose: Represents an individual question within a form.
-- -----------------------------------------------------------------
CREATE TABLE `evaluation_questions` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `form_template_id` INT NOT NULL,
    `criterion_id` INT NULL COMMENT 'If NULL, this is a form-level (e.g., open-ended) question.',
    `question_text` TEXT NOT NULL,
    `question_type` ENUM('likert', 'open_ended') NOT NULL,
    `is_required` BOOLEAN NOT NULL DEFAULT TRUE,
    `min_word_count` SMALLINT NULL,
    `max_word_count` SMALLINT NULL,
    `order` SMALLINT NOT NULL DEFAULT 0 COMMENT 'Controls the display order of questions within a criterion/form.',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_questions_form_template_id` FOREIGN KEY (`form_template_id`) REFERENCES `evaluation_form_templates` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_questions_criterion_id` FOREIGN KEY (`criterion_id`) REFERENCES `evaluation_criteria` (`id`) ON DELETE CASCADE,
    INDEX `idx_questions_form_template_id` (`form_template_id`),
    INDEX `idx_questions_criterion_id` (`criterion_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------
-- Table: evaluation_periods
-- Purpose: Defines a "live" evaluation window, activating forms.
-- -----------------------------------------------------------------
CREATE TABLE `evaluation_periods` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `university_id` INT NOT NULL,
    `school_term_id` INT NOT NULL,
    `assessment_period_id` INT NOT NULL,
    `student_form_template_id` INT NOT NULL COMMENT 'The form template to be used by students.',
    `dept_head_form_template_id` INT NULL COMMENT 'The optional, separate form for Department Heads.',
    `start_date_time` DATETIME NOT NULL,
    `end_date_time` DATETIME NOT NULL,
    `status` ENUM('scheduled', 'active', 'closed', 'cancelling', 'cancelled') NOT NULL DEFAULT 'scheduled',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_periods_university_id` FOREIGN KEY (`university_id`) REFERENCES `universities` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_periods_school_term_id` FOREIGN KEY (`school_term_id`) REFERENCES `school_terms` (`id`),
    CONSTRAINT `fk_periods_assessment_period_id` FOREIGN KEY (`assessment_period_id`) REFERENCES `assessment_periods` (`id`),
    CONSTRAINT `fk_periods_student_form_id` FOREIGN KEY (`student_form_template_id`) REFERENCES `evaluation_form_templates` (`id`),
    CONSTRAINT `fk_periods_dept_head_form_id` FOREIGN KEY (`dept_head_form_template_id`) REFERENCES `evaluation_form_templates` (`id`),
    UNIQUE KEY `uk_university_term_assessment` (`university_id`, `school_term_id`, `assessment_period_id`),
    INDEX `idx_periods_status` (`status`),
    INDEX `idx_periods_start_time` (`start_date_time`),
    INDEX `idx_periods_end_time` (`end_date_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

```

***

### **Group 4: Evaluation Submission & Integrity Tables**

This group of tables is responsible for storing the raw evaluation data as it is submitted by users. It includes the central submission record, tables for both Likert and open-ended answers, and the necessary structures for flagging and managing submissions that require administrative review.

```sql
-- =================================================================
-- Group 4: Evaluation Submission & Integrity Tables (Refined)
-- =================================================================

-- -----------------------------------------------------------------
-- Table: evaluation_submissions
-- Purpose: The central record for a single, complete evaluation submission.
-- -----------------------------------------------------------------
CREATE TABLE `evaluation_submissions` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `university_id` INT NOT NULL,
    `evaluation_period_id` INT NOT NULL,
    `evaluator_id` INT NOT NULL COMMENT 'The user submitting the evaluation.',
    `evaluatee_id` INT NOT NULL COMMENT 'The user being evaluated.',
    `subject_offering_id` INT NOT NULL COMMENT 'The class context for the evaluation.',
    `status` ENUM('submitted', 'processing', 'processed', 'archived', 'invalidated_for_resubmission', 'cancelled') NOT NULL DEFAULT 'submitted',
    `integrity_check_status` ENUM('pending', 'completed', 'failed') NOT NULL DEFAULT 'pending',
    `analysis_status` ENUM('pending', 'quant_qual_complete', 'aggregation_complete', 'failed') NOT NULL DEFAULT 'pending',
    `submitted_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `is_resubmission` BOOLEAN NOT NULL DEFAULT FALSE,
    `original_submission_id` INT NULL COMMENT 'If a resubmission, links to the original invalidated submission.',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_submissions_university_id` FOREIGN KEY (`university_id`) REFERENCES `universities` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_submissions_period_id` FOREIGN KEY (`evaluation_period_id`) REFERENCES `evaluation_periods` (`id`),
    CONSTRAINT `fk_submissions_evaluator_id` FOREIGN KEY (`evaluator_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_submissions_evaluatee_id` FOREIGN KEY (`evaluatee_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_submissions_offering_id` FOREIGN KEY (`subject_offering_id`) REFERENCES `subject_offerings` (`id`),
    CONSTRAINT `fk_submissions_original_id` FOREIGN KEY (`original_submission_id`) REFERENCES `evaluation_submissions` (`id`) ON DELETE SET NULL,
    UNIQUE KEY `uk_submission_uniqueness` (`evaluation_period_id`, `evaluator_id`, `evaluatee_id`, `subject_offering_id`),
    INDEX `idx_submissions_status` (`status`),
    INDEX `idx_submissions_integrity_status` (`integrity_check_status`),
    INDEX `idx_submissions_analysis_status` (`analysis_status`),
    INDEX `idx_evaluatee_period` (`evaluatee_id`, `evaluation_period_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------
-- Table: evaluation_likert_answers
-- Purpose: Stores a user's answer to a single Likert-scale question.
-- -----------------------------------------------------------------
CREATE TABLE `evaluation_likert_answers` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `submission_id` INT NOT NULL,
    `question_id` INT NOT NULL,
    `answer_value` TINYINT NOT NULL COMMENT 'The integer value of the answer provided (e.g., 1, 2, 3, 4, 5).',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_likert_answers_submission_id` FOREIGN KEY (`submission_id`) REFERENCES `evaluation_submissions` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_likert_answers_question_id` FOREIGN KEY (`question_id`) REFERENCES `evaluation_questions` (`id`) ON DELETE CASCADE,
    UNIQUE KEY `uk_likert_answer_uniqueness` (`submission_id`, `question_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------
-- Table: evaluation_open_ended_answers
-- Purpose: Stores a user's textual answer to an open-ended question.
-- -----------------------------------------------------------------
CREATE TABLE `evaluation_open_ended_answers` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `submission_id` INT NOT NULL,
    `question_id` INT NOT NULL,
    `answer_text` TEXT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_open_answers_submission_id` FOREIGN KEY (`submission_id`) REFERENCES `evaluation_submissions` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_open_answers_question_id` FOREIGN KEY (`question_id`) REFERENCES `evaluation_questions` (`id`) ON DELETE CASCADE,
    UNIQUE KEY `uk_open_answer_uniqueness` (`submission_id`, `question_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------
-- Table: flagged_evaluations
-- Purpose: Tracks submissions flagged for administrative review.
-- -----------------------------------------------------------------
CREATE TABLE `flagged_evaluations` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `submission_id` INT NOT NULL UNIQUE,
    `flag_reason` ENUM('Low-Confidence', 'Recycled Content', 'Sentiment Mismatch') NOT NULL,
    `flag_details` JSON COMMENT 'Stores metadata that triggered the flag, e.g., highlight indexes.',
    `status` ENUM('pending', 'resolved') NOT NULL DEFAULT 'pending',
    `resolution` ENUM('approved', 'archived', 'resubmission_requested') NULL,
    `resolved_by_admin_id` INT NULL,
    `resolved_at` DATETIME NULL,
    `admin_notes` TEXT NULL,
    `resubmission_grace_period_ends_at` DATETIME NULL COMMENT 'Must be set to resolved_at + 48 hours when resolution is resubmission_requested.',
    `version` INT NOT NULL DEFAULT 1 COMMENT 'Used for optimistic locking.',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_flagged_submission_id` FOREIGN KEY (`submission_id`) REFERENCES `evaluation_submissions` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_flagged_resolved_by_admin_id` FOREIGN KEY (`resolved_by_admin_id`) REFERENCES `users` (`id`) ON DELETE SET NULL,
    INDEX `idx_flagged_status` (`status`),
    INDEX `idx_flagged_resolution` (`resolution`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

```

***

### **Group 5: Processed Data & Analysis Tables**

This group of tables stores the output of the server-side analysis pipeline. After a submission is made, background workers populate these tables with calculated quantitative scores, sentiment analysis results, and extracted keywords. These records are the single source of truth for all data visualizations and reports.

```sql
-- =================================================================
-- Group 5: Processed Data & Analysis Tables (Refined)
-- =================================================================

-- -----------------------------------------------------------------
-- Table: numerical_aggregates
-- Purpose: Stores the final, calculated quantitative scores for a single submission.
-- -----------------------------------------------------------------
CREATE TABLE `numerical_aggregates` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `submission_id` INT NOT NULL UNIQUE,
    `per_question_median_scores` JSON NOT NULL COMMENT 'Stores the median score for each Likert question.',
    `per_criterion_average_scores` JSON NOT NULL COMMENT 'Stores the average score for each criterion.',
    `quant_score_raw` DECIMAL(10, 4) NOT NULL COMMENT 'The initial weighted mean score from Likert answers.',
    `z_quant` DECIMAL(10, 4) NOT NULL COMMENT 'The normalized Z-score for the quantitative part.',
    `final_score_60_40` DECIMAL(10, 4) NOT NULL COMMENT 'The final combined score (60% quant, 40% qual).',
    `cohort_n` INT NOT NULL COMMENT 'The size (N) of the comparison group.',
    `cohort_mean` DECIMAL(10, 4) NOT NULL COMMENT 'The mean score (μ) of the cohort.',
    `cohort_std_dev` DECIMAL(10, 4) NOT NULL COMMENT 'The standard deviation (σ) of the cohort.',
    `is_final_snapshot` BOOLEAN NOT NULL DEFAULT FALSE COMMENT 'Set to true when the evaluation period is locked.',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_num_agg_submission_id` FOREIGN KEY (`submission_id`) REFERENCES `evaluation_submissions` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------
-- Table: open_ended_sentiments
-- Purpose: Stores the detailed sentiment analysis for a single open-ended answer.
-- -----------------------------------------------------------------
CREATE TABLE `open_ended_sentiments` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `open_ended_answer_id` INT NOT NULL UNIQUE,
    `predicted_sentiment_label` ENUM('positive', 'neutral', 'negative') NOT NULL,
    `predicted_sentiment_label_score` FLOAT NOT NULL,
    `positive_score` FLOAT NOT NULL,
    `neutral_score` FLOAT NOT NULL,
    `negative_score` FLOAT NOT NULL,
    `accuracy` FLOAT,
    `confidence` FLOAT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_sentiment_answer_id` FOREIGN KEY (`open_ended_answer_id`) REFERENCES `evaluation_open_ended_answers` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------
-- Table: open_ended_keywords
-- Purpose: Stores a keyword or phrase extracted from an open-ended answer.
-- -----------------------------------------------------------------
CREATE TABLE `open_ended_keywords` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `open_ended_answer_id` INT NOT NULL,
    `keyword` VARCHAR(255) NOT NULL,
    `relevance_score` FLOAT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_keyword_answer_id` FOREIGN KEY (`open_ended_answer_id`) REFERENCES `evaluation_open_ended_answers` (`id`) ON DELETE CASCADE,
    UNIQUE KEY `uk_answer_keyword` (`open_ended_answer_id`, `keyword`),
    INDEX `idx_keyword` (`keyword`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------
-- Table: sentiment_aggregates
-- Purpose: Stores the aggregated and normalized qualitative scores for a submission.
-- -----------------------------------------------------------------
CREATE TABLE `sentiment_aggregates` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `submission_id` INT NOT NULL UNIQUE,
    `average_positive_score` DECIMAL(10, 4) NOT NULL COMMENT 'Average positive sentiment across all answers.',
    `average_neutral_score` DECIMAL(10, 4) NOT NULL COMMENT 'Average neutral sentiment across all answers.',
    `average_negative_score` DECIMAL(10, 4) NOT NULL COMMENT 'Average negative sentiment across all answers.',
    `qual_score_raw` DECIMAL(10, 4) NOT NULL COMMENT 'The raw qualitative score, averaged from sentiment results.',
    `z_qual` DECIMAL(10, 4) NOT NULL COMMENT 'The normalized Z-score for the qualitative part.',
    `is_final_snapshot` BOOLEAN NOT NULL DEFAULT FALSE COMMENT 'Set to true when the evaluation period is locked.',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_sent_agg_submission_id` FOREIGN KEY (`submission_id`) REFERENCES `evaluation_submissions` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

```

***

### **Group 6: AI & Reporting Tables**

This group of tables supports the "AI Assistant" and "Report Center" features. They are responsible for persisting the outputs of AI generation and for managing the queue and final artifacts of asynchronously generated reports.

```sql
-- =================================================================
-- Group 6: AI & Reporting Tables (Final & Verified)
-- =================================================================

-- -----------------------------------------------------------------
-- Table: ai_suggestions
-- Purpose: Stores AI-generated suggestion reports for user review.
-- -----------------------------------------------------------------
CREATE TABLE `ai_suggestions` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `university_id` INT NOT NULL,
    `generated_for_user_id` INT NOT NULL COMMENT 'The user who is the subject of the report.',
    `generated_by_user_id` INT NOT NULL COMMENT 'The user who ran the report generation.',
    `context_school_term_id` INT NOT NULL,
    `context_assessment_period_id` INT NOT NULL,
    `suggestion_title` VARCHAR(255) NOT NULL,
    `suggestion_content` LONGTEXT NOT NULL COMMENT 'The full markdown or text content from the Gemini API.',
    `prompt_sent_to_api` LONGTEXT NOT NULL COMMENT 'The full prompt sent to the API, for auditing.',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_ai_suggestions_university_id` FOREIGN KEY (`university_id`) REFERENCES `universities` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_ai_suggestions_for_user_id` FOREIGN KEY (`generated_for_user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_ai_suggestions_by_user_id` FOREIGN KEY (`generated_by_user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_ai_suggestions_term_id` FOREIGN KEY (`context_school_term_id`) REFERENCES `school_terms` (`id`),
    CONSTRAINT `fk_ai_suggestions_period_id` FOREIGN KEY (`context_assessment_period_id`) REFERENCES `assessment_periods` (`id`),
    INDEX `idx_ai_suggestions_for_user` (`generated_for_user_id`),
    INDEX `idx_ai_suggestions_by_user` (`generated_by_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------
-- Table: generated_reports
-- Purpose: Manages the lifecycle of asynchronously generated report files.
-- -----------------------------------------------------------------
CREATE TABLE `generated_reports` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `university_id` INT NOT NULL,
    `requested_by_user_id` INT NOT NULL,
    `report_type` VARCHAR(100) NOT NULL COMMENT 'e.g., Faculty Performance Summary',
    `report_parameters` JSON NOT NULL COMMENT 'Stores the filters used to generate the report.',
    `status` ENUM('queued', 'generating', 'ready', 'failed') NOT NULL DEFAULT 'queued',
    `file_format` ENUM('PDF', 'CSV') NOT NULL,
    `storage_path` VARCHAR(1024) NULL COMMENT 'The server path to the final generated file.',
    `error_message` TEXT NULL COMMENT 'Stores error details if the job failed.',
    `expires_at` TIMESTAMP NOT NULL COMMENT 'When the generated file can be safely deleted.',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_reports_university_id` FOREIGN KEY (`university_id`) REFERENCES `universities` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_reports_requested_by_id` FOREIGN KEY (`requested_by_user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
    INDEX `idx_reports_status` (`status`),
    INDEX `idx_reports_requested_by` (`requested_by_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

```

***

### **Group 7: System & Operations Tables**

This group of tables supports cross-cutting operational concerns such as background job monitoring, security auditing, user notifications, and tenant-specific configuration. They are essential for the overall health, maintainability, and administration of the platform.

```sql
-- =================================================================
-- Group 7: System & Operations Tables (Final & Verified)
-- =================================================================

-- -----------------------------------------------------------------
-- Table: background_tasks
-- Purpose: A unified, observable record for all asynchronous jobs.
-- -----------------------------------------------------------------
CREATE TABLE `background_tasks` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `university_id` INT NOT NULL,
    `job_type` ENUM(
        'ACADEMIC_STRUCTURE_IMPORT',
        'USER_IMPORT',
        'HISTORICAL_USER_ENROLLMENT_IMPORT',
        'HISTORICAL_EVALUATION_IMPORT',
        'PERIOD_CANCELLATION',
        'REPORT_GENERATION',
        'RECYCLED_CONTENT_CHECK',
        'QUANTITATIVE_ANALYSIS',
        'QUALITATIVE_ANALYSIS',
        'FINAL_AGGREGATION'
    ) NOT NULL,
    `status` ENUM(
        'queued',
        'processing',
        'cancellation_requested',
        'completed_success',
        'completed_partial_failure',
        'failed',
        'cancelled'
    ) NOT NULL DEFAULT 'queued',
    `submitted_by_user_id` INT NOT NULL,
    `job_parameters` JSON,
    `progress` TINYINT UNSIGNED NOT NULL DEFAULT 0,
    `result_message` TEXT,
    `result_storage_path` VARCHAR(1024) NULL,
    `log_output` TEXT COMMENT 'Stores exception tracebacks or detailed log output for debugging.',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `started_at` DATETIME NULL,
    `completed_at` DATETIME NULL,
    `rows_total` INT NULL,
    `rows_processed` INT NULL,
    `rows_failed` INT NULL,
    CONSTRAINT `fk_tasks_university_id` FOREIGN KEY (`university_id`) REFERENCES `universities` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_tasks_submitted_by_id` FOREIGN KEY (`submitted_by_user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
    INDEX `idx_tasks_status` (`status`),
    INDEX `idx_tasks_job_type` (`job_type`),
    INDEX `idx_tasks_submitted_by` (`submitted_by_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------
-- Table: audit_logs
-- Purpose: A permanent, immutable record of significant actions.
-- -----------------------------------------------------------------
CREATE TABLE `audit_logs` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `university_id` INT NULL,
    `actor_user_id` INT NULL,
    `action` VARCHAR(100) NOT NULL,
    `target_entity` VARCHAR(100) NULL,
    `target_id` INT NULL,
    `details` JSON,
    `ip_address` VARCHAR(45) NOT NULL,
    `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_audit_university_id` FOREIGN KEY (`university_id`) REFERENCES `universities` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_audit_actor_user_id` FOREIGN KEY (`actor_user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL,
    INDEX `idx_audit_action` (`action`),
    INDEX `idx_audit_target` (`target_entity`, `target_id`),
    INDEX `idx_audit_actor` (`actor_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------
-- Table: notifications
-- Purpose: Manages notifications sent to users and super admins.
-- -----------------------------------------------------------------
CREATE TABLE `notifications` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `university_id` INT NULL COMMENT 'NULL for platform-level notifications to Super Admins.',
    `recipient_id` INT NOT NULL,
    `recipient_type` VARCHAR(50) NOT NULL COMMENT 'e.g., ''User'', ''SuperAdmin''',
    `actor_id` INT NULL,
    `actor_type` VARCHAR(50) NULL COMMENT 'e.g., ''User'', ''SuperAdmin'', ''System''',
    `action_type` VARCHAR(100) NOT NULL COMMENT 'e.g., IMPORT_COMPLETE',
    `content` TEXT NOT NULL,
    `delivery_methods` JSON NOT NULL COMMENT 'e.g., [\"IN_APP\", \"EMAIL\"]',
    `status` ENUM('unread', 'read', 'archived') NOT NULL DEFAULT 'unread',
    `read_at` DATETIME NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_notifications_university_id` FOREIGN KEY (`university_id`) REFERENCES `universities` (`id`) ON DELETE CASCADE,
    INDEX `idx_notifications_recipient` (`recipient_id`, `recipient_type`),
    INDEX `idx_notifications_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------
-- Table: university_settings
-- Purpose: Stores tenant-specific, configurable key-value settings.
-- -----------------------------------------------------------------
CREATE TABLE `university_settings` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `university_id` INT NOT NULL,
    `setting_name` VARCHAR(100) NOT NULL COMMENT 'e.g., score_weight_quantitative',
    `setting_value` VARCHAR(255) NOT NULL COMMENT 'e.g., 0.60',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_settings_university_id` FOREIGN KEY (`university_id`) REFERENCES `universities` (`id`) ON DELETE CASCADE,
    UNIQUE KEY `uk_university_setting_name` (`university_id`, `setting_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

```

***
