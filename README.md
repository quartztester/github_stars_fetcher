# Github Star List Fetcher
Obtain your github stars in 1 click - a simple CLI and GUI to get your github stars in a list. Works on any operating system that can run python.

## Github Token Reccomended due to rate limiting.

## **GUI Start with command line**: 
```
>python fetch_stars_gui.py
```
<img width="331" height="156" alt="image" src="https://github.com/user-attachments/assets/cadeac12-b7cb-4908-a427-ba3c8aac160a" />

## CLI Start with command line:
```
python fetch_stars_cli.py --username githubuser --token ghp_xxxxxxxxxxxxx --output filename --format txt`
```
Example: 
```
python fetch_stars_cli.py --username octocat --token ghp_1234567890abcdef --output stars.txt --format txt
```

CLI Arguements
| Argument     | Description                                       |
| ------------ | ------------------------------------------------- |
| `--username` | GitHub username                                   |
| `--token`    | GitHub personal access token                      |
| `--output`   | Output filename                                   |
| `--format`   | Output format: `csv` or `txt` (default: markdown) |

