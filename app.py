import time
from html import escape

import streamlit as st

from locales import LANGUAGES, tr
from vehicles import VEHICLES

st.set_page_config(
    page_title="AI Auto Advisor",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded",
)


DEFAULT_FILTERS = {
    "query": "",
    "vehicle_type": "ALL",
    "budget": (1.0, 65.0),
    "fuels": [],
    "usage": [],
    "sort": "sort_price_low",
}


USAGE_KEYS = ["urban", "family", "luxury", "touring", "sport", "adventure"]
FUEL_KEYS = ["ev", "petrol", "diesel", "hybrid"]
SORT_KEYS = ["sort_price_low", "sort_price_high", "sort_range"]


for key, value in {
    "lang": "en",
    "booted": False,
    "filters": DEFAULT_FILTERS.copy(),
}.items():
    if key not in st.session_state:
        st.session_state[key] = value


def reset_filters():
    st.session_state["filters"] = DEFAULT_FILTERS.copy()


if not st.session_state["booted"]:
    st.markdown(
        """
        <style>
            .stApp {background: radial-gradient(circle at top left, #e5f1ff, #f7fbff 45%, #eef8ff 100%);} 
            .boot-wrap {
                min-height: 92vh;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-direction: column;
                color: #15314f;
                text-align: center;
                gap: 1rem;
            }
            .wheel-shell {
                width: 180px;
                height: 180px;
                position: relative;
                display: grid;
                place-items: center;
            }
            .wheel-speed {
                position: absolute;
                width: 240px;
                height: 4px;
                background: linear-gradient(90deg, transparent, #42b7ff, transparent);
                animation: streak 0.7s linear infinite;
                border-radius: 999px;
                opacity: 0.85;
            }
            .wheel-speed:nth-child(2) {transform: translateY(-26px); animation-delay: 0.12s; width: 190px;}
            .wheel-speed:nth-child(3) {transform: translateY(26px); animation-delay: 0.24s; width: 210px;}
            .wheel {
                width: 126px;
                height: 126px;
                border-radius: 50%;
                background: radial-gradient(circle at 35% 35%, #c8efff, #69b8ff 55%, #1d4275 100%);
                box-shadow: 0 0 0 10px rgba(12, 52, 96, 0.12), 0 18px 35px rgba(41, 89, 155, 0.22);
                position: relative;
                animation: spin 0.8s linear infinite;
            }
            .wheel:before, .wheel:after {
                content: "";
                position: absolute;
                inset: 12px;
                border-radius: 50%;
                border: 5px dashed rgba(255,255,255,0.92);
            }
            .wheel:after {
                inset: 42px;
                border-style: solid;
                border-width: 8px;
                border-color: rgba(20, 49, 79, 0.85);
                background: #edf6ff;
            }
            .boot-title {font-size: 2rem; font-weight: 800;}
            .boot-text {font-size: 1rem; max-width: 620px; color: #45607f;}
            @keyframes spin {from {transform: rotate(0deg);} to {transform: rotate(360deg);}}
            @keyframes streak {
                0% {transform: translateX(-22px); opacity: 0.15;}
                50% {opacity: 0.95;}
                100% {transform: translateX(22px); opacity: 0.15;}
            }
        </style>
        <div class="boot-wrap">
            <div class="wheel-shell">
                <div class="wheel-speed"></div>
                <div class="wheel-speed"></div>
                <div class="wheel-speed"></div>
                <div class="wheel"></div>
            </div>
            <div class="boot-title">AI Auto Advisor</div>
            <div class="boot-text">Launching a smoother multilingual garage experience with a rotating wheel loader.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    time.sleep(2.1)
    st.session_state["booted"] = True
    st.rerun()


lang = st.session_state["lang"]


st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Inter', 'Noto Sans Telugu', 'Noto Sans Devanagari', sans-serif;
        }
        .stApp {
            background:
                radial-gradient(circle at 15% 15%, rgba(102,185,255,0.22), transparent 20%),
                radial-gradient(circle at 85% 10%, rgba(99,114,255,0.16), transparent 18%),
                linear-gradient(180deg, #f6fbff 0%, #eef6ff 46%, #f7fbff 100%);
            color: #16304f;
        }
        .stApp::before {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            background-image:
                linear-gradient(rgba(64,126,201,0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(64,126,201,0.05) 1px, transparent 1px);
            background-size: 32px 32px;
            mask-image: linear-gradient(to bottom, rgba(0,0,0,0.7), transparent 90%);
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(243,249,255,0.96), rgba(233,244,255,0.98));
            border-right: 1px solid rgba(80, 133, 194, 0.16);
        }
        [data-testid="stSidebar"] * {
            color: #173453 !important;
        }
        .hero-card {
            position: relative;
            overflow: hidden;
            border-radius: 28px;
            padding: 1.7rem 1.7rem 1.5rem;
            background: linear-gradient(140deg, rgba(255,255,255,0.86), rgba(226,241,255,0.88));
            border: 1px solid rgba(126, 179, 232, 0.3);
            backdrop-filter: blur(20px);
            box-shadow: 0 24px 60px rgba(80, 123, 183, 0.16);
            animation: floatUp 1.1s ease;
        }
        .hero-card::after {
            content: "";
            position: absolute;
            width: 220px;
            height: 220px;
            right: -60px;
            top: -80px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(92,174,255,0.35), rgba(92,174,255,0.02));
        }
        .badge-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.65rem;
            margin-bottom: 1rem;
        }
        .glass-badge {
            padding: 0.45rem 0.8rem;
            border-radius: 999px;
            background: rgba(255,255,255,0.72);
            border: 1px solid rgba(107, 168, 233, 0.35);
            color: #1a4b7a;
            font-size: 0.87rem;
            font-weight: 600;
            box-shadow: 0 10px 24px rgba(88, 134, 195, 0.08);
        }
        .hero-title {
            font-size: clamp(2rem, 3vw, 3.2rem);
            line-height: 1.08;
            font-weight: 800;
            margin-bottom: 0.75rem;
            color: #11355f;
            max-width: 860px;
        }
        .hero-subtitle {
            font-size: 1rem;
            line-height: 1.8;
            color: #42617e;
            max-width: 860px;
        }
        .section-title {
            font-size: 1.45rem;
            font-weight: 800;
            color: #133a63;
            margin-top: 0.5rem;
            margin-bottom: 0.2rem;
        }
        .section-subtitle {
            color: #50708d;
            margin-bottom: 0.9rem;
        }
        .stat-card, .info-card, .vehicle-card {
            background: linear-gradient(180deg, rgba(255,255,255,0.88), rgba(238,247,255,0.88));
            border: 1px solid rgba(120, 180, 235, 0.28);
            border-radius: 24px;
            padding: 1.1rem 1.15rem;
            box-shadow: 0 18px 44px rgba(78, 120, 178, 0.10);
        }
        .stat-card {text-align: center;}
        .stat-value {font-size: 1.6rem; font-weight: 800; color: #103e72;}
        .stat-label {font-size: 0.9rem; color: #567693; margin-top: 0.15rem;}
        .vehicle-card {
            min-height: 320px;
            transition: transform 0.25s ease, box-shadow 0.25s ease;
            margin-bottom: 1rem;
        }
        .vehicle-card:hover {
            transform: translateY(-5px) scale(1.01);
            box-shadow: 0 24px 54px rgba(80, 125, 182, 0.18);
        }
        .vehicle-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 0.7rem;
            margin-bottom: 0.7rem;
        }
        .vehicle-name {
            font-size: 1.14rem;
            font-weight: 800;
            color: #133760;
        }
        .type-pill {
            padding: 0.38rem 0.65rem;
            border-radius: 999px;
            background: linear-gradient(135deg, #4cc9ff, #6a7dff);
            color: white;
            font-weight: 700;
            font-size: 0.77rem;
            letter-spacing: 0.02em;
        }
        .price-tag {
            font-size: 1.45rem;
            font-weight: 800;
            color: #0f4678;
            margin: 0.35rem 0 0.75rem;
        }
        .detail-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.55rem;
            margin-bottom: 0.9rem;
        }
        .detail-chip {
            background: rgba(255,255,255,0.75);
            border: 1px solid rgba(110, 173, 238, 0.22);
            border-radius: 16px;
            padding: 0.65rem 0.75rem;
        }
        .chip-label {font-size: 0.76rem; color: #5d7e9d; margin-bottom: 0.1rem;}
        .chip-value {font-size: 0.93rem; font-weight: 700; color: #1a446c;}
        .bullets {
            padding-left: 1rem;
            margin: 0.4rem 0 0.7rem;
            color: #365877;
        }
        .bullets li {margin-bottom: 0.25rem;}
        .usage-wrap {
            display: flex;
            flex-wrap: wrap;
            gap: 0.45rem;
            margin-top: 0.6rem;
        }
        .usage-badge {
            padding: 0.32rem 0.6rem;
            border-radius: 999px;
            background: rgba(64, 183, 255, 0.12);
            color: #15538a;
            border: 1px solid rgba(65, 150, 223, 0.25);
            font-size: 0.8rem;
            font-weight: 700;
        }
        .recommend-box {
            background: linear-gradient(135deg, rgba(255,255,255,0.92), rgba(227,243,255,0.92));
            border-radius: 24px;
            border: 1px solid rgba(120,180,235,0.28);
            box-shadow: 0 20px 50px rgba(76, 118, 180, 0.12);
            padding: 1.35rem;
        }
        .recommend-title {font-size: 1.35rem; font-weight: 800; color: #113a68;}
        .recommend-sub {color: #53708b; margin-bottom: 0.9rem;}
        .footer-note {
            text-align: center;
            color: #5c7a98;
            padding: 0.8rem 0 1.8rem;
            font-size: 0.95rem;
        }
        .stButton > button, .stFormSubmitButton > button {
            border-radius: 16px !important;
            border: 0 !important;
            background: linear-gradient(135deg, #32b6ff, #637cff) !important;
            color: white !important;
            font-weight: 700 !important;
            box-shadow: 0 14px 34px rgba(78, 126, 188, 0.22);
            transition: transform 0.18s ease, box-shadow 0.18s ease;
        }
        .stButton > button:hover, .stFormSubmitButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 18px 40px rgba(78, 126, 188, 0.30);
        }
        .stTextInput > div > div > input,
        .stSelectbox > div > div,
        .stMultiSelect > div > div,
        .stSlider,
        .stNumberInput > div > div > input {
            border-radius: 16px !important;
        }
        @keyframes floatUp {
            from {opacity: 0; transform: translateY(18px);} 
            to {opacity: 1; transform: translateY(0);} 
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def type_label(vehicle_type: str, current_lang: str) -> str:
    if vehicle_type == "2W":
        return tr(current_lang, "two_wheeler")
    return tr(current_lang, "four_wheeler")


UNIT_LABEL = {
    "en": "lakh",
    "hi": "लाख",
    "te": "లక్షలు",
}


def price_label(value: float, current_lang: str) -> str:
    return f"₹{value:.2f} {UNIT_LABEL.get(current_lang, 'lakh')}"



def range_label(vehicle: dict) -> str:
    if vehicle["fuel"] == "ev":
        return f"{vehicle['range_km']} km"
    return f"{vehicle['range_km']} km/l"



def normalize(text: str) -> str:
    return " ".join(text.lower().strip().split())



def matches_search(vehicle: dict, query: str, current_lang: str) -> bool:
    if not query:
        return True
    haystack = [
        vehicle["brand"],
        vehicle["model"],
        tr(current_lang, vehicle["fuel"]),
        type_label(vehicle["type"], current_lang),
        *vehicle["highlights"],
        *[tr(current_lang, item) for item in vehicle["usage"]],
    ]
    search_blob = normalize(" ".join(haystack))
    return normalize(query) in search_blob



def sort_vehicles(items: list[dict], sort_key: str) -> list[dict]:
    if sort_key == "sort_price_high":
        return sorted(items, key=lambda x: x["price_lakh"], reverse=True)
    if sort_key == "sort_range":
        return sorted(items, key=lambda x: x["range_km"], reverse=True)
    return sorted(items, key=lambda x: x["price_lakh"])



def score_vehicle(vehicle: dict, budget: float, family_size: int, drive_mode: str, preference: str) -> tuple[int, list[str]]:
    score = 0
    reasons = []

    if vehicle["price_lakh"] <= budget:
        score += 5
        reasons.append("reason_budget")
    else:
        score -= 5

    if drive_mode == "city" and "urban" in vehicle["usage"]:
        score += 3
        reasons.append("reason_city")
    elif drive_mode == "highway" and "touring" in vehicle["usage"]:
        score += 3
        reasons.append("reason_highway")
    elif drive_mode == "mixed" and ({"urban", "touring"} & set(vehicle["usage"])):
        score += 3
        reasons.append("reason_mixed")

    if preference == "premium" and "luxury" in vehicle["usage"]:
        score += 3
        reasons.append("reason_luxury")
    elif preference == "performance" and "sport" in vehicle["usage"]:
        score += 3
        reasons.append("reason_performance")
    elif preference == "balanced":
        score += 2

    if family_size >= 5 and vehicle["seating"] >= 5:
        score += 2
    elif family_size <= 2 and vehicle["type"] == "2W":
        score += 1
    elif family_size >= 4 and vehicle["type"] == "2W":
        score -= 2

    if budget < 5 and vehicle["type"] == "2W":
        score += 2
    if budget > 20 and vehicle["type"] == "4W":
        score += 1

    deduped_reasons = []
    for reason in reasons:
        if reason not in deduped_reasons:
            deduped_reasons.append(reason)

    return score, deduped_reasons[:4]



def render_vehicle_card(vehicle: dict, current_lang: str):
    usage_html = "".join(
        f"<span class='usage-badge'>{escape(tr(current_lang, usage))}</span>" for usage in vehicle["usage"]
    )
    highlights_html = "".join(f"<li>{escape(item)}</li>" for item in vehicle["highlights"])
    st.markdown(
        f"""
        <div class="vehicle-card">
            <div class="vehicle-top">
                <div class="vehicle-name">{escape(vehicle['brand'])} {escape(vehicle['model'])}</div>
                <div class="type-pill">{escape(type_label(vehicle['type'], current_lang))}</div>
            </div>
            <div class="price-tag">{escape(price_label(vehicle['price_lakh'], current_lang))}</div>
            <div class="detail-grid">
                <div class="detail-chip"><div class="chip-label">{escape(tr(current_lang, 'fuel'))}</div><div class="chip-value">{escape(tr(current_lang, vehicle['fuel']))}</div></div>
                <div class="detail-chip"><div class="chip-label">{escape(tr(current_lang, 'transmission'))}</div><div class="chip-value">{escape(vehicle['transmission'])}</div></div>
                <div class="detail-chip"><div class="chip-label">{escape(tr(current_lang, 'range'))}</div><div class="chip-value">{escape(range_label(vehicle))}</div></div>
                <div class="detail-chip"><div class="chip-label">{escape(tr(current_lang, 'seating'))}</div><div class="chip-value">{escape(str(vehicle['seating']))}</div></div>
            </div>
            <div class="chip-label">{escape(tr(current_lang, 'highlights'))}</div>
            <ul class="bullets">{highlights_html}</ul>
            <div class="chip-label">{escape(tr(current_lang, 'recommended_for'))}</div>
            <div class="usage-wrap">{usage_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


left, right = st.columns([0.8, 0.2])
with left:
    st.markdown(
        f"""
        <div class="hero-card">
            <div class="badge-row">
                <span class="glass-badge">✨ {escape(tr(lang, 'hero_badge'))}</span>
                <span class="glass-badge">⚡ {escape(tr(lang, 'feature_ui'))}</span>
                <span class="glass-badge">🌐 {escape(tr(lang, 'feature_lang'))}</span>
            </div>
            <div class="hero-title">{escape(tr(lang, 'hero_title'))}</div>
            <div class="hero-subtitle">{escape(tr(lang, 'hero_subtitle'))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with right:
    selected_lang = st.selectbox(
        tr(lang, "language_label"),
        options=list(LANGUAGES.keys()),
        format_func=lambda code: LANGUAGES[code],
        index=list(LANGUAGES.keys()).index(lang),
    )
    if selected_lang != st.session_state["lang"]:
        st.session_state["lang"] = selected_lang
        st.rerun()

lang = st.session_state["lang"]
filters = st.session_state["filters"]

with st.sidebar:
    st.markdown(f"## {tr(lang, 'sidebar_title')}")
    st.caption(tr(lang, "search_help"))

    with st.form("filter_form"):
        query = st.text_input(
            tr(lang, "search_label"),
            value=filters["query"],
            placeholder=tr(lang, "search_placeholder"),
        )
        vehicle_type = st.selectbox(
            tr(lang, "vehicle_type"),
            options=["ALL", "2W", "4W"],
            format_func=lambda x: {
                "ALL": tr(lang, "all"),
                "2W": tr(lang, "two_wheeler"),
                "4W": tr(lang, "four_wheeler"),
            }[x],
            index=["ALL", "2W", "4W"].index(filters["vehicle_type"]),
        )
        budget = st.slider(
            tr(lang, "budget"),
            min_value=1.0,
            max_value=65.0,
            value=filters["budget"],
            step=0.5,
        )
        fuels = st.multiselect(
            tr(lang, "fuel_type"),
            options=FUEL_KEYS,
            default=filters["fuels"],
            format_func=lambda x: tr(lang, x),
        )
        usage = st.multiselect(
            tr(lang, "usage"),
            options=USAGE_KEYS,
            default=filters["usage"],
            format_func=lambda x: tr(lang, x),
        )
        sort_key = st.selectbox(
            tr(lang, "sort_by"),
            options=SORT_KEYS,
            index=SORT_KEYS.index(filters["sort"]),
            format_func=lambda x: tr(lang, x),
        )
        apply_filters = st.form_submit_button(tr(lang, "apply_filters"))

    if apply_filters:
        st.session_state["filters"] = {
            "query": query,
            "vehicle_type": vehicle_type,
            "budget": budget,
            "fuels": fuels,
            "usage": usage,
            "sort": sort_key,
        }
        filters = st.session_state["filters"]

    if st.button(tr(lang, "clear_filters"), use_container_width=True):
        reset_filters()
        st.rerun()


filtered = []
for vehicle in VEHICLES:
    if filters["vehicle_type"] != "ALL" and vehicle["type"] != filters["vehicle_type"]:
        continue
    if not (filters["budget"][0] <= vehicle["price_lakh"] <= filters["budget"][1]):
        continue
    if filters["fuels"] and vehicle["fuel"] not in filters["fuels"]:
        continue
    if filters["usage"] and not set(filters["usage"]).intersection(vehicle["usage"]):
        continue
    if not matches_search(vehicle, filters["query"], lang):
        continue
    filtered.append(vehicle)

filtered = sort_vehicles(filtered, filters["sort"])

stat_cols = st.columns(4)
stat_data = [
    (len(filtered), tr(lang, "stats_cars")),
    (len(LANGUAGES), tr(lang, "stats_langs")),
    (len(USAGE_KEYS), tr(lang, "stats_modes")),
    (tr(lang, "smoothness_value"), tr(lang, "stats_uptime")),
]
for col, (value, label) in zip(stat_cols, stat_data):
    with col:
        st.markdown(
            f"<div class='stat-card'><div class='stat-value'>{escape(str(value))}</div><div class='stat-label'>{escape(label)}</div></div>",
            unsafe_allow_html=True,
        )

st.markdown(f"<div class='section-title'>{escape(tr(lang, 'catalog_title'))}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='section-subtitle'>{escape(tr(lang, 'catalog_subtitle'))}</div>", unsafe_allow_html=True)
st.caption(tr(lang, "search_summary").format(count=len(filtered)))

if filtered:
    cols = st.columns(3)
    for index, vehicle in enumerate(filtered):
        with cols[index % 3]:
            render_vehicle_card(vehicle, lang)
else:
    st.info(tr(lang, "empty_state"))

st.markdown(f"<div class='section-title'>{escape(tr(lang, 'consultation_title'))}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='section-subtitle'>{escape(tr(lang, 'consultation_subtitle'))}</div>", unsafe_allow_html=True)

with st.form("consultation_form"):
    consult_cols = st.columns(4)
    with consult_cols[0]:
        consult_budget = st.number_input(tr(lang, "budget_input"), min_value=1.0, max_value=100.0, value=25.0, step=0.5)
    with consult_cols[1]:
        family_size = st.number_input(tr(lang, "family_size"), min_value=1, max_value=8, value=4, step=1)
    with consult_cols[2]:
        drive_mode = st.selectbox(tr(lang, "city_priority"), options=["city", "mixed", "highway"], format_func=lambda x: tr(lang, x))
    with consult_cols[3]:
        preference = st.selectbox(tr(lang, "luxury_priority"), options=["balanced", "premium", "performance"], format_func=lambda x: tr(lang, x))

    consult_submit = st.form_submit_button(tr(lang, "submit"), use_container_width=True)

if consult_submit:
    recommendation_pool = filtered if filtered else VEHICLES
    scored = []
    for vehicle in recommendation_pool:
        score, reasons = score_vehicle(vehicle, consult_budget, int(family_size), drive_mode, preference)
        scored.append((score, reasons, vehicle))
    scored.sort(key=lambda item: (item[0], -item[2]["price_lakh"], item[2]["range_km"]), reverse=True)
    best_score, best_reasons, best_vehicle = scored[0]
    reasons_html = "".join(f"<li>{escape(tr(lang, reason))}</li>" for reason in best_reasons)
    st.markdown(
        f"""
        <div class="recommend-box">
            <div class="recommend-title">🏁 {escape(tr(lang, 'top_match'))}: {escape(best_vehicle['brand'])} {escape(best_vehicle['model'])}</div>
            <div class="recommend-sub">{escape(type_label(best_vehicle['type'], lang))} • {escape(price_label(best_vehicle['price_lakh'], lang))} • {escape(tr(lang, best_vehicle['fuel']))}</div>
            <div class="chip-label">{escape(tr(lang, 'recommendation_reason'))}</div>
            <ul class="bullets">{reasons_html}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

info_cols = st.columns([1.1, 0.9])
with info_cols[0]:
    st.markdown(
        f"<div class='info-card'><div class='section-title'>{escape(tr(lang, 'i18n_title'))}</div><div class='section-subtitle'>{escape(tr(lang, 'i18n_body'))}</div></div>",
        unsafe_allow_html=True,
    )
with info_cols[1]:
    st.markdown(
        f"""
        <div class='info-card'>
            <div class='section-title'>{escape(tr(lang, 'app_title'))}</div>
            <div class='section-subtitle'>{escape(tr(lang, 'tagline'))}</div>
            <div class='usage-wrap'>
                <span class='usage-badge'>{escape(tr(lang, 'feature_fast'))}</span>
                <span class='usage-badge'>{escape(tr(lang, 'feature_lang'))}</span>
                <span class='usage-badge'>{escape(tr(lang, 'feature_ui'))}</span>
                <span class='usage-badge'>{escape(tr(lang, 'feature_ready'))}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(f"<div class='footer-note'>{escape(tr(lang, 'footer'))}</div>", unsafe_allow_html=True)
