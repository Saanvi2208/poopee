import streamlit as st
import requests

API_URL = "http://localhost:8000"  # Adjust backend URL as needed

TOILETS = [
    {"name": "Central Market Public Toilet", "area": "Fort District", "trust": 91, "condition": 90, "freshness": 92},
    {"name": "West Bazaar Restroom", "area": "Fort District", "trust": 84, "condition": 82, "freshness": 86},
    {"name": "Harbor View Facility", "area": "Fort District", "trust": 52, "condition": 48, "freshness": 56},
]

JOBS = [
    {"title": "Deep Clean & Sanitize", "place": "Central Market", "time": "2 hours", "pay": "₹450", "distance": "0.4 km", "tag": "Urgent"},
    {"title": "Water Tank Maintenance", "place": "Harbor View", "time": "4 hours", "pay": "₹800", "distance": "1.2 km", "tag": "Maintenance"},
]


def inject_css():
    st.markdown(
        """
        <style>
        .brand { font-family: sans-serif; margin-bottom: 20px; }
        .eyebrow { font-size: 11px; letter-spacing: 1px; color: #65758b; text-transform: uppercase; font-weight: 600; }
        .hero { background: #f8fafc; padding: 24px; border-radius: 12px; margin-bottom: 24px; border: 1px solid #e2e8f0; }
        .section { font-size: 20px; font-weight: 600; margin: 24px 0 12px 0; }
        .stat { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; text-align: center; }
        .stat .value { font-size: 28px; font-weight: 700; color: #0f172a; }
        .toilet { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; margin-bottom: 12px; }
        .notice { background: #fffbe6; border: 1px solid #ffe58f; padding: 12px; border-radius: 8px; margin-bottom: 16px; }
        .pill { background: #e0f2fe; color: #0369a1; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: 600; }
        .score.bad { color: #ef4444; }
        .score.warn { color: #f59e0b; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def toilet_card(t):
    st.markdown(
        f"""
        <div class="toilet">
            <div style="display:flex;justify-content:space-between;align-items:center">
                <div>
                    <h3 style="margin:0">{t["name"]}</h3>
                    <p style="color:#65758b;margin:0">{t["area"]}</p>
                </div>
                <div style="text-align:right">
                    <div style="font-size:24px;font-weight:700;color:#10a878">{t["trust"]}</div>
                    <small style="color:#65758b">Trust Score</small>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def auth_screen():
    st.markdown(
        """
        <div class="brand">
            <b style="font-size:22px;color:#0f172a">PooPee</b>
            <div style="color:#65758b;font-size:12px;margin-top:4px">The civic sanitation network</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown(
            """
            <div class="eyebrow">WELCOME TO POOPEE</div>
            <h1 style="font-size:42px">Trust, before you go.</h1>
            <p style="color:#65758b">Sign in to find cleaner public spaces, report issues, or connect with local sanitation work.</p>
            """,
            unsafe_allow_html=True,
        )
        email = st.text_input("Email", value="demo@poopee.city", key="login-email")
        password = st.text_input("Password", value="demo123", type="password", key="login-password")
        role = st.selectbox("I am joining as", ["Citizen", "Sanitation worker", "Facility manager"], key="login-role")

        if st.button("Enter PooPee", type="primary", use_container_width=True, key="login-submit"):
            api_role = {"Citizen": "citizen", "Sanitation worker": "worker", "Facility manager": "admin"}[role]
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
                st.session_state.page = "Home"
                st.rerun()
            except requests.RequestException:
                st.error("We could not reach PooPee right now. Please try again.")
        st.caption("Create your role-based demo account with any email and password")


def home():
    user_email = st.session_state.get("user", {}).get("email", "USER").split("@")[0].upper()
    st.markdown(
        f"""
        <div class="hero">
            <div class="eyebrow">GOOD MORNING, {user_email} · LIVE CITY VIEW</div>
            <h1>Know if you can trust it.</h1>
            <p>Public sanitation, made visible. Every score is built from condition, freshness, reports, and verified cleaning.</p>
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
    for c, (v, label) in zip(cols, stats):
        with c:
            st.markdown(
                f"""
                <div class="stat">
                    <div class="eyebrow">POOPEE LIVE</div>
                    <div class="value">{v}</div>
                    <div style="color:#65758b;font-size:13px">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="section">Nearest facilities <span style="font:500 13px DM Sans;color:#65758b">· Demo location: Fort District</span></div>',
        unsafe_allow_html=True,
    )
    left, right = st.columns([1.15, 1])
    with left:
        st.markdown(
            """
            <div style="background:#f1f5f9;height:240px;border-radius:12px;display:flex;align-items:center;justify-content:center;border:1px solid #cbd5e1;">
                <b style="color:#475569">FORT DISTRICT · 8 facilities nearby</b>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption("◉ Map markers show Trust Index · Location is simulated for this demo")
        if st.button("Find nearest toilet", type="primary", use_container_width=True, key="find-nearest"):
            st.session_state.selected = TOILETS[0]["name"]
            st.toast("Central Market is 450 m away · Trust 91")
    with right:
        for t in TOILETS[:2]:
            toilet_card(t)

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
    search = st.text_input("Search by place or area", placeholder="Try ‘market’ or ‘station’", key="toilet-search")
    visible = [t for t in TOILETS if search.lower() in (t["name"] + t["area"]).lower()]
    for t in visible:
        toilet_card(t)
        a, b, c = st.columns([1, 1, 2])
        with a:
            if st.button("View details", key=f"view-{t['name']}"):
                st.session_state.detail = t["name"]
        with b:
            if st.button("Navigate", key=f"nav-{t['name']}"):
                st.toast(f"Demo route to {t['name']} opened")
        with c:
            if st.button("Report issue", key=f"report-{t['name']}"):
                st.session_state.report_toilet = t["name"]
                st.session_state.page = "Report issue"
                st.rerun()

    if st.session_state.get("detail"):
        t = next(x for x in TOILETS if x["name"] == st.session_state.detail)
        st.markdown(
            f"""
            <div class="section">{t["name"]} · transparent score</div>
            <div class="stat">
                <b>Condition {t["condition"]}/100</b> &nbsp; 
                <b>Freshness {t["freshness"]}/100</b> &nbsp; 
                <b>Trust {t["trust"]}/100</b><br>
                <small style="color:#65758b">Trust = cleanliness 25% · water 20% · availability 15% · maintenance 15% · safety 10% · accessibility 5% · information freshness 10%</small>
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
    names = [t["name"] for t in TOILETS]
    toilet = st.selectbox(
        "Toilet",
        names,
        index=names.index(st.session_state.get("report_toilet", names[0])),
        key="report-toilet",
    )
    issue = st.selectbox(
        "Issue type",
        [
            "Dirty toilet",
            "No water",
            "Broken toilet",
            "Overflowing waste",
            "Bad smell",
            "No lighting",
            "Accessibility problem",
            "Toilet closed",
            "Other",
        ],
        key="report-issue",
    )
    image = st.file_uploader("Upload photo (optional)", type=["png", "jpg", "jpeg"], key="report-image")
    description = st.text_area("What did you notice?", placeholder="Add useful details for the response team", key="report-description")

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
                        <div style="font-size:24px;font-weight:700;color:#0f172a">{job["pay"]}</div>
                        <small style="color:#65758b">{job["distance"]} away</small>
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
    stats = [
        ("148", "monitored toilets", ""),
        ("19", "critical", "bad"),
        ("24", "active jobs", "warn"),
        ("96%", "completion rate", ""),
    ]
    for c, (v, label, tone) in zip(cols, stats):
        with c:
            st.markdown(
                f"""
                <div class="stat">
                    <div class="score {tone}" style="font-size:30px;font-weight:700">{v}</div>
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
        st.selectbox("Facility", [t["name"] for t in TOILETS], key="admin-facility")
        st.selectbox("Job type", ["Cleaning", "Maintenance", "Water inspection"], key="admin-type")
    with b:
        st.number_input("Payment (₹)", min_value=200, value=600, step=50, key="admin-payment")
        st.text_input("Start time", value="7:00 PM", key="admin-time")

    if st.button("Post job", type="primary", key="post-job"):
        st.success("Job posted · matched workers were notified")


def notifications_page():
    st.markdown(
        """
        <div class="eyebrow">UPDATES & ALERTS</div>
        <h1>Notifications</h1>
        <p style="color:#65758b">Stay informed about local sanitation updates, status shifts, and job responses.</p>
        """,
        unsafe_allow_html=True,
    )
    alerts = [
        {"time": "10 min ago", "title": "Shift Confirmed", "body": "Your application for Central Market Public Toilet cleaning was accepted."},
        {"time": "2 hours ago", "title": "Report Resolved", "body": "The reported water issue at Riverside Gate has been fixed by maintenance."},
        {"time": "1 day ago", "title": "Facility Status Alert", "body": "West Bazaar Public Toilet is temporarily closed for maintenance."},
    ]
    for alert in alerts:
        st.markdown(
            f"""
            <div class="toilet">
                <div style="display:flex;justify-content:space-between;align-items:center">
                    <h3 style="margin:0">{alert["title"]}</h3>
                    <small style="color:#65758b">{alert["time"]}</small>
                </div>
                <p style="color:#65758b;margin:8px 0 0">{alert["body"]}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def main():
    inject_css()

    if "user" not in st.session_state:
        auth_screen()
        return

    user_role = st.session_state.user.get("role", "Citizen")

    if user_role == "Facility manager":
        options = ["Home", "Command center", "Nearby toilets", "Notifications"]
    else:
        options = ["Home", "Nearby toilets", "Report issue", "Find work", "Notifications"]

    if "page" in st.session_state and st.session_state.page in options:
        st.session_state.nav = st.session_state.page
        del st.session_state.page

    with st.sidebar:
        st.markdown(
            """
            <div class="brand">
                <span style="font-size:20px">◉</span>
                <b style="font-size:20px">PooPee</b>
                <div style="color:#9db9b6;font-size:12px;margin-top:7px">Fort District · Live demo</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption(f"SIGNED IN AS {user_role.upper()}")

        page = st.radio("Navigation", options, key="nav")
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