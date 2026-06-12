import os
import datetime
import streamlit as st
from ml_engine import generate_response, VEHICLES, get_greeting, TRANSLATIONS, is_ollama_available

st.set_page_config(page_title="AutoMatch AI Advisor", page_icon="🚗", layout="wide")

LANG_OPTIONS = {"English": "en", "हिन्दी (Hindi)": "hi", "తెలుగు (Telugu)": "te"}

GAMER_THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800;900&family=Share+Tech+Mono&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css');

html, body, .stApp, [class*="css"] {
    font-family: 'Share Tech Mono', 'Apple Color Emoji', 'Segoe UI Emoji', 'Noto Color Emoji', 'EmojiOne Color', monospace, sans-serif;
    background-color: #050507 !important;
    color: #E2E8F0 !important;
}

@keyframes fadeInApp {
    from { opacity: 0; filter: blur(5px); }
    to { opacity: 1; filter: blur(0); }
}

.main .block-container {
    animation: fadeInApp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

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

for key, default in (
    ("messages", []),
    ("history", []),
    ("lang", "en"),
    ("user_info", {}),
    ("user_registered", False),
    ("ai_mode", "rule"),
):
    if key not in st.session_state:
        st.session_state[key] = default

st.sidebar.markdown('<h2 style="font-family:Orbitron,sans-serif;color:#FF0055;text-transform:uppercase"><i class="fas fa-cog"></i> Configuration</h2>', unsafe_allow_html=True)

selected_lang_display = st.sidebar.selectbox(
    "Language / भाषा / భాష",
    options=list(LANG_OPTIONS.keys()),
    index=0
)
selected_lang = LANG_OPTIONS[selected_lang_display]

if selected_lang != st.session_state.get("lang"):
    st.session_state.lang = selected_lang
    if not any(m["role"] == "user" for m in st.session_state.messages):
        greeting = get_greeting(
            "Two Wheeler" if st.session_state.get("prev_vehicle_pref", "Two Wheeler") == "Two Wheeler" else "Four Wheeler",
            selected_lang
        )
        st.session_state.messages = [{"role": "assistant", "text": greeting}]
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown(f'<h3 style="font-family:Orbitron,sans-serif;color:#FF0055;text-transform:uppercase"><i class="fas fa-microchip"></i> AI Engine</h3>', unsafe_allow_html=True)

ollama_status = is_ollama_available()
ollama_label = "Ollama: Connected" if ollama_status else "Ollama: Not Connected"
st.sidebar.caption(f"{'🟢' if ollama_status else '🔴'} {ollama_label}")

ai_options = ["⚡ Quick (Rule-based)", "🤖 AI (Ollama)"]
ai_mode_labels = ["rule", "ollama"]
if not ollama_status and len(ai_options) > 1:
    ai_options = ["⚡ Quick (Rule-based)"]
    ai_mode_labels = ["rule"]

selected_ai = st.sidebar.radio(
    "Response Mode" if selected_lang == "en" else ("प्रतिक्रिया मोड" if selected_lang == "hi" else "ప్రతిస్పందన మోడ్"),
    options=ai_options,
    index=0
)
selected_ai_mode = ai_mode_labels[ai_options.index(selected_ai)] if selected_ai in ai_options else "rule"
st.session_state.ai_mode = selected_ai_mode

st.sidebar.markdown("---")
st.sidebar.markdown(f'<h3 style="font-family:Orbitron,sans-serif;color:#FF0055;text-transform:uppercase"><i class="fas fa-user"></i> User Registration</h3>', unsafe_allow_html=True)

if not st.session_state.user_registered:
    with st.sidebar.form("user_registration_form"):
        name = st.text_input("Full Name" if selected_lang == "en" else ("पूरा नाम" if selected_lang == "hi" else "పూర్తి పేరు"))
        phone = st.text_input("Phone Number" if selected_lang == "en" else ("फ़ोन नंबर" if selected_lang == "hi" else "ఫోన్ నంబర్"))
        vehicle_type = st.selectbox(
            "Vehicle Type" if selected_lang == "en" else ("वाहन प्रकार" if selected_lang == "hi" else "వాహనం రకం"),
            options=["Two Wheeler", "Four Wheeler"]
        )
        fuel_type = st.selectbox(
            "Fuel Type" if selected_lang == "en" else ("ईंधन प्रकार" if selected_lang == "hi" else "ఇంధన రకం"),
            options=["Petrol", "Diesel", "Electric", "Hybrid"]
        )
        submitted = st.form_submit_button(
            "Register" if selected_lang == "en" else ("पंजीकरण करें" if selected_lang == "hi" else "నమోదు చేయండి"),
            use_container_width=True
        )
        if submitted and name and phone:
            st.session_state.user_info = {
                "name": name,
                "phone": phone,
                "vehicle_type": vehicle_type,
                "fuel_type": fuel_type,
            }
            st.session_state.user_registered = True
            if selected_lang == "hi":
                msg = f"स्वागत है, {name}! आपका फ़ोन नंबर {phone} दर्ज कर लिया गया है। आप {vehicle_type} और {fuel_type} में रुचि रखते हैं। मैं आपकी कैसे मदद कर सकता हूँ?"
            elif selected_lang == "te":
                msg = f"స్వాగతం, {name}! మీ ఫోన్ నంబర్ {phone} నమోదు చేయబడింది. మీరు {vehicle_type} మరియు {fuel_type} పై ఆసక్తి కలిగి ఉన్నారు. నేను మీకు ఎలా సహాయం చేయగలను?"
            else:
                msg = f"Welcome, {name}! Your phone number {phone} is registered. You're interested in {vehicle_type} with {fuel_type}. How can I help you today?"
            st.session_state.messages.append({"role": "assistant", "text": msg})
            st.rerun()
        elif submitted:
            if selected_lang == "hi":
                st.error("कृपया नाम और फ़ोन नंबर भरें")
            elif selected_lang == "te":
                st.error("దయచేసి పేరు మరియు ఫోన్ నంబర్ నింపండి")
            else:
                st.error("Please fill in Name and Phone Number")
else:
    info = st.session_state.user_info
    lang_text = {"en": "Registered User", "hi": "पंजीकृत उपयोगकर्ता", "te": "నమోదిత వినియోగదారు"}
    st.sidebar.success(f"**{lang_text[selected_lang]}**")
    st.sidebar.write(f"👤 {info.get('name', '')}")
    st.sidebar.write(f"📞 {info.get('phone', '')}")
    st.sidebar.write(f"🚗 {info.get('vehicle_type', '')}")
    st.sidebar.write(f"⛽ {info.get('fuel_type', '')}")
    if st.sidebar.button(
        "Edit Info" if selected_lang == "en" else ("जानकारी संपादित करें" if selected_lang == "hi" else "సమాచారాన్ని సవరించండి"),
        use_container_width=True
    ):
        st.session_state.user_registered = False
        st.rerun()

st.sidebar.markdown("---")

vehicle_pref = st.sidebar.radio(
    "Vehicle Preference" if selected_lang == "en" else ("वाहन प्राथमिकता" if selected_lang == "hi" else "వాహన ప్రాధాన్యత"),
    options=["🏍️ Two Wheeler", "🚗 Four Wheeler"],
    index=0
)

clean_pref = vehicle_pref.replace("🏍️ ", "").replace("🚗 ", "")

greeting = get_greeting(clean_pref, selected_lang)

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

st.sidebar.markdown("---")
st.sidebar.markdown(f'<h3 style="font-family:Orbitron,sans-serif;color:#FF0055;text-transform:uppercase"><i class="fas fa-history"></i> Chat History</h3>', unsafe_allow_html=True)

if len(st.session_state.messages) > 1:
    save_text = "Save Chat to History" if selected_lang == "en" else ("चैट इतिहास में सहेजें" if selected_lang == "hi" else "చాట్ ను చరిత్రలో సేవ్ చేయండి")
    if st.sidebar.button(f"💾 {save_text}", use_container_width=True):
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
        st.toast("Chat saved to history!" if selected_lang == "en" else ("चैट सहेजा गया!" if selected_lang == "hi" else "చాట్ సేవ్ చేయబడింది!"))
        st.rerun()

if st.session_state.history:
    with st.sidebar.expander("Saved Chats" if selected_lang == "en" else ("सहेजे गए चैट" if selected_lang == "hi" else "సేవ్ చేసిన చాట్‌లు"), expanded=True):
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
    no_chats_text = "No saved chats yet." if selected_lang == "en" else ("अभी तक कोई सहेजा गया चैट नहीं है।" if selected_lang == "hi" else "ఇంకా సేవ్ చేసిన చాట్‌లు లేవు.")
    st.sidebar.caption(no_chats_text)

if len(st.session_state.messages) > 1:
    st.sidebar.markdown("---")
    clear_text = "Clear Current Chat" if selected_lang == "en" else ("वर्तमान चैट साफ़ करें" if selected_lang == "hi" else "ప్రస్తుత చాట్‌ను క్లియర్ చేయండి")
    if st.sidebar.button(f"🗑️ {clear_text}", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "text": get_greeting(clean_pref, selected_lang)}]
        st.rerun()

