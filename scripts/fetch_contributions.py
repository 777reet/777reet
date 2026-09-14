import json,re
from datetime import date, timedelta
from pathlib import Path
import requests
from bs4 import BeautifulSoup

USERNAME='777reet'
URL=f'https://github.com/users/{USERNAME}/contributions'
out=Path('data/contributions.json')
html=requests.get(URL,headers={'User-Agent':'Mozilla/5.0'},timeout=30).text
soup=BeautifulSoup(html,'html.parser')
days=[]
for cell in soup.select('td.ContributionCalendar-day, rect.ContributionCalendar-day'):
    d=cell.get('data-date')
    if not d: continue
    level=cell.get('data-level')
    label=cell.get('aria-label') or cell.get('title') or ''
    m=re.search(r'(\d+) contribution',label)
    count=int(m.group(1)) if m else (0 if level in (None,'0') else 1)
    days.append({'date':d,'count':count,'level':int(level or 0)})
if not days:
    raise SystemExit('Could not find contribution day cells.')
# Deduplicate and sort
days={x['date']:x for x in days}
days=sorted(days.values(),key=lambda x:x['date'])
counts=[x['count'] for x in days]
total=sum(counts)
current=0
for x in reversed(days):
    if x['count']>0: current+=1
    else: break
best=0; run=0
for x in days:
    run=run+1 if x['count']>0 else 0
    best=max(best,run)
best_day=max(days,key=lambda x:x['count'])
monthly={}
for x in days:
    key=x['date'][:7]; monthly[key]=monthly.get(key,0)+x['count']
data={'username':USERNAME,'generated_at':date.today().isoformat(),'total':total,'current_streak':current,'longest_streak':best,'best_day':best_day,'monthly':monthly,'days':days}
out.write_text(json.dumps(data,indent=2),encoding='utf-8')
print(f'Fetched {len(days)} days / {total} contributions')
