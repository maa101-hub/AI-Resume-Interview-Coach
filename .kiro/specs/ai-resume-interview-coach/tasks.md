# Implementation Plan: AI Resume & Interview Coach

## Overview

This plan implements a Python/Flask web application that parses resumes (PDF/DOCX), calculates ATS compatibility scores, generates improvement suggestions, and produces interview practice questions using OpenAI. The implementation follows an incremental approach: project setup → data models → parser → scorer → suggestions → interview coach → web layer → frontend → integration wiring.

## Tasks

- [x] 1. Set up project structure and core data models
  - [x] 1.1 Initialize project structure with Flask app skeleton
    - Create directory structure: `app/`, `app/static/`, `app/templates/`, `tests/unit/`, `tests/property/`, `tests/integration/`
    - Create `requirements.txt` with dependencies: flask, pymupdf, python-docx, openai, hypothesis, pytest
    - Create `app/__init__.py` and `app/models.py`
    - Create a minimal `app/app.py` with Flask app factory and placeholder routes
    - _Requirements: 5.1_

  - [x] 1.2 Implement data models and enums
    - Create all dataclasses and enums in `app/models.py`: `SectionType`, `Section`, `ParsedResume`, `ATSCriterionScore`, `ATSResult`, `Priority`, `SuggestionCategory`, `Suggestion`, `QuestionCategory`, `AnswerFramework`, `InterviewQuestion`
    - Create custom exception classes in `app/exceptions.py`: `FileFormatError`, `EmptyFileError`, `FileSizeError`, `ScoringError`, `InsufficientContentError`, `AIServiceError`
    - _Requirements: 1.1, 2.1, 2.4, 3.1, 3.2, 4.2, 4.5_

- [ ] 2. Implement Resume Parser
  - [~] 2.1 Implement ResumeParser class with file validation and text extraction
    - Create `app/resume_parser.py` with `ResumeParser` class
    - Implement file extension validation (PDF/DOCX only, case-insensitive)
    - Implement file size validation (reject > 5MB)
    - Implement `_extract_pdf()` using PyMuPDF (fitz)
    - Implement `_extract_docx()` using python-docx
    - Raise `FileFormatError` for unsupported formats, `EmptyFileError` for empty/no-text files, `FileSizeError` for oversized files
    - _Requirements: 1.1, 1.2, 1.3, 1.4_

  - [~] 2.2 Implement section identification logic
    - Implement `_identify_sections()` method using heading pattern matching
    - Identify sections: experience, education, skills, summary
    - Return only successfully identified sections (partial parsing support)
    - Calculate `word_count` from raw text
    - _Requirements: 1.1, 1.5_

  - [ ]* 2.3 Write property tests for Resume Parser (Properties 1-3)
    - **Property 1: Section identification preserves content** — parsed section contents are subsets of original text
    - **Property 2: Invalid file format rejection** — non-PDF/DOCX extensions raise FileFormatError
    - **Property 3: Partial parsing returns identified subset** — returned section types are subset of valid types with non-empty content
    - **Validates: Requirements 1.1, 1.2, 1.5**

  - [ ]* 2.4 Write unit tests for Resume Parser
    - Test empty file (0 bytes) handling
    - Test file at exactly 5MB boundary
    - Test various PDF structures and DOCX formats
    - Test case-insensitive extension matching (.PDF, .Docx)
    - Test resume with no identifiable sections
    - _Requirements: 1.2, 1.3, 1.4, 1.5_

