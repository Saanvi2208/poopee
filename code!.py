import os
import requests
import streamlit as st
from dotenv import load_dotenv

# --- CONFIG & ENVIRONMENT ---
st.set_page_config(
    page_title="CleanTrust",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_dotenv("/app/frontend/.env")
BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "http://localhost:8000").rstrip("/")
API_URL = f"{BASE_URL}/api"

# --- DATASETS ---
TOILETS = [
    {
        "name": "Central Market",
        "area": "Old Town · Block 4",
        "trust": 91,
        "condition": 94,
        "freshness": 96,
        "cleanliness": "Excellent",
        "water": "Available",
        "open": True,
        "accessible": True,
        "cleaned": "12 min ago",
        "distance": "450 m",
        "lat": 19.076,
        "lng": 72.8777,
        "reports": 1,
    },
    {
        "name": "Riverside Gate",
        "area": "East Promenade",
        "trust": 84,
        "condition": 82,
        "freshness": 89,
        "cleanliness": "Good",
        "water": "Available",
        "open": True,
        "accessible": True,
        "cleaned": "38 min ago",
        "distance": "0.8 km",
        "lat": 19.080,
        "lng": 72.884,
        "reports": 2,
    },
    {
        "name": "Civic Square",
        "area": "Municipal Plaza",
        "trust": 73,
        "condition": 76,
        "freshness": 62,
        "cleanliness": "Fair",
        "water": "Low pressure",
        "open": True,
        "accessible": False,
        "cleaned": "8 hr ago",
        "distance": "1.1 km",
        "lat": 19.071,
        "lng": 72.870,
        "reports": 5,
    },
    {
        "name": "Harbor View",
        "area": "South Jetty",
        "trust": 64,
        "condition": 69,
        "freshness": 45,
        "cleanliness": "Needs attention",
        "water": "Unavailable",
        "open": True,
        "accessible": False,
        "cleaned": "Yesterday",
        "distance": "1.6 km",
        "lat": 19.061,
        "lng": 72.879,
        "reports": 8,
    },
    {
        "name": "North Station",
        "area": "Transit Hub",
        "trust": 88,
        "condition": 90,
        "freshness": 92,
        "cleanliness": "Good",
        "water": "Available",
        "open": True,
        "accessible": True,
        "cleaned": "21 min ago",
        "distance": "2.0 km",
        "lat": 19.093,
        "lng": 72.875,
        "reports": 1,
    },
    {
        "name": "Lakeview Park",
        "area": "Green Loop",
        "trust": 79,
        "condition": 81,
        "freshness": 71,
        "cleanliness": "Good",
        "water": "Available",
        "open": True,
        "accessible": True,
        "cleaned": "3 hr ago",
        "distance": "2.4 km",
        "lat": 19.084,
        "lng": 72.862,
        "reports": 3,
    },
    {
        "name": "West Bazaar",
        "area": "Market Road",
        "trust": 52,
        "condition": 58,
        "freshness": 35,
        "cleanliness": "Critical",
        "water": "Unavailable",
        "open": False,
        "accessible": False,
        "cleaned": "2 days ago",
        "distance": "2.8 km",
        "lat": 19.068,
        "lng": 72.851,
        "reports": 11,
    },
    {
        "name": "University Lane",
        "area": "Campus District",
        "trust": 86,
        "condition": 87,
        "freshness": 86,
        "cleanliness": "Good",
        "water": "Available",
        "open": True,
        "accessible": True,
        "cleaned": "44 min ago",
        "distance": "3.2 km",
        "lat": 19.102,
        "lng": 72.889,
        "reports": 2,
    },
]

JOBS = [
    {
        "title": "Cleaning & maintenance",
        "place": "Central Market Public Toilet",
        "time": "Today · 7:00 PM",
        "pay": "₹600",
        "distance": "1.2 km",
        "tag": "Urgent",
    },
    {
        "title": "Water line inspection",
        "place": "Harbor View Facility",
        "time": "Tomorrow · 9:30 AM",
        "pay": "₹950",
        "distance": "2.1 km",
        "tag": "Maintenance",
    },
    {
        "title": "Evening sanitation shift",
        "place": "Riverside Gate",
        "time": "Fri · 5:00 PM",
        "pay": "₹720",
        "distance": "0.8 km",
        "tag": "New",
    },
]


