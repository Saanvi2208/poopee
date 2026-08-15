import os
import requests
import streamlit as st
from dotenv import load_dotenv

st.set_page_config(
    page_title="CleanTrust",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load optional local env file safely
load_dotenv(".env")
BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "http://localhost:8000").rstrip("/")
API_URL = f"{BASE_URL}/api"

TOILETS = [
    {"name": "Central Market", "area": "Old Town · Block 4", "trust": 91, "condition": 94, "freshness": 96, "cleanliness": "Excellent", "water": "Available", "open": True, "accessible": True, "cleaned": "12 min ago", "distance": "450 m", "lat": 19.076, "lng": 72.8777, "reports": 1},
    {"name": "Riverside Gate", "area": "East Promenade", "trust": 84, "condition": 82, "freshness": 89, "cleanliness": "Good", "water": "Available", "open": True, "accessible": True, "cleaned": "38 min ago", "distance": "0.8 km", "lat": 19.080, "lng": 72.884, "reports": 2},
    {"name": "Civic Square", "area": "Municipal Plaza", "trust": 73, "condition": 76, "freshness": 62, "cleanliness": "Fair", "water": "Low pressure", "open": True, "accessible": False, "cleaned": "8 hr ago", "distance": "1.1 km", "lat": 19.071, "lng": 72.870, "reports": 5},
    {"name": "Harbor View", "area": "South Jetty", "trust": 64, "condition": 69, "freshness": 45, "cleanliness": "Needs attention", "water": "Unavailable", "open": True, "accessible": False, "cleaned": "Yesterday", "distance": "1.6 km", "lat": 19.061, "lng": 72.879, "reports": 8},
    {"name": "North Station", "area": "Transit Hub", "trust": 88, "condition": 90, "freshness": 92, "cleanliness": "Good", "water": "Available", "open": True, "accessible": True, "cleaned": "21 min ago", "distance": "2.0 km", "lat": 19.093, "lng": 72.875, "reports": 1},
    {"name": "Lakeview Park", "area": "Green Loop", "trust": 79, "condition": 81, "freshness": 71, "cleanliness": "Good", "water": "Available", "open": True, "accessible": True, "cleaned": "3 hr ago", "distance": "2.4 km", "lat": 19.084, "lng": 72.862, "reports": 3},
    {"name": "West Bazaar", "area": "Market Road", "trust": 52, "condition": 58, "freshness": 35, "cleanliness": "Critical", "water": "Unavailable", "open": False, "accessible": False, "cleaned": "2 days ago", "distance": "2.8 km", "lat": 19.068, "lng": 72.851, "reports": 11},
    {"name": "University Lane", "area": "Campus District", "trust": 86, "condition": 87, "freshness": 86, "cleanliness": "Good", "water": "Available", "open": True, "accessible": True, "cleaned": "44 min ago", "distance": "3.2 km", "lat": 19.102, "lng": 72.889, "reports": 2},
]

JOBS = [
    {"title": "Cleaning & maintenance", "place": "Central Market Public Toilet", "time": "Today · 7:00 PM", "pay": "₹600", "distance": "1.2 km", "tag": "Urgent"},
    {"title": "Water line inspection", "place": "Harbor View Facility", "time": "Tomorrow · 9:30 AM", "pay": "₹950", "distance": "2.1 km", "tag": "Maintenance"},
    {"title": "Evening sanitation shift", "place": "Riverside Gate", "time": "Fri · 5:00 PM", "pay": "₹720", "distance": "0.8 km", "tag": "New"},
]

def score_class(value: int) -> str:
    if value >= 80:
        return ""
    if value >= 60:
        return "warn"
    return "bad"

