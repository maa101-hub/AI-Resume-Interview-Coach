# Requirements Document

## Introduction

AI Resume & Interview Coach is a simple web application that helps job seekers improve their resumes and prepare for interviews. The application parses uploaded resumes, calculates an ATS (Applicant Tracking System) compatibility score, provides actionable improvement suggestions, and generates interview practice questions based on the resume content. The project is designed to be built incrementally in small daily steps.

## Glossary

- **Application**: The AI Resume & Interview Coach web application
- **Resume_Parser**: The module responsible for extracting text and structured data from uploaded resume files
- **ATS_Scorer**: The module that evaluates a resume against Applicant Tracking System compatibility criteria
- **Suggestion_Engine**: The module that generates actionable improvement recommendations for a resume
- **Interview_Coach**: The module that generates interview practice questions based on resume content
- **User**: A job seeker who uploads their resume and uses the application for feedback
- **ATS_Score**: A numerical score (0-100) representing how well a resume is optimized for Applicant Tracking Systems
- **Job_Description**: An optional text input describing the target job role for tailored scoring and questions

## Requirements

### Requirement 1: Resume Upload and Parsing

**User Story:** As a User, I want to upload my resume file, so that the application can analyze its content.

#### Acceptance Criteria

1. WHEN a User uploads a PDF or DOCX file of 5MB or less, THE Resume_Parser SHALL extract the text content and return structured data containing identified sections (experience, education, skills, summary), where each section includes its heading label and associated text content
2. WHEN a User uploads a file that is not PDF or DOCX format, THE Resume_Parser SHALL display an error message indicating the supported file formats (PDF and DOCX)
3. IF the uploaded file is empty (0 bytes) or contains no extractable text, THEN THE Resume_Parser SHALL display an error message indicating the cause of failure
4. IF the uploaded file exceeds 5MB in size, THEN THE Resume_Parser SHALL reject the file and display an error message indicating the maximum allowed file size
5. WHEN the Resume_Parser cannot identify one or more of the expected sections (experience, education, skills, summary), THE Resume_Parser SHALL return the successfully identified sections and omit the unrecognized sections from the structured data
6. THE Resume_Parser SHALL complete text extraction within 5 seconds for files up to 5MB in size

### Requirement 2: ATS Score Calculation

**User Story:** As a User, I want to see my resume's ATS compatibility score, so that I know how well my resume will perform with automated screening systems.

#### Acceptance Criteria

