
from flask import Flask, render_template, request, jsonify
import fitz
from docx import Document

from ml.analyzer import analyze_resume

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024


@app.route("/")
def home():
    return render_template("index.html")


def extract_pdf_text(file):
    text = ""

    pdf = fitz.open(stream=file.read(), filetype="pdf")

    for page in pdf:
        text += page.get_text()

    pdf.close()
    return text


def extract_docx_text(file):
    document = Document(file)

    text = "\n".join(
        paragraph.text for paragraph in document.paragraphs
    )

    return text


@app.route("/analyze", methods=["POST"])
def analyze():

    if "resume" not in request.files:
        return jsonify({"error": "Resume file not found"}), 400

    resume_file = request.files["resume"]

    job_description = request.form.get(
        "job_description", ""
    ).strip()

    if resume_file.filename == "":
        return jsonify({"error": "Please select a resume"}), 400

    if not job_description:
        return jsonify({"error": "Please enter job description"}), 400

    filename = resume_file.filename.lower()

    try:
        if filename.endswith(".pdf"):
            resume_text = extract_pdf_text(resume_file)

        elif filename.endswith(".docx"):
            resume_text = extract_docx_text(resume_file)

        else:
            return jsonify({
                "error": "Only PDF and DOCX files are supported"
            }), 400

    except Exception:
        return jsonify({
            "error": "Unable to read resume. Upload a valid file."
        }), 400

    if not resume_text.strip():
        return jsonify({
            "error": "No text found in resume. Scanned PDFs are not supported."
        }), 400

    try:
        result = analyze_resume(resume_text, job_description)

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "error": "Analysis failed: " + str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
