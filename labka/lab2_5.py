import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.python.org/jobs/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
jobs = soup.select("ol.list-recent-jobs li")
data = []

for i, job in enumerate(jobs, 1):
    title_tag = job.find("h2")
    company_tag = job.find("span", class_="listing-company-name")

    if title_tag:
        a_tag = title_tag.find("a")
        title = a_tag.text.strip()
        link = "https://www.python.org" + a_tag.get("href")

        company = company_tag.text.strip() if company_tag else "N/A"

        print(f"{i}. {title}")
        print(f"   Company: {company}")
        print(f"   Link: {link}\n")

        data.append([title, company, link])

with open("python_jobs.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Company", "Link"])
    writer.writerows(data)

print("Готово! Данные сохранены в python_jobs.csv")