1. WHEN the Resume_Parser completes text extraction, THE ATS_Scorer SHALL calculate an ATS_Score as an integer between 0 and 100 within 3 seconds
2. THE ATS_Scorer SHALL evaluate the resume against these criteria: keyword relevance (presence of industry-standard terms for the resume's apparent field), formatting compatibility (parseable section headings, no image-only content, consistent structure), section completeness (presence of experience, education, skills, and summary sections), and contact information presence (at least name and one of: email address, phone number, or LinkedIn URL)
3. WHEN a Job_Description is provided, THE ATS_Scorer SHALL weight keyword matching against the Job_Description as the primary factor in the keyword relevance sub-score
4. THE ATS_Scorer SHALL display the ATS_Score along with a breakdown showing individual scores (each as an integer between 0 and 100) for each evaluation criterion
5. IF the resume contains fewer than 50 words of extractable text, THEN THE ATS_Scorer SHALL display a warning that the resume may not have been parsed correctly
6. IF the ATS_Scorer fails to complete scoring, THEN THE ATS_Scorer SHALL display an error message indicating that scoring could not be completed and prompt the User to retry

### Requirement 3: Resume Improvement Suggestions

**User Story:** As a User, I want to receive specific suggestions to improve my resume, so that I can increase my chances of passing ATS screening and impressing recruiters.

#### Acceptance Criteria

1. WHEN the ATS_Scorer completes scoring, THE Suggestion_Engine SHALL generate between 1 and 10 actionable improvement suggestions, where each suggestion includes: the category it belongs to, the priority level, a description of the issue found, and a specific recommended change
2. THE Suggestion_Engine SHALL categorize suggestions into priority levels: high, medium, and low, where high indicates issues that directly reduce ATS_Score by 10 or more points, medium indicates issues that reduce ATS_Score by 5 to 9 points, and low indicates minor optimization opportunities
3. THE Suggestion_Engine SHALL provide suggestions covering: missing keywords, formatting issues, weak action verbs (generic verbs such as "helped", "worked", "did", "handled" that lack specificity), missing quantifiable achievements, and section improvements
4. WHEN a Job_Description is provided, THE Suggestion_Engine SHALL include at least one suggestion referencing specific keywords or skills from the Job_Description that are absent from the resume
5. THE Suggestion_Engine SHALL limit suggestions to a maximum of 10 items and display them ordered by priority level from high to low
6. IF the Suggestion_Engine cannot generate any suggestions due to insufficient parsed resume content, THEN THE Suggestion_Engine SHALL display a message indicating that the resume content was insufficient for analysis and recommend the User verify the uploaded file

### Requirement 4: Interview Question Generation

**User Story:** As a User, I want to receive interview practice questions based on my resume, so that I can prepare for interviews with relevant questions.

#### Acceptance Criteria

1. WHEN the User requests interview coaching, THE Interview_Coach SHALL generate practice questions that reference skills, experiences, or qualifications found in the parsed resume content within 10 seconds
2. THE Interview_Coach SHALL generate questions in these categories: behavioral, technical, and experience-based, with at least one question from each category
3. THE Interview_Coach SHALL generate between 5 and 15 practice questions per session
4. WHEN a Job_Description is provided, THE Interview_Coach SHALL generate at least 2 questions that reference responsibilities or skills mentioned in the Job_Description
5. THE Interview_Coach SHALL provide a sample answer framework for each generated question, containing: a suggested structure (e.g., situation, action, result), key points to address from the resume, and a recommended answer length in sentences (between 3 and 8)
6. IF the parsed resume contains fewer than 3 identifiable skills or experiences, THEN THE Interview_Coach SHALL display a message indicating that the resume lacks sufficient detail for tailored questions and SHALL generate general interview questions for the requested categories

### Requirement 5: Simple Web Interface

**User Story:** As a User, I want a clean and simple web interface, so that I can easily upload my resume and view results without confusion.

#### Acceptance Criteria

1. THE Application SHALL present a single-page interface with visually distinct, labeled sections for upload, score display, suggestions, and interview questions
2. WHILE the Application is processing the resume, THE Application SHALL display a loading indicator that confirms the operation is in progress
3. WHEN processing is complete, THE Application SHALL display results organized under labeled headings for ATS score, suggestions, and interview questions, with each section visually separated
4. THE Application SHALL render all content and interactive elements without horizontal scrolling on viewports from 320px wide (mobile) to 1440px wide (desktop)
5. IF a processing error occurs, THEN THE Application SHALL display an error message indicating what went wrong and at least one actionable step the User can take to resolve the issue
6. WHEN the User first loads the page and no resume has been uploaded, THE Application SHALL display only the upload section and hide the results sections

### Requirement 6: Job Description Input

**User Story:** As a User, I want to optionally provide a job description, so that the analysis and questions are tailored to my target role.

#### Acceptance Criteria

1. THE Application SHALL provide a text input area for the User to paste a Job_Description with a maximum length of 5000 characters
2. IF no Job_Description is provided, THEN THE Application SHALL proceed with general ATS scoring, suggestions, and interview question generation without role-specific tailoring
3. WHEN a Job_Description is provided, THE Application SHALL indicate to the User that role-specific tailoring is active and pass the Job_Description to the ATS_Scorer, Suggestion_Engine, and Interview_Coach for tailored output
4. IF the provided Job_Description contains fewer than 20 characters, THEN THE Application SHALL display a message indicating the input is too short to provide meaningful tailoring and treat it as not provided
5. THE Application SHALL allow the User to clear or modify the Job_Description and re-run the analysis
