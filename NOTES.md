# AI Resume & Interview Coach — Daily Progress & Interview Notes

---

## Day 1 — May 21, 2026 (Thursday)

### What We Did

- **Task 1.1**: Set up project structure with Flask app skeleton
  - Created directories: `app/`, `app/static/`, `app/templates/`, `tests/unit/`, `tests/property/`, `tests/integration/`
  - Created `requirements.txt` (flask, pymupdf, python-docx, openai, hypothesis, pytest — all pinned)
  - Created `app/app.py` with Flask app factory (`create_app()`) and placeholder routes
  - Created `app/__init__.py`

- **Task 1.2**: Implemented data models and custom exceptions
  - `app/models.py` — 4 enums + 7 dataclasses covering the full domain
  - `app/exceptions.py` — 6 custom exception classes with default user-facing messages

### Interview Talking Points

**Architecture**
- Pipeline pattern: Upload → Parse → Score → Suggest → Display
- Flask app factory for testability and config flexibility
- Stateless, in-memory processing (no database)
- Rule-based ATS scoring for deterministic, explainable results
- OpenAI only for interview question generation (creativity matters there)

**Library Choices**
- PyMuPDF over pypdf: faster, better with complex PDF layouts
- python-docx: standard Word parser, well-maintained
- Hypothesis: property-based testing proves invariants for ALL valid inputs

**Data Modeling**
- Dataclasses (lightweight, no extra dependency for internal models)
- Enums for type safety on categories/priorities
- `ParsedResume.sections` as dict: O(1) lookup, prevents duplicates
- Optional fields use `None` default (e.g., `ATSResult.warning`)

**Error Handling**
- Fail fast on validation (400/413)
- Retry suggestion on processing errors (500)
- Graceful degradation on AI failures (503, 10s timeout)
- Partial success: parser returns whatever sections it identifies

**Testing Strategy**
- Property tests (Hypothesis): universal invariants (score always 0-100, always 4 criteria, etc.)
- Unit tests: edge cases and boundaries (exactly 5MB, exactly 50 words)
- Integration tests: full pipeline end-to-end

### What's Next (Day 2)
- Task 2.1: Resume Parser — file validation + PDF/DOCX text extraction
- Task 8.1: Job Description input handling (can run in parallel)
- Task 2.2: Section identification logic

---

<!-- Add new days below this line -->
