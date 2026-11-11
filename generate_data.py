"""Generate deterministic, clearly fictional SaaS account-month data."""
from pathlib import Path
import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent / 'data'
OUT.mkdir(exist_ok=True)
rng = np.random.default_rng(42)
months = pd.period_range('2024-01', '2026-10', freq='M')
regions = ['North America', 'Europe', 'Latin America', 'APAC']
plans = ['Starter', 'Growth', 'Enterprise']
channels = ['Organic', 'Paid Search', 'Partner', 'Referral']
rows=[]
for i in range(1500):
    start = int(rng.integers(0, len(months)-1))
    plan = rng.choice(plans, p=[.48,.37,.15])
    region = rng.choice(regions, p=[.38,.31,.19,.12])
    channel = rng.choice(channels, p=[.32,.31,.20,.17])
    base = {'Starter':79,'Growth':249,'Enterprise':899}[plan]
    mrr = float(base*rng.uniform(.75,1.3))
    churn_prob = {'Starter':.037,'Growth':.023,'Enterprise':.012}[plan]
    for j in range(start,len(months)):
        if j>start and rng.random()<churn_prob:
            rows.append([f'ACC-{i+1:05d}',str(months[j]),str(months[start]),region,plan,channel,0.0,'churned'])
            break
        if j>start:
            mrr *= rng.choice([.92,1,1,1,1.10],p=[.07,.26,.28,.28,.11])
        rows.append([f'ACC-{i+1:05d}',str(months[j]),str(months[start]),region,plan,channel,round(mrr,2),'active'])
cols=['account_id','month','cohort_month','region','plan','acquisition_channel','mrr','status']
pd.DataFrame(rows,columns=cols).to_csv(OUT/'saas_accounts_demo.csv',index=False)
print('Generated',len(rows),'account-month records')
