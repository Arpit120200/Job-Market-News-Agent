from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def clean_report(text):
    import re
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        line = line.strip()
        line = re.sub(r'\*\*?(.*?)\*\*?', r'\1', line)
        line = re.sub(r'#{1,6}\s?', '', line)
        cleaned.append(line)
    return "\n".join(cleaned)

def summarise_job_market(collected_data):
    """
    Synthesises all collected data into a structured
    daily report using OpenAI.
    """

    if not collected_data:
        return "No data was collected from sources today."

    today = datetime.now().strftime("%A, %B %d, %Y")

    sources_text = ""
    for source_name, content in collected_data.items():
        sources_text += f"\n\nSOURCE: {source_name}\n{content}"

    prompt = f"""You are a senior job market analyst writing a daily briefing for job seekers in the United States. Today is {today}.

Based on the content collected from multiple sources below, write a comprehensive daily job market report.

IMPORTANT FORMATTING RULES:
- Do NOT use markdown symbols like **, *, #, or backticks anywhere
- Use plain text only
- Use UPPERCASE for section headers
- Use a dash and space for bullet points like this: - item

The report must have exactly these six sections:

1. MARKET OVERVIEW
Write 4 to 5 sentences summarising the overall job market sentiment today. Include any macro trends, economic factors affecting hiring, and general outlook for job seekers.

2. LAYOFFS AND HIRING FREEZES
List any companies that have announced layoffs, hiring freezes, or workforce reductions. Include company name, number of employees affected if mentioned, and reason if stated. If none found in today's data, write: No major layoffs reported today.

3. COMPANIES ACTIVELY HIRING
List companies, sectors, or roles that are seeing strong hiring activity. Include the type of roles if mentioned. If none found, write: No specific hiring announcements found today.

4. IN DEMAND SKILLS AND ROLES
Based on today's data, list the skills and job titles that appear most in demand. Include both technical and non-technical roles.

5. SALARY AND COMPENSATION TRENDS
Any mentions of salary changes, compensation trends, or benefits shifts in today's data. If none found, provide general context based on current market conditions.

6. KEY TAKEAWAYS FOR JOB SEEKERS
Write 4 to 5 specific, actionable bullet points with practical advice for someone actively job searching in the US market today. Make these genuinely useful, not generic.

Here is today's collected data:
{sources_text}

Write the full report now. Use plain text only, no markdown formatting."""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior job market analyst. You write clear, accurate, actionable daily briefings for job seekers. You always use plain text with no markdown formatting."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=1500
        )
        return clean_report(response.choices[0].message.content)

    except Exception as e:
        return f"Could not generate summary: {str(e)}"