from __future__ import annotations
import io
from datetime import date, timedelta
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="StudentSmart AI", page_icon="✦", layout="wide", initial_sidebar_state="expanded")

# ---------- Design system ----------
NAVY = "#10172A"
INK = "#18243B"
MUTED = "#758198"
MINT = "#B8F4D5"
LIME = "#D8F36A"
PAPER = "#F5F7FB"
PURPLE = "#6D5AE6"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
:root {{ --navy:{NAVY}; --ink:{INK}; --muted:{MUTED}; --mint:{MINT}; --lime:{LIME}; --paper:{PAPER}; --purple:{PURPLE}; }}
html, body, [class*="css"] {{ font-family:'DM Sans',sans-serif; }}
.stApp {{ background:var(--paper); color:var(--ink); }}
.block-container {{ padding-top:1.5rem; padding-bottom:3rem; max-width:1440px; }}
[data-testid="stSidebar"] {{ background:var(--navy); border-right:1px solid #202a43; }}
[data-testid="stSidebar"] * {{ color:#F5F7FF !important; }}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{ color:#AEB9D0 !important; }}
.brand-mark {{ display:flex; align-items:center; gap:11px; margin:7px 0 25px; }}
.brand-icon {{ width:42px; height:42px; display:grid; place-items:center; border-radius:14px; background:var(--lime); color:var(--navy); font-size:24px; font-weight:900; }}
.brand-name {{ font-family:'Space Grotesk',sans-serif; font-size:20px; font-weight:700; letter-spacing:-.7px; }}
.brand-sub {{ font-size:11px; color:#AEB9D0; letter-spacing:1.6px; text-transform:uppercase; margin-top:2px; }}
.eyebrow {{ color:var(--purple); font-size:11px; font-weight:800; letter-spacing:1.8px; text-transform:uppercase; margin-bottom:8px; }}
.hero {{ background:var(--navy); color:white; border-radius:26px; padding:28px 32px; position:relative; overflow:hidden; margin-bottom:22px; }}
.hero:after {{ content:''; position:absolute; width:260px; height:260px; border:1px solid #39445d; border-radius:50%; right:-45px; top:-110px; box-shadow:0 0 0 28px rgba(255,255,255,.025),0 0 0 58px rgba(255,255,255,.02); }}
.hero h1 {{ color:white; font-family:'Space Grotesk',sans-serif; font-size:34px; line-height:1.15; margin:0 0 10px; letter-spacing:-1.2px; }}
.hero p {{ color:#C3CBE0; margin:0; font-size:14px; max-width:620px; }}
.hero-pill {{ display:inline-block; border:1px solid #46516b; border-radius:100px; padding:6px 10px; font-size:11px; color:var(--mint); margin-bottom:15px; letter-spacing:.5px; }}
.panel {{ background:white; border:1px solid #E7EBF3; border-radius:20px; padding:20px 22px; height:100%; box-shadow:0 4px 18px rgba(23,34,60,.025); }}
.panel-title {{ font-family:'Space Grotesk',sans-serif; font-size:16px; font-weight:700; color:var(--ink); margin:0 0 4px; }}
.panel-sub {{ font-size:12px; color:var(--muted); margin-bottom:16px; }}
.metric-label {{ color:#AAB4C8; font-size:11px; text-transform:uppercase; letter-spacing:1.4px; font-weight:700; }}
.metric-value {{ color:white; font-family:'Space Grotesk',sans-serif; font-size:31px; font-weight:700; letter-spacing:-1px; margin:5px 0 3px; }}
.metric-foot {{ color:#C2CBE0; font-size:12px; }}
.metric-card {{ background:var(--navy); border-radius:18px; padding:18px 20px; min-height:126px; }}
.metric-card.light {{ background:white; border:1px solid #E7EBF3; }}
.metric-card.light .metric-label {{ color:var(--muted); }} .metric-card.light .metric-value {{ color:var(--ink); }} .metric-card.light .metric-foot {{ color:var(--muted); }}
.score-ring {{ width:112px; height:112px; border-radius:50%; border:8px solid #29344F; border-top-color:var(--lime); border-right-color:var(--lime); display:flex; align-items:center; justify-content:center; flex-direction:column; }}
.score-num {{ font-family:'Space Grotesk',sans-serif; font-size:27px; font-weight:700; color:white; line-height:1; }}
.score-den {{ color:#AEB9D0; font-size:10px; margin-top:5px; }}
.tag {{ display:inline-block; padding:5px 9px; border-radius:7px; background:#EEF0FF; color:#5949C6; font-size:11px; font-weight:700; }}
.tip {{ background:#EEF9F2; border:1px solid #D8F0E1; border-radius:15px; padding:15px 17px; color:#244C38; }}
.tip strong {{ color:#163B29; }}
.warning {{ background:#FFF6E6; border:1px solid #F8E2B9; border-radius:15px; padding:14px 16px; color:#79531C; }}
.section-heading {{ font-family:'Space Grotesk',sans-serif; font-size:21px; font-weight:700; letter-spacing:-.6px; margin:18px 0 12px; }}
div[data-testid="stButton"] > button {{ border-radius:12px; border:1px solid #DDE3EE; font-weight:700; min-height:43px; }}
div[data-testid="stButton"] > button[kind="primary"] {{ background:var(--lime); color:var(--navy); border:0; }}
div[data-testid="stButton"] > button[kind="primary"]:hover {{ background:#c7e64e; color:var(--navy); }}
.stTabs [data-baseweb="tab-list"] {{ gap:8px; }}
.stTabs [data-baseweb="tab"] {{ background:#EDEFF6; border-radius:10px; padding:8px 14px; }}
.stTabs [aria-selected="true"] {{ background:var(--navy) !important; color:white !important; }}

.login-shell {{ max-width:1120px; margin:3vh auto; background:white; border:1px solid #E6EAF2; border-radius:28px; overflow:hidden; box-shadow:0 24px 70px rgba(16,23,42,.10); }}
.login-brand-panel {{ background:var(--navy); color:white; padding:42px 38px; min-height:590px; position:relative; overflow:hidden; border-radius:24px; }}
.login-brand-panel:after {{ content:''; position:absolute; width:300px; height:300px; right:-120px; bottom:-130px; border:1px solid #45516B; border-radius:50%; box-shadow:0 0 0 30px rgba(255,255,255,.025),0 0 0 65px rgba(255,255,255,.02); }}
.login-logo {{ display:inline-grid; place-items:center; width:48px; height:48px; border-radius:16px; background:var(--lime); color:var(--navy); font-size:27px; font-weight:900; margin-bottom:34px; }}
.login-title {{ font-family:'Space Grotesk',sans-serif; font-size:37px; line-height:1.12; font-weight:700; letter-spacing:-1.3px; margin:0 0 16px; color:white; }}
.login-copy {{ color:#C3CBE0; font-size:14px; line-height:1.8; max-width:380px; }}
.login-feature {{ border:1px solid #35415C; background:rgba(255,255,255,.035); border-radius:15px; padding:13px 15px; margin-top:12px; color:#EAF0FF; font-size:13px; }}
.login-form-panel {{ padding:42px 40px; }}
.login-kicker {{ color:var(--purple); font-size:11px; font-weight:800; letter-spacing:1.8px; text-transform:uppercase; }}
.login-heading {{ font-family:'Space Grotesk',sans-serif; font-size:29px; line-height:1.2; color:var(--ink); letter-spacing:-.8px; margin:10px 0 8px; }}
.login-muted {{ color:var(--muted); font-size:13px; line-height:1.7; margin-bottom:22px; }}
.demo-credential {{ background:#F4F6FB; border:1px solid #E6EAF2; border-radius:12px; padding:12px 14px; color:#5F6B82; font-size:12px; line-height:1.8; margin-top:16px; }}

footer {{visibility:hidden;}}
</style>
""", unsafe_allow_html=True)

# ---------- Login gate (demo authentication) ----------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "student_name" not in st.session_state:
    st.session_state.student_name = "Campus Explorer"
# Demo accounts live only in this Streamlit session; they are not stored securely or persistently.
if "demo_accounts" not in st.session_state:
    st.session_state.demo_accounts = {"student@demo.com": {"password": "smart123", "name": "Campus Explorer"}}

if not st.session_state.authenticated:
    st.markdown("<div style='height:2vh'></div><div class='eyebrow'>STUDENT FINANCE · PERSONAL COMMAND CENTRE</div>", unsafe_allow_html=True)
    login_left, login_right = st.columns([1, 1], gap="large")
    with login_left:
        st.markdown("""
        <div class="login-brand-panel">
          <div class="login-logo">✦</div>
          <div style="font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#B8F4D5;font-weight:800;margin-bottom:15px;">STUDENT FINANCE, REIMAGINED</div>
          <div class="login-title">Your money.<br/>Your next move.</div>
          <div class="login-copy">A calmer way to manage student spending, build better habits, and make confident money decisions—one small step at a time.</div>
          <div style="height:22px"></div>
          <div class="login-feature">◈ &nbsp; See your money picture at a glance</div>
          <div class="login-feature">⌁ &nbsp; Test a purchase before you spend</div>
          <div class="login-feature">◇ &nbsp; Spot common scam warning signs</div>
          <div style="margin-top:38px;color:#8996B0;font-size:11px;letter-spacing:1px;">BUILT FOR STUDENT LIFE · DEMO EDITION</div>
        </div>
        """, unsafe_allow_html=True)
    with login_right:
        st.markdown("""
        <div style='padding:22px 10px 8px 10px;'>
          <div class='login-kicker'>WELCOME TO STUDENTSMART</div>
          <div class='login-heading'>Your money space starts here</div>
          <div class='login-muted'>Sign in to an existing demo account, or sign up to try the prototype with a new session-only account.</div>
        </div>
        """, unsafe_allow_html=True)
        signin_tab, signup_tab = st.tabs(["🔑  Sign In", "✨  Sign Up"])
        with signin_tab:
            with st.form("student_login_form", clear_on_submit=False):
                login_email = st.text_input("Email address", placeholder="student@demo.com", key="signin_email")
                login_password = st.text_input("Password", type="password", placeholder="Enter your password", key="signin_password")
                login_submit = st.form_submit_button("Sign In  →", type="primary", use_container_width=True)
            if login_submit:
                account = st.session_state.demo_accounts.get(login_email.strip().lower())
                if account and account["password"] == login_password:
                    st.session_state.authenticated = True
                    st.session_state.student_name = account["name"]
                    st.rerun()
                else:
                    st.error("Email or password didn't match. Check your details or sign up for a demo account.")
            st.markdown("<div class='demo-credential'><b>Demo account</b><br/>Email: student@demo.com<br/>Password: smart123</div>", unsafe_allow_html=True)
        with signup_tab:
            with st.form("student_signup_form", clear_on_submit=True):
                signup_name = st.text_input("Your name", placeholder="e.g. Asha")
                signup_email = st.text_input("Email address", placeholder="you@example.com")
                signup_password = st.text_input("Create password", type="password", placeholder="At least 6 characters")
                signup_confirm = st.text_input("Confirm password", type="password", placeholder="Enter it again")
                signup_submit = st.form_submit_button("Create Account  →", type="primary", use_container_width=True)
            if signup_submit:
                email_key = signup_email.strip().lower()
                if not signup_name.strip() or not email_key or "@" not in email_key:
                    st.error("Please enter your name and a valid email address.")
                elif len(signup_password) < 6:
                    st.error("Please use a password with at least 6 characters.")
                elif signup_password != signup_confirm:
                    st.error("The passwords don't match. Please try again.")
                elif email_key in st.session_state.demo_accounts:
                    st.error("An account with that email already exists. Please sign in instead.")
                else:
                    st.session_state.demo_accounts[email_key] = {"password": signup_password, "name": signup_name.strip()}
                    st.session_state.authenticated = True
                    st.session_state.student_name = signup_name.strip()
                    st.success("Demo account created! Opening your dashboard…")
                    st.rerun()
            st.caption("Prototype only: accounts exist only for this running session. Do not use a real or reused password.")
        if st.button("Explore demo without signing in", use_container_width=True):
            st.session_state.authenticated = True
            st.session_state.student_name = "Campus Explorer"
            st.rerun()
        st.markdown("<div style='margin-top:22px;color:#98A2B4;font-size:11px;text-align:center'>🔒 Sample data only · No bank account connected</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;color:#98A2B4;font-size:11px;margin-top:20px'>STUDENTSMART AI · HACKATHON PROTOTYPE</div>", unsafe_allow_html=True)
    st.stop()

# ---------- Demo data ----------
@st.cache_data
def sample_data():
    rng = np.random.default_rng(14)
    items = [
        ("Pocket money", "Income", 5000), ("Hostel fee", "Housing", -2200),
        ("Campus canteen", "Food", -85), ("Metro / bus", "Transport", -60),
        ("Coffee with friends", "Food", -160), ("Data recharge", "Bills", -299),
        ("Study materials", "Education", -420), ("Freelance design", "Income", 1800),
        ("Food delivery", "Food", -340), ("Print shop", "Education", -90),
        ("Movie night", "Entertainment", -280), ("UPI transfer", "Shopping", -550),
        ("Scholarship credit", "Income", 2500), ("Groceries", "Food", -360),
        ("Online course", "Education", -699), ("Auto ride", "Transport", -140),
        ("Food delivery", "Food", -490), ("Subscription", "Bills", -199),
        ("Emergency medicine", "Health", -230), ("Club contribution", "Social", -150),
    ]
    start = date.today() - timedelta(days=23)
    rows=[]
    for i,(merchant,cat,amount) in enumerate(items):
        rows.append({"Date": start+timedelta(days=i), "Merchant":merchant, "Category":cat, "Amount":amount, "Type":"Income" if amount>0 else "Expense"})
    return pd.DataFrame(rows)

if "transactions" not in st.session_state:
    st.session_state.transactions = sample_data()
if "page" not in st.session_state: st.session_state.page = "Overview"

df = st.session_state.transactions.copy()
df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date

def money(v): return f"₹{v:,.0f}"
def categorize(text):
    t=text.lower()
    rules={"Food":["food","cafe","coffee","canteen","restaurant","swiggy","zomato","grocery"],"Transport":["bus","metro","auto","uber","ola","fuel","petrol"],"Education":["book","course","college","print","study","tuition"],"Bills":["recharge","wifi","electric","subscription","mobile"],"Shopping":["shop","amazon","clothes","transfer"],"Health":["medical","medicine","doctor","pharmacy"]}
    for c,words in rules.items():
        if any(w in t for w in words): return c
    return "Other"

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("<div class='brand-mark'><div class='brand-icon'>✦</div><div><div class='brand-name'>StudentSmart</div><div class='brand-sub'>AI money mentor</div></div></div>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:10px;letter-spacing:1.7px;font-weight:800;color:#75839F !important;'>YOUR MONEY SPACE</p>", unsafe_allow_html=True)
    pages = ["Overview", "Spend Simulator", "Scam Shield", "Money Mentor", "Transactions"]
    icons = {"Overview":"◈","Spend Simulator":"⌁","Scam Shield":"◇","Money Mentor":"✳","Transactions":"≋"}
    for p in pages:
        if st.button(f"{icons[p]}   {p}", key=f"nav_{p}", use_container_width=True, type="primary" if st.session_state.page==p else "secondary"):
            st.session_state.page=p; st.rerun()
    st.markdown("<div style='height:25px'></div><div style='border-top:1px solid #2A3550;padding-top:17px;color:#8F9BB4;font-size:11px;letter-spacing:1.2px;font-weight:700;'>DEMO PROFILE</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='display:flex;align-items:center;gap:10px;margin-top:12px'><div style='width:38px;height:38px;border-radius:13px;background:#29344F;display:grid;place-items:center;font-size:18px'>🎓</div><div><div style='font-weight:700;font-size:13px'>{st.session_state.student_name}</div><div style='font-size:11px;color:#AEB9D0'>Student account · Demo</div></div></div>", unsafe_allow_html=True)
    if st.button('↪  Sign out', use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()
    st.markdown("<div style='margin-top:26px;padding:13px;background:#1A2540;border-radius:14px;font-size:11px;color:#AEB9D0;line-height:1.6'>🔒 <b style='color:#F5F7FF'>Privacy-first prototype</b><br/>Uses sample or uploaded data only. No bank account is connected.</div>", unsafe_allow_html=True)

# ---------- Calculations ----------
income = float(df.loc[df.Amount>0,"Amount"].sum())
expenses = float(-df.loc[df.Amount<0,"Amount"].sum())
net = income-expenses
savings_rate = max(0,min(100,round(net/income*100))) if income else 0
score = int(max(350,min(950, 600 + savings_rate*3 - max(0, expenses-income)*.03 + min(100, df[df.Amount<0].shape[0]*2))))
score = int(max(350,min(950,score)))

# ---------- Header ----------
c1,c2 = st.columns([7,2])
with c1:
    st.markdown("<div class='eyebrow'>STUDENT FINANCE · PERSONAL COMMAND CENTRE</div>",unsafe_allow_html=True)
with c2:
    st.markdown(f"<div style='text-align:right;color:{MUTED};font-size:12px;padding-top:4px'>◉ Demo mode &nbsp;·&nbsp; {date.today().strftime('%d %b %Y')}</div>",unsafe_allow_html=True)

if st.session_state.page == "Overview":
    st.markdown("<div class='hero'><div class='hero-pill'>✦ YOUR MONEY, WITH A GAME PLAN</div><h1>Small choices.<br/>Stronger money habits.</h1><p>Your student-friendly money dashboard turns everyday spending into clearer decisions—without the finance jargon.</p></div>",unsafe_allow_html=True)
    a,b,c,d = st.columns(4, gap="medium")
    with a: st.markdown(f"<div class='metric-card'><div class='metric-label'>Student Smart Score</div><div class='metric-value'>{score}<span style='font-size:15px;color:#AEB9D0'> /1000</span></div><div class='metric-foot'>Habit indicator · not a credit score</div></div>",unsafe_allow_html=True)
    with b: st.markdown(f"<div class='metric-card light'><div class='metric-label'>Money in</div><div class='metric-value'>{money(income)}</div><div class='metric-foot'>Income in loaded transactions</div></div>",unsafe_allow_html=True)
    with c: st.markdown(f"<div class='metric-card light'><div class='metric-label'>Money out</div><div class='metric-value'>{money(expenses)}</div><div class='metric-foot'>Spending in loaded transactions</div></div>",unsafe_allow_html=True)
    with d: st.markdown(f"<div class='metric-card light'><div class='metric-label'>Net balance change</div><div class='metric-value' style='color:{'#1A8A59' if net>=0 else '#D05A53'}'>{money(net)}</div><div class='metric-foot'>{'Positive cash flow' if net>=0 else 'Spending exceeds income'}</div></div>",unsafe_allow_html=True)
    st.markdown("<div class='section-heading'>Your money at a glance</div>",unsafe_allow_html=True)
    left,right=st.columns([1.45,1],gap="medium")
    with left:
        st.markdown("<div class='panel'><div class='panel-title'>Cash flow rhythm</div><div class='panel-sub'>Income and expenses by transaction date</div>",unsafe_allow_html=True)
        if not df.empty:
            chart=df.copy(); chart["Date"]=pd.to_datetime(chart["Date"]); chart=chart.groupby(["Date","Type"],as_index=False)["Amount"].sum(); chart["Amount"]=chart.apply(lambda r: abs(r.Amount),axis=1)
            fig=px.bar(chart,x="Date",y="Amount",color="Type",barmode="group",color_discrete_map={"Income":"#27A978","Expense":"#6D5AE6"})
            fig.update_layout(margin=dict(l=0,r=0,t=4,b=0),height=260,paper_bgcolor="white",plot_bgcolor="white",font=dict(family="DM Sans",color="#758198",size=11),legend=dict(orientation="h",y=1.15,x=0),xaxis=dict(showgrid=False,title=""),yaxis=dict(showgrid=True,gridcolor="#EDF0F6",title="₹"))
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
        st.markdown("</div>",unsafe_allow_html=True)
    with right:
        st.markdown("<div class='panel'><div class='panel-title'>Where your money goes</div><div class='panel-sub'>Expense mix by category</div>",unsafe_allow_html=True)
        cats=df[df.Amount<0].groupby("Category",as_index=False).Amount.sum(); cats["Amount"]=-cats["Amount"]
        if not cats.empty:
            fig2=px.pie(cats,names="Category",values="Amount",hole=.68,color_discrete_sequence=["#6D5AE6","#B8F4D5","#F2C66D","#F08C79","#92A5FF","#B9A7E8"])
            fig2.update_layout(margin=dict(l=0,r=0,t=0,b=0),height=240,paper_bgcolor="white",font=dict(family="DM Sans",color="#758198",size=11),legend=dict(orientation="h",y=-.1,x=0))
            st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})
        st.markdown("</div>",unsafe_allow_html=True)
    st.markdown("<div class='section-heading'>One small move for this week</div>",unsafe_allow_html=True)
    food=-float(df[(df.Category=="Food")&(df.Amount<0)].Amount.sum())
    save_goal=max(100,round(food*.15/10)*10)
    st.markdown(f"<div class='tip'>✦ &nbsp; <strong>Try a 15% food-spend reset.</strong> Your loaded food spending is {money(food)}. If you trim it by 15%, you could keep about <strong>{money(save_goal)}</strong> more. Treat this as a planning estimate, not a guarantee.</div>",unsafe_allow_html=True)
    st.markdown("<div class='section-heading'>Quick actions</div>",unsafe_allow_html=True)
    q1,q2,q3=st.columns(3)
    with q1:
        if st.button("⌁  Try a spending decision",use_container_width=True,type="primary"):
            st.session_state.page="Spend Simulator"; st.rerun()
    with q2:
        if st.button("◇  Check a suspicious message",use_container_width=True):
            st.session_state.page="Scam Shield"; st.rerun()
    with q3:
        if st.button("✳  Ask the money mentor",use_container_width=True):
            st.session_state.page="Money Mentor"; st.rerun()

elif st.session_state.page == "Spend Simulator":
    st.markdown("<div class='eyebrow'>FEATURE LAB · LIVE WHAT-IF TOOL</div><div class='section-heading' style='font-size:30px;margin-top:0'>Before you spend, run the what-if.</div><p style='color:#758198;margin-top:-6px'>A quick decision simulator for student budgets. Change one choice and see the monthly effect instantly.</p>",unsafe_allow_html=True)
    l,r=st.columns([1,1],gap="large")
    with l:
        st.markdown("<div class='panel'><div class='panel-title'>Build your scenario</div><div class='panel-sub'>Use your own estimate—no transaction is made.</div>",unsafe_allow_html=True)
        current_balance=st.number_input("Money available right now (₹)",min_value=0,value=max(0,int(net+2500)),step=100)
        purchase=st.number_input("Thing you're thinking of buying (₹)",min_value=0,value=799,step=50)
        frequency=st.slider("How often would you buy it this month?",1,20,1)
        daily_spend=st.number_input("Estimated daily essentials (₹)",min_value=0,value=180,step=10)
        days_left=st.slider("Days left until your next income",1,31,14)
        goal=st.number_input("Savings goal this month (₹)",min_value=0,value=2000,step=100)
        st.markdown("</div>",unsafe_allow_html=True)
    projected=current_balance-(purchase*frequency)-(daily_spend*days_left)
    with r:
        st.markdown("<div class='panel'><div class='panel-title'>Your decision, made visible</div><div class='panel-sub'>Illustrative projection from the values you entered</div>",unsafe_allow_html=True)
        colA,colB=st.columns(2)
        colA.metric("After planned purchase(s)",money(current_balance-purchase*frequency),delta=f"-{money(purchase*frequency)} purchase cost",delta_color="inverse")
        colB.metric("After essentials too",money(projected),delta="Estimated end-of-period balance")
        if projected<0: st.error(f"Your estimate is short by {money(abs(projected))}. Consider lowering the purchase or setting aside essentials first.")
        elif projected<goal: st.warning(f"You may finish below your {money(goal)} savings goal by {money(goal-projected)}. Could a smaller version of this purchase work?")
        else: st.success(f"Your estimate leaves room for essentials and your {money(goal)} goal—with {money(projected-goal)} to spare.")
        vals=[max(0,current_balance),max(0,current_balance-purchase*frequency),max(0,projected),goal]
        fig=go.Figure(go.Bar(x=["Available now","After purchase","After essentials","Savings goal"],y=vals,marker_color=[NAVY,PURPLE,"#27A978" if projected>=goal else "#E5A23E","#AAB4C8"]))
        fig.update_layout(height=250,margin=dict(l=0,r=0,t=10,b=0),paper_bgcolor="white",plot_bgcolor="white",font=dict(family="DM Sans",color="#758198",size=10),yaxis=dict(title="₹",gridcolor="#EDF0F6"),xaxis=dict(showgrid=False))
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
        st.markdown("<div class='tip'>💡 <strong>Decision rule:</strong> protect essentials first, then choose a savings amount, then spend what remains. A simulation is only as accurate as your estimates.</div>",unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)

elif st.session_state.page == "Scam Shield":
    st.markdown("<div class='eyebrow'>SAFETY LAB · RULE-BASED DEMO</div><div class='section-heading' style='font-size:30px;margin-top:0'>Pause. Check. Then pay.</div><p style='color:#758198;margin-top:-6px'>Paste a suspicious payment message or describe the request. This demo checks for common warning signs—it cannot verify a sender or transaction.</p>",unsafe_allow_html=True)
    left,right=st.columns([1.15,.85],gap="large")
    with left:
        st.markdown("<div class='panel'><div class='panel-title'>Inspect a message</div><div class='panel-sub'>Use a fake example—never share OTPs, PINs, passwords, or personal banking details.</div>",unsafe_allow_html=True)
        msg=st.text_area("Message or payment request",height=155,placeholder="Example: Your account will be blocked. Share your OTP now to receive a scholarship...")
        check=st.button("Scan for warning signs",type="primary",use_container_width=True)
        st.markdown("</div>",unsafe_allow_html=True)
    with right:
        st.markdown("<div class='panel'><div class='panel-title'>Red flags to watch for</div><div class='panel-sub'>Common scam patterns, not a definitive detection model</div><div style='display:flex;flex-direction:column;gap:12px'><div class='warning'>⚠️ <b>Urgency or threats</b><br/>“Account blocked”, “act now”, “last chance”</div><div class='warning'>⚠️ <b>Secret credentials</b><br/>Requests for OTP, UPI PIN, password, or screen sharing</div><div class='warning'>⚠️ <b>Unexpected reward</b><br/>Scholarship, refund, or prize you did not apply for</div><div class='warning'>⚠️ <b>Payment to receive money</b><br/>Being asked to pay or enter a PIN to accept funds</div></div></div>",unsafe_allow_html=True)
    if check:
        text=msg.lower()
        rules={"Urgency or threat words":["urgent","immediately","blocked","suspend","expire","last chance","act now"],"OTP / PIN / password request":["otp","upi pin","pin number","password","screen share","remote access"],"Unexpected reward / refund":["prize","won","reward","scholarship","refund","lottery","cashback"],"Suspicious payment language":["pay to receive","send money","processing fee","verify account","click link","claim now"]}
        hits=[name for name,words in rules.items() if any(w in text for w in words)]
        st.markdown("<div class='section-heading'>Scan result</div>",unsafe_allow_html=True)
        if not msg.strip(): st.info("Enter a message first, then scan it.")
        elif hits:
            st.error(f"{len(hits)} warning pattern group(s) found. Treat this message cautiously.")
            for h in hits: st.write("•",h)
            st.markdown("<div class='warning'><b>Safer next step:</b> Do not click links or share credentials. Open your bank or official service app directly, and verify through a known official contact.</div>",unsafe_allow_html=True)
        else: st.info("No listed warning patterns detected. That does not mean the message is safe—verify independently before acting.")

elif st.session_state.page == "Money Mentor":
    st.markdown("<div class='eyebrow'>MONEY MENTOR · GUIDED LEARNING</div><div class='section-heading' style='font-size:30px;margin-top:0'>No judgement. Just a clearer next step.</div><p style='color:#758198;margin-top:-6px'>Pick a topic and get a short, practical student-focused guide. This prototype uses curated rules, not a connected LLM.</p>",unsafe_allow_html=True)
    topic=st.selectbox("What would you like help with?",["I run out of money before month-end","How do I start saving?","How do I build credit readiness?","How can I spot a UPI scam?","How do I make a simple budget?"])
    language=st.selectbox("Guidance language",["English","ಕನ್ನಡ · Kannada","हिन्दी · Hindi"])
    answers={
    "I run out of money before month-end":("Find the leak, not the blame.",["List your fixed essentials first: rent/hostel, transport, food, data.","Set a weekly limit for flexible spending rather than one monthly guess.","Keep a small buffer before optional purchases.","Use Spend Simulator to test a purchase against days until your next income."]),
    "How do I start saving?":("Make saving small enough to repeat.",["Pick a realistic starter target—even ₹50–₹100 per week counts.","Move the amount aside when income arrives, if it is safe and practical.","Track progress weekly, not every hour.","Avoid borrowing or risky investments just to hit a savings target."]),
    "How do I build credit readiness?":("Build healthy habits before borrowing.",["Keep a record of regular income and essential expenses.","Pay any existing bills on time where possible.","Avoid taking loans only to create a credit history.","A habit score in this demo is not a lender's credit score or a guarantee of approval."]),
    "How can I spot a UPI scam?":("Never share secrets to receive money.",["Never share your UPI PIN or OTP with anyone.","Be suspicious of urgency, screen-sharing requests, or unexpected prizes.","Verify inside the official app rather than through a message link.","If money is lost, contact your bank and official cybercrime reporting channels promptly."]),
    "How do I make a simple budget?":("Give every rupee a job.",["Start with money you can reasonably expect this month.","Subtract essentials and fixed bills.","Choose a savings amount that does not put essentials at risk.","Divide the remaining flexible amount by the weeks left."])}
    title,steps=answers[topic]
    if language.startswith("ಕನ್ನಡ"):
        translations={"Find the leak, not the blame.":"ಖರ್ಚು ಎಲ್ಲಿ ಹೆಚ್ಚುತ್ತಿದೆ ಎಂದು ನೋಡಿ; ನಿಮ್ಮನ್ನು ದೂಷಿಸಬೇಡಿ.","Make saving small enough to repeat.":"ಮತ್ತೆ ಮತ್ತೆ ಮಾಡಬಹುದಾದಷ್ಟು ಸಣ್ಣ ಉಳಿತಾಯದಿಂದ ಪ್ರಾರಂಭಿಸಿ.","Build healthy habits before borrowing.":"ಸಾಲ ಪಡೆಯುವ ಮೊದಲು ಉತ್ತಮ ಹಣಕಾಸು ಅಭ್ಯಾಸಗಳನ್ನು ಬೆಳೆಸಿಕೊಳ್ಳಿ.","Never share secrets to receive money.":"ಹಣ ಸ್ವೀಕರಿಸಲು OTP ಅಥವಾ UPI PIN ಹಂಚಿಕೊಳ್ಳಬೇಡಿ.","Give every rupee a job.":"ಪ್ರತಿ ರೂಪಾಯಿಗೂ ಒಂದು ಉದ್ದೇಶ ನಿಗದಿಪಡಿಸಿ."}
        title=translations.get(title,title)
    elif language.startswith("हिन्दी"):
        translations={"Find the leak, not the blame.":"खर्च कहाँ बढ़ रहा है, यह समझें—खुद को दोष न दें।","Make saving small enough to repeat.":"छोटी बचत से शुरू करें जिसे आप नियमित रख सकें।","Build healthy habits before borrowing.":"उधार लेने से पहले अच्छी वित्तीय आदतें बनाएं।","Never share secrets to receive money.":"पैसे पाने के लिए OTP या UPI PIN कभी साझा न करें।","Give every rupee a job.":"हर रुपये का एक उद्देश्य तय करें।"}
        title=translations.get(title,title)
    st.markdown(f"<div class='hero' style='margin-top:20px'><div class='hero-pill'>✳ YOUR NEXT STEP</div><h1 style='font-size:28px'>{title}</h1><p>Simple, practical, and designed for student life.</p></div>",unsafe_allow_html=True)
    for i,step in enumerate(steps,1):
        st.markdown(f"<div class='panel' style='margin-bottom:10px;display:flex;align-items:center;gap:15px;padding:15px 18px'><div style='min-width:34px;height:34px;border-radius:11px;background:#EEF0FF;color:#5949C6;display:grid;place-items:center;font-weight:800'>{i:02}</div><div style='font-size:14px'>{step}</div></div>",unsafe_allow_html=True)
    st.caption("Educational guidance only—not personalised investment, lending, tax, or legal advice.")

elif st.session_state.page == "Transactions":
    st.markdown("<div class='eyebrow'>YOUR DATA · MANUAL & CSV</div><div class='section-heading' style='font-size:30px;margin-top:0'>Transactions, made tidy.</div><p style='color:#758198;margin-top:-6px'>Add a transaction, import a CSV, or export your demo ledger. Data stays in this running session.</p>",unsafe_allow_html=True)
    tab1,tab2,tab3=st.tabs(["＋ Add transaction","⇧ Import CSV","≋ Ledger"])
    with tab1:
        with st.form("add_tx",clear_on_submit=True):
            c1,c2=st.columns(2)
            txdate=c1.date_input("Date",value=date.today()); merchant=c2.text_input("Merchant / description",placeholder="e.g. Campus canteen")
            c3,c4,c5=st.columns(3)
            amount=c3.number_input("Amount (₹)",min_value=0.0,value=100.0,step=10.0); kind=c4.selectbox("Type",["Expense","Income"]); category=c5.selectbox("Category",["Auto-detect","Food","Transport","Education","Bills","Shopping","Health","Housing","Income","Entertainment","Other"])
            submitted=st.form_submit_button("Save transaction",type="primary")
            if submitted:
                if not merchant.strip(): st.error("Add a short description first.")
                else:
                    cat=categorize(merchant) if category=="Auto-detect" else category
                    signed=amount if kind=="Income" else -amount
                    new=pd.DataFrame([{"Date":txdate,"Merchant":merchant.strip(),"Category":cat,"Amount":signed,"Type":kind}])
                    st.session_state.transactions=pd.concat([st.session_state.transactions,new],ignore_index=True); st.success("Transaction added to this session."); st.rerun()
    with tab2:
        st.markdown("Upload a CSV with columns **Date, Merchant, Amount**. Positive amounts are income; negative amounts are expenses.")
        uploaded=st.file_uploader("Choose transaction CSV",type=["csv"])
        if uploaded:
            try:
                imp=pd.read_csv(uploaded); imp.columns=[x.strip().title() for x in imp.columns]
                if not {"Date","Merchant","Amount"}.issubset(imp.columns): st.error("CSV needs Date, Merchant and Amount columns.")
                else:
                    imp["Date"]=pd.to_datetime(imp["Date"],errors="coerce").dt.date
                    imp["Amount"]=pd.to_numeric(imp["Amount"],errors="coerce")
                    imp=imp.dropna(subset=["Date","Merchant","Amount"])
                    if "Category" not in imp: imp["Category"]=imp["Merchant"].astype(str).apply(categorize)
                    imp["Type"]=np.where(imp["Amount"]>=0,"Income","Expense")
                    st.dataframe(imp.head(10),use_container_width=True,hide_index=True)
                    if st.button("Import these rows",type="primary"):
                        st.session_state.transactions=pd.concat([st.session_state.transactions,imp[["Date","Merchant","Category","Amount","Type"]]],ignore_index=True); st.success(f"Imported {len(imp)} rows."); st.rerun()
            except Exception as e: st.error(f"Could not read CSV: {e}")
    with tab3:
        show=df.sort_values("Date",ascending=False)
        st.dataframe(show,use_container_width=True,hide_index=True,column_config={"Amount":st.column_config.NumberColumn("Amount (₹)",format="₹%.2f"),"Date":st.column_config.DateColumn("Date")})
        csv=show.to_csv(index=False).encode("utf-8")
        st.download_button("Download ledger CSV",csv,"studentsmart_transactions.csv","text/csv",type="primary")
        if st.button("Reset to sample transactions"):
            st.session_state.transactions=sample_data(); st.rerun()

st.markdown("<div style='border-top:1px solid #E4E8F0;margin-top:35px;padding-top:15px;color:#9AA4B7;font-size:11px;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap'><span>STUDENTSMART AI · HACKATHON PROTOTYPE</span><span>Explainable by design · No real payments · No bank connection</span></div>",unsafe_allow_html=True)
