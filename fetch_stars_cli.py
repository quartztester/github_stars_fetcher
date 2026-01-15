import requests
import os
import argparse
import csv
from datetime import datetime

# --- Parse command-line arguments ---
parser = argparse.ArgumentParser(description="Fetch GitHub starred repositories")
parser.add_argument("--username", required=True, help="GitHub username to fetch stars for")
parser.add_argument("--token", default=None, help="GitHub personal access token (optional)")
parser.add_argument("--output", default="github_stars", help="Output file name (without extension)")
parser.add_argument("--format", choices=["md", "csv", "txt"], default="md",
                    help="Output format: md (Markdown), csv, txt")
args = parser.parse_args()

USERNAME = args.username
TOKEN = args.token
OUTPUT_FILE = args.output
FORMAT = args.format.lower()

# --- Setup headers ---
headers = {
    "Accept": "application/vnd.github.star+json"  # needed to get `starred_at`
}
if TOKEN:
    headers["Authorization"] = f"token {TOKEN}"

# --- Fetch starred repos ---
url = f"https://api.github.com/users/{USERNAME}/starred"
params = {"per_page": 100}

stars = []

while url:
    r = requests.get(url, headers=headers, params=params)
    r.raise_for_status()
    stars.extend(r.json())
    url = r.links.get("next", {}).get("url")

# --- Determine full output file name ---
ext_map = {"md": ".md", "csv": ".csv", "txt": ".txt"}
OUTPUT_FILE = OUTPUT_FILE + ext_map[FORMAT]

# --- Save output ---
if FORMAT == "md":
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("| Repository | Description | ⭐ Stars | ⭐ Starred On |\n")
        f.write("|------------|-------------|--------:|-------------|\n")
        for item in stars:
            repo = item["repo"]
            name = repo["full_name"]
            link = repo["html_url"]
            desc = (repo["description"] or "").replace("\n", " ")
            star_count = repo["stargazers_count"]
            starred_at = datetime.fromisoformat(item["starred_at"].replace("Z", "+00:00")).date()
            f.write(f"| [{name}]({link}) | {desc} | {star_count} | {starred_at} |\n")

elif FORMAT == "csv":
    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Repository", "Description", "Stars", "Starred On"])
        for item in stars:
            repo = item["repo"]
            writer.writerow([
                repo["full_name"],
                repo["description"] or "",
                repo["stargazers_count"],
                datetime.fromisoformat(item["starred_at"].replace("Z", "+00:00")).date()
            ])

elif FORMAT == "txt":
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for item in stars:
            repo = item["repo"]
            f.write(f"{repo['full_name']} - {repo['stargazers_count']} ⭐ - {repo['html_url']}\n")

else:
    raise ValueError(f"Unsupported format: {FORMAT}")

print(f"Saved {len(stars)} starred repositories to {OUTPUT_FILE}")