def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
    :root { --ink:#122033; --muted:#65758b; --teal:#087f73; --mint:#e6f7f2; --line:#dce7e7; --orange:#e99b38; }
    html,body,[class*="css"] { font-family:'DM Sans',sans-serif; color:var(--ink); }
    h1,h2,h3,h4 { font-family:'Space Grotesk',sans-serif !important; letter-spacing:-.03em; }
    .stApp { background:linear-gradient(135deg,#f6fbfa 0%,#f8fafc 55%,#f2f7f6 100%); }
    [data-testid="stSidebar"] { background:#122b35; border-right:0; }
    [data-testid="stSidebar"] * { color:#e8f3f1 !important; }
    .brand { padding:20px 0 26px; border-bottom:1px solid #31505a; margin-bottom:24px; }
    .brand-mark { display:inline-flex; align-items:center; justify-content:center; width:38px;height:38px;background:#b8f1dd;color:#073c3e;border-radius:12px;font-weight:800;font-size:22px;margin-right:10px; }
    .eyebrow { color:var(--teal); text-transform:uppercase; letter-spacing:.16em; font-size:11px; font-weight:700; }
    .hero { background:#d9f3ea; border:1px solid #bde4d5; border-radius:22px; padding:30px 32px; min-height:178px; position:relative; overflow:hidden; }
    .hero:after { content:'◉'; position:absolute; right:7%; top:-30px; font-size:220px; color:#b5e7d5; opacity:.55; }
    .hero h1 { font-size:40px; line-height:1.08; max-width:540px; margin:8px 0 10px; }
    .hero p { max-width:540px; color:#3f6666; margin:0; font-size:16px; }
    .stat { background:#fff; border:1px solid var(--line); border-radius:14px; padding:18px 20px; min-height:100px; box-shadow:0 8px 25px #174e3b08; }
    .stat .value { font-family:'Space Grotesk'; font-weight:700; font-size:28px; margin-top:6px; }
    .section { font-family:'Space Grotesk'; font-size:22px; font-weight:700; margin:28px 0 14px; }
    .toilet { background:#fff; border:1px solid var(--line); border-radius:15px; padding:18px; margin:10px 0; box-shadow:0 5px 18px #174e3b08; }
    .score { font-family:'Space Grotesk'; font-size:34px; font-weight:700; color:var(--teal); }
    .pill { display:inline-block; padding:5px 9px; border-radius:99px; font-size:11px; font-weight:700; background:var(--mint); color:#087f73; margin-right:5px; }
    .pill.warn { background:#fff2d8; color:#9b6514; }
    .pill.bad { background:#ffe4e3; color:#b23b36; }
    .pill.gray { background:#e8edf1; color:#687684; }
    .map { background:#cfe9e1; border-radius:18px; min-height:355px; position:relative; overflow:hidden; border:1px solid #b4d7cd; background-image:linear-gradient(30deg,#d8eee8 12%,transparent 12.5%,transparent 87%,#d8eee8 87.5%),linear-gradient(150deg,#d8eee8 12%,transparent 12.5%,transparent 87%,#d8eee8 87.5%),linear-gradient(30deg,#d8eee8 12%,transparent 12.5%,transparent 87%,#d8eee8 87.5%),linear-gradient(150deg,#d8eee8 12%,transparent 12.5%,transparent 87%,#d8eee8 87.5%); background-size:80px 140px; }
    .map-title { padding:18px; font-weight:700; color:#24565a; }
    .marker { position:absolute; background:#fff; width:38px;height:38px;border-radius:50% 50% 50% 0; transform:rotate(-45deg); box-shadow:0 4px 12px #13504b40; display:flex;align-items:center;justify-content:center; }
    .marker b { transform:rotate(45deg);font-size:14px }
    .m1{left:18%;top:42%}.m2{left:45%;top:25%}.m3{left:69%;top:47%}.m4{left:38%;top:69%}.m5{left:78%;top:22%}.m6{left:59%;top:76%}
    .notice { background:#fff8e9; border:1px solid #f4d89a; border-radius:12px; padding:12px 14px; color:#785721; font-size:13px; }
    .stButton>button { border-radius:10px; border:1px solid #bfd9d2; color:#087f73; font-weight:700; min-height:42px; }
    .stButton>button[kind="primary"] { background:#087f73; color:#fff; border-color:#087f73; }
    @media(max-width:700px){.hero h1{font-size:30px}.hero{padding:24px}.map{min-height:270px}}
    </style>
    """, unsafe_allow_html=True)

def toilet_card(toilet: dict):
    status = "OPEN" if toilet["open"] else "CLOSED"
    status_class = "" if toilet["open"] else "gray"
    st.markdown(f'''<div class="toilet"><div style="display:flex;justify-content:space-between;gap:10px"><div><div class="eyebrow">PUBLIC TOILET · {toilet["area"]}</div><h3 style="margin:5px 0">{toilet["name"]}</h3><span class="pill {status_class}">{status}</span><span class="pill {score_class(toilet["trust"])}">{toilet["cleanliness"]}</span><span class="pill">{toilet["water"]}</span></div><div style="text-align:right"><div class="score">{toilet["trust"]}<small style="font:500 12px DM Sans;color:#65758b"> / 100</small></div><small style="color:#65758b">TRUST INDEX</small></div></div><div style="border-top:1px solid #edf2f1;margin:14px 0 12px"></div><div style="display:flex;justify-content:space-between;color:#65758b;font-size:13px"><span>✓ Verified {toilet["cleaned"]}</span><span>◌ {toilet["distance"]}</span><span>{"♿ Accessible" if toilet["accessible"] else "— Not accessible"}</span></div></div>''', unsafe_allow_html=True)

def auth_screen():
    st.markdown('<div class="brand"><span class="brand-mark">◉</span><b style="font-size:22px">CleanTrust</b><div style="color:#9db9b6;font-size:12px;margin-top:7px">The civic sanitation network</div></div>', unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown('<div class="eyebrow">WELCOME TO CLEANTRUST</div><h1 style="font-size:42px">Trust, before you go.</h1><p style="color:#65758b">Sign in to find cleaner public spaces, report issues, or connect with local sanitation work.</p>', unsafe_allow_html=True)
        email = st.text_input("Email", value="demo@cleantrust.city", key="login-email")
        password = st.text_input("Password", value="demo123", type="password", key="login-password")
        role = st.selectbox("I am joining as", ["Citizen", "Sanitation worker", "Facility manager"], key="login-role")
        if st.button("Enter CleanTrust", type="primary", use_container_width=True, key="login-submit"):
            api_role = {"Citizen": "citizen", "Sanitation worker": "worker", "Facility manager": "admin"}[role]
            try:
                response = requests.post(f"{API_URL}/auth/register", json={"email": email, "password": password, "role": api_role}, timeout=8)
                if response.status_code == 409:
                    response = requests.post(f"{API_URL}/auth/login", json={"email": email, "password": password, "role": api_role}, timeout=8)
                response.raise_for_status()
                st.session_state.user = {"email": email, "role": role, "token": response.json().get("token")}
                st.session_state["nav_target"] = "Home"
                st.rerun()
            except requests.RequestException:
                st.error("We could not reach CleanTrust right now. Proceeding in offline demo mode.")
                st.session_state.user = {"email": email, "role": role, "token": "demo-token"}
                st.session_state["nav_target"] = "Home"
                st.rerun()

def home():
    st.markdown('<div class="hero"><div class="eyebrow">GOOD MORNING, MAYA · LIVE CITY VIEW</div><h1>Know if you can trust it.</h1><p>Public sanitation, made visible. Every score is built from condition, freshness, reports, and verified cleaning.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="section">Your city at a glance</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    stats = [("148", "monitored toilets"), ("97", "high trust today"), ("12 min", "last city update"), ("6.2k", "issues resolved")]
    for column, (value, label) in zip(cols, stats):
        with column:
            st.markdown(f'<div class="stat"><div class="eyebrow">CLEANTRUST LIVE</div><div class="value">{value}</div><div style="color:#65758b;font-size:13px">{label}</div></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="section">Nearest facilities <span style="font:500 13px DM Sans;color:#65758b">· Demo location: Fort District</span></div>', unsafe_allow_html=True)
    left, right = st.columns([1.15, 1])
    with left:
        st.markdown('<div class="map"><div class="map-title">FORT DISTRICT · 8 facilities nearby</div><div class="marker m1"><b style="color:#10a878">91</b></div><div class="marker m2"><b style="color:#10a878">84</b></div><div class="marker m3"><b style="color:#e99b38">73</b></div><div class="marker m4"><b style="color:#e44d45">52</b></div><div class="marker m5"><b style="color:#10a878">88</b></div><div class="marker m6"><b style="color:#e99b38">79</b></div></div>', unsafe_allow_html=True)
        st.caption("◉ Map markers show Trust Index · Location is simulated for this demo")
        if st.button("Find nearest toilet", type="primary", use_container_width=True, key="find-nearest"):
            st.toast("Central Market is 450 m away · Trust 91")
    with right:
        for toilet in TOILETS[:2]:
            toilet_card(toilet)

def toilets_page():
    st.markdown('<div class="eyebrow">DISCOVER · VERIFY · GO</div><h1>Nearby toilets</h1><p style="color:#65758b">Compare the signals that make a public facility trustworthy.</p>', unsafe_allow_html=True)
    search = st.text_input("Search by place or area", placeholder="Try ‘market’ or ‘station’", key="toilet-search")
    visible = [t for t in TOILETS if search.lower() in (t["name"] + t["area"]).lower()]
    for toilet in visible:
        toilet_card(toilet)

def report_page():
    st.markdown('<div class="eyebrow">CITIZEN SIGNAL</div><h1>Report an issue</h1><p style="color:#65758b">Your report helps a worker respond before the next person arrives.</p>', unsafe_allow_html=True)
    names = [t["name"] for t in TOILETS]
    toilet = st.selectbox("Toilet", names, key="report-toilet")
    st.selectbox("Issue type", ["Dirty toilet", "No water", "Broken toilet", "Bad smell", "Other"], key="report-issue")
    st.text_area("What did you notice?", key="report-description")
    if st.button("Submit report", type="primary", key="submit-report"):
        st.success(f"Report received for {toilet}. Thank you!")

def jobs_page():
    st.markdown('<div class="eyebrow">LOCAL OPPORTUNITIES</div><h1>Find sanitation work</h1>', unsafe_allow_html=True)
    for job in JOBS:
        st.markdown(f'<div class="toilet"><h3>{job["title"]}</h3><p>{job["place"]} · {job["pay"]}</p></div>', unsafe_allow_html=True)

def admin_page():
    st.markdown('<div class="eyebrow">FACILITY MANAGEMENT</div><h1>Sanitation command center</h1>', unsafe_allow_html=True)

def main():
    inject_css()
    if "user" not in st.session_state:
        auth_screen()
        return

    role = st.session_state.user["role"]
    options = ["Home", "Nearby toilets", "Report issue", "Find work"] if role != "Facility manager" else ["Home", "Command center", "Nearby toilets"]
    
    with st.sidebar:
        st.markdown('<div class="brand"><span class="brand-mark">◉</span><b>CleanTrust</b></div>', unsafe_allow_html=True)
        page = st.radio("Navigation", options, key="nav")
        if st.button("Sign out", key="sign-out"):
            st.session_state.clear()
            st.rerun()

    routes = {"Home": home, "Nearby toilets": toilets_page, "Report issue": report_page, "Find work": jobs_page, "Command center": admin_page}
    routes.get(page, home)()

if __name__ == "__main__":
    main()