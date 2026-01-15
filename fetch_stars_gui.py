import requests
import os
import csv
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

# --- Function to fetch starred repos ---
def fetch_stars(username, token=None):
    headers = {"Accept": "application/vnd.github.star+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    
    url = f"https://api.github.com/users/{username}/starred"
    params = {"per_page": 100}
    stars = []

    while url:
        r = requests.get(url, headers=headers, params=params)
        r.raise_for_status()
        stars.extend(r.json())
        url = r.links.get("next", {}).get("url")
    
    return stars

# --- Function to save output ---
def save_output(stars, filename, fmt):
    if fmt == "Markdown":
        with open(filename, "w", encoding="utf-8") as f:
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
    elif fmt == "CSV":
        with open(filename, "w", encoding="utf-8", newline="") as f:
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
    elif fmt == "TXT":
        with open(filename, "w", encoding="utf-8") as f:
            for item in stars:
                repo = item["repo"]
                f.write(f"{repo['full_name']} - {repo['stargazers_count']} ⭐ - {repo['html_url']}\n")
    else:
        raise ValueError("Unsupported format")

# --- Function to run when button clicked ---
def run():
    username = username_entry.get().strip()
    token = token_entry.get().strip() or None
    fmt = format_var.get()
    filename = filedialog.asksaveasfilename(
        defaultextension={"Markdown":".md","CSV":".csv","TXT":".txt"}[fmt],
        filetypes=[(fmt, {"Markdown":"*.md","CSV":"*.csv","TXT":"*.txt"}[fmt])]
    )
    if not filename:
        return

    try:
        stars = fetch_stars(username, token)
        save_output(stars, filename, fmt)
        messagebox.showinfo("Success", f"Saved {len(stars)} starred repositories to {filename}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- GUI ---
root = tk.Tk()
root.title("GitHub Starred Repos Exporter")

tk.Label(root, text="GitHub Username:").grid(row=0, column=0, sticky="e")
username_entry = tk.Entry(root, width=30)
username_entry.grid(row=0, column=1)

tk.Label(root, text="GitHub Token (optional):").grid(row=1, column=0, sticky="e")
token_entry = tk.Entry(root, width=30, show="*")
token_entry.grid(row=1, column=1)

tk.Label(root, text="Output Format:").grid(row=2, column=0, sticky="e")
format_var = tk.StringVar(value="Markdown")
tk.OptionMenu(root, format_var, "Markdown", "CSV", "TXT").grid(row=2, column=1, sticky="w")

tk.Button(root, text="Run", command=run, width=20).grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()