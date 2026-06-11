import os
import datetime
import streamlit as st
from ml_engine import generate_response, VEHICLES

st.set_page_config(page_title="AutoMatch Chatbot", page_icon="🚗", layout="wide")

# ---------------------------------------------------------------------------
# Custom Gamer Tech Red & Black CSS Styling
# ---------------------------------------------------------------------------
GAMER_THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800;900&family=Share+Tech+Mono&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css');

/* Main App & Sidebar Gamified Styling */
html, body, .stApp, [class*="css"] {
    font-family: 'Share Tech Mono', 'Apple Color Emoji', 'Segoe UI Emoji', 'Noto Color Emoji', 'EmojiOne Color', monospace, sans-serif;
    background-color: #050507 !important;
    color: #E2E8F0 !important;
}

/* Page Entrance Animation */
@keyframes fadeInApp {
    from { opacity: 0; filter: blur(5px); }
    to { opacity: 1; filter: blur(0); }
}

.main .block-container {
    animation: fadeInApp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

/* Neon Red Title Header */
h1 {
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 900 !important;
    letter-spacing: 2px;
    background: linear-gradient(135deg, #FF0055 0%, #FF3366 50%, #FF1E27 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-transform: uppercase;
    text-shadow: 0 0 15px rgba(255, 0, 85, 0.4);
    animation: titleNeonPulse 2s ease-in-out infinite alternate;
}

@keyframes titleNeonPulse {
    0% { filter: drop-shadow(0 0 2px rgba(255, 0, 85, 0.2)); }
    100% { filter: drop-shadow(0 0 12px rgba(255, 0, 85, 0.6)); }
}

/* Chat Input Gaming Style */
div[data-testid="stChatInput"] {
    border: 2px solid #FF0055 !important;
    border-radius: 8px !important;
    background-color: #0D0D11 !important;
    box-shadow: 0 0 10px rgba(255, 0, 85, 0.15) !important;
    transition: all 0.3s ease !important;
}

div[data-testid="stChatInput"]:focus-within {
    border-color: #FF3366 !important;
    box-shadow: 0 0 20px rgba(255, 0, 85, 0.4) !important;
}

/* Chat Message styling as Cyber Terminal Cards */
@keyframes terminalSlide {
    from { opacity: 0; transform: translateX(-15px); }
    to { opacity: 1; transform: translateX(0); }
}

div[data-testid="stChatMessage"] {
    border-radius: 8px !important;
    border: 1px solid rgba(255, 0, 85, 0.15) !important;
    border-left: 5px solid #FF0055 !important;
    background-color: #0E0E12 !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5) !important;
    animation: terminalSlide 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

div[data-testid="stChatMessage"]:hover {
    border-color: #FF0055 !important;
    background-color: #121217 !important;
    box-shadow: 0 0 20px rgba(255, 0, 85, 0.25) !important;
    transform: translateY(-1px);
}

/* Gamer Sidebar styling */
section[data-testid="stSidebar"] {
    background-color: #050507 !important;
    border-right: 2px solid #FF0055 !important;
}

section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
    font-family: 'Orbitron', sans-serif !important;
    color: #FF0055 !important;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* Neo-Gamer Buttons (Black & Red neon transitions) */
div.stButton > button {
    background: #0E0E12 !important;
    border: 1px solid #FF0055 !important;
    border-radius: 6px !important;
    color: #FF0055 !important;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
}

div.stButton > button:hover {
    background: #FF0055 !important;
    border-color: transparent !important;
    color: #FFFFFF !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 0 20px rgba(255, 0, 85, 0.5) !important;
}

div.stButton > button:active {
    transform: translateY(0px) !important;
}

/* Laser-Scanned Vehicle Cards */
@keyframes laserScan {
    0% { top: 0%; opacity: 0; }
    10% { opacity: 1; }
    90% { opacity: 1; }
    100% { top: 100%; opacity: 0; }
}

.vehicle-card {
    position: relative;
    overflow: hidden;
    background: #0D0D11;
    border: 1px solid rgba(255, 0, 85, 0.2);
    border-left: 4px solid #FF0055;
    border-radius: 12px;
    padding: 16px;
    margin-top: 14px;
    margin-bottom: 14px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.vehicle-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg, transparent, #FF0055, transparent);
    animation: laserScan 2s linear infinite;
    pointer-events: none;
}

.vehicle-card:hover {
    transform: scale(1.01) translateY(-3px);
    border-color: #FF0055;
    box-shadow: 0 0 25px rgba(255, 0, 85, 0.35);
    background: #111116;
}

.vehicle-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.vehicle-name {
    margin: 0 !important;
    font-family: 'Orbitron', sans-serif !important;
    font-size: 1.25rem !important;
    font-weight: 800 !important;
    color: #FFFFFF !important;
    text-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
}

.vehicle-tag {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    color: #FF0055;
    background: rgba(255, 0, 85, 0.12);
    padding: 2px 8px;
    border-radius: 4px;
    border: 1px solid rgba(255, 0, 85, 0.25);
}

.vehicle-price {
    font-size: 1.05rem;
    font-weight: 600;
    color: #FF8E53;
    margin-bottom: 10px;
}

.pros-list, .cons-list {
    margin: 4px 0;
    font-size: 0.95rem;
    line-height: 1.4;
}

.pros-list { color: #00FF87; }
.cons-list { color: #FF3366; }

.pros-list i, .cons-list i {
    margin-right: 6px;
    width: 16px;
    text-align: center;
}

.icon-glow {
    filter: drop-shadow(0 0 4px currentColor);
}

/* Driving Track Gaming Animation */
.driving-track-container {
    background: rgba(255, 0, 85, 0.02);
    border: 1px solid rgba(255, 0, 85, 0.15);
    border-radius: 8px;
    padding: 8px;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
}

.scanner-text {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
    color: #FF0055;
    letter-spacing: 3px;
    margin-bottom: 4px;
    text-align: center;
    animation: scannerBlink 1s infinite alternate;
}

@keyframes scannerBlink {
    0% { opacity: 0.3; }
    100% { opacity: 1; text-shadow: 0 0 8px #FF0055; }
}

.driving-track {
    position: relative;
    width: 100%;
    height: 35px;
    background: repeating-linear-gradient(90deg, transparent, transparent 15px, rgba(255, 0, 85, 0.08) 15px, rgba(255, 0, 85, 0.08) 30px);
    border-bottom: 2px dashed #FF0055;
    overflow: hidden;
}

.driving-vehicle {
    position: absolute;
    bottom: -3px;
    font-size: 26px;
    animation: driveEngine 3.5s cubic-bezier(0.25, 0.8, 0.25, 1) infinite;
}

@keyframes driveEngine {
    0% { left: -50px; transform: scaleX(1); }
    40% { left: calc(50% - 13px); transform: scaleX(1); }
    50% { left: calc(50% - 13px); transform: scaleX(1) translateY(-3px); }
    60% { left: calc(50% - 13px); transform: scaleX(1) translateY(0); }
    100% { left: 100%; transform: scaleX(1); }
}

/* Comparison sheet table updates */
.ev-comparison-table {
    width: 100%;
    border-collapse: collapse;
    margin: 16px 0;
    border: 1px solid rgba(255, 0, 85, 0.15);
    border-radius: 6px;
    overflow: hidden;
}

.ev-comparison-table th {
    background: rgba(255, 0, 85, 0.15);
    color: #FF0055;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 700;
    padding: 10px;
    text-align: left;
    border-bottom: 2px solid #FF0055;
}

.ev-comparison-table td {
    padding: 10px;
    border-bottom: 1px solid rgba(255, 0, 85, 0.1);
    font-size: 0.95rem;
    background-color: #0E0E12;
}
</style>
"""
st.markdown(GAMER_THEME_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Session state defaults
# ---------------------------------------------------------------------------
for key, default in (
    ("messages", []),
    ("history", []),
):
    if key not in st.session_state:
        st.session_state[key] = default

# ---------------------------------------------------------------------------
# Sidebar – Configuration & Vehicle Type Preference
# ---------------------------------------------------------------------------
st.sidebar.markdown('<h2 style="font-family:Orbitron,sans-serif;color:#FF0055;text-transform:uppercase"><i class="fas fa-cog"></i> Configuration</h2>', unsafe_allow_html=True)

vehicle_pref = st.sidebar.radio(
    "Vehicle Preference",
    options=["🏍️ Two Wheeler", "🚗 Four Wheeler"],
    index=0
)

clean_pref = vehicle_pref.replace("🏍️ ", "").replace("🚗 ", "")

_GREETING_TW = (
    "Hello! I'm your AutoMatch **Two Wheeler** Advisor.\n\n"
    "💡 **Try asking:**\n"
    "- Scooter under ₹1 lakh\n"
    "- Best sports bike\n"
    "- EV vs Petrol comparison\n"
    "- Reliable daily commuter"
)
_GREETING_FW = (
    "Hello! I'm your AutoMatch **Four Wheeler** Advisor.\n\n"
    "💡 **Try asking:**\n"
    "- SUV under ₹15 lakh\n"
    "- Best hatchback\n"
    "- EV vs Petrol comparison\n"
    "- Family car with good safety"
)

greeting = _GREETING_TW if clean_pref == "Two Wheeler" else _GREETING_FW

if not st.session_state.messages:
    st.session_state.messages = [
        {"role": "assistant", "text": greeting}
    ]

if "prev_vehicle_pref" not in st.session_state:
    st.session_state.prev_vehicle_pref = clean_pref

if clean_pref != st.session_state.prev_vehicle_pref:
    st.session_state.prev_vehicle_pref = clean_pref
    has_user_msg = any(m["role"] == "user" for m in st.session_state.messages)
    if not has_user_msg:
        st.session_state.messages = [
            {"role": "assistant", "text": greeting}
        ]
        st.rerun()

# ---------------------------------------------------------------------------
# Sidebar – History Section
# ---------------------------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.markdown('<h3 style="font-family:Orbitron,sans-serif;color:#FF0055;text-transform:uppercase"><i class="fas fa-history"></i> Chat History</h3>', unsafe_allow_html=True)

if len(st.session_state.messages) > 1:
    if st.sidebar.button("💾 Save Chat to History", use_container_width=True):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        first_query = "Vehicle Inquiry"
        for m in st.session_state.messages:
            if m["role"] == "user":
                first_query = m["text"][:22] + "..."
                break
        st.session_state.history.append({
            "title": f"[{clean_pref}] {now} - {first_query}",
            "messages": list(st.session_state.messages),
            "pref": clean_pref
        })
        st.toast("Chat saved to history!")
        st.rerun()

if st.session_state.history:
    with st.sidebar.expander("📂 Saved Chats", expanded=True):
        for idx, session in enumerate(st.session_state.history):
            col_load, col_del = st.columns([5, 1])
            if col_load.button(session["title"], key=f"load_{idx}", use_container_width=True):
                st.session_state.messages = list(session["messages"])
                st.session_state.prev_vehicle_pref = session["pref"]
                st.rerun()
            if col_del.button("❌", key=f"del_{idx}"):
                st.session_state.history.pop(idx)
                st.rerun()
else:
    st.sidebar.caption("No saved chats yet. Click 'Save Chat to History' above when chatting to save.")

if len(st.session_state.messages) > 1:
    st.sidebar.markdown("---")
    if st.sidebar.button("🗑️ Clear Current Chat", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "text": _GREETING_TW if clean_pref == "Two Wheeler" else _GREETING_FW}]

# ---------------------------------------------------------------------------
# Interactive Gamer Track Animation (At the top of the chat area)
# ---------------------------------------------------------------------------
vehicle_icon = '<i class="fas fa-motorcycle"></i>' if clean_pref == "Two Wheeler" else '<i class="fas fa-car"></i>'
track_label = f"SYSTEM SCANNING: {clean_pref.upper()} INTERFACE"

st.markdown(
    f"""
    <div class="driving-track-container">
        <div class="scanner-text">{track_label}</div>
        <div class="driving-track">
            <div class="driving-vehicle">{vehicle_icon}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------------------------
# AI logic imported from ml_engine.py (generate_response, VEHICLES)
# ---------------------------------------------------------------------------
# Display chat history (always first in widget order)
# ---------------------------------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if "<div" in msg["text"] or "<table" in msg["text"]:
            st.markdown(msg["text"], unsafe_allow_html=True)
        else:
            st.markdown(msg["text"])

# ---------------------------------------------------------------------------
# Input handling (always last in widget order - fixed position)
# ---------------------------------------------------------------------------
user_input = st.chat_input("Ask for advice or tell me your budget and preferences...")

if user_input:
    output = generate_response(user_input, clean_pref)
    st.session_state.messages.append({"role": "user", "text": user_input})
    st.session_state.messages.append({"role": "assistant", "text": output})
    st.rerun()
