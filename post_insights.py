"""Prepare GitHub issue comment body and issue number for the Actions workflow."""
import datetime
import json
import subprocess

date = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')

with open('insights_output.txt') as f:
    output = f.read()

body = f"## Insights — {date}\n\n```\n{output}\n```"
with open('comment_body.txt', 'w') as f:
    f.write(body)

result = subprocess.run(
    ['gh', 'issue', 'list', '--label', 'quiverquant-insights',
     '--state', 'open', '--json', 'number', '--jq', '.[0].number'],
    capture_output=True, text=True
)
issue_num = result.stdout.strip()

if not issue_num:
    result = subprocess.run(
        ['gh', 'issue', 'create',
         '--title', 'QuiverQuant Daily Insights',
         '--body', 'Daily market insights feed from QuiverQuant.',
         '--label', 'quiverquant-insights',
         '--json', 'number', '--jq', '.number'],
        capture_output=True, text=True
    )
    issue_num = result.stdout.strip()

with open('issue_num.txt', 'w') as f:
    f.write(issue_num)