- [~] 3. Checkpoint - Ensure parser tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 4. Implement ATS Scorer
  - [~] 4.1 Implement ATSScorer class with scoring criteria
    - Create `app/ats_scorer.py` with `ATSScorer` class
    - Implement `_score_keyword_relevance()`: evaluate industry-standard terms, weight against JD if provided
    - Implement `_score_formatting()`: check parseable headings, consistent structure
    - Implement `_score_section_completeness()`: check presence of experience, education, skills, summary
    - Implement `_score_contact_info()`: check for name, email/phone/LinkedIn
    - Implement `score()`: calculate weighted average, return ATSResult with exactly 4 criteria
    - Set warning if `word_count < 50`
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

  - [ ]* 4.2 Write property tests for ATS Scorer (Properties 4-6)
    - **Property 4: ATS score range and structure invariant** — overall_score in [0,100], exactly 4 criteria, each in [0,100]
    - **Property 5: Job description matching improves keyword relevance** — matching JD produces >= keyword score vs non-matching JD
    - **Property 6: Low word count triggers warning** — word_count < 50 → warning not None; word_count >= 50 → warning is None
    - **Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5**

  - [ ]* 4.3 Write unit tests for ATS Scorer
    - Test scoring with exactly 50 words (boundary)
    - Test scoring with 49 words (warning triggered)
    - Test scoring with and without job description
    - Test scoring failure scenario raises ScoringError
    - _Requirements: 2.1, 2.5, 2.6_

- [ ] 5. Implement Suggestion Engine
  - [~] 5.1 Implement SuggestionEngine class
    - Create `app/suggestion_engine.py` with `SuggestionEngine` class
    - Implement `_check_missing_keywords()`: identify missing JD keywords
    - Implement `_check_formatting_issues()`: detect formatting problems
    - Implement `_check_weak_verbs()`: find generic verbs (helped, worked, did, handled)
    - Implement `_check_quantifiable_achievements()`: detect missing metrics/numbers
    - Implement `_check_section_improvements()`: suggest section-level improvements based on ATS scores
    - Implement `generate()`: aggregate suggestions, cap at 10, order by priority (high → medium → low)
    - Raise `InsufficientContentError` when resume content is too sparse
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

  - [ ]* 5.2 Write property tests for Suggestion Engine (Properties 7-10)
    - **Property 7: Suggestion count bounds** — returns between 1 and 10 suggestions
    - **Property 8: Suggestion validity** — each suggestion has valid priority and category
    - **Property 9: Job description triggers keyword suggestion** — JD with missing keywords produces at least one missing_keywords suggestion
    - **Property 10: Suggestion priority ordering** — suggestions ordered high → medium → low
    - **Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5**

  - [ ]* 5.3 Write unit tests for Suggestion Engine
    - Test maximum 10 suggestions cap
    - Test insufficient content raises InsufficientContentError
    - Test weak verb detection with known examples
    - Test suggestion generation without job description
    - _Requirements: 3.1, 3.5, 3.6_

- [~] 6. Checkpoint - Ensure scorer and suggestion tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 7. Implement Interview Coach
  - [~] 7.1 Implement InterviewCoach class with OpenAI integration
    - Create `app/interview_coach.py` with `InterviewCoach` class
    - Implement `generate_questions()` using OpenAI API with structured output
    - Generate 5-15 questions with at least one from each category (behavioral, technical, experience_based)
    - Include answer framework for each question (structure, key_points, recommended_length 3-8)
    - Implement 10-second timeout for AI calls
    - Raise `AIServiceError` on timeout or API failure
    - Handle resumes with fewer than 3 identifiable skills (generate general questions)
    - When JD provided, generate at least 2 JD-referencing questions
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6_

  - [ ]* 7.2 Write property tests for Interview Coach (Properties 11-12)
    - **Property 11: Question generation invariants** — generates 5-15 questions with at least one per category (using mocked AI responses)
    - **Property 12: Answer framework validity** — non-empty structure, non-empty key_points, recommended_length in [3,8]
    - **Validates: Requirements 4.2, 4.3, 4.5**

  - [ ]* 7.3 Write unit tests for Interview Coach
    - Test with fewer than 3 skills (fallback to general questions)
    - Test AI timeout handling (raises AIServiceError)
    - Test question generation with and without job description
    - Test answer framework structure validation
    - _Requirements: 4.1, 4.4, 4.6_

