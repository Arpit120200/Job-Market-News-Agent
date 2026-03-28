# 🤖 AI Job Market Agent

An automated AI-powered agent that scrapes job market data from 
13 sources daily, synthesises it into a structured report using 
OpenAI, generates a formatted PDF, and delivers it via email. 
Includes a Flask dashboard for viewing report history and 
triggering the agent on demand.

## 🛠️ Tech Stack

* **Backend:** Python (Flask)
* **Frontend:** HTML5, CSS3, JavaScript (Fetch API)
* **AI Engine:** OpenAI API (GPT-3.5 Turbo)
* **Data Collection:** feedparser (RSS), requests, BeautifulSoup
* **PDF Generation:** ReportLab
* **Email Delivery:** smtplib (Gmail SMTP)
* **Scheduling:** schedule library
* **Environment:** Dotenv for secure credential management

## 🚀 Key Features

* **Multi-Source Intelligence:** Scrapes 13 sources including 
  TechCrunch, BBC, CNBC, WSJ, Glassdoor, GitHub Blog, 
  Hacker News and Layoffs.fyi
* **AI Synthesis:** OpenAI generates a structured six-section 
  report covering market overview, layoffs, hiring activity, 
  in-demand skills, salary trends and job seeker takeaways
* **PDF Report:** Clean formatted PDF generated automatically 
  with ReportLab and available for download
* **Flask Dashboard:** View current and historical reports, 
  download PDFs, and trigger the agent from the browser
* **Email Delivery:** Optional email delivery to any address 
  via Gmail SMTP
* **Scheduled Automation:** Runs daily at 8AM automatically 
  using the schedule library

## 📂 Architecture

The project follows a single responsibility pattern across 
five modules:

* `scraper.py` — RSS feed parsing and HTML scraping
* `summariser.py` — OpenAI prompt construction and summarisation
* `pdf_generator.py` — ReportLab PDF generation
* `emailer.py` — Gmail SMTP email delivery
* `agent.py` — Orchestrates all modules on a schedule
* `dashboard.py` — Flask web dashboard

## ⚙️ Getting Started

### Prerequisites

* Python 3.10+
* OpenAI API Key
* Gmail account with App Password enabled

### Installation & Setup

1. **Clone the repository:**
```bash
   git clone https://github.com/yourusername/job-market-news-agent.git
   cd job-market-agent
```

2. **Install dependencies:**
```bash
   pip install flask flask-cors openai python-dotenv requests
   beautifulsoup4 feedparser reportlab schedule
```

3. **Configure environment variables:**
   Create a `.env` file and add:
```bash
   OPENAI_API_KEY=your_openai_key
   GMAIL_ADDRESS=your_gmail@gmail.com
   GMAIL_APP_PASSWORD=your_app_password
   SCHEDULED_RECIPIENT=your_email@gmail.com
```

4. **Run the agent once to generate your first report:**
```bash
   python agent.py
```

5. **Start the dashboard:**
```bash
   python dashboard.py
```

6. **Access the dashboard:**
   Open [http://127.0.0.1:5001](http://127.0.0.1:5001)

## 📸 Preview
<img width="633" height="455" alt="image" src="https://github.com/user-attachments/assets/7442b88a-7ec5-424c-90f2-3f90b50cde37" />



## 🔮 Planned Improvements

* User authentication for multi-user support
* Keyword filtering to focus reports on specific industries
* Historical trend charts showing hiring activity over time
```
