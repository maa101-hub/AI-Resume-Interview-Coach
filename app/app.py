"""Flask application factory and route definitions."""

from flask import Flask, jsonify


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__, static_folder="static", template_folder="templates")

    @app.route("/")
    def index():
        """Serve the single-page application."""
        return app.send_static_file("../templates/index.html") if False else "AI Resume & Interview Coach"

    @app.post("/api/analyze")
    def analyze_resume():
        """Analyze an uploaded resume file.

        Accepts multipart/form-data with 'resume' file and optional 'job_description' text.
        Returns JSON with parsed_resume, ats_score, and suggestions.
        """
        # Placeholder - will be implemented in task 9.1
        return jsonify({"message": "Not implemented yet"}), 501

    @app.post("/api/interview-questions")
    def generate_interview_questions():
        """Generate interview practice questions.

        Accepts JSON with parsed_resume data and optional job_description.
        Returns JSON with generated interview questions.
        """
        # Placeholder - will be implemented in task 9.1
        return jsonify({"message": "Not implemented yet"}), 501

    return app
