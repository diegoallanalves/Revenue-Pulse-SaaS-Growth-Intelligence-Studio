"""RevenuePulse: original SaaS growth intelligence portfolio demo."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title='RevenuePulse | Growth Intelligence', page_icon='◈', layout='wide', initial_sidebar_state='expanded')
ROOT=Path(__file__).resolve().parent
ACCENT='#A994FF'
PALETTE=['#A994FF','#34D7C4','#FFB86B','#FF6E91']

st.markdown('''<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"],[data-testid="stApp"]{font-family:'DM Sans',sans-serif}
[data-testid="stAppViewContainer"]{background:radial-gradient(ellipse at 80% 5%,rgba(80,51,151,.18),transparent 35%),#0B1020;color:#F2F4FF}
[data-testid="stHeader"]{background:transparent}
.block-container{padding-top:1.1rem;max-width:1560px;padding-bottom:2rem}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#15172F,#101627);border-right:1px solid #30334F}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p{font-size:.88rem}
[data-testid="stSidebar"] [role="radiogroup"] label{border-radius:9px;padding:3px 5px}
[data-testid="stMetric"]{background:linear-gradient(135deg,#1E203C,#171F36);border:1px solid #393B62;padding:1.1rem 1.15rem;border-radius:16px;box-shadow:0 12px 25px rgba(0,0,0,.13)}
[data-testid="stMetricLabel"]{color:#AFB7D3}
[data-testid="stMetricValue"]{color:#F9F8FF;font-weight:800;letter-spacing:-.045em}
[data-testid="stVerticalBlockBorderWrapper"]{border-color:#323955}
h1,h2,h3{letter-spacing:-.04em}
h3{font-size:1.22rem!important}
.hero{padding:1.6rem 2rem;border-radius:20px;background:radial-gradient(circle at 90% 15%,rgba(46,220,203,.18),transparent 32%),linear-gradient(115deg,#2B2054,#1B2347 62%,#113E49);border:1px solid #4B467B;margin-bottom:1rem;box-shadow:0 16px 35px rgba(0,0,0,.18)}
.eyebrow{color:#67E8D8;font-weight:800;font-size:.73rem;letter-spacing:.19em}
.hero h1{font-size:2.4rem;margin:.4rem 0;color:#fff;line-height:1.14}
.hero p{color:#D0D6EB;font-size:.96rem;max-width:850px;margin-bottom:.2rem}
.note{padding:12px 16px;background:#1E233A;border-left:3px solid #A994FF;border-radius:8px;color:#D6DAE7}
.glass-strip{display:flex;gap:12px;flex-wrap:wrap;margin:.3rem 0 1.1rem}
.glass-pill{padding:8px 13px;border:1px solid #3B4469;background:#1A223A;border-radius:999px;color:#C9D5EA;font-size:.78rem}
.glass-pill b{color:#65E6D7}
div[data-testid="stPlotlyChart"]{border:1px solid #303651;border-radius:16px;background:linear-gradient(145deg,rgba(30,34,61,.74),rgba(15,24,43,.72));padding:12px 12px 4px;box-shadow:0 10px 25px rgba(0,0,0,.1)}
div[data-testid="stButton"] button,div[data-testid="stDownloadButton"] button{border-radius:10px}
[data-testid="stSidebar"] hr{border-color:#343854}
</style>''',unsafe_allow_html=True)

@st.cache_data
def load_default():
    return pd.read_csv(ROOT/'data'/'saas_accounts_demo.csv')

def validate(df):
    required={'account_id','month','cohort_month','region','plan','acquisition_channel','mrr','status'}
    missing=required-set(df.columns)
    if missing: raise ValueError(f'Missing required columns: {", ".join(sorted(missing))}')
    df=df.copy()
    df['month']=pd.to_datetime(df['month'].astype(str)+'-01',errors='coerce')
    df['cohort_month']=pd.to_datetime(df['cohort_month'].astype(str)+'-01',errors='coerce')
    df['mrr']=pd.to_numeric(df['mrr'],errors='coerce')
    if df[['month','cohort_month','mrr']].isna().any().any(): raise ValueError('Invalid date or MRR values.')
    if (df['mrr']<0).any(): raise ValueError('MRR must be nonnegative.')
    if df.duplicated(['account_id','month']).any(): raise ValueError('Duplicate account-month rows.')
    return df

with st.sidebar:
    st.markdown('## ◈ RevenuePulse <span style="color:#7BE7D7;font-size:.7rem;vertical-align:middle">PRO</span>',unsafe_allow_html=True)
    st.caption('GROWTH INTELLIGENCE STUDIO')
    st.divider()
    source=st.radio('Data source',['Included synthetic demo','Upload your CSV'],label_visibility='visible')
    if source=='Upload your CSV':
        uploaded=st.file_uploader('Account-month CSV',type='csv')
        if uploaded is None:
            st.info('Upload a CSV using the template columns, or select the included demo.')
            st.stop()
        try: raw=pd.read_csv(uploaded)
        except Exception as e: st.error(f'Could not read CSV: {e}');st.stop()
    else: raw=load_default()
    try: df=validate(raw)
    except ValueError as e: st.error(str(e));st.stop()
    regions=st.multiselect('Regions',sorted(df.region.dropna().unique()),default=sorted(df.region.dropna().unique()))
    plans=st.multiselect('Plans',sorted(df.plan.dropna().unique()),default=sorted(df.plan.dropna().unique()))
    df=df[df.region.isin(regions)&df.plan.isin(plans)].copy()
    if df.empty: st.warning('No accounts match your filters.');st.stop()
    st.divider()
    page=st.radio('Workspace',['Executive overview','Retention laboratory','Revenue explorer','Scenario simulator','Data quality & methodology'])
    st.divider()
    st.caption('SYNTHETIC DATA • DEMONSTRATION ONLY')
    st.link_button('View GitHub profile','https://github.com/diegoallanalves',use_container_width=True)

st.markdown('''<div class="hero"><div class="eyebrow">◈ REVENUEPULSE PRO &nbsp; / &nbsp; INTELLIGENCE WORKSPACE</div><h1>Revenue intelligence,<br/>beautifully connected.</h1><p>Understand recurring revenue, customer retention and commercial performance — all in one interactive analytics workspace.</p></div>''',unsafe_allow_html=True)
st.markdown('''<div class="glass-strip"><span class="glass-pill">● &nbsp;<b>Demo data active</b></span><span class="glass-pill">◈ &nbsp;Interactive intelligence</span><span class="glass-pill">▣ &nbsp;Multi-region analytics</span><span class="glass-pill">✦ &nbsp;Built with Python + Streamlit</span></div>''',unsafe_allow_html=True)
st.caption('All included values are generated synthetic examples. No real company, customer or market performance is represented.')

active=df[df.status.eq('active')].copy()
monthly=active.groupby('month',as_index=False).agg(mrr=('mrr','sum'),customers=('account_id','nunique'))
monthly=monthly.sort_values('month')
if monthly.empty: st.warning('No active account records in selected data.');st.stop()
latest=monthly.iloc[-1]
prev=monthly.iloc[-2] if len(monthly)>1 else latest
latest_month=latest['month']
current=active[active.month.eq(latest_month)]
prior=active[active.month.eq(prev['month'])]
current_ids=set(current.account_id)
prior_ids=set(prior.account_id)
churned_ids=prior_ids-current_ids
churn_rate=len(churned_ids)/len(prior_ids) if prior_ids else 0
mrr_growth=(latest.mrr/prev.mrr-1)*100 if prev.mrr else 0

def plot(fig):
    fig.update_layout(template='plotly_dark',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',font=dict(color='#DCE5FA',family='DM Sans'),margin=dict(l=8,r=8,t=18,b=8),legend_title_text='',height=330,hovermode='x unified',xaxis=dict(showgrid=False,zeroline=False),yaxis=dict(gridcolor='rgba(180,190,230,.12)',zeroline=False))
    st.plotly_chart(fig,use_container_width=True)

def headline(title,desc):
    st.subheader(title)
    st.caption(desc)

if page=='Executive overview':
    c1,c2,c3,c4=st.columns(4)
    c1.metric('Monthly recurring revenue',f'£{latest.mrr:,.0f}',f'{mrr_growth:+.1f}% vs prior month')
    c2.metric('Annualised run rate',f'£{latest.mrr*12:,.0f}')
    c3.metric('Active accounts',f'{int(latest.customers):,}')
    c4.metric('Logo churn (monthly)',f'{churn_rate:.1%}',help='Previous-month active accounts missing from the latest month, divided by previous-month active accounts.')
    a,b=st.columns([1.7,1])
    with a:
        headline('Recurring revenue trajectory','Monthly sum of active account MRR')
        fig=px.area(monthly,x='month',y='mrr',color_discrete_sequence=[ACCENT],labels={'month':'Month','mrr':'MRR (£)'})
        fig.update_traces(line_width=3.5,fillcolor='rgba(169,148,255,.20)');plot(fig)
    with b:
        headline('Revenue mix by plan','Latest available month')
        mix=current.groupby('plan',as_index=False).mrr.sum()
        fig=px.pie(mix,names='plan',values='mrr',hole=.68,color_discrete_sequence=PALETTE)
        fig.update_traces(textinfo='percent+label',marker=dict(line=dict(color='#161B32',width=3)));plot(fig)
    headline('Customer base growth','Active account count by month')
    fig=px.bar(monthly,x='month',y='customers',color_discrete_sequence=['#34D7C4'],labels={'customers':'Active accounts','month':'Month'})
    plot(fig)
    st.markdown('### Executive signals')
    x,y,z=st.columns(3)
    with x:
        st.info(f'**Current revenue**  \\n£{latest.mrr:,.0f} in the most recent observed month.')
    with y:
        st.info(f'**Account footprint**  \\n{int(latest.customers):,} active accounts across selected regions.')
    with z:
        st.info(f'**Revenue movement**  \\n{mrr_growth:+.1f}% versus the previous month.')
elif page=='Retention laboratory':
    headline('Cohort retention heatmap','Percentage of each signup cohort still active after N months')
    first=active[['account_id','cohort_month']].drop_duplicates('account_id')
    cohort_counts=first.groupby('cohort_month').account_id.nunique()
    cohort=active.copy()
    cohort['age']=(cohort.month.dt.year-cohort.cohort_month.dt.year)*12+(cohort.month.dt.month-cohort.cohort_month.dt.month)
    counts=cohort.groupby(['cohort_month','age']).account_id.nunique().unstack()
    retention=counts.div(cohort_counts,axis=0)*100
    retention=retention.sort_index().tail(16).iloc[:,:13]
    if not retention.empty:
        fig=px.imshow(retention.round(1),text_auto='.0f',aspect='auto',color_continuous_scale=[[0,'#1B2640'],[.5,'#5B54B0'],[1,'#35CDBD']],labels={'x':'Months since acquisition','y':'Cohort','color':'Retention %'})
        fig.update_yaxes(tickvals=list(range(len(retention.index))),ticktext=retention.index.strftime('%Y-%m'))
        plot(fig)
    st.markdown('<div class="note">Cohorts are grouped by first signup month. Later cohorts have fewer observed months; blank cells are not zero retention.</div>',unsafe_allow_html=True)
    st.subheader('Retention by acquisition channel')
    tmp=active.copy();tmp['age']=(tmp.month.dt.year-tmp.cohort_month.dt.year)*12+(tmp.month.dt.month-tmp.cohort_month.dt.month)
    selected=st.slider('Months after acquisition',1,12,3)
    base=active.drop_duplicates('account_id').groupby('acquisition_channel').account_id.nunique()
    retained=tmp[tmp.age.eq(selected)].groupby('acquisition_channel').account_id.nunique()
    out=(retained/base*100).dropna().sort_values(ascending=False).rename('retention_pct').reset_index()
    plot(px.bar(out,x='acquisition_channel',y='retention_pct',color='acquisition_channel',color_discrete_sequence=PALETTE,labels={'retention_pct':'Observed retention (%)','acquisition_channel':'Channel'}))
    st.caption('Channel rates are descriptive; cohorts without enough elapsed time are not adjusted for censoring in this simple view.')
elif page=='Revenue explorer':
    headline('Revenue segmentation','Understand revenue concentration by region, plan and acquisition channel')
    group=st.selectbox('Group by',['region','plan','acquisition_channel'])
    agg=current.groupby(group,as_index=False).agg(mrr=('mrr','sum'),accounts=('account_id','nunique')).sort_values('mrr',ascending=False)
    a,b=st.columns([1.3,1])
    with a: plot(px.bar(agg,x=group,y='mrr',color=group,color_discrete_sequence=PALETTE,labels={'mrr':'Monthly revenue (£)'}))
    with b: st.dataframe(agg,use_container_width=True,hide_index=True)
    st.subheader('Compare revenue over time')
    series=active.groupby(['month',group],as_index=False).mrr.sum()
    plot(px.line(series,x='month',y='mrr',color=group,color_discrete_sequence=PALETTE,labels={'mrr':'MRR (£)','month':'Month'}))
    st.download_button('Download filtered account-month data',df.to_csv(index=False).encode(),file_name='revenuepulse_filtered.csv',mime='text/csv')
elif page=='Scenario simulator':
    headline('Growth scenario studio','Illustrative projections, not forecasts or financial advice')
    a,b,c=st.columns(3)
    with a: new_mrr=st.slider('New MRR added per month (£)',0,25000,5000,500)
    with b: expansion=st.slider('Existing revenue expansion (% / month)',0.0,5.0,1.0,.1)
    with c: loss=st.slider('Revenue churn (% / month)',0.0,10.0,2.0,.25)
    periods=st.slider('Projection horizon (months)',3,24,12)
    values=[float(latest.mrr)]
    for _ in range(periods): values.append(values[-1]*(1+expansion/100-loss/100)+new_mrr)
    timeline=pd.date_range(latest_month,periods=periods+1,freq='MS')
    sim=pd.DataFrame({'month':timeline,'projected_mrr':values})
    c1,c2,c3=st.columns(3)
    c1.metric('Starting MRR',f'£{values[0]:,.0f}')
    c2.metric('Scenario ending MRR',f'£{values[-1]:,.0f}')
    c3.metric('Scenario change',f'{(values[-1]/values[0]-1):+.1%}')
    fig=px.line(sim,x='month',y='projected_mrr',markers=True,color_discrete_sequence=['#34D7C4'],labels={'month':'Month','projected_mrr':'Scenario MRR (£)'})
    plot(fig)
    st.info('Assumption: revenue expands and churns at fixed monthly rates, and a fixed amount of new MRR is added monthly. This is a deterministic what-if calculation, not a predictive model.')
    st.download_button('Export scenario',sim.to_csv(index=False),file_name='scenario.csv',mime='text/csv')
else:
    headline('Data quality and reproducibility','Inspect the data feeding this dashboard')
    x,y,z=st.columns(3)
    x.metric('Rows',f'{len(df):,}')
    y.metric('Unique accounts',f'{df.account_id.nunique():,}')
    z.metric('Missing values',f'{int(df.isna().sum().sum()):,}')
    st.dataframe(df.head(30),use_container_width=True,hide_index=True)
    st.subheader('Column-level missingness')
    st.dataframe(df.isna().sum().rename('missing_rows'),use_container_width=True)
    st.subheader('How the metrics work')
    st.markdown('''**MRR** is the sum of active account monthly recurring revenue in the selected month.  
**ARR run rate** is MRR multiplied by 12; it is not recognised annual revenue.  
**Logo churn** compares active account IDs in two consecutive months.  
**Cohort retention** tracks active accounts relative to the cohort's initial signup count.  
**Scenario modelling** applies fixed monthly expansion, churn and new revenue assumptions.  

**Caveats:** This app is an educational demonstration using generated data. Filtering by plan or region describes the selected slice, not necessarily a customer's original plan or region if those change over time. Churn records are excluded from MRR totals. Uploads are processed in the active session, not written to a database.''')
    st.download_button('Download example CSV schema',load_default().head(10).to_csv(index=False),file_name='schema_example.csv',mime='text/csv')

st.divider()
st.caption('RevenuePulse © 2026 · Built as an independent portfolio demonstration · Python · Streamlit · Plotly · Synthetic data')
