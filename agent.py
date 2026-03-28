import schedule
import time
import os
from datetime import datetime
from scraper import collect_job_market_data
from summariser import summarise_job_market
from pdf_generator import generate_pdf
from emailer import send_report


def run_agent():
    """
    The main agent pipeline. Runs all four steps in sequence:
    scrape → summarise → generate PDF → email
    """
    print(f"\n{'='*50}")
    print(f"Job Market Agent starting — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*50}")

    # Step 1 — Scrape
    print("\n[1/4] Collecting job market data...")
    collected_data = collect_job_market_data()

    if not collected_data:
        print("No data collected. Skipping this run.")
        return

    print(f"Collected data from {len(collected_data)} sources")

    # Step 2 — Summarise with AI
    print("\n[2/4] Generating AI summary...")
    report_text = summarise_job_market(collected_data)
    print("Summary generated")

    # Step 3 — Generate PDF
    print("\n[3/4] Creating PDF report...")
    pdf_path = generate_pdf(report_text)

    # Save text version so the dashboard can display it
    date_str = datetime.now().strftime("%Y-%m-%d")
    txt_path = os.path.join("reports", f"job_market_report_{date_str}.txt")
    os.makedirs("reports", exist_ok=True)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(f"Text report saved: {txt_path}")

    # Step 4 — Email
    print("\n[4/4] Sending email...")
    scheduled_recipient = os.getenv("SCHEDULED_RECIPIENT")
    send_report(pdf_path, scheduled_recipient)

    print(f"\nAgent completed successfully at {datetime.now().strftime('%H:%M')}")


# Run immediately once when the script starts
# so you can test it without waiting for the schedule
run_agent()

# Then schedule it to run every day at 8:00 AM
schedule.every().day.at("08:00").do(run_agent)

print("\nAgent scheduled. Running daily at 08:00 AM.")
print("Press Ctrl+C to stop.\n")

# Keep the script running so the scheduler works
while True:
    schedule.run_pending()
    time.sleep(60)