- [ ] 8. Implement Job Description validation
  - [~] 8.1 Implement Job Description input handling
    - Create `app/utils.py` with JD validation utility
    - Implement: strings < 20 characters treated as not provided
    - Implement: strings > 5000 characters truncated at 5000
    - Integrate validation into the web layer request handling
    - _Requirements: 6.1, 6.2, 6.4_

  - [ ]* 8.2 Write property test for Job Description validation (Property 13)
    - **Property 13: Short job description treated as absent** — JD < 20 chars produces same results as null JD
    - **Validates: Requirements 6.4**

- [ ] 9. Implement Flask Web Layer
  - [~] 9.1 Implement API endpoints and request handling
    - Implement `POST /api/analyze` endpoint in `app/app.py`
    - Accept multipart/form-data with 'resume' file and optional 'job_description' text
    - Validate file type and size before processing
    - Wire together: ResumeParser → ATSScorer → SuggestionEngine
    - Return JSON response with parsed_resume, ats_score, suggestions
    - Implement `POST /api/interview-questions` endpoint
    - Accept JSON with parsed resume data and optional job_description
    - Return JSON with generated interview questions
    - Implement error handling: map exceptions to appropriate HTTP status codes (400, 413, 422, 500, 503)
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.6, 3.6, 5.5_

  - [ ]* 9.2 Write unit tests for web layer
    - Test file upload validation (wrong format, too large, empty)
    - Test successful analysis response format
    - Test error response format and HTTP status codes
    - Test job description passthrough to modules
    - _Requirements: 1.2, 1.3, 1.4, 5.5_

- [ ] 10. Implement Frontend
  - [~] 10.1 Create single-page HTML/CSS/JS frontend
    - Create `app/templates/index.html` with upload form, JD text area, and result sections
    - Create `app/static/style.css` with responsive layout (320px to 1440px, no horizontal scroll)
    - Create `app/static/app.js` with fetch API calls to backend endpoints
    - Implement loading indicator during processing
    - Display results under labeled headings: ATS Score, Suggestions, Interview Questions
    - Show only upload section on initial load (hide results)
    - Display error messages with actionable steps
    - Implement JD clear/modify and re-run functionality
    - Indicate when role-specific tailoring is active
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 6.1, 6.3, 6.5_

- [ ] 11. Integration wiring and final validation
  - [~] 11.1 Wire all components and create application entry point
    - Create `run.py` as the application entry point
    - Ensure Flask serves the frontend template and static files
    - Verify full pipeline: upload → parse → score → suggest → display
    - Verify interview question flow: request → generate → display
    - Ensure JD flows through all modules when provided
    - _Requirements: 1.1, 2.1, 3.1, 4.1, 5.1, 6.2, 6.3_

  - [ ]* 11.2 Write integration tests for full pipeline
    - Test end-to-end upload flow with sample PDF and DOCX files
    - Test full pipeline with and without job description
    - Test error propagation through the pipeline
    - _Requirements: 1.1, 2.1, 3.1, 4.1, 6.2_

- [~] 12. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties from the design document using Hypothesis
- Unit tests validate specific examples and edge cases using pytest
- The Interview Coach uses mocked OpenAI responses in tests to avoid API costs and flakiness
- No database is needed; all processing is in-memory per request

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["1.2"] },
    { "id": 2, "tasks": ["2.1", "8.1"] },
    { "id": 3, "tasks": ["2.2"] },
    { "id": 4, "tasks": ["2.3", "2.4", "4.1"] },
    { "id": 5, "tasks": ["4.2", "4.3", "5.1"] },
    { "id": 6, "tasks": ["5.2", "5.3", "7.1"] },
    { "id": 7, "tasks": ["7.2", "7.3", "8.2"] },
    { "id": 8, "tasks": ["9.1"] },
    { "id": 9, "tasks": ["9.2", "10.1"] },
    { "id": 10, "tasks": ["11.1"] },
    { "id": 11, "tasks": ["11.2"] }
  ]
}
```
