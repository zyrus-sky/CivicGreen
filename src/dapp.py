import streamlit as st
import pandas as pd
import datetime
from PIL import Image


st.set_page_config(page_title="CivicGreen Municipal Dashboard", layout="wide")

st.markdown("""
    <style>
    body {
        background-color: #0d0d0d;
        color: #ffffff;
        font-family: 'Segoe UI', sans-serif;
        overflow-x: hidden;
    }
    section[data-testid="stSidebar"] {
        background-color: #0d0d0d;
        border-right: 1px solid #1a1a1a;
    }
    /* Neon Cards with Hover Glow and Fade-in */
    .card {
        background: linear-gradient(145deg,#1a1a1a,#0d0d0d);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 0 15px #a855f7;
        text-align: center;
        margin: 10px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: fadeIn 1.2s ease;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 0 25px #a855f7;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #22c55e;
        animation: pulseGlow 2s infinite;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #aaa;
    }
    /* Blinking + Pulsing Flag */
    .flagged {
        color: red;
        font-weight: bold;
        animation: blinkPulse 1.2s infinite;
        text-shadow: 0 0 5px red, 0 0 10px red;
    }
    @keyframes blinkPulse {
        0% { opacity: 1; text-shadow: 0 0 5px red, 0 0 10px red; }
        50% { opacity: 0.4; text-shadow: 0 0 20px red, 0 0 30px red; }
        100% { opacity: 1; text-shadow: 0 0 5px red, 0 0 10px red; }
    }
    /* Metric Pulse Glow */
    @keyframes pulseGlow {
        0% { text-shadow: 0 0 5px #22c55e, 0 0 10px #22c55e; }
        50% { text-shadow: 0 0 20px #22c55e, 0 0 40px #22c55e; }
        100% { text-shadow: 0 0 5px #22c55e, 0 0 10px #22c55e; }
    }
    /* Fade-in Animation for Table Rows */
    table tr {
        animation: fadeIn 0.8s ease-in;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(5px); }
        to { opacity: 1; transform: translateY(0); }
    }
    /* Neon Buttons with Hover Scale */
    div.stButton > button {
        background: linear-gradient(145deg,#a855f7,#6d28d9);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease-in-out;
    }
    div.stButton > button:hover {
        background: linear-gradient(145deg,#6d28d9,#a855f7);
        box-shadow: 0 0 20px #a855f7;
        transform: scale(1.05);
    }
    /* Hover Effect for Table Cells */
    .dataframe td:hover {
        background-color: #2a2a2a !important;
        color: #a855f7 !important;
        transition: 0.3s ease;
    }
    /* Purple Neon Cursor Glow */
    #cursor-glow {
        position: fixed;
        top: 0;
        left: 0;
        width: 150px;
        height: 150px;
        pointer-events: none;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(168,85,247,0.4) 0%, rgba(168,85,247,0) 70%);
        filter: blur(50px);
        transform: translate(-50%, -50%);
        z-index: 9999;
        mix-blend-mode: screen;
    }
    </style>

    <div id="cursor-glow"></div>

    <script>
    const glow = document.getElementById('cursor-glow');
    document.addEventListener('mousemove', e => {
        glow.style.top = e.clientY + 'px';
        glow.style.left = e.clientX + 'px';
    });
    </script>
""", unsafe_allow_html=True)

if "municipalities" not in st.session_state:
    st.session_state.municipalities = {
        "City A": {"points": 450, "spent": 120, "status": "Safe", "flagged": False},
        "City B": {"points": 320, "spent": 50,  "status": "Alert", "flagged": False},
        "City C": {"points": 150, "spent": 10,  "status": "Flagged", "flagged": True},
        "City D": {"points": 900, "spent": 300, "status": "Safe", "flagged": False},
    }

if "transaction_history" not in st.session_state:
    st.session_state.transaction_history = [
        {"date": "2025-07-01", "city": "City A", "action": "Clean Market Street", "points": +20},
        {"date": "2025-07-05", "city": "City B", "action": "Flagged Unclean Dump", "points": -15},
        {"date": "2025-07-10", "city": "City A", "action": "Redeemed: Streetlights", "points": -50},
    ]

municipalities = st.session_state.municipalities
transaction_history = st.session_state.transaction_history

today = datetime.date(2025, 8, 2)
season_start = datetime.date(2025, 7, 1)
mid_season_check = season_start + datetime.timedelta(days=60)
season_end = season_start + datetime.timedelta(days=90)

def calculate_tier(points):
    if points >= 800: return 5
    elif points >= 600: return 4
    elif points >= 400: return 3
    elif points >= 200: return 2
    return 1

def log_transaction(city, action, points):
    transaction_history.append({
        "date": today.isoformat(),
        "city": city,
        "action": action,
        "points": points
    })

