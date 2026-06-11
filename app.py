import os
import streamlit as st
import datetime
import re

st.set_page_config(page_title="AutoMatch Chatbot", page_icon="🚗", layout="centered")

# ---------------------------------------------------------------------------
# Custom Gamer Tech Red & Black CSS Styling
# ---------------------------------------------------------------------------
GAMER_THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800;900&family=Share+Tech+Mono&display=swap');

/* Main App & Sidebar Gamified Styling */
html, body, [class*="css"] {
    font-family: 'Share Tech Mono', monospace;
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
# Offline Vehicle Database
# ---------------------------------------------------------------------------
VEHICLES = {
    "Two Wheeler": [
        {
            "name": "Ola S1 Pro (EV)",
            "price": "₹1.40 Lakh",
            "budget_val": 1.4,
            "type": "EV Scooter",
            "pros": "Great range (195 km), loaded with tech features, fast acceleration.",
            "cons": "Panel gaps in some batches, software bugs occasionally."
        },
        {
            "name": "TVS Raider 125",
            "price": "₹95,000",
            "budget_val": 0.95,
            "type": "Commuter Bike",
            "pros": "Stylish design, excellent mileage (60+ kmpl), digital console.",
            "cons": "Rear tyre grip could be better, soft suspension for high speeds."
        },
        {
            "name": "Royal Enfield Classic 350",
            "price": "₹1.93 - ₹2.24 Lakh",
            "budget_val": 2.1,
            "type": "Cruiser Bike",
            "pros": "Timeless retro design, heavy thumping engine, very comfortable cruising.",
            "cons": "Heavy weight (195 kg), lacks modern features like LED headlamps."
        },
        {
            "name": "Yamaha R15 V4",
            "price": "₹1.82 Lakh",
            "budget_val": 1.82,
            "type": "Sports Bike",
            "pros": "Exceptional track handling, high-revving engine, premium looks.",
            "cons": "Aggressive committed riding posture (causes wrist pain in traffic)."
        },
        {
            "name": "Honda Activa 6G",
            "price": "₹76,000",
            "budget_val": 0.76,
            "type": "Scooter",
            "pros": "Highly reliable engine, solid metal body, great resale value.",
            "cons": "Telescopic suspension only in higher variants, outdated digital console."
        }
    ],
    "Four Wheeler": [
        {
            "name": "Tata Nexon",
            "price": "₹8.10 - ₹15.50 Lakh",
            "budget_val": 11.0,
            "type": "Compact SUV",
            "pros": "5-star Global NCAP safety rating, spacious cabin, comfortable ride.",
            "cons": "AMT transmission can feel jerky, infotainment UI feels slightly laggy."
        },
        {
            "name": "Maruti Suzuki Swift",
            "price": "₹6.49 - ₹9.64 Lakh",
            "budget_val": 8.0,
            "type": "Hatchback",
            "pros": "Extremely fuel-efficient (24+ kmpl), easy to drive in traffic, low maintenance.",
            "cons": "Build quality is lightweight, cabin noise at high speeds."
        },
        {
            "name": "Mahindra XUV700",
            "price": "₹13.99 - ₹26.99 Lakh",
            "budget_val": 20.0,
            "type": "Mid-size SUV",
            "pros": "Powerful petrol/diesel engines, ADAS safety tech, premium dual-screen setup.",
            "cons": "Long waiting periods, heavy footprint in tight city parking."
        },
        {
            "name": "Hyundai Creta",
            "price": "₹11.00 - ₹20.15 Lakh",
            "budget_val": 15.0,
            "type": "SUV",
            "pros": "Feature loaded (panoramic sunroof, ventilated seats), smooth ride quality.",
            "cons": "Polarizing exterior design, safety rating is average compared to Tata."
        },
        {
            "name": "Tata Tiago EV",
            "price": "₹7.99 - ₹11.89 Lakh",
            "budget_val": 9.5,
            "type": "EV Hatchback",
            "pros": "Most affordable full-size EV, silent cabin, low running cost.",
            "cons": "Real-world range is around 180-200 km (less than advertised 250-315 km)."
        }
    ]
}

# ---------------------------------------------------------------------------
# Session state defaults
# ---------------------------------------------------------------------------
for key, default in (
    ("messages", []),
    ("history", []),
    ("quick_pick", ""),
):
    if key not in st.session_state:
        st.session_state[key] = default

# ---------------------------------------------------------------------------
# Sidebar – Configuration & Vehicle Type Preference
# ---------------------------------------------------------------------------
st.sidebar.header("🔧 Configuration")

vehicle_pref = st.sidebar.radio(
    "Vehicle Preference",
    options=["🏍️ Two Wheeler", "🚗 Four Wheeler"],
    index=0
)

clean_pref = vehicle_pref.replace("🏍️ ", "").replace("🚗 ", "")

_GREETING = (
    f"Hello! I'm your AutoMatch {clean_pref} Advisor. What kind of vehicle are you looking "
    f"to buy today, and what is your budget?"
)

if not st.session_state.messages:
    st.session_state.messages = [
        {"role": "assistant", "text": _GREETING}
    ]

if "prev_vehicle_pref" not in st.session_state:
    st.session_state.prev_vehicle_pref = clean_pref

if clean_pref != st.session_state.prev_vehicle_pref:
    st.session_state.prev_vehicle_pref = clean_pref
    has_user_msg = any(m["role"] == "user" for m in st.session_state.messages)
    if not has_user_msg:
        st.session_state.messages = [
            {"role": "assistant", "text": _GREETING}
        ]
        st.rerun()

# ---------------------------------------------------------------------------
# Sidebar – History Section
# ---------------------------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("📜 Chat History")

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
        st.session_state.messages = [{"role": "assistant", "text": _GREETING}]
        st.session_state.quick_pick = ""
        st.rerun()

# ---------------------------------------------------------------------------
# Interactive Gamer Track Animation (At the top of the chat area)
# ---------------------------------------------------------------------------
vehicle_emoji = "🏍️" if clean_pref == "Two Wheeler" else "🚗"
track_label = f"SYSTEM SCANNING: {clean_pref.upper()} INTERFACE"

st.markdown(
    f"""
    <div class="driving-track-container">
        <div class="scanner-text">{track_label}</div>
        <div class="driving-track">
            <div class="driving-vehicle">{vehicle_emoji}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------------------------
# Offline AI Matchmaking Logic (Generates Laser-Scanned Cards)
# ---------------------------------------------------------------------------
def generate_response(user_input, pref):
    text = user_input.lower()
    
    if text.strip() in ("hi", "hello", "hey", "hola", "greetings"):
        return f"Hello! How can I help you find the perfect {pref} today? Tell me your budget or preferences."
        
    if any(kw in text for kw in ("ev vs", "versus", "comparison", "petrol vs", "electric vs")):
        return (
            "### 💰 EV vs Petrol Comparison\n\n"
            "<table class='ev-comparison-table'>"
            "<tr><th>Feature</th><th>EV (Electric Vehicle)</th><th>Petrol Vehicle</th></tr>"
            "<tr><td><b>Initial Cost</b></td><td>Higher upfront purchase price</td><td>Lower initial cost</td></tr>"
            "<tr><td><b>Running Cost</b></td><td>Extremely low (~₹0.5 - ₹1 per km)</td><td>Higher (~₹6 - ₹9 per km)</td></tr>"
            "<tr><td><b>Maintenance</b></td><td>Minimal (no engine oil, fewer parts)</td><td>Regular servicing (filters, plugs, oil)</td></tr>"
            "<tr><td><b>Convenience</b></td><td>Needs regular charging</td><td>Refuel in 2 mins anywhere</td></tr>"
            "</table>"
            "**Recommendation:** Buy an **EV** if your daily run is >40 km inside the city. Choose **Petrol** if you do frequent long highway runs."
        )

    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", text)
    budget = None
    if numbers:
        try:
            budget = float(numbers[0])
            if budget > 1000:
                budget = budget / 100000.0
        except ValueError:
            pass

    candidates = VEHICLES[pref]
    matched = []
    
    if budget:
        for v in candidates:
            if v["budget_val"] <= budget * 1.25:
                matched.append(v)
        matched.sort(key=lambda x: abs(x["budget_val"] - budget))
    
    filtered_by_type = []
    for keyword in ("ev", "suv", "scooter", "bike", "hatchback", "cruiser"):
        if keyword in text:
            target_list = matched if matched else candidates
            filtered_by_type = [v for v in target_list if keyword in v["type"].lower() or keyword in v["name"].lower()]
            break
            
    if filtered_by_type:
        matched = filtered_by_type

    if not matched:
        matched = candidates[:3]

    res = f"### 🚗 AutoMatch Advisor Recommendations ({pref})\n\n"
    if budget:
        res += f"Here are the best options matching your budget of **~₹{budget:.2f} Lakh**:\n\n"
    elif filtered_by_type:
        res += "Here are the best options matching your preference:\n\n"
    else:
        res += "Here are our top recommended options for you:\n\n"

    for v in matched:
        res += f"""
        <div class="vehicle-card">
            <div class="vehicle-header">
                <h4 class="vehicle-name">{v['name']}</h4>
                <span class="vehicle-tag">{v['type']}</span>
            </div>
            <div class="vehicle-price">Estimated Price: <b>{v['price']}</b></div>
            <div class="pros-list"><b>✅ PROS:</b> {v['pros']}</div>
            <div class="cons-list"><b>❌ CONS:</b> {v['cons']}</div>
        </div>
        """

    res += "\n\n---\n"
    res += "*Would you like to adjust your budget, or get details on a specific model listed above?*"
    return res

# ---------------------------------------------------------------------------
# Quick-action suggestion chips (before any user message)
# ---------------------------------------------------------------------------
has_user_msg = any(m["role"] == "user" for m in st.session_state.messages)

if not has_user_msg:
    st.markdown("**Quick start – tap a suggestion:**")
    cols = st.columns(3)
    if clean_pref == "Two Wheeler":
        suggestions = [
            "🏍️ Best 2-wheeler under ₹1.5L",
            "🛵 Reliable daily scooter",
            "💰 EV vs Petrol comparison",
        ]
    else:
        suggestions = [
            "🚗 Family SUV for ₹10-15L",
            "⚡ EV options under ₹10L",
            "💰 EV vs Petrol comparison",
        ]
        
    for col, suggestion in zip(cols, suggestions):
        if col.button(suggestion, use_container_width=True):
            st.session_state.quick_pick = suggestion
            st.rerun()

# ---------------------------------------------------------------------------
# Display chat history
# ---------------------------------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if "<div" in msg["text"] or "<table" in msg["text"]:
            st.markdown(msg["text"], unsafe_allow_html=True)
        else:
            st.markdown(msg["text"])

# ---------------------------------------------------------------------------
# Input handling
# ---------------------------------------------------------------------------
user_input = None

if st.session_state.quick_pick:
    user_input = st.session_state.quick_pick
    st.session_state.quick_pick = ""

if user_input is None:
    user_input = st.chat_input("Ask for advice or tell me your budget and preferences...")

if user_input:
    st.session_state.messages.append({"role": "user", "text": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing recommendations..."):
            output = generate_response(user_input, clean_pref)
            if "<div" in output or "<table" in output:
                st.markdown(output, unsafe_allow_html=True)
            else:
                st.markdown(output)
            st.session_state.messages.append(
                {"role": "assistant", "text": output}
            )
            st.rerun()