# --- HELPERS ---
def score_class(value: int) -> str:
    if value >= 80:
        return ""
    if value >= 60:
        return "warn"
    return "bad"


# --- STYLING ---
def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

        :root {
            --ink: #122033;
            --muted: #65758b;
            --teal: #087f73;
            --mint: #e6f7f2;
            --line: #dce7e7;
            --orange: #e99b38;
        }

        html, body, [class*="css"] {
            font-family: "DM Sans", sans-serif;
            color: var(--ink);
        }

        h1, h2, h3, h4 {
            font-family: "Space Grotesk", sans-serif !important;
            letter-spacing: -0.03em;
        }

        .stApp {
            background: linear-gradient(135deg, #f6fbfa 0%, #f8fafc 55%, #f2f7f6 100%);
        }

        [data-testid="stSidebar"] {
            background: #122b35;
            border-right: 0;
        }

        [data-testid="stSidebar"] * {
            color: #e8f3f1 !important;
        }

        .brand {
            padding: 20px 0 26px;
            border-bottom: 1px solid #31505a;
            margin-bottom: 24px;
        }

        .brand-mark {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 38px;
            height: 38px;
            background: #b8f1dd;
            color: #073c3e;
            border-radius: 12px;
            font-weight: 800;
            font-size: 22px;
            margin-right: 10px;
        }

        .eyebrow {
            color: var(--teal);
            text-transform: uppercase;
            letter-spacing: 0.16em;
            font-size: 11px;
            font-weight: 700;
        }

        .hero {
            background: #d9f3ea;
            border: 1px solid #bde4d5;
            border-radius: 22px;
            padding: 30px 32px;
            min-height: 178px;
            position: relative;
            overflow: hidden;
        }

        .hero:after {
            content: "◉";
            position: absolute;
            right: 7%;
            top: -30px;
            font-size: 220px;
            color: #b5e7d5;
            opacity: 0.55;
        }

        .hero h1 {
            font-size: 40px;
            line-height: 1.08;
            max-width: 540px;
            margin: 8px 0 10px;
        }

        .hero p {
            max-width: 540px;
            color: #3f6666;
            margin: 0;
            font-size: 16px;
        }

        .stat {
            background: #ffffff;
            border: 1px solid var(--line);
            border-radius: 14px;
            padding: 18px 20px;
            min-height: 100px;
            box-shadow: 0 8px 25px #174e3b08;
        }

        .stat .value {
            font-family: "Space Grotesk";
            font-weight: 700;
            font-size: 28px;
            margin-top: 6px;
        }

        .section {
            font-family: "Space Grotesk";
            font-size: 22px;
            font-weight: 700;
            margin: 28px 0 14px;
        }

        .toilet {
            background: #ffffff;
            border: 1px solid var(--line);
            border-radius: 15px;
            padding: 18px;
            margin: 10px 0;
            box-shadow: 0 5px 18px #174e3b08;
        }

        .score {
            font-family: "Space Grotesk";
            font-size: 34px;
            font-weight: 700;
            color: var(--teal);
        }

        .pill {
            display: inline-block;
            padding: 5px 9px;
            border-radius: 99px;
            font-size: 11px;
            font-weight: 700;
            background: var(--mint);
            color: #087f73;
            margin-right: 5px;
        }

        .pill.warn { background: #fff2d8; color: #9b6514; }
        .pill.bad { background: #ffe4e3; color: #b23b36; }
        .pill.gray { background: #e8edf1; color: #687684; }

        .map {
            background: #cfe9e1;
            border-radius: 18px;
            min-height: 355px;
            position: relative;
            overflow: hidden;
            border: 1px solid #b4d7cd;
            background-image:
                linear-gradient(30deg, #d8eee8 12%, transparent 12.5%, transparent 87%, #d8eee8 87.5%),
                linear-gradient(150deg, #d8eee8 12%, transparent 12.5%, transparent 87%, #d8eee8 87.5%),
                linear-gradient(30deg, #d8eee8 12%, transparent 12.5%, transparent 87%, #d8eee8 87.5%),
                linear-gradient(150deg, #d8eee8 12%, transparent 12.5%, transparent 87%, #d8eee8 87.5%);
            background-size: 80px 140px;
        }

        .map-title {
            padding: 18px;
            font-weight: 700;
            color: #24565a;
        }

        .marker {
            position: absolute;
            background: #ffffff;
            width: 38px;
            height: 38px;
            border-radius: 50% 50% 50% 0;
            transform: rotate(-45deg);
            box-shadow: 0 4px 12px #13504b40;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .marker b {
            transform: rotate(45deg);
            font-size: 14px;
        }

        .m1 { left: 18%; top: 42%; }
        .m2 { left: 45%; top: 25%; }
        .m3 { left: 69%; top: 47%; }
        .m4 { left: 38%; top: 69%; }
        .m5 { left: 78%; top: 22%; }
        .m6 { left: 59%; top: 76%; }

        .notice {
            background: #fff8e9;
            border: 1px solid #f4d89a;
            border-radius: 12px;
            padding: 12px 14px;
            color: #785721;
            font-size: 13px;
        }

        .stButton > button {
            border-radius: 10px;
            border: 1px solid #bfd9d2;
            color: #087f73;
            font-weight: 700;
            min-height: 42px;
        }

        .stButton > button[kind="primary"] {
            background: #087f73;
            color: #ffffff;
            border-color: #087f73;
        }

        @media (max-width: 700px) {
            .hero h1 { font-size: 30px; }
            .hero { padding: 24px; }
            .map { min-height: 270px; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# --- UI COMPONENTS ---
def toilet_card(toilet: dict):
    status = "OPEN" if toilet["open"] else "CLOSED"
    status_class = "" if toilet["open"] else "gray"

    st.markdown(
        f"""
        <div class="toilet">
            <div style="display:flex;justify-content:space-between;gap:10px">
                <div>
                    <div class="eyebrow">PUBLIC TOILET · {toilet["area"]}</div>
                    <h3 style="margin:5px 0">{toilet["name"]}</h3>
                    <span class="pill {status_class}">{status}</span>
                    <span class="pill {score_class(toilet["trust"])}">{toilet["cleanliness"]}</span>
                    <span class="pill">{toilet["water"]}</span>
                </div>
                <div style="text-align:right">
                    <div class="score">
                        {toilet["trust"]}
                        <small style="font:500 12px DM Sans;color:#65758b">/ 100</small>
                    </div>
                    <small style="color:#65758b">TRUST INDEX</small>
                </div>
            </div>
            <div style="border-top:1px solid #edf2f1;margin:14px 0 12px"></div>
            <div style="display:flex;justify-content:space-between;color:#65758b;font-size:13px">
                <span>✓ Verified {toilet["cleaned"]}</span>
                <span>◌ {toilet["distance"]}</span>
                <span>{" Accessible" if toilet["accessible"] else "— Not accessible"}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# --- PAGE VIEWS ---
def auth_screen():
    st.markdown(
        """
        <div class="brand">
            <span class="brand-mark">◉</span>
            <b style="font-size:22px">CleanTrust</b>
            <div style="color:#9db9b6;font-size:12px;margin-top:7px">The civic sanitation network</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, col, _ = st.columns([1, 1.2, 1])

    with col:
        st.markdown(
            """
            <div class="eyebrow">WELCOME TO CLEANTRUST</div>
            <h1 style="font-size:42px">Trust, before you go.</h1>
            <p style="color:#65758b">
                Sign in to find cleaner public spaces, report issues, or connect with local sanitation work.
            </p>
            """,
            unsafe_allow_html=True,
        )

        email = st.text_input("Email", value="demo@cleantrust.city", key="login-email")
        password = st.text_input("Password", value="demo123", type="password", key="login-password")
        role = st.selectbox(
            "I am joining as",
            ["Citizen", "Sanitation worker", "Facility manager"],
            key="login-role",
        )

        if st.button("Enter CleanTrust", type="primary", use_container_width=True, key="login-submit"):
            api_role = {
                "Citizen": "citizen",
                "Sanitation worker": "worker",
                "Facility manager": "admin",
            }[role]

            try:
                response = requests.post(
                    f"{API_URL}/auth/register",
                    json={"email": email, "password": password, "role": api_role},
                    timeout=8,
                )

                if response.status_code == 409:
                    response = requests.post(
                        f"{API_URL}/auth/login",
                        json={"email": email, "password": password, "role": api_role},
                        timeout=8,
                    )

                response.raise_for_status()

                st.session_state.user = {
                    "email": email,
                    "role": role,
                    "token": response.json().get("token"),
                }
                st.session_state["nav_target"] = "Home"
                st.rerun()

            except requests.RequestException:
                st.error("We could not reach CleanTrust right now. Please try again.")

        st.caption("Create your role-based demo account with any email and password")


def home():
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">GOOD MORNING, MAYA · LIVE CITY VIEW</div>
            <h1>Know if you can trust it.</h1>
            <p>
                Public sanitation, made visible. Every score is built from condition, freshness, reports, and verified cleaning.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section">Your city at a glance</div>', unsafe_allow_html=True)

    cols = st.columns(4)
    stats = [
        ("148", "monitored toilets"),
        ("97", "high trust today"),
        ("12 min", "last city update"),
        ("6.2k", "issues resolved"),
    ]

    for column, (value, label) in zip(cols, stats):
        with column:
            st.markdown(
                f"""
                <div class="stat">
                    <div class="eyebrow">CLEANTRUST LIVE</div>
                    <div class="value">{value}</div>
                    <div style="color:#65758b;font-size:13px">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        """
        <div class="section">
            Nearest facilities
            <span style="font:500 13px DM Sans;color:#65758b">· Demo location: Fort District</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.15, 1])

    with left:
        st.markdown(
            """
            <div class="map">
                <div class="map-title">FORT DISTRICT · 8 facilities nearby</div>
                <div class="marker m1"><b style="color:#10a878">91</b></div>
                <div class="marker m2"><b style="color:#10a878">84</b></div>
                <div class="marker m3"><b style="color:#e99b38">73</b></div>
                <div class="marker m4"><b style="color:#e44d45">52</b></div>
                <div class="marker m5"><b style="color:#10a878">88</b></div>
                <div class="marker m6"><b style="color:#e99b38">79</b></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.caption("◉ Map markers show Trust Index · Location is simulated for this demo")

        if st.button("Find nearest toilet", type="primary", use_container_width=True, key="find-nearest"):
            st.session_state.selected = TOILETS[0]["name"]
            st.toast("Central Market is 450 m away · Trust 91")

    with right:
        for toilet in TOILETS[:2]:
            toilet_card(toilet)

    st.markdown('<div class="section">What needs attention</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="notice">
            <b>2 reports need a response</b><br>
            Harbor View has 8 recent reports, including no water. A maintenance shift is available nearby.
        </div>
        """,
        unsafe_allow_html=True,
    )


def toilets_page():
    st.markdown(
        """
        <div class="eyebrow">DISCOVER · VERIFY · GO</div>
        <h1>Nearby toilets</h1>
        <p style="color:#65758b">Compare the signals that make a public facility trustworthy.</p>
        """,
        unsafe_allow_html=True,
    )

    search = st.text_input(
        "Search by place or area",
        placeholder="Try ‘market’ or ‘station’",
        key="toilet-search",
    )

    visible = [
        toilet for toilet in TOILETS
        if search.lower() in (toilet["name"] + toilet["area"]).lower()
    ]

    for toilet in visible:
        toilet_card(toilet)
        a, b, c = st.columns([1, 1, 2])

        with a:
            if st.button("View details", key=f"view-{toilet['name']}"):
                st.session_state.detail = toilet["name"]

        with b:
            if st.button("Navigate", key=f"nav-btn-{toilet['name']}"):
                st.toast(f"Demo route to {toilet['name']} opened")

        with c:
            if st.button("Report issue", key=f"report-{toilet['name']}"):
                st.session_state.report_toilet = toilet["name"]
                st.session_state["nav_target"] = "Report issue"
                st.rerun()

    if st.session_state.get("detail"):
        toilet = next((item for item in TOILETS if item["name"] == st.session_state.detail), TOILETS[0])
        st.markdown(
            f"""
            <div class="section">{toilet["name"]} · transparent score</div>
            <div class="stat">
                <b>Condition {toilet["condition"]}/100</b> &nbsp;
                <b>Freshness {toilet["freshness"]}/100</b> &nbsp;
                <b>Trust {toilet["trust"]}/100</b>
                <br>
                <small style="color:#65758b">
                    Trust = cleanliness 25% · water 20% · availability 15% · maintenance 15% · safety 10% · accessibility 5% · information freshness 10%
                </small>
            </div>
            """,
            unsafe_allow_html=True,
        )


def report_page():
    st.markdown(
        """
        <div class="eyebrow">CITIZEN SIGNAL</div>
        <h1>Report an issue</h1>
        <p style="color:#65758b">Your report helps a worker respond before the next person arrives.</p>
        """,
        unsafe_allow_html=True,
    )

    names = [toilet["name"] for toilet in TOILETS]
    selected_toilet = st.session_state.get("report_toilet", names[0])
    toilet_index = names.index(selected_toilet) if selected_toilet in names else 0

    toilet = st.selectbox("Toilet", names, index=toilet_index, key="report-toilet")
    st.selectbox(
        "Issue type",
        [
            "Dirty toilet", "No water", "Broken toilet", "Overflowing waste",
            "Bad smell", "No lighting", "Accessibility problem", "Toilet closed", "Other"
        ],
        key="report-issue",
    )

    image = st.file_uploader("Upload photo (optional)", type=["png", "jpg", "jpeg"], key="report-image")
    st.text_area(
        "What did you notice?",
        placeholder="Add useful details for the response team",
        key="report-description",
    )

    if image:
        st.info("AI-assisted analysis · Possible cleanliness issue detected. Human verification recommended.")

    if st.button("Submit report", type="primary", key="submit-report"):
        st.session_state.report_submitted = True
        st.session_state.report_count = st.session_state.get("report_count", 0) + 1
        st.success(f"Report received for {toilet}. A response team has been notified.")


def jobs_page():
    st.markdown(
        """
        <div class="eyebrow">LOCAL OPPORTUNITIES</div>
        <h1>Find sanitation work</h1>
        <p style="color:#65758b">Fair, nearby work that keeps public spaces running.</p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="notice">
            <b>Worker profile strength: 86%</b> · Add availability to get matched with more shifts
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section">Recommended near you</div>', unsafe_allow_html=True)

    for job in JOBS:
        st.markdown(
            f"""
            <div class="toilet">
                <div style="display:flex;justify-content:space-between">
                    <div>
                        <span class="pill">{job["tag"]}</span>
                        <h3>{job["title"]}</h3>
                        <p style="color:#65758b;margin:0">{job["place"]} · {job["time"]}</p>
                    </div>
                    <div style="text-align:right">
                        <div class="score" style="font-size:27px;color:#122033">{job["pay"]}</div>
                        <small>{job["distance"]} away</small>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Apply for this job", key=f"apply-{job['title']}"):
            st.success("Application sent. The facility manager will review your profile.")


def admin_page():
    st.markdown(
        """
        <div class="eyebrow">FACILITY MANAGEMENT</div>
        <h1>Sanitation command center</h1>
        <p style="color:#65758b">A live operating view for a cleaner Fort District.</p>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(4)
    admin_stats = [
        ("148", "monitored toilets", ""),
        ("19", "critical", "bad"),
        ("24", "active jobs", "warn"),
        ("96%", "completion rate", ""),
    ]

    for column, (value, label, tone) in zip(cols, admin_stats):
        with column:
            st.markdown(
                f"""
                <div class="stat">
                    <div class="score {tone}" style="font-size:30px">{value}</div>
                    <div style="color:#65758b;font-size:13px">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<div class="section">Today’s response queue</div>', unsafe_allow_html=True)
    st.dataframe(
        {
            "Priority": ["Critical", "High", "Medium", "High"],
            "Facility": ["Harbor View", "West Bazaar", "Civic Square", "Central Market"],
            "Signal": ["No water · 8 reports", "Closed · 11 reports", "Low pressure", "Cleanliness report"],
            "Status": ["Job available", "Assigned", "Monitoring", "New"],
        },
        use_container_width=True,
        hide_index=True,
    )

    st.markdown('<div class="section">Post a sanitation job</div>', unsafe_allow_html=True)
    a, b = st.columns(2)

    with a:
        st.selectbox("Facility", [toilet["name"] for toilet in TOILETS], key="admin-facility")
        st.selectbox("Job type", ["Cleaning", "Maintenance", "Water inspection"], key="admin-type")

    with b:
        st.number_input("Payment (₹)", min_value=200, value=600, step=50, key="admin-payment")
        st.text_input("Start time", value="7:00 PM", key="admin-time")

    if st.button("Post job", type="primary", key="post-job"):
        st.success("Job posted · matched workers were notified")


def notifications_page():
    st.markdown(
        """
        <div class="eyebrow">UPDATES THAT MATTER</div>
        <h1>Notifications</h1>
        """,
        unsafe_allow_html=True,
    )

    notifications = [
        ("Report received", "Your sanitation report for Central Market is now in the response queue."),
        ("New work nearby", "A cleaning shift opened 0.8 km away."),
        ("Trust improved", "Riverside Gate moved to 84 after a verified cleaning."),
    ]

    for title, text in notifications:
        st.markdown(
            f"""
            <div class="toilet">
                <b>{title}</b>
                <p style="color:#65758b;margin:5px 0 0">{text}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# --- MAIN APP ENTRYPOINT ---
def main():
    inject_css()

    if "user" not in st.session_state:
        auth_screen()
        return

    role = st.session_state.user["role"]

    options = (
        ["Home", "Nearby toilets", "Report issue", "Find work", "Notifications"]
        if role != "Facility manager"
        else ["Home", "Command center", "Nearby toilets", "Notifications"]
    )

    # Handle navigation redirection via state safely
    if "nav_target" in st.session_state:
        target = st.session_state.pop("nav_target")
        if target in options:
            st.session_state["nav"] = target

    with st.sidebar:
        st.markdown(
            """
            <div class="brand">
                <span class="brand-mark">◉</span>
                <b style="font-size:20px">CleanTrust</b>
                <div style="color:#9db9b6;font-size:12px;margin-top:7px">Fort District · Live demo</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.caption(f"SIGNED IN AS {role.upper()}")

        # Ensure index defaults cleanly if state target was passed
        current_index = 0
        if "nav" in st.session_state and st.session_state["nav"] in options:
            current_index = options.index(st.session_state["nav"])

        page = st.radio("Navigation", options, index=current_index, key="nav")
        st.divider()

        st.markdown(
            """
            **Impact so far**

            2,840 jobs completed

            ₹8.4L wages facilitated
            """
        )

        if st.button("Sign out", key="sign-out"):
            st.session_state.clear()
            st.rerun()

    # View Router
    routes = {
        "Home": home,
        "Nearby toilets": toilets_page,
        "Report issue": report_page,
        "Find work": jobs_page,
        "Command center": admin_page,
        "Notifications": notifications_page,
    }

    routes.get(page, home)()


if __name__ == "__main__":
    main()