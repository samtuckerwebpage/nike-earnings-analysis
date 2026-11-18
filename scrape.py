
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path

url = "https://investors.nike.com/financial-information/financial-results"

headers = {
    "User-Agent": "NikeEarningsResearch/1.0 (educational project)"
}

response = requests.get(url, headers=headers, timeout=20)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

results = []

for link in soup.find_all("a", href=True):
    title = link.get_text(" ", strip=True)
    href = requests.compat.urljoin(url, link["href"])

    if any(word in title.lower() for word in
           ["earnings", "quarter", "financial", "results", "transcript"]):
        results.append({
            "title": title,
            "source_url": href
        })

Path("data").mkdir(exist_ok=True)

df = pd.DataFrame(results, columns=["title", "source_url"])
df.drop_duplicates(inplace=True)
df.to_csv("data/nike_earnings.csv", index=False)

print(f"Found {len(df)} relevant links.")
print("Saved to data/nike_earnings.csv")

