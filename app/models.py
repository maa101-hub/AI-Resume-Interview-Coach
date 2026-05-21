"""Data models for the AI Resume & Interview Coach application."""

from dataclasses import dataclass, field
from enum import Enum


class SectionType(Enum):
    """Types of resume sections that can be identified."""

    EXPERIENCE = "experience"
    EDUCATION = "education"
    SKILLS = "skills"
    SUMMARY = "summary"


@dataclass
class Section:
    """A single identified section from a parsed resume."""

    section_type: SectionType
    heading: str  # The actual heading text found in the resume
    content: str  # The text content of the section


@dataclass
class ParsedResume:
    """Structured data extracted from a resume file."""

    raw_text: str
    sections: dict[SectionType, Section]  # Only includes identified sections
    word_count: int
    filename: str


@dataclass
class ATSCriterionScore:
    """Score for a single ATS evaluation criterion."""

    criterion: str  # e.g., "keyword_relevance", "formatting"
    score: int  # 0-100
    details: str  # Human-readable explanation


@dataclass
class ATSResult:
    """Complete ATS scoring result with breakdown."""

    overall_score: int  # 0-100, weighted average of criteria
    criteria: list[ATSCriterionScore]
    warning: str | None = None  # Set if word_count < 50


class Priority(Enum):
    """Priority levels for improvement suggestions."""

    HIGH = "high"  # Reduces ATS score by 10+ points
    MEDIUM = "medium"  # Reduces ATS score by 5-9 points
    LOW = "low"  # Minor optimization opportunity


class SuggestionCategory(Enum):
    """Categories of resume improvement suggestions."""

    MISSING_KEYWORDS = "missing_keywords"
    FORMATTING = "formatting"
    WEAK_VERBS = "weak_verbs"
    QUANTIFIABLE_ACHIEVEMENTS = "quantifiable_achievements"
    SECTION_IMPROVEMENT = "section_improvement"


@dataclass
class Suggestion:
    """A single actionable improvement suggestion."""

    category: SuggestionCategory
    priority: Priority
    issue: str  # Description of the issue found
    recommendation: str  # Specific recommended change


class QuestionCategory(Enum):
    """Categories of interview practice questions."""

    BEHAVIORAL = "behavioral"
    TECHNICAL = "technical"
    EXPERIENCE_BASED = "experience_based"


@dataclass
class AnswerFramework:
    """Framework for structuring an answer to an interview question."""

    structure: str  # e.g., "Situation, Action, Result"
    key_points: list[str]  # Points to address from the resume
    recommended_length: int  # Number of sentences (3-8)


@dataclass
class InterviewQuestion:
    """A generated interview practice question with answer guidance."""

    category: QuestionCategory
    question: str
    answer_framework: AnswerFramework