vehicle_icon = '<i class="fas fa-motorcycle"></i>' if clean_pref == "Two Wheeler" else '<i class="fas fa-car"></i>'
system_label = "SYSTEM SCANNING"
if selected_lang == "hi":
    system_label = "सिस्टम स्कैन कर रहा है"
elif selected_lang == "te":
    system_label = "సిస్టమ్ స్కాన్ చేస్తోంది"
track_label = f"{system_label}: {clean_pref.upper()} INTERFACE"

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

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if "<div" in msg["text"] or "<table" in msg["text"]:
            st.markdown(msg["text"], unsafe_allow_html=True)
        else:
            st.markdown(msg["text"])

user_input = st.chat_input("Ask for advice or tell me your budget and preferences...")

if user_input:
    user_info = st.session_state.get("user_info")
    ai_mode = st.session_state.get("ai_mode", "rule")
    if ai_mode == "ollama":
        with st.spinner("🤖 AI is thinking..." if selected_lang == "en" else ("🤖 AI सोच रहा है..." if selected_lang == "hi" else "🤖 AI ఆలోచిస్తోంది...")):
            output = generate_response(user_input, clean_pref, selected_lang, user_info, ai_mode)
    else:
        output = generate_response(user_input, clean_pref, selected_lang, user_info, ai_mode)
    st.session_state.messages.append({"role": "user", "text": user_input})
    st.session_state.messages.append({"role": "assistant", "text": output})
    st.rerun()
