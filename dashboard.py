from flask import Flask, render_template, jsonify, send_file, request
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_FOLDER = os.path.join(BASE_DIR, "reports")


def read_report_file(filepath):
    """
    Reads a report text file and strips leading
    whitespace from each line to fix indentation.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()
    return "\n".join(line.strip() for line in raw.split("\n"))


def get_latest_report():
    """
    Reads the most recently generated report text file.
    Returns the report content and date or None if no reports exist.
    """
    if not os.path.exists(REPORTS_FOLDER):
        return None, None

    report_files = [
        f for f in os.listdir(REPORTS_FOLDER)
        if f.startswith("job_market_report_") and f.endswith(".txt")
    ]

    if not report_files:
        return None, None

    report_files.sort(reverse=True)
    latest = report_files[0]

    date_str = latest.replace("job_market_report_", "").replace(".txt", "")
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%A, %B %d, %Y")
    except:
        date = date_str

    content = read_report_file(os.path.join(REPORTS_FOLDER, latest))
    return content, date


def get_all_reports():
    """Returns a list of all available report dates."""
    if not os.path.exists(REPORTS_FOLDER):
        return []

    report_files = [
        f for f in os.listdir(REPORTS_FOLDER)
        if f.startswith("job_market_report_") and f.endswith(".txt")
    ]

    report_files.sort(reverse=True)
    reports = []

    for f in report_files:
        date_str = f.replace("job_market_report_", "").replace(".txt", "")
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%B %d, %Y")
        except:
            date = date_str
        reports.append({"filename": f, "date": date, "date_str": date_str})

    return reports


@app.route("/")
def index():
    content, date = get_latest_report()
    reports = get_all_reports()
    return render_template(
        "index.html",
        content=content,
        date=date,
        reports=reports
    )


@app.route("/report/<date_str>")
def get_report(date_str):
    """Returns a specific report by date."""
    filepath = os.path.join(REPORTS_FOLDER, f"job_market_report_{date_str}.txt")
    if not os.path.exists(filepath):
        return jsonify({"error": "Report not found"}), 404

    content = read_report_file(filepath)

    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%A, %B %d, %Y")
    except:
        date = date_str

    return jsonify({"content": content, "date": date})


@app.route("/download/<date_str>")
def download_report(date_str):
    """Downloads the PDF version of a report."""
    filepath = os.path.join(REPORTS_FOLDER, f"job_market_report_{date_str}.pdf")
    if not os.path.exists(filepath):
        return jsonify({"error": "PDF not found"}), 404
    return send_file(filepath, as_attachment=True)


@app.route("/run-agent", methods=["POST"])
def run_agent_now():
    try:
        from scraper import collect_job_market_data
        from summariser import summarise_job_market
        from pdf_generator import generate_pdf
        from emailer import send_report

        data = request.get_json()
        recipient_email = data.get("recipient_email") or None

        print(f"Dashboard triggered agent run. Sending to: {recipient_email}")

        collected_data = collect_job_market_data()
        if not collected_data:
            return jsonify({"error": "No data collected"}), 500

        report_text = summarise_job_market(collected_data)
        pdf_path = generate_pdf(report_text)

        date_str = datetime.now().strftime("%Y-%m-%d")
        txt_path = os.path.join(REPORTS_FOLDER, f"job_market_report_{date_str}.txt")
        os.makedirs(REPORTS_FOLDER, exist_ok=True)
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(report_text)

        send_report(pdf_path, recipient_email)

        return jsonify({
            "message": "Report generated and emailed successfully",
            "date": datetime.now().strftime("%B %d, %Y")
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5001)