def auto_flagging():
    for city, data in municipalities.items():
        tier = calculate_tier(data["points"])
        if tier < 3 and today >= mid_season_check:
            data["flagged"] = True
            data["status"] = "Flagged"
        elif tier >= 3:
            data["flagged"] = False
            data["status"] = "Safe"

st.sidebar.title("🌱 CivicGreen")
page = st.sidebar.radio("Navigation", ["Dashboard", "Municipal Actions", "Redeem Points", "History & Analytics", "Admin/Settings"])


if page == "Dashboard":
    st.markdown("## 🌍 Municipal Tier Dashboard")
    auto_flagging()

    col1, col2, col3, col4 = st.columns(4)
    total_points = sum([data["points"] for data in municipalities.values()])
    flagged_count = sum([1 for data in municipalities.values() if data["flagged"]])
    days_to_mid = (mid_season_check - today).days
    days_to_end = (season_end - today).days

    with col1:
        st.markdown(f'<div class="card"><div class="metric-value">{total_points}</div><div class="metric-label">Total Points</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="card"><div class="metric-value">{flagged_count}</div><div class="metric-label">Flagged Municipalities</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="card"><div class="metric-value">{days_to_mid}</div><div class="metric-label">Days to Mid-Season Check</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="card"><div class="metric-value">{days_to_end}</div><div class="metric-label">Days to Season Reset</div></div>', unsafe_allow_html=True)

    st.markdown("### 🏆 Tier Leaderboard")
    leaderboard_data = []
    for city, data in municipalities.items():
        tier = calculate_tier(data["points"])
        status_display = f'<span class="flagged">🚨 {data["status"]}</span>' if data["flagged"] else data["status"]
        leaderboard_data.append([city, f"Tier {tier}", data["points"], data["spent"], status_display])
    df_leaderboard = pd.DataFrame(leaderboard_data, columns=["Municipality", "Tier", "Points", "Spent", "Status"])
    st.markdown(df_leaderboard.to_html(escape=False, index=False), unsafe_allow_html=True)

elif page == "Municipal Actions":
    st.markdown("## 🏗 Municipal Actions & AI Verification")
    city = st.selectbox("Select Your Municipality", list(municipalities.keys()))
    uploaded_file = st.file_uploader("Upload a waste site image", type=["jpg","png","jpeg"])
    action = st.selectbox("Select Action Type", ["Cleaned Area (+20)", "Collected Recyclables (+20)", "Removed Illegal Dump (-15)"])

    if st.button("Submit Action"):
        points = -15 if "Removed" in action else 20
        municipalities[city]["points"] += points
        log_transaction(city, action, points)
        st.success(f"✅ {city}: {action} | Points Change: {points:+d}")

    st.markdown("### Recent Actions")
    st.dataframe(pd.DataFrame(transaction_history).tail(5))

elif page == "Redeem Points":
    st.markdown("## 🎁 Redeem Points for Community Benefits")
    city = st.selectbox("Select Your Municipality", list(municipalities.keys()))
    rewards = {"💡 Streetlights (50 pts)": 50, "🗑 Recycling Bins (100 pts)": 100, "🍲 Food Drive (200 pts)": 200}
    reward_choice = st.radio("Choose a Reward", list(rewards.keys()))
    if st.button("Redeem"):
        cost = rewards[reward_choice]
        if municipalities[city]["points"] >= cost:
            municipalities[city]["points"] -= cost
            municipalities[city]["spent"] += cost
            log_transaction(city, f"Redeemed: {reward_choice}", -cost)
            st.success(f"🎉 {reward_choice} redeemed for {city}!")
        else:
            st.error("Not enough points to redeem.")


elif page == "History & Analytics":
    st.markdown("## 📜 Points & Tier History")
    df = pd.DataFrame(transaction_history)
    st.dataframe(df)

    st.markdown("### 📈 Points Trend")
    city_filter = st.selectbox("Filter by City", ["All"] + list(municipalities.keys()))
    df_plot = df if city_filter == "All" else df[df["city"] == city_filter]
    df_plot["cumulative"] = df_plot["points"].cumsum()
    st.line_chart(df_plot.set_index("date")["cumulative"])


elif page == "Admin/Settings":
    st.markdown("## ⚙️ Admin Controls & Flagging System")
    auto_flagging()
    for city, data in municipalities.items():
        tier = calculate_tier(data["points"])
        status = "🚨 Flagged" if data["flagged"] else "✅ Safe"
        st.write(f"**{city}** - Tier {tier} - {status}")

        if data["flagged"]:
            st.markdown(f"**Mock Social Post:** _'{city} has failed to maintain cleanliness and is now under government watch.'_")

    if st.button("Simulate Season Reset"):
        for city in municipalities:
            municipalities[city]["points"] = 0
            municipalities[city]["spent"] = 0
            municipalities[city]["flagged"] = False
            municipalities[city]["status"] = "Safe"
        transaction_history.clear()
        st.success("Season reset! All points cleared, new cycle started.")
