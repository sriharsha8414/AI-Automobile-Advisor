import streamlit as st
import time
import re
import json
import urllib.request
import urllib.parse
import os

# Set page config FIRST
st.set_page_config(page_title="AI Auto Advisor", page_icon="🚗", layout="centered")

# ==================================================
# 🎨 CUSTOM STYLING (Luxury & Premium Theme)
# Navy Blue (#001F3F) and Gold (#FFD700) accents.
# ==================================================
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #050c18 !important;
        font-family: 'Outfit', sans-serif !important;
        color: #e2e8f0 !important;
    }
    
    [data-testid="stHeader"] {
        background-color: #050c18 !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #001f3f !important;
        border-right: 2px solid #FFD700 !important;
    }
    
    /* Make sidebar elements styled */
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p, 
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {
        color: #e2e8f0 !important;
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Custom style for sidebar titles */
    .sidebar-title {
        color: #FFD700 !important;
        font-size: 1.5em;
        font-weight: 800;
        margin-bottom: 20px;
        text-align: center;
        border-bottom: 2px solid #FFD700;
        padding-bottom: 10px;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #FFD700 !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800 !important;
    }

    /* Target native Streamlit chat bubbles for styling */
    div[data-testid="stChatMessage"] {
        background-color: #0c2340 !important;
        border-left: 4px solid #FFD700 !important;
        border-radius: 12px !important;
        padding: 15px !important;
        margin-bottom: 15px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Styling input area */
    div[data-testid="stChatInputContainer"] {
        border: 2px solid #FFD700 !important;
        border-radius: 10px !important;
        background-color: #0c2340 !important;
    }
    
    div[data-testid="stChatInputContainer"] textarea {
        color: #ffffff !important;
        font-family: 'Outfit', sans-serif !important;
    }

    /* Styling buttons */
    .stButton>button {
        background-color: #0c2340 !important;
        color: #FFD700 !important;
        border: 1px solid #FFD700 !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    .stButton>button:hover {
        background-color: #FFD700 !important;
        color: #050c18 !important;
        box-shadow: 0 0 10px rgba(255, 215, 0, 0.5) !important;
    }
</style>
"""

# ==================================================
# ✨ LOADING ANIMATION (The "Wow" Factor)
# Renders a premium steering wheel style animation for 3s.
# ==================================================
def render_spinning_wheel():
    placeholder = st.empty()
    placeholder.markdown("""
    <div style="
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 85vh;
        background-color: #050c18;
        color: #e2e8f0;
        font-family: 'Outfit', sans-serif;
    ">
        <h1 style="color: #FFD700; font-size: 3.2em; margin-bottom: 10px; font-weight: 800; letter-spacing: 2px;">AI AUTO ADVISOR</h1>
        <p style="font-size: 1.1em; color: #8a9ba8; margin-bottom: 50px; letter-spacing: 2px; text-transform: uppercase;">Tailoring your bespoke automotive profile...</p>
        <div class="wheel-box">
            <svg width="140" height="140" viewBox="0 0 100 100" class="spinner">
                <defs>
                    <linearGradient id="gold-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#FFD700" stop-opacity="1" />
                        <stop offset="100%" stop-color="#001f3f" stop-opacity="0.1" />
                    </linearGradient>
                </defs>
                <!-- Outer wheel rim -->
                <circle cx="50" cy="50" r="42" stroke="url(#gold-grad)" stroke-dasharray="200 60" stroke-width="6" fill="none" stroke-linecap="round" />
                <!-- Steering wheel hub and spokes -->
                <circle cx="50" cy="50" r="10" stroke="#FFD700" stroke-width="2.5" fill="none" />
                <line x1="50" y1="8" x2="50" y2="40" stroke="#FFD700" stroke-width="2.5" />
                <line x1="14" y1="64" x2="40" y2="55" stroke="#FFD700" stroke-width="2.5" />
                <line x1="86" y1="64" x2="60" y2="55" stroke="#FFD700" stroke-width="2.5" />
            </svg>
        </div>
        <p style="font-size: 0.9em; color: #a0aec0; margin-top: 40px; font-style: italic;">Analyzing global vehicle database...</p>
        <style>
            .wheel-box {
                background: radial-gradient(circle, rgba(0,31,63,0.3) 0%, rgba(5,12,24,0) 70%);
                padding: 20px;
                border-radius: 50%;
            }
            .spinner {
                animation: spin 1.8s cubic-bezier(0.4, 0.1, 0.2, 1) infinite;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# 🌐 REAL-TIME DATA FETCHING: DUCKDUCKGO & WIKIPEDIA
# ==================================================
def search_duckduckgo(query, max_results=3):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    encoded_query = urllib.parse.quote(query)
    url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
        results = []
        matches = re.finditer(r'<a\s+class="result__a"\s+href="([^"]+)"[^>]*>(.*?)</a>', html, re.DOTALL)
        snippets = re.findall(r'<a\s+class="result__snippet"[^>]*>(.*?)</a>', html, re.DOTALL)
        
        for i, match in enumerate(matches):
            if i >= max_results:
                break
            raw_url = match.group(1)
            url_match = re.search(r'uddg=([^&]+)', raw_url)
            url = urllib.parse.unquote(url_match.group(1)) if url_match else raw_url
            
            title = re.sub(r'<[^>]+>', '', match.group(2)).strip()
            
            snippet = ""
            if i < len(snippets):
                snippet = re.sub(r'<[^>]+>', '', snippets[i]).strip()
                
            results.append({
                "title": title,
                "url": url,
                "snippet": snippet
            })
        return results
    except Exception as e:
        print(f"DuckDuckGo search error: {e}")
        return []

def get_wikipedia_image(vehicle_name):
    """Fetches high-quality official vehicle image from Wikipedia Page Image API."""
    search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(vehicle_name)}&format=json"
    headers = {
        'User-Agent': 'AIAutoAdvisor/1.0 (contact@aiautoadvisor.com)'
    }
    try:
        req = urllib.request.Request(search_url, headers=headers)
        with urllib.request.urlopen(req, timeout=3) as response:
            data = json.loads(response.read().decode('utf-8'))
            search_results = data.get('query', {}).get('search', [])
            if not search_results:
                return None
            best_title = search_results[0]['title']
            
        img_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(best_title)}&prop=pageimages&format=json&pithumbsize=600"
        req = urllib.request.Request(img_url, headers=headers)
        with urllib.request.urlopen(req, timeout=3) as response:
            data = json.loads(response.read().decode('utf-8'))
            pages = data.get('query', {}).get('pages', {})
            for page_id, page_data in pages.items():
                thumbnail = page_data.get('thumbnail', {})
                if 'source' in thumbnail:
                    return thumbnail['source']
    except Exception as e:
        print(f"Wikipedia image fetch error for {vehicle_name}: {e}")
    return None

# ==================================================
# 🔌 FREE & SPECIFIC AI BACKENDS
# ==================================================
def call_ddg_ai(prompt, system_instruction=""):
    """Queries DuckDuckGo's free unauthenticated GPT-4o-mini chat endpoint."""
    status_url = "https://duckduckgo.com/duckchat/v1/status"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "x-vqd-accept": "1"
    }
    
    try:
        req = urllib.request.Request(status_url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as response:
            token = response.info().get("x-vqd-token")
            
        if not token:
            return None
            
        chat_url = "https://duckduckgo.com/duckchat/v1/chat"
        chat_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Content-Type": "application/json",
            "x-vqd-token": token
        }
        
        full_prompt = f"{system_instruction}\n\nUser Input:\n{prompt}" if system_instruction else prompt
        
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "user", "content": full_prompt}
            ]
        }
        
        req2 = urllib.request.Request(
            chat_url,
            data=json.dumps(payload).encode("utf-8"),
            headers=chat_headers,
            method="POST"
        )
        
        with urllib.request.urlopen(req2, timeout=8) as response2:
            resp_str = response2.read().decode("utf-8", errors="ignore")
            
            content_parts = []
            for line in resp_str.split("\n"):
                if line.startswith("data:"):
                    data_str = line[5:].strip()
                    if data_str == "[DONE]":
                        break
                    try:
                        data_json = json.loads(data_str)
                        chunk = data_json.get("message", "")
                        if chunk:
                            content_parts.append(chunk)
                    except:
                        pass
            return "".join(content_parts)
    except Exception as e:
        print(f"DuckDuckGo AI Call failed: {e}")
        return None

def call_gemini_api(api_key, system_instruction, user_prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": user_prompt}]}],
        "systemInstruction": {"parts": [{"text": system_instruction}]},
        "generationConfig": {"responseMimeType": "application/json"}
    }
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            text_response = result['candidates'][0]['content']['parts'][0]['text']
            return json.loads(text_response)
    except:
        return None

def call_openai_api(api_key, system_instruction, user_prompt):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_prompt}
        ],
        "response_format": {"type": "json_object"}
    }
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            text_response = result['choices'][0]['message']['content']
            return json.loads(text_response)
    except:
        return None

def call_free_llm(prompt, system_instruction):
    env_gemini = os.environ.get("GEMINI_API_KEY")
    env_openai = os.environ.get("OPENAI_API_KEY")
    
    if env_gemini:
        res = call_gemini_api(env_gemini, system_instruction, prompt)
        if res: return res
        
    if env_openai:
        res = call_openai_api(env_openai, system_instruction, prompt)
        if res: return res
        
    raw_response = call_ddg_ai(prompt, system_instruction)
    if raw_response:
        json_match = re.search(r'(\{.*\})', raw_response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except:
                pass
    return None

def call_llm_concierge(prompt, history, profile):
    conv = []
    for msg in history:
        conv.append(f"{msg['role'].title()}: {msg['content']}")
    conv.append(f"User: {prompt}")
    history_str = "\n".join(conv)
    
    system_instruction = (
        "You are a luxury automotive advisor. Extract profile parameters from the conversation history and decide what to ask next. "
        "Your response MUST be strictly a JSON object containing keys:\n"
        "- 'profile': object containing 'budget', 'type', 'body_style', 'fuel_type', 'daily_distance', 'road_condition' (updated with values found or null)\n"
        "- 'concierge_response': string containing your polite next response to the user. If parameters are missing, ask for them politely. If all set, congratulate them and state you are searching.\n"
        "- 'all_set': boolean (true if all 6 parameters are successfully collected, false otherwise)"
    )
    return call_free_llm(history_str, system_instruction)

# ==================================================
# 🚀 INITIALIZATION: SESSION STATE SETUP
# ==================================================
def initialize_state():
    if "messages" not in st.session_state:
        welcome_message = {
            "role": "assistant",
            "content": (
                "Welcome to **AI Auto Advisor**, your personal automotive concierge. "
                "I am here to guide you in discovering the perfect luxury vehicle tailored "
                "to your budget, lifestyle, and driving preferences.\n\n"
                "To begin our consultation, please tell me: "
                "Are you looking for a **2-Wheeler or a 4-Wheeler**, and what is your **budget range**?"
            )
        }
        st.session_state['messages'] = [welcome_message]

    if "profile" not in st.session_state:
        st.session_state['profile'] = {
            'budget': None,
            'type': None,
            'body_style': None,
            'fuel_type': None,
            'daily_distance': None,
            'road_condition': None,
            'condition': 'Brand New'  # default; updated passively from chat
        }
        
    if "step" not in st.session_state:
        st.session_state['step'] = 'gathering_profile'
        
    if "recommendations" not in st.session_state:
        st.session_state['recommendations'] = None
        
    if "selected_model" not in st.session_state:
        st.session_state['selected_model'] = None

# ==================================================
# ⚙️ SIDEBAR SUMMARY DISPLAY
# ==================================================
def display_profile_summary():
    st.sidebar.markdown('<div class="sidebar-title">⚙️ CLIENT PROFILE</div>', unsafe_allow_html=True)
    
    profile = st.session_state['profile']
    
    # Render fields as status indicators
    fields = [
        ("Budget", profile['budget'], "💰"),
        ("Type", profile['type'], "🚗"),
        ("Body Style", profile['body_style'], "✨"),
        ("Fuel Type", profile['fuel_type'], "🔌"),
        ("Daily Distance", profile['daily_distance'], "🛣️"),
        ("Road Conditions", profile['road_condition'], "⛰️")
    ]
    
    for label, val, icon in fields:
        if val:
            st.sidebar.markdown(f"**{icon} {label}:** <span style='color: #FFD700;'>{val}</span> ✅", unsafe_allow_html=True)
        else:
            st.sidebar.markdown(f"**{icon} {label}:** <span style='color: #8a9ba8;'>Not Set</span> ⏳", unsafe_allow_html=True)
            
    st.sidebar.markdown("---")
    
    # Status Summary
    missing_count = sum(1 for v in profile.values() if v is None)
    if missing_count == 0:
        st.sidebar.success("🎉 Profile Complete!")
    else:
        st.sidebar.info(f"⏳ {missing_count} parameters pending...")
        
    # Backend indicator
    st.sidebar.markdown("🤖 **Backend Concierge:**")
    st.sidebar.info("GPT-4o-mini (Free / Open API)")
    st.sidebar.markdown("---")
    
    # Reset button
    if st.sidebar.button("🔄 Reset Consultation"):
        st.session_state.clear()
        st.rerun()

# ==================================================
# 🧠 EXTRACT & CONCIERGE DIALOGUE CONTROL
# ==================================================
def extract_profile_data(text, profile, overwrite=False):
    text_lower = text.lower()
    # Remove 2-wheeler / 4-wheeler to prevent matching their numbers (e.g. "4" in "4 wheeler") as budget/distance
    clean_text = re.sub(r'\b[24]\s*-?\s*wheel(?:er)?s?\b', '', text_lower)
    updated = False
    
    # 1. Type
    if profile['type'] is None or overwrite:
        two_wheel_keywords = ["bike", "motorcycle", "scooter", "2 wheeler", "2-wheeler", "two wheeler", "superbike", "cruiser", "activa", "bullet", "ktm", "vespa"]
        four_wheel_keywords = ["car", "4 wheeler", "4-wheeler", "four wheeler", "suv", "sedan", "hatchback", "coupe", "convertible", "crossover", "truck", "automobile", "jeep"]
        new_val = None
        if any(kw in text_lower for kw in two_wheel_keywords):
            new_val = "2-Wheeler"
        elif any(kw in text_lower for kw in four_wheel_keywords):
            new_val = "4-Wheeler"
            
        if new_val and profile['type'] != new_val:
            profile['type'] = new_val
            updated = True

    # 2. Budget
    if profile['budget'] is None or overwrite:
        budget_match = re.search(r'(?:under|below|up\s+to|max|around|budget\s+of)?\s*(?:rs\.?|₹|\$|usd)?\s*(\d+(?:\.\d+)?)\s*(lakh|lakhs|l|lac|lacs|cr|crore|crores|k|m|million)?\b', clean_text)
        if budget_match:
            num = budget_match.group(1)
            unit = budget_match.group(2)
            
            # Check if this is a year (e.g. 2025, 2026) instead of a budget
            is_year = False
            if unit is None:
                try:
                    val = int(num)
                    if 1900 <= val <= 2100:
                        is_year = True
                except:
                    pass
            
            if not is_year:
                new_budget = None
                if unit in ['lakh', 'lakhs', 'l', 'lac', 'lacs']:
                    new_budget = f"₹ {num} Lakh"
                elif unit in ['cr', 'crore', 'crores']:
                    new_budget = f"₹ {num} Crore"
                elif unit == 'k':
                    new_budget = f"₹ {num}k" if 'rs' in clean_text or '₹' in clean_text or 'lakh' in clean_text or 'lac' in clean_text else f"$ {num}k"
                elif unit in ['m', 'million']:
                    new_budget = f"$ {num} Million"
                else:
                    if '$' in clean_text:
                        new_budget = f"$ {num}"
                    else:
                        new_budget = f"₹ {num} Lakh"
                if new_budget and profile['budget'] != new_budget:
                    profile['budget'] = new_budget
                    updated = True
            
    # 3. Body Style
    if profile['body_style'] is None or overwrite:
        vehicle_type = profile.get('type')
        if vehicle_type == '2-Wheeler':
            styles = {
                # Scooter variants
                'scooter': 'Scooter',
                'scooty': 'Scooter',
                'moped': 'Scooter',
                'activa': 'Scooter',
                'vespa': 'Scooter',
                # Superbike / Sports
                'superbike': 'Superbike',
                'sport': 'Superbike',
                'racing': 'Superbike',
                'race': 'Superbike',
                'sports bike': 'Superbike',
                'sportsbike': 'Superbike',
                # Cruiser / Touring
                'cruiser': 'Cruiser',
                'touring': 'Cruiser',
                'chopper': 'Cruiser',
                # Naked / Standard
                'naked': 'Naked / Street',
                'standard': 'Naked / Street',
                'street': 'Naked / Street',
                'normal': 'Naked / Street',
                'regular': 'Naked / Street',
                'commuter': 'Naked / Street',
                'daily': 'Naked / Street',
                # Adventure / Off-road
                'adventure': 'Adventure Bike',
                'adv': 'Adventure Bike',
                'dirt': 'Dirt Bike',
                'dirt bike': 'Dirt Bike',
                'enduro': 'Dirt Bike',
                'motocross': 'Dirt Bike',
                # Cafe Racer / Retro
                'cafe racer': 'Cafe Racer',
                'cafe': 'Cafe Racer',
                'retro': 'Cafe Racer',
                'classic': 'Cafe Racer',
                # Luxury / Premium
                'luxury': 'Cruiser',
                'premium': 'Superbike',
                'high-end': 'Cruiser',
                # Bullet shorthand
                'bullet': 'Cruiser',
                'ktm': 'Superbike',
            }
        else:
            styles = {
                'suv': 'SUV',
                'sedan': 'Sedan',
                'hatchback': 'Hatchback',
                'coupe': 'Coupe',
                'convertible': 'Convertible',
                'crossover': 'Crossover',
                'sports': 'Sports Car',
                'luxury': 'Sedan',
                'premium': 'SUV',
            }
        for kw, style in styles.items():
            if kw in clean_text:
                if profile['body_style'] != style:
                    profile['body_style'] = style
                    updated = True
                break
                
    # 4. Fuel Type
    if profile['fuel_type'] is None or overwrite:
        fuels = {
            'electric': 'Electric',
            'ev': 'Electric',
            'diesel': 'Diesel',
            'petrol': 'Petrol',
            'gasoline': 'Petrol',
            'hybrid': 'Hybrid',
            'phev': 'Hybrid',
            'cng': 'CNG'
        }
        for kw, fuel in fuels.items():
            if kw in clean_text:
                if profile['fuel_type'] != fuel:
                    profile['fuel_type'] = fuel
                    updated = True
                break
 
    # 5. Daily Distance
    if profile['daily_distance'] is None or overwrite:
        dist_match = re.search(r'(\d+)\s*(?:km|kms|miles|mile|kilometer|kilometers)', clean_text)
        if dist_match:
            new_dist = f"{dist_match.group(1)} km/day"
            if profile['daily_distance'] != new_dist:
                profile['daily_distance'] = new_dist
                updated = True
 
    # 6. Road Condition
    if profile['road_condition'] is None or overwrite:
        road_conditions = {
            'off-road': 'Off-Road / Rough',
            'offroad': 'Off-Road / Rough',
            'off road': 'Off-Road / Rough',
            'rough': 'Off-Road / Rough',
            'potholes': 'Off-Road / Rough',
            'muddy': 'Off-Road / Rough',
            'unpaved': 'Off-Road / Rough',
            'mountain': 'Hilly / Mountain',
            'hills': 'Hilly / Mountain',
            'ghat': 'Hilly / Mountain',
            'highway': 'Highway / Long Distance',
            'expressway': 'Highway / Long Distance',
            'freeway': 'Highway / Long Distance',
            'long drive': 'Highway / Long Distance',
            'city': 'City / Traffic',
            'traffic': 'City / Traffic',
            'urban': 'City / Traffic',
            'streets': 'City / Traffic',
            'town': 'City / Traffic',
            'track': 'Racetrack',
            'racetrack': 'Racetrack',
            'racing': 'Racetrack',
            'circuit': 'Racetrack',
            'drag': 'Racetrack',
        }
        for kw, cond in road_conditions.items():
            if kw in clean_text:
                if profile['road_condition'] != cond:
                    profile['road_condition'] = cond
                    updated = True
                break
                
    return updated

REQUIRED_PROFILE_KEYS = ['budget', 'type', 'body_style', 'fuel_type', 'daily_distance', 'road_condition']

def get_missing_parameters(profile):
    return [k for k in REQUIRED_PROFILE_KEYS if profile.get(k) is None]

def generate_concierge_question(profile):
    missing = get_missing_parameters(profile)
    if not missing:
        return None

    vehicle_type = profile.get('type')
    is_two_wheeler = vehicle_type == '2-Wheeler'

    prompts = {
        'type': "whether you are looking for a **2-Wheeler** (Motorcycle/Scooter) or a **4-Wheeler** (Car/SUV)",
        'budget': "your **budget range** (e.g., ₹2 Lakh, ₹10 Lakh, ₹50k)",
        'body_style': (
            "your preferred **riding style** — choose from:\n"
            "&nbsp;&nbsp;🛵 **Scooter** (Activa-style, everyday commuter)\n"
            "&nbsp;&nbsp;🏍️ **Naked / Street** (standard commuter bike)\n"
            "&nbsp;&nbsp;⚡ **Superbike** (sports / racing)\n"
            "&nbsp;&nbsp;🤠 **Cruiser** (Bullet / touring style)\n"
            "&nbsp;&nbsp;🌄 **Adventure Bike** (off-road capable)\n"
            "&nbsp;&nbsp;☕ **Cafe Racer** (retro / classic style)"
            if is_two_wheeler else
            "your preferred **body style** — e.g., SUV, Sedan, Hatchback, Coupe, Crossover"
        ),
        'fuel_type': (
            "your preferred **fuel type** — Petrol, Electric/EV, or CNG"
            if is_two_wheeler else
            "your preferred **fuel type** — Petrol, Diesel, Hybrid, or Electric/EV"
        ),
        'daily_distance': "your typical **daily riding distance** (e.g., 20 km, 50 km)" if is_two_wheeler else "your typical **daily driving distance** (e.g., 30 km, 50 miles)",
        'road_condition': (
            "your primary **road conditions** — City / Traffic, Highway, Off-Road, Hilly, or Racetrack"
            if is_two_wheeler else
            "the primary **road conditions** you drive on — City, Highway, Rough terrain, or Mixed"
        )
    }

    if len(missing) == 6:
        return (
            "Welcome! To tailor your perfect vehicle selection, "
            "please let me know: are you looking for a **2-Wheeler or a 4-Wheeler**, and what is your **budget**?"
        )

    elif len(missing) > 1:
        first_key = missing[0]
        second_key = missing[1]
        first_lbl = first_key.replace('_', ' ').title()
        second_lbl = second_key.replace('_', ' ').title()
        first_hint = prompts.get(first_key, f"your **{first_lbl}**")
        second_hint = prompts.get(second_key, f"your **{second_lbl}**")
        return (
            f"Got it! Your profile is taking shape.\n\n"
            f"Next, please tell me {first_hint}.\n\n"
            f"Also — {second_hint}?"
        )
    else:
        last_key = missing[0]
        last_hint = prompts.get(last_key, f"your preferred **{last_key.replace('_', ' ').title()}**")
        return f"Almost done! Just one more thing — {last_hint}?"

def clean_vehicle_name(name):
    """Helper to clean vehicle names of CPO/Used tags before searching web/wiki."""
    clean = re.sub(r'(?i)certified\s+', '', name)
    clean = re.sub(r'(?i)pre-owned\s+', '', clean)
    clean = re.sub(r'(?i)used\s+', '', clean)
    clean = re.sub(r'(?i)cpo\s+', '', clean)
    clean = re.sub(r'(?i)\s+ev$', '', clean)
    clean = re.sub(r'(?i)\s+electric$', '', clean)
    clean = re.sub(r'(?i)\s+hybrid$', '', clean)
    clean = re.sub(r'(?i)\s+gen\s+\d+$', '', clean)
    return clean.strip()

# ==================================================
# 🔍 SEARCH ENGINE AND DYNAMIC RECOMMENDATION
# ==================================================
# Master database of vehicles to power the advisor
VEHICLE_DATABASE = [
    # 🛵 2-WHEELER: Electric
    {
        "type": "2-Wheeler", "style": "Scooter", "fuel": "Electric",
        "name": "Ather 450X", "price": "₹ 1.45 Lakh",
        "description": "Premium electric scooter with high-performance warp mode, active touchscreen dashboard, and stellar city maneuverability.",
        "link": "https://www.atherenergy.com/450x"
    },
    {
        "type": "2-Wheeler", "style": "Scooter", "fuel": "Electric",
        "name": "Ola S1 Pro Gen 2", "price": "₹ 1.30 Lakh",
        "description": "High-speed electric scooter boasting a massive 195 km range, cruise control, and futuristic tech features.",
        "link": "https://www.olaelectric.com/s1-pro"
    },
    {
        "type": "2-Wheeler", "style": "Scooter", "fuel": "Electric",
        "name": "TVS iQube ST", "price": "₹ 1.25 Lakh",
        "description": "Elegant, silent, and highly reliable electric family scooter with advanced smart connection and comfortable ride quality.",
        "link": "https://www.tvsmotor.com/electric/iqube"
    },
    # 🛵 2-WHEELER: Scooter (Petrol)
    {
        "type": "2-Wheeler", "style": "Scooter", "fuel": "Petrol",
        "name": "Honda Activa 6G", "price": "₹ 78,000",
        "description": "India's highest selling and most reliable petrol family scooter with a smooth 110cc engine.",
        "link": "https://www.honda2wheelersindia.com/products/scooter/activa-6g"
    },
    {
        "type": "2-Wheeler", "style": "Scooter", "fuel": "Petrol",
        "name": "Suzuki Access 125", "price": "₹ 82,000",
        "description": "Highly popular retro-styled scooter known for its refined 125cc performance and excellent mileage.",
        "link": "https://www.suzukimotorcycle.co.in/product-details/access-125"
    },
    {
        "type": "2-Wheeler", "style": "Scooter", "fuel": "Petrol",
        "name": "TVS Jupiter 125", "price": "₹ 86,000",
        "description": "Practical family scooter featuring class-leading under-seat storage space and superb comfort.",
        "link": "https://www.tvsmotor.com/jupiter-125"
    },
    {
        "type": "2-Wheeler", "style": "Scooter", "fuel": "Petrol",
        "name": "Vespa VXL 150", "price": "₹ 1.45 Lakh",
        "description": "Iconic, premium Italian monocoque steel body scooter offering distinct retro aesthetics and luxury appeal.",
        "link": "https://www.vespaindia.com/"
    },
    {
        "type": "2-Wheeler", "style": "Scooter", "fuel": "Petrol",
        "name": "Aprilia SXR 160", "price": "₹ 1.46 Lakh",
        "description": "Premium maxi-styled scooter with aggressive design, high-speed stability, and comfortable long-distance cruising.",
        "link": "https://www.apriliaindia.com/"
    },
    {
        "type": "2-Wheeler", "style": "Scooter", "fuel": "Petrol",
        "name": "TVS Ntorq 125 XT", "price": "₹ 1.05 Lakh",
        "description": "Tech-loaded sporty scooter with a multi-screen instrument cluster, Bluetooth navigation, and punchy 125cc engine.",
        "link": "https://www.tvsmotor.com/ntorq"
    },
    # 🏍️ 2-WHEELER: Cruiser
    {
        "type": "2-Wheeler", "style": "Cruiser", "fuel": "Petrol",
        "name": "Royal Enfield Bullet 350", "price": "₹ 1.74 Lakh",
        "description": "The legendary icon of Indian motorcycling, offering high torque, signature thumping throb, and classic retro styling.",
        "link": "https://www.royalenfield.com/in/en/motorcycles/bullet/"
    },
    {
        "type": "2-Wheeler", "style": "Cruiser", "fuel": "Petrol",
        "name": "TVS Ronin", "price": "₹ 1.49 Lakh",
        "description": "Modern-retro scrambler cruiser featuring dual-channel ABS, slipper clutch, and highly comfortable city ergonomics.",
        "link": "https://www.tvsmotor.com/tvs-ronin"
    },
    {
        "type": "2-Wheeler", "style": "Cruiser", "fuel": "Petrol",
        "name": "Jawa 350", "price": "₹ 1.99 Lakh",
        "description": "Classy vintage cruiser reborn with modern liquid-cooled tech, deep double exhaust note, and authentic heritage styling.",
        "link": "https://www.jawamotorcycles.com/motorcycles/jawa-350"
    },
    {
        "type": "2-Wheeler", "style": "Cruiser", "fuel": "Petrol",
        "name": "Royal Enfield Meteor 350", "price": "₹ 2.05 Lakh",
        "description": "Classic cruiser offering a smooth highway ride, retro styling, and a refined 350cc engine.",
        "link": "https://www.royalenfield.com/in/en/motorcycles/meteor350/"
    },
    {
        "type": "2-Wheeler", "style": "Cruiser", "fuel": "Petrol",
        "name": "Honda H'ness CB350", "price": "₹ 2.10 Lakh",
        "description": "Modern-retro cruiser with outstanding reliability, assist-slipper clutch, and dual-channel ABS.",
        "link": "https://www.hondabigwing.in/the-hness-cb350/"
    },
    {
        "type": "2-Wheeler", "style": "Cruiser", "fuel": "Petrol",
        "name": "Harley-Davidson X440", "price": "₹ 2.40 Lakh",
        "description": "Premium entry-level cruiser co-developed with Hero, offering signature Harley styling and high torque.",
        "link": "https://www.harley-davidson.com/in/en/motorcycles/street.html"
    },
    # 🏍️ 2-WHEELER: Superbike / Sports
    {
        "type": "2-Wheeler", "style": "Superbike", "fuel": "Petrol",
        "name": "Yamaha YZF-R15 V4", "price": "₹ 1.82 Lakh",
        "description": "Track-inspired entry-level sports bike featuring traction control, quickshifter, and aggressive aerodynamic styling.",
        "link": "https://www.yamaha-motor-india.com/yamaha-r15v4.html"
    },
    {
        "type": "2-Wheeler", "style": "Superbike", "fuel": "Petrol",
        "name": "Suzuki Gixxer SF 250", "price": "₹ 1.92 Lakh",
        "description": "Refined quarter-litre sports tourer powered by a unique oil-cooled engine, offering comfortable sporty riding.",
        "link": "https://www.suzukimotorcycle.co.in/product-details/gixxer-sf-250"
    },
    {
        "type": "2-Wheeler", "style": "Superbike", "fuel": "Petrol",
        "name": "Hero Karizma XMR", "price": "₹ 1.80 Lakh",
        "description": "Reborn sports icon featuring modern DOHC liquid-cooled engine and adjustable windshield.",
        "link": "https://www.heromotocorp.com/en-in/motorcycles/performance/karizma-xmr.html"
    },
    {
        "type": "2-Wheeler", "style": "Superbike", "fuel": "Petrol",
        "name": "KTM RC 390", "price": "₹ 3.18 Lakh",
        "description": "Purebred track machine with cornering ABS, traction control, and unmatched power-to-weight ratio.",
        "link": "https://www.ktmindia.com/en/ktm-rc-390.html"
    },
    {
        "type": "2-Wheeler", "style": "Superbike", "fuel": "Petrol",
        "name": "TVS Apache RR 310", "price": "₹ 2.72 Lakh",
        "description": "Highly advanced sport bike featuring riding modes, smart Bluetooth connectivity, and excellent track dynamics.",
        "link": "https://www.tvsmotor.com/tvs-apache/rr-310"
    },
    {
        "type": "2-Wheeler", "style": "Superbike", "fuel": "Petrol",
        "name": "Kawasaki Ninja 300", "price": "₹ 3.43 Lakh",
        "description": "Smooth parallel-twin entry-level sports bike with legendary reliability and racing heritage styling.",
        "link": "https://www.kawasaki.co.in/models/Ninja300/"
    },
    {
        "type": "2-Wheeler", "style": "Superbike", "fuel": "Petrol",
        "name": "Kawasaki Ninja 400", "price": "₹ 5.20 Lakh",
        "description": "High-performance twin-cylinder sport bike with aggressive styling and race-replica ergonomics.",
        "link": "https://www.kawasaki.co.in/models/Ninja400/"
    },
    {
        "type": "2-Wheeler", "style": "Superbike", "fuel": "Petrol",
        "name": "Yamaha YZF-R3", "price": "₹ 4.60 Lakh",
        "description": "Agile and track-ready sport bike powered by a liquid-cooled parallel-twin engine.",
        "link": "https://www.yamaha-motor-india.com/yzf-r3.html"
    },
    {
        "type": "2-Wheeler", "style": "Superbike", "fuel": "Petrol",
        "name": "Kawasaki Ninja ZX-4R", "price": "₹ 8.49 Lakh",
        "description": "Extremely high-revving 4-cylinder screamer producing 77 PS of power, offering true racetrack capabilities.",
        "link": "https://www.kawasaki.co.in/models/ninja-zx-4r/"
    },
    # 🏍️ 2-WHEELER: Naked / Street
    {
        "type": "2-Wheeler", "style": "Naked / Street", "fuel": "Petrol",
        "name": "TVS Raider 125", "price": "₹ 95,000",
        "description": "Sporty commuter 125cc bike with riding modes, digital console, and class-leading refinement.",
        "link": "https://www.tvsmotor.com/tvs-raider"
    },
    {
        "type": "2-Wheeler", "style": "Naked / Street", "fuel": "Petrol",
        "name": "TVS Apache RTR 160 4V", "price": "₹ 1.24 Lakh",
        "description": "Punchy 160cc streetfighter featuring a highly refined oil-cooled engine, smart connection, and top-tier handling.",
        "link": "https://www.tvsmotor.com/tvs-apache"
    },
    {
        "type": "2-Wheeler", "style": "Naked / Street", "fuel": "Petrol",
        "name": "Honda SP125", "price": "₹ 86,000",
        "description": "Highly refined, silent-start commuter bike with outstanding fuel efficiency and premium LED styling.",
        "link": "https://www.honda2wheelersindia.com/products/motorcycle/sp125"
    },
    {
        "type": "2-Wheeler", "style": "Naked / Street", "fuel": "Petrol",
        "name": "Yamaha MT-15 V2", "price": "₹ 1.68 Lakh",
        "description": "Aggressive streetfighter powered by the legendary R15 engine, featuring Variable Valve Actuation (VVA) and traction control.",
        "link": "https://www.yamaha-motor-india.com/yamaha-mt-15-v2.html"
    },
    {
        "type": "2-Wheeler", "style": "Naked / Street", "fuel": "Petrol",
        "name": "KTM Duke 250", "price": "₹ 2.39 Lakh",
        "description": "Premium quarter-litre street bike with advanced styling, quickshifter, and aggressive Duke attitude.",
        "link": "https://www.ktmindia.com/en/ktm-duke-250.html"
    },
    {
        "type": "2-Wheeler", "style": "Naked / Street", "fuel": "Petrol",
        "name": "Triumph Speed 400", "price": "₹ 2.33 Lakh",
        "description": "Beautifully crafted British street roadster co-developed with Bajaj, offering punchy 40 PS power and superb styling.",
        "link": "https://www.triumphmotorcycles.in/motorcycles/roadsters/speed-400"
    },
    {
        "type": "2-Wheeler", "style": "Naked / Street", "fuel": "Petrol",
        "name": "KTM Duke 390", "price": "₹ 3.11 Lakh",
        "description": "The ultimate pocket-rocket streetfighter featuring cornering ABS, launch control, and adjustable suspension.",
        "link": "https://www.ktmindia.com/en/ktm-duke-390.html"
    },
    {
        "type": "2-Wheeler", "style": "Naked / Street", "fuel": "Petrol",
        "name": "Triumph Street Triple R", "price": "₹ 10.17 Lakh",
        "description": "Bespoke high-performance triple-cylinder naked bike with racetrack suspension and razor-sharp handling.",
        "link": "https://www.triumphmotorcycles.in/motorcycles/roadsters/street-triple"
    },
    {
        "type": "2-Wheeler", "style": "Naked / Street", "fuel": "Petrol",
        "name": "Kawasaki Z900", "price": "₹ 9.38 Lakh",
        "description": "Silky smooth inline-four super-naked motorcycle offering explosive performance and aggressive Sugomi styling.",
        "link": "https://www.kawasaki.co.in/models/z900/"
    },
    # 🏍️ 2-WHEELER: Cafe Racer
    {
        "type": "2-Wheeler", "style": "Cafe Racer", "fuel": "Petrol",
        "name": "Royal Enfield Hunter 350", "price": "₹ 1.50 Lakh",
        "description": "Agile, modern-retro roadster cafe racer with a sporty chassis and easy maneuverability.",
        "link": "https://www.royalenfield.com/in/en/motorcycles/hunter-350/"
    },
    {
        "type": "2-Wheeler", "style": "Cafe Racer", "fuel": "Petrol",
        "name": "Husqvarna Vitpilen 250", "price": "₹ 2.19 Lakh",
        "description": "Striking neo-retro Swedish cafe racer with a highly futuristic look and dynamic DOHC engine.",
        "link": "https://www.husqvarna-motorcycles.com/"
    },
    {
        "type": "2-Wheeler", "style": "Cafe Racer", "fuel": "Petrol",
        "name": "Royal Enfield Classic 350", "price": "₹ 1.93 Lakh",
        "description": "Classic post-war design cruiser with modern refinement, comfortable upright riding, and timeless appeal.",
        "link": "https://www.royalenfield.com/in/en/motorcycles/classic350/"
    },
    {
        "type": "2-Wheeler", "style": "Cafe Racer", "fuel": "Petrol",
        "name": "Royal Enfield Continental GT 650", "price": "₹ 3.19 Lakh",
        "description": "Pure cafe racer powered by a twin-cylinder 650cc engine, featuring clip-on handlebars and retro racing fuel tank.",
        "link": "https://www.royalenfield.com/in/en/motorcycles/continental-gt/"
    },
    {
        "type": "2-Wheeler", "style": "Cafe Racer", "fuel": "Petrol",
        "name": "Triumph Speed Twin 900", "price": "₹ 8.49 Lakh",
        "description": "Bespoke modern classic British retro roadster offering incredible torque, sound, and premium finishes.",
        "link": "https://www.triumphmotorcycles.in/motorcycles/classic/speed-twin-900"
    },
    # 🏍️ 2-WHEELER: Adventure Bike
    {
        "type": "2-Wheeler", "style": "Adventure Bike", "fuel": "Petrol",
        "name": "Hero XPulse 200 4V", "price": "₹ 1.46 Lakh",
        "description": "True lightweight off-road/dirt bike with long-travel suspension, high ground clearance, and spoked wheels.",
        "link": "https://www.heromotocorp.com/en-in/motorcycles/performance/xpulse-200-4v.html"
    },
    {
        "type": "2-Wheeler", "style": "Adventure Bike", "fuel": "Petrol",
        "name": "Honda CB200X", "price": "₹ 1.47 Lakh",
        "description": "Urban adventure-themed motorcycle offering comfortable upright ergonomics and block-pattern tires.",
        "link": "https://www.honda2wheelersindia.com/products/motorcycle/cb200x"
    },
    {
        "type": "2-Wheeler", "style": "Adventure Bike", "fuel": "Petrol",
        "name": "Royal Enfield Himalayan 450", "price": "₹ 2.85 Lakh",
        "description": "Versatile adventure tourer built for rough terrains, featuring a liquid-cooled Sherpa 450 engine.",
        "link": "https://www.royalenfield.com/in/en/motorcycles/himalayan/"
    },
    {
        "type": "2-Wheeler", "style": "Adventure Bike", "fuel": "Petrol",
        "name": "BMW G 310 GS", "price": "₹ 3.30 Lakh",
        "description": "Premium adventure entry-level motorcycle from BMW, offering excellent build quality and comfort.",
        "link": "https://www.bmw-motorrad-india.com/en/models/adventure/g310gs.html"
    },
    {
        "type": "2-Wheeler", "style": "Adventure Bike", "fuel": "Petrol",
        "name": "KTM 390 Adventure", "price": "₹ 3.60 Lakh",
        "description": "Feature-rich adventure bike with fully adjustable suspension, quickshifter, and cornering traction control.",
        "link": "https://www.ktmindia.com/en/ktm-390-adventure.html"
    },

    # 🚗 4-WHEELER: Electric
    {
        "type": "4-Wheeler", "style": "Hatchback", "fuel": "Electric",
        "name": "Tata Tiago EV", "price": "₹ 8.0 Lakh",
        "description": "Highly affordable electric hatchback featuring good range, silent drive, and premium connectivity.",
        "link": "https://www.tatamotors.com/cars/tiago-ev/"
    },
    {
        "type": "4-Wheeler", "style": "Hatchback", "fuel": "Electric",
        "name": "MG Comet EV", "price": "₹ 7.0 Lakh",
        "description": "Ultra-compact electric city car, extremely easy to park and navigate through dense traffic.",
        "link": "https://www.mgmotor.co.in/vehicles/mgcomet"
    },
    {
        "type": "4-Wheeler", "style": "SUV", "fuel": "Electric",
        "name": "Tata Punch EV", "price": "₹ 11.0 Lakh",
        "description": "Compact electric SUV built on the advanced active.ev architecture with long range.",
        "link": "https://www.tatamotors.com/cars/punch-ev/"
    },
    {
        "type": "4-Wheeler", "style": "SUV", "fuel": "Electric",
        "name": "Tata Nexon EV", "price": "₹ 14.5 Lakh",
        "description": "India's bestselling electric SUV featuring long range, elegant styling, and an advanced connected infotainment system.",
        "link": "https://www.tatamotors.com/cars/nexon-ev/"
    },
    {
        "type": "4-Wheeler", "style": "SUV", "fuel": "Electric",
        "name": "MG ZS EV", "price": "₹ 18.9 Lakh",
        "description": "Highly premium electric SUV with a 50.3 kWh battery, panoramic sunroof, and level 2 ADAS features.",
        "link": "https://www.mgmotor.co.in/vehicles/mgzsev"
    },
    {
        "type": "4-Wheeler", "style": "SUV", "fuel": "Electric",
        "name": "BYD Atto 3", "price": "₹ 25.0 Lakh",
        "description": "Futuristic premium electric SUV with a rotating touchscreen, ADAS, and a ultra-safe Blade battery.",
        "link": "https://www.bydautoindia.com/byd-atto3"
    },
    {
        "type": "4-Wheeler", "style": "SUV", "fuel": "Electric",
        "name": "Hyundai Ioniq 5", "price": "₹ 46.8 Lakh",
        "description": "Retro-futuristic electric crossover built on E-GMP platform, featuring 800V ultra-fast charging.",
        "link": "https://www.hyundai.com/in/en/find-a-car/ioniq-5"
    },
    {
        "type": "4-Wheeler", "style": "SUV", "fuel": "Electric",
        "name": "Kia EV6", "price": "₹ 60.9 Lakh",
        "description": "Striking, luxury electric crossover with high performance, a sporty cabin, and long-range capability.",
        "link": "https://www.kia.com/in/our-vehicles/ev6"
    },
    {
        "type": "4-Wheeler", "style": "SUV", "fuel": "Electric",
        "name": "Volvo XC40 Recharge", "price": "₹ 57.9 Lakh",
        "description": "Luxury electric SUV from Volvo featuring dual motors, 408 hp, and top-tier safety standards.",
        "link": "https://www.volvocars.com/en-in/cars/models/xc40/xc40-electric"
    },
    {
        "type": "4-Wheeler", "style": "Sedan", "fuel": "Electric",
        "name": "Audi e-tron GT", "price": "₹ 1.7 Crore",
        "description": "Bespoke luxury electric grand tourer with breathtaking design, supercar performance, and high-tech cabin.",
        "link": "https://www.audi.in/en/models/e-tron-gt.html"
    },
    {
        "type": "4-Wheeler", "style": "Sedan", "fuel": "Electric",
        "name": "BMW i7", "price": "₹ 2.1 Crore",
        "description": "The ultimate luxury electric sedan, featuring a massive 31.3-inch rear theater screen and absolute cabin serenity.",
        "link": "https://www.bmw.in/en/all-models/7-series/i7/"
    },
    {
        "type": "4-Wheeler", "style": "Sedan", "fuel": "Electric",
        "name": "Porsche Taycan", "price": "₹ 1.6 Crore",
        "description": "High-performance luxury electric sports sedan offering Porsche's handling dynamics and premium craftsmanship.",
        "link": "https://www.porsche.com/india/models/taycan/"
    },

    # 🚗 4-WHEELER: SUV (Petrol/Diesel)
    {
        "type": "4-Wheeler", "style": "SUV", "fuel": "Petrol",
        "name": "Certified Pre-Owned Mahindra Bolero", "price": "₹ 3.8 Lakh",
        "description": "Rugged, ladder-frame utility vehicle, perfect for rough roads and off-road driving, offering top value.",
        "link": "https://www.cars24.com/buy-used-mahindra-bolero-cars/"
    },
    {
        "type": "4-Wheeler", "style": "SUV", "fuel": "Petrol",
        "name": "Certified Pre-Owned Ford EcoSport", "price": "₹ 4.2 Lakh",
        "description": "Premium urban compact SUV known for solid build quality, excellent handling, and safety features.",
        "link": "https://www.cars24.com/buy-used-ford-ecosport-cars/"
    },
    {
        "type": "4-Wheeler", "style": "SUV", "fuel": "Petrol",
        "name": "Certified Pre-Owned Maruti Suzuki Vitara Brezza", "price": "₹ 4.5 Lakh",
        "description": "Highly reliable, spacious, and fuel-efficient family SUV with superb safety ratings.",
        "link": "https://www.cars24.com/buy-used-maruti-suzuki-vitara-brezza-cars/"
    },
    {
        "type": "4-Wheeler", "style": "SUV", "fuel": "Petrol",
        "name": "Tata Punch", "price": "₹ 6.1 Lakh",
        "description": "Highly popular micro-SUV with robust build quality, excellent 5-star safety, and great city utility.",
        "link": "https://www.tatamotors.com/cars/punch/"
    },
    {
        "type": "4-Wheeler", "style": "SUV", "fuel": "Petrol",
        "name": "Nissan Magnite", "price": "₹ 6.0 Lakh",
        "description": "Spacious and feature-rich compact SUV with a powerful turbo-petrol option and high ground clearance.",
        "link": "https://www.nissan.in/vehicles/new/magnite.html"
    },
    {
        "type": "4-Wheeler", "style": "SUV", "fuel": "Petrol",
        "name": "Renault Kiger", "price": "₹ 6.5 Lakh",
        "description": "Sporty and modern compact SUV offering class-leading boot space and strong value-for-money.",
        "link": "https://www.renault.co.in/cars/renault-kiger.html"
    },
    {
        "type": "4-Wheeler", "style": "SUV", "fuel": "Petrol",
        "name": "Hyundai Exter", "price": "₹ 6.13 Lakh",
        "description": "Smart, brand-new micro SUV packed with modern technology, 6 standard airbags, and a segment-first dual camera dashcam.",
        "link": "https://www.hyundai.com/in/en/find-a-car/exter"
    },
    {
        "type": "4-Wheeler", "style": "SUV", "fuel": "Petrol",
        "name": "Mahindra XUV3XO", "price": "₹ 7.49 Lakh",
        "description": "Bespoke compact SUV featuring level 2 ADAS, panoramic sunroof, and a very quiet refined cabin.",
        "link": "https://auto.mahindra.com/suv/xuv3xo"
    },
    {
        "type": "4-Wheeler", "style": "SUV", "fuel": "Petrol",
        "name": "Kia Sonet", "price": "₹ 7.99 Lakh",
        "description": "Premium brand-new compact SUV with ventilated front seats, premium Bose sound system, and sharp styling.",
        "link": "https://www.kia.com/in/our-vehicles/sonet"
    },
    {
        "type": "4-Wheeler", "style": "SUV", "fuel": "Petrol",
        "name": "Mahindra Bolero Neo", "price": "₹ 9.9 Lakh",
        "description": "Rugged, ladder-frame SUV designed to handle rough/off-road terrains with absolute ease.",
        "link": "https://auto.mahindra.com/suv/bolero-neo"
    },
    {
        "type": "4-Wheeler", "style": "SUV", "fuel": "Petrol",
        "name": "Tata Nexon", "price": "₹ 8.0 Lakh",
        "description": "High-tech compact SUV with superb 5-star safety rating, comfortable cabin, and punchy engine options.",
        "link": "https://www.tatamotors.com/cars/nexon/"
    },
    {
        "type": "4-Wheeler", "style": "SUV", "fuel": "Petrol",
        "name": "Hyundai Venue", "price": "₹ 7.9 Lakh",
        "description": "Feature-loaded urban SUV with responsive turbo engine options and supreme cabin refinement.",
        "link": "https://www.hyundai.com/in/en/find-a-car/venue"
    },
    {
        "type": "4-Wheeler", "style": "SUV", "fuel": "Petrol",
        "name": "Mahindra XUV700", "price": "₹ 14.0 Lakh",
        "description": "Sophisticated mid-size SUV featuring dual screens, powerful diesel/petrol engines, and level 2 ADAS.",
        "link": "https://auto.mahindra.com/suv/xuv700"
    },
    {
        "type": "4-Wheeler", "style": "SUV", "fuel": "Petrol",
        "name": "Tata Safari", "price": "₹ 16.2 Lakh",
        "description": "Flagship 3-row luxury SUV with bold styling, premium ventilated seats, and outstanding road presence.",
        "link": "https://www.tatamotors.com/cars/safari/"
    },
    {
        "type": "4-Wheeler", "style": "SUV", "fuel": "Petrol",
        "name": "Hyundai Creta", "price": "₹ 11.0 Lakh",
        "description": "The benchmark mid-size SUV offering a highly refined ride, panoramic sunroof, and excellent resale value.",
        "link": "https://www.hyundai.com/in/en/find-a-car/creta"
    },
    {
        "type": "4-Wheeler", "style": "SUV", "fuel": "Petrol",
        "name": "Toyota Fortuner", "price": "₹ 33.4 Lakh",
        "description": "Legendary SUV known for its bulletproof reliability, massive road presence, and incredible off-road capabilities.",
        "link": "https://www.toyotabharat.com/cars/fortuner/"
    },
    {
        "type": "4-Wheeler", "style": "SUV", "fuel": "Petrol",
        "name": "Jeep Compass", "price": "₹ 20.7 Lakh",
        "description": "Premium compact SUV offering true American off-road DNA, class-leading ride dynamics, and a high-end cabin.",
        "link": "https://www.jeep-india.com/all-vehicles/compass.html"
    },
    {
        "type": "4-Wheeler", "style": "SUV", "fuel": "Petrol",
        "name": "Hyundai Tucson", "price": "₹ 29.0 Lakh",
        "description": "Flagship premium SUV featuring parametric lighting design, HTRAC AWD system, and a spacious, whisper-quiet cabin.",
        "link": "https://www.hyundai.com/in/en/find-a-car/tucson"
    },
    {
        "type": "4-Wheeler", "style": "SUV", "fuel": "Petrol",
        "name": "Range Rover Sport", "price": "₹ 1.7 Crore",
        "description": "The definition of luxury off-roading, combining peerless British design, high-end air suspension, and dynamic engines.",
        "link": "https://www.landrover.in/vehicles/range-rover-sport/"
    },
    {
        "type": "4-Wheeler", "style": "SUV", "fuel": "Petrol",
        "name": "Porsche Cayenne", "price": "₹ 1.4 Crore",
        "description": "The sportscar of luxury SUVs, offering unmatched on-road handling and an exceptionally crafted digital cockpit.",
        "link": "https://www.porsche.com/india/models/cayenne/"
    },
    {
        "type": "4-Wheeler", "style": "SUV", "fuel": "Petrol",
        "name": "BMW X5", "price": "₹ 96.0 Lakh",
        "description": "Elite luxury SUV offering an ideal blend of performance, technology, and spacious comfort.",
        "link": "https://www.bmw.in/en/all-models/x-series/x5/"
    },

    # 🚗 4-WHEELER: Sedan
    {
        "type": "4-Wheeler", "style": "Sedan", "fuel": "Petrol",
        "name": "Certified Pre-Owned Honda Amaze", "price": "₹ 3.8 Lakh",
        "description": "Extremely reliable compact sedan with a smooth CVT gearbox and premium cabin space.",
        "link": "https://www.cars24.com/buy-used-honda-amaze-cars/"
    },
    {
        "type": "4-Wheeler", "style": "Sedan", "fuel": "Petrol",
        "name": "Certified Pre-Owned Maruti Suzuki Dzire", "price": "₹ 3.5 Lakh",
        "description": "India's highest-selling sedan, offering superb mileage, low maintenance, and excellent comfort.",
        "link": "https://www.cars24.com/buy-used-maruti-suzuki-dzire-cars/"
    },
    {
        "type": "4-Wheeler", "style": "Sedan", "fuel": "Petrol",
        "name": "Certified Pre-Owned Hyundai Xcent", "price": "₹ 3.2 Lakh",
        "description": "Premium features, silent cabin, and smooth ride quality makes this pre-owned sedan a stellar value.",
        "link": "https://www.cars24.com/buy-used-hyundai-xcent-cars/"
    },
    {
        "type": "4-Wheeler", "style": "Sedan", "fuel": "Petrol",
        "name": "Maruti Suzuki Dzire", "price": "₹ 6.5 Lakh",
        "description": "India's highest-selling sedan, offering superb mileage, low maintenance, and excellent comfort.",
        "link": "https://www.marutisuzuki.com/cars/dzire"
    },
    {
        "type": "4-Wheeler", "style": "Sedan", "fuel": "Petrol",
        "name": "Tata Tigor", "price": "₹ 6.3 Lakh",
        "description": "Stylish and safe compact sedan offering a 4-star safety rating, great cabin space, and premium features.",
        "link": "https://www.tatamotors.com/cars/tigor/"
    },
    {
        "type": "4-Wheeler", "style": "Sedan", "fuel": "Petrol",
        "name": "Hyundai Aura", "price": "₹ 6.5 Lakh",
        "description": "Modern and feature-packed compact sedan offering a highly refined engine and comfortable ride.",
        "link": "https://www.hyundai.com/in/en/find-a-car/aura"
    },
    {
        "type": "4-Wheeler", "style": "Sedan", "fuel": "Petrol",
        "name": "Hyundai Verna", "price": "₹ 11.0 Lakh",
        "description": "Futuristic fastback sedan with a powerful 1.5L turbo-petrol engine, ventilated seats, and level 2 ADAS.",
        "link": "https://www.hyundai.com/in/en/find-a-car/verna"
    },
    {
        "type": "4-Wheeler", "style": "Sedan", "fuel": "Petrol",
        "name": "Skoda Slavia", "price": "₹ 11.5 Lakh",
        "description": "European elegance coupled with excellent ride and handling, offering a massive 521-litre boot.",
        "link": "https://www.skoda-auto.co.in/models/slavia"
    },
    {
        "type": "4-Wheeler", "style": "Sedan", "fuel": "Petrol",
        "name": "Honda City", "price": "₹ 11.8 Lakh",
        "description": "The gold standard of mid-size sedans, offering a comfortable rear seat, reliable i-VTEC engine, and ADAS.",
        "link": "https://www.hondacarindia.com/honda-city"
    },
    {
        "type": "4-Wheeler", "style": "Sedan", "fuel": "Petrol",
        "name": "Skoda Superb", "price": "₹ 34.0 Lakh",
        "description": "Flagship Skoda sedan offering luxury space, legendary ride quality, and premium features matching German standards.",
        "link": "https://www.skoda-auto.co.in/"
    },
    {
        "type": "4-Wheeler", "style": "Sedan", "fuel": "Petrol",
        "name": "Toyota Camry Hybrid", "price": "₹ 46.0 Lakh",
        "description": "Self-charging luxury hybrid sedan offering exceptional fuel efficiency, whisper-quiet cabin, and rear seat reclining comfort.",
        "link": "https://www.toyotabharat.com/cars/camry/"
    },
    {
        "type": "4-Wheeler", "style": "Sedan", "fuel": "Petrol",
        "name": "Certified Pre-Owned Audi A4", "price": "₹ 28.0 Lakh",
        "description": "Excellent entry into luxury German engineering, offering dynamic drive, digital cockpit, and premium sound.",
        "link": "https://www.cars24.com/buy-used-audi-a4-cars/"
    },
    {
        "type": "4-Wheeler", "style": "Sedan", "fuel": "Petrol",
        "name": "BMW 3 Series Gran Limousine", "price": "₹ 60.6 Lakh",
        "description": "Class-leading executive sedan offering extended wheelbase, superb rear legroom, and signature BMW driving dynamics.",
        "link": "https://www.bmw.in/en/all-models/3-series/3-series-gran-limousine/"
    },
    {
        "type": "4-Wheeler", "style": "Sedan", "fuel": "Petrol",
        "name": "Mercedes-Benz C-Class", "price": "₹ 61.8 Lakh",
        "description": "Often called the baby S-Class, offering a highly luxurious interior with a large vertical screen.",
        "link": "https://www.mercedes-benz.co.in/passengercars/models/saloon/c-class/"
    },
    {
        "type": "4-Wheeler", "style": "Sedan", "fuel": "Petrol",
        "name": "Audi A4", "price": "₹ 46.0 Lakh",
        "description": "Refined luxury sedan featuring a silent cabin, smooth TFSI engine, and a very comfortable ride quality.",
        "link": "https://www.audi.in/en/models/a4.html"
    },
    {
        "type": "4-Wheeler", "style": "Sedan", "fuel": "Petrol",
        "name": "Mercedes-Benz S-Class", "price": "₹ 1.8 Crore",
        "description": "The absolute pinnacle of luxury sedans, offering rear-seat reclining calf-massage seats and industry-leading ride comfort.",
        "link": "https://www.mercedes-benz.co.in/passengercars/models/saloon/s-class/"
    },
    {
        "type": "4-Wheeler", "style": "Sedan", "fuel": "Petrol",
        "name": "BMW 7 Series", "price": "₹ 1.8 Crore",
        "description": "Futuristic flagship luxury sedan featuring a cinematic rear theater screen and executive lounge seating.",
        "link": "https://www.bmw.in/en/all-models/7-series/"
    },
    {
        "type": "4-Wheeler", "style": "Sedan", "fuel": "Petrol",
        "name": "Audi A8 L", "price": "₹ 1.3 Crore",
        "description": "Premium aluminum spaceframe luxury sedan with predictive active suspension and aircraft-style seating.",
        "link": "https://www.audi.in/en/models/a8.html"
    },

    # 🚗 4-WHEELER: Hatchback
    {
        "type": "4-Wheeler", "style": "Hatchback", "fuel": "Petrol",
        "name": "Tata Tiago", "price": "₹ 5.6 Lakh",
        "description": "Safe, premium, and feature-rich hatchback with excellent 4-star safety rating and great sound system.",
        "link": "https://www.tatamotors.com/cars/tiago/"
    },
    {
        "type": "4-Wheeler", "style": "Hatchback", "fuel": "Petrol",
        "name": "Maruti Suzuki WagonR", "price": "₹ 5.5 Lakh",
        "description": "Extremely practical tall-boy hatchback offering unmatched cabin space, high fuel efficiency, and practicality.",
        "link": "https://www.marutisuzuki.com/cars/wagon-r"
    },
    {
        "type": "4-Wheeler", "style": "Hatchback", "fuel": "Petrol",
        "name": "Hyundai Grand i10 Nios", "price": "₹ 5.9 Lakh",
        "description": "Highly refined and premium hatchback offering a quiet cabin, smooth engine, and premium features.",
        "link": "https://www.hyundai.com/in/en/find-a-car/grand-i10-nios"
    },
    {
        "type": "4-Wheeler", "style": "Hatchback", "fuel": "Petrol",
        "name": "Hyundai i20 N Line", "price": "₹ 10.0 Lakh",
        "description": "Premium hot hatch with sporty exhaust note, stiffened suspension, and excellent steering feedback.",
        "link": "https://www.hyundai.com/in/en/find-a-car/i20-n-line"
    },
    {
        "type": "4-Wheeler", "style": "Hatchback", "fuel": "Petrol",
        "name": "Tata Altroz", "price": "₹ 6.6 Lakh",
        "description": "Premium hatchback with a 5-star global NCAP safety rating and sleek design language.",
        "link": "https://www.tatamotors.com/cars/altroz/"
    },
    {
        "type": "4-Wheeler", "style": "Hatchback", "fuel": "Petrol",
        "name": "Maruti Suzuki Baleno", "price": "₹ 6.6 Lakh",
        "description": "Feature-packed premium hatchback with a highly fuel-efficient K-series engine.",
        "link": "https://www.nexaexperience.com/baleno"
    },
    # 🏍️ 2-WHEELER: Pre-Owned
    {
        "type": "2-Wheeler", "style": "Naked / Street", "fuel": "Petrol",
        "name": "Certified Pre-Owned KTM Duke 200", "price": "₹ 1.20 Lakh",
        "description": "Exhilarating entry-level streetfighter in excellent condition, offering high performance at a great value.",
        "link": "https://www.orangebookvalue.com/"
    },
    {
        "type": "2-Wheeler", "style": "Cruiser", "fuel": "Petrol",
        "name": "Certified Pre-Owned Royal Enfield Classic 350", "price": "₹ 1.30 Lakh",
        "description": "Timeless retro cruiser with signature thump, well-maintained and perfect for daily commutes and touring.",
        "link": "https://www.orangebookvalue.com/"
    },
    {
        "type": "2-Wheeler", "style": "Scooter", "fuel": "Petrol",
        "name": "Certified Pre-Owned Honda Activa 5G", "price": "₹ 45,000",
        "description": "India's favorite family scooter, highly reliable, easy to ride, and offering superb mileage.",
        "link": "https://www.orangebookvalue.com/"
    },
    {
        "type": "2-Wheeler", "style": "Naked / Street", "fuel": "Petrol",
        "name": "Certified Pre-Owned TVS Apache RTR 160", "price": "₹ 75,000",
        "description": "Sporty city commuter with track-tuned suspension and responsive performance, perfect for daily riding.",
        "link": "https://www.orangebookvalue.com/"
    },
    {
        "type": "2-Wheeler", "style": "Scooter", "fuel": "Petrol",
        "name": "Certified Pre-Owned Suzuki Access 125", "price": "₹ 55,000",
        "description": "Power-packed 125cc scooter with retro styling, offering high comfort and smooth performance.",
        "link": "https://www.orangebookvalue.com/"
    },
    {
        "type": "2-Wheeler", "style": "Adventure Bike", "fuel": "Petrol",
        "name": "Certified Pre-Owned Royal Enfield Himalayan 411", "price": "₹ 1.60 Lakh",
        "description": "Highly capable and simple adventure motorcycle, built for rough terrains and high altitude touring.",
        "link": "https://www.orangebookvalue.com/"
    },
    {
        "type": "2-Wheeler", "style": "Superbike", "fuel": "Petrol",
        "name": "Certified Pre-Owned KTM RC 200", "price": "₹ 1.40 Lakh",
        "description": "Track-oriented street bike in immaculate condition, offering sharp handling and high-revving performance.",
        "link": "https://www.orangebookvalue.com/"
    },
    {
        "type": "2-Wheeler", "style": "Cafe Racer", "fuel": "Petrol",
        "name": "Certified Pre-Owned Royal Enfield Continental GT 535", "price": "₹ 1.80 Lakh",
        "description": "Retro British cafe racer styled single-cylinder touring bike, offering immense character and classic design.",
        "link": "https://www.orangebookvalue.com/"
    },
    {
        "type": "4-Wheeler", "style": "Hatchback", "fuel": "Petrol",
        "name": "Certified Pre-Owned Maruti Swift", "price": "₹ 4.50 Lakh",
        "description": "Fun-to-drive sporty hatchback with low maintenance costs and excellent city ride comfort.",
        "link": "https://www.cars24.com/"
    },
    {
        "type": "4-Wheeler", "style": "Coupe", "fuel": "Petrol",
        "name": "Certified Pre-Owned Ford Mustang GT", "price": "₹ 55.0 Lakh",
        "description": "Legendary V8 muscle car in pristine condition, offering incredible performance and unmatched road presence.",
        "link": "https://www.cars24.com/"
    }
]

def parse_price_to_lakh(price_str):
    try:
        price_str_clean = price_str.replace('₹', '').replace(',', '').strip().lower()
        if 'crore' in price_str_clean or 'cr' in price_str_clean:
            nums = re.findall(r'\d+(?:\.\d+)?', price_str_clean)
            return float(nums[0]) * 100 if nums else 0.0
        elif 'lakh' in price_str_clean or 'l' in price_str_clean:
            nums = re.findall(r'\d+(?:\.\d+)?', price_str_clean)
            return float(nums[0]) if nums else 0.0
        else:
            nums = re.findall(r'\d+(?:\.\d+)?', price_str_clean)
            return float(nums[0]) / 100000.0 if nums else 0.0
    except:
        return 0.0

def get_candidate_vehicles(profile, refinement_prompt=None):
    v_type = profile.get('type')
    style = profile.get('body_style', 'SUV')
    fuel = profile.get('fuel_type', 'Petrol')
    budget_str = profile.get('budget', '')
    
    budget_val = 50.0  # default
    try:
        nums = re.findall(r'\d+(?:\.\d+)?', budget_str)
        if nums:
            budget_val = float(nums[0])
            if 'cr' in budget_str.lower() or 'crore' in budget_str.lower():
                budget_val *= 100
            elif 'lakh' in budget_str.lower() or 'lac' in budget_str.lower():
                pass
            elif 'k' in budget_str.lower():
                budget_val /= 100
    except:
        pass

    # Determine condition preference (Brand New vs Pre-Owned)
    condition_pref = profile.get('condition', 'Brand New')
    condition_changed = False
    if refinement_prompt:
        ref_lower = refinement_prompt.lower()
        new_cond = None
        if any(w in ref_lower for w in ["brand new", "new car", "new cars", "new models", "new model", "not used", "not pre-owned"]):
            new_cond = "Brand New"
        elif any(w in ref_lower for w in ["pre-owned", "used", "second hand", "cpo", "certified"]):
            new_cond = "Pre-Owned"
            
        if new_cond and new_cond != condition_pref:
            condition_pref = new_cond
            profile['condition'] = new_cond
            condition_changed = True

    # Scoring candidates
    scored_candidates = []
    for v in VEHICLE_DATABASE:
        if v['type'] != v_type:
            continue
            
        score = 100.0
        
        # 1. Price scoring
        v_price = parse_price_to_lakh(v['price'])
        price_ratio = v_price / budget_val if budget_val > 0 else 1.0
        
        if v_price > budget_val:
            # Over budget penalties
            if price_ratio > 1.5:
                # Disqualify if way over budget (more than 50% over budget)
                score -= 1000.0
            elif price_ratio > 1.15:
                # Moderate/heavy penalty for 15% - 50% stretch
                score -= (v_price - budget_val) * 15.0
            else:
                # Light penalty for minor stretch (up to 15% budget stretch)
                score -= (v_price - budget_val) * 3.0
        else:
            # Under budget (we prefer matches close to the budget to provide best value)
            score -= (budget_val - v_price) * 0.2
            
        # 2. Fuel type match
        v_fuel = v.get('fuel', 'Petrol')
        if fuel == 'Electric':
            if v_fuel != 'Electric':
                score -= 200.0  # heavy penalty for non-EV when EV requested
        else:
            if v_fuel == 'Electric':
                score -= 200.0  # heavy penalty for EV when non-EV requested
            elif fuel != v_fuel:
                score -= 40.0
                
        # 3. Style match
        if v['style'] != style:
            score -= 120.0
            
        # 4. Condition match
        is_pre_owned_car = any(tag in v['name'].lower() for tag in ["pre-owned", "used", "cpo", "certified"])
        if condition_pref == "Brand New" and is_pre_owned_car:
            score -= 80.0
        elif condition_pref == "Pre-Owned" and not is_pre_owned_car:
            score -= 80.0
            
        scored_candidates.append((score, v))
        
    scored_candidates.sort(key=lambda x: x[0], reverse=True)
    matches = [item[1] for item in scored_candidates]

    # Handle offset / pagination cycling when user requests "more / different"
    if refinement_prompt:
        ref_lower = refinement_prompt.lower()
        if condition_changed:
            st.session_state['recommendation_offset'] = 0
        elif any(kw in ref_lower for kw in ["more", "other", "else", "different", "another", "next"]):
            if 'recommendation_offset' not in st.session_state:
                st.session_state['recommendation_offset'] = 0
            st.session_state['recommendation_offset'] += 3

    offset = st.session_state.get('recommendation_offset', 0)
    if offset >= len(matches):
        offset = 0
        st.session_state['recommendation_offset'] = 0

    return matches[offset : offset + 3]

def perform_web_search(profile, refinement_prompt=None):
    v_type = profile.get('type')
    style = profile.get('body_style', 'SUV')
    
    # Build search query
    base_query = f"best {profile['fuel_type'] or ''} {style} under {profile['budget']} for {profile['road_condition'] or ''} road conditions and daily distance {profile['daily_distance'] or ''}"
    if refinement_prompt:
        query = f"{base_query} {refinement_prompt}"
    else:
        query = base_query
    
    # PRIMARY: curated budget-tier results (always correct)
    base_candidates = get_candidate_vehicles(profile, refinement_prompt=refinement_prompt)
    candidates = []
    for bc in base_candidates:
        candidates.append({
            "name": bc['name'],
            "price": bc['price'],
            "description": bc['description'],
            "link": bc.get('link', ''),
            "image": bc.get('image', '')
        })

    # Fetch live search results from DuckDuckGo for context/enrichment (optional)
    web_results = []
    try:
        web_results = search_duckduckgo(query, max_results=3)
    except:
        pass
        
    # Query AI backend to enrich the descriptions based on profile and web results
    system_instruction = (
        "You are a luxury automotive advisor. Your task is to customize and enrich the descriptions of the candidate vehicles "
        "to explain exactly how they fit the user's daily distance, road conditions, and any specific refinement requests (e.g. latest 2026 models).\n\n"
        "CRITICAL RULES:\n"
        "1. If the user's refinement request asks for 'more', 'new', 'different', 'other', 'latest', or newer model years (e.g., 2025/2026) that are not in the Base Candidates list, "
        "you MUST propose alternative/new real-world vehicles (under their budget) matching their request. Use information from the web search results or your knowledge.\n"
        "2. For any new vehicles, provide their real-world name, a realistic price, a custom description, and leave 'link' and 'image' empty.\n"
        "3. If they are not asking for new/more/different vehicles, strictly use and enrich the provided Base Candidates.\n"
        "Response MUST be strictly a JSON object containing a 'candidates' list."
    )
    user_prompt = (
        f"Automotive Profile:\n{json.dumps(profile, indent=2)}\n\n"
        f"Base Candidates:\n{json.dumps(candidates, indent=2)}\n\n"
        f"Web Search Results for Context:\n{json.dumps(web_results, indent=2)}\n\n"
        f"User Refinement Request: {refinement_prompt if refinement_prompt else 'None'}"
    )
    
    try:
        extracted_data = call_free_llm(user_prompt, system_instruction)
        if extracted_data and 'candidates' in extracted_data:
            enriched_candidates = extracted_data['candidates']
            valid_enriched = []
            for ec in enriched_candidates:
                # Ensure the enriched candidate is in our base candidates list (using case-insensitive substring match)
                match_bc = next((bc for bc in base_candidates if clean_vehicle_name(bc['name']).lower() in clean_vehicle_name(ec.get('name', '')).lower() 
                                 or clean_vehicle_name(ec.get('name', '')).lower() in clean_vehicle_name(bc['name']).lower()), None)
                if match_bc:
                    valid_enriched.append({
                        "name": match_bc['name'], # Keep curated name
                        "price": match_bc['price'], # Keep curated price
                        "description": ec.get('description', match_bc['description']), # Use enriched description
                        "link": match_bc.get('link', ''), # Keep curated link
                        "image": match_bc.get('image', '') # Keep curated image
                    })
                else:
                    # Allow new/alternative candidates if user specifically requested them
                    is_more_requested = False
                    if refinement_prompt:
                        ref_lower = refinement_prompt.lower()
                        more_keywords = ["more", "new", "different", "other", "else", "alternative", "change", "refine", "update", "2025", "2026", "latest", "preowned", "pre-owned", "used", "old", "older", "second hand", "cpo", "certified"]
                        if any(kw in ref_lower for kw in more_keywords):
                            is_more_requested = True
                    
                    if is_more_requested and ec.get('name'):
                        valid_enriched.append({
                            "name": ec['name'].strip(),
                            "price": ec.get('price', 'Price on Request'),
                            "description": ec.get('description', 'Dynamic recommendation matching your refined preferences.'),
                            "link": ec.get('link', ''),
                            "image": ec.get('image', '')
                        })
            if len(valid_enriched) >= 1: # Ensure we got at least 1 valid result
                candidates = valid_enriched
    except Exception as e:
        # Fall back to base_candidates if any error
        pass

    # === IMAGE & LINK RESOLUTION ===
    # For every candidate, try to get a model-specific Wikipedia image.
    # If Wikipedia returns something, it replaces the generic fallback.
    # If Wikipedia fails, keep the curated Unsplash image (already body-style-matched).
    style_lower = style.lower()
    fallback_images = {
        "suv":      "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=600&auto=format&fit=crop",
        "sedan":    "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=600&auto=format&fit=crop",
        "hatchback":"https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?w=600&auto=format&fit=crop",
        "bike":     "https://images.unsplash.com/photo-1558981806-ec527fa84c39?w=600&auto=format&fit=crop",
        "default":  "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=600&auto=format&fit=crop",
    }
    for c in candidates:
        clean_name = clean_vehicle_name(c.get('name', ''))

        # Try Wikipedia for a photo of the actual model
        wiki_img = get_wikipedia_image(clean_name)
        if wiki_img:
            c['image'] = wiki_img          # Model-specific photo wins
        elif not c.get('image'):           # No curated image either — use body-style fallback
            if "suv" in style_lower:
                c['image'] = fallback_images["suv"]
            elif "sedan" in style_lower:
                c['image'] = fallback_images["sedan"]
            elif "hatchback" in style_lower:
                c['image'] = fallback_images["hatchback"]
            elif v_type == "2-Wheeler":
                c['image'] = fallback_images["bike"]
            else:
                c['image'] = fallback_images["default"]

        # Ensure link is a real URL
        if not c.get('link', '').startswith('http'):
            c['link'] = f"https://www.google.com/search?q={urllib.parse.quote(clean_name + ' India buy official site')}"

    res = {
        "search_query": query,
        "status": "success",
        "web_results": web_results,
        "candidates": candidates
    }
    # Save search metadata for st.status UI rendering
    st.session_state['latest_search_metadata'] = {
        "query": query,
        "results": {
            "search_query": query,
            "status": "success",
            "results": [
                {"model": c['name'], "price": c['price'], "link": c['link']} for c in candidates
            ]
        }
    }
    return res

# ==================================================
# 🤝 COMMITMENT DETECTION
# ==================================================
def detect_commitment(user_message, recommendations):
    if not recommendations:
        return None
    user_message_lower = user_message.lower()
    # Remove generic words like "want", "like", "get" to avoid false positives in refinement
    commitment_indicators = ["love", "go with", "choose", "select", "buy", "go for", "commit", "prefer", "book", "finalize", "decide on", "take the"]
    
    for model in recommendations:
        model_name = model['name']
        clean_model = clean_vehicle_name(model_name).lower()
        model_keywords = [clean_model]
        parts = clean_model.split()
        for p in parts:
            if len(p) > 3 and p not in ["tata", "hyundai", "bmw", "audi", "porsche", "range", "rover", "toyota", "royal", "enfield", "honda", "volvo", "ola", "ather"]:
                model_keywords.append(p)
        
        has_commitment_phrase = any(phrase in user_message_lower for phrase in commitment_indicators)
        has_model_keyword = any(kw in user_message_lower for kw in model_keywords)
        
        if has_model_keyword:
            if has_commitment_phrase or len(user_message.strip().split()) <= 3:
                return model
    return None

def format_search_metadata(results):
    # Metadata is now displayed via st.status in the rendering loop — return empty string
    return ""

# ==================================================
# 💬 USER MESSAGE PROCESSING
# ==================================================
def handle_user_message(prompt):
    profile = st.session_state['profile']
    step = st.session_state['step']
    
    # 1. Gather profile using LLM if possible
    if step == 'gathering_profile':
        res = call_llm_concierge(prompt, st.session_state['messages'][:-1], profile)
        if res:
            if 'profile' in res:
                for k, v in res['profile'].items():
                    if v is not None:
                        profile[k] = v
            
            if res.get('all_set') or not get_missing_parameters(profile):
                results = perform_web_search(profile)
                st.session_state['recommendations'] = results['candidates']
                st.session_state['step'] = 'results_displayed'
                
                cards_md = ""
                for i, c in enumerate(results['candidates'], 1):
                    cards_md += (
                        f"### 💎 Option {i}: {c['name']}\n"
                        f"**Price Guide:** {c['price']}\n\n"
                        f"![{c['name']}]({c['image']})\n\n"
                        f"*{c['description']}*\n\n"
                        f"🔗 **[View Official Manufacturer Page]({c['link']})**\n\n"
                        f"---\n\n"
                    )
                
                ai_response = (
                    f"Thank you for completing your profile! Here are your curated selections:\n\n"
                    f"{cards_md}"
                    f"Which of these exquisite options speaks to you? Let me know to proceed."
                )
                return ai_response
            else:
                return res.get('concierge_response', "Could you provide more details?")
                
    # Fallback/Default gathering profile (if free LLM API fails or rate limits)
    if step == 'gathering_profile':
        extract_profile_data(prompt, profile)
        missing = get_missing_parameters(profile)
        
        if missing:
            response_text = generate_concierge_question(profile)
            return response_text
        else:
            results = perform_web_search(profile)
            st.session_state['recommendations'] = results['candidates']
            st.session_state['step'] = 'results_displayed'
            
            cards_md = ""
            for i, c in enumerate(results['candidates'], 1):
                cards_md += (
                    f"### 💎 Option {i}: {c['name']}\n"
                    f"**Price Guide:** {c['price']}\n\n"
                    f"![{c['name']}]({c['image']})\n\n"
                    f"*{c['description']}*\n\n"
                    f"🔗 **[View Official Manufacturer Page]({c['link']})**\n\n"
                    f"---\n\n"
                )
                
            ai_response = (
                f"Thank you for completing your profile! Here are your curated selections:\n\n"
                f"{cards_md}"
                f"Which of these exquisite options speaks to you? Let me know to proceed."
            )
            return ai_response
            
    # 2. Results displayed state — handle selection OR refinement
    elif step == 'results_displayed':
        recs = st.session_state['recommendations']
        prompt_lower = prompt.lower()

        # --- Detect profile-refinement intent BEFORE commitment check ---
        REFINEMENT_TRIGGERS = [
            "luxury", "premium", "high-end", "expensive", "brand new", "new car", "new",
            "fresh", "different", "something else", "change", "refine", "update",
            "more options", "other options", "show me more", "fetch", "search again",
            "higher budget", "lower budget", "budget", "cheaper", "costlier",
            "electric", "petrol", "diesel", "hybrid", "cng",
            "suv", "sedan", "hatchback", "coupe", "bike", "scooter",
            "off-road", "highway", "city", "mountain",
            "latest", "model", "models", "year", "2025", "2026", "modern", "recent",
            "color", "sunroof", "features", "safety", "mileage", "specs",
            "preowned", "pre-owned", "used", "old", "older", "second hand", "cpo", "certified"
        ]
        is_refinement = any(kw in prompt_lower for kw in REFINEMENT_TRIGGERS)

        if is_refinement:
            # Map common shorthand phrases to profile fields before re-searching
            REFINEMENT_MAP = {
                "luxury":       {"body_style": None},   # reset style so budget tier drives it
                "premium":      {"body_style": None},
                "high-end":     {"body_style": None},
                "brand new":    {"condition": "Brand New"}, # reset condition
                "new car":      {"condition": "Brand New"},
                "electric":     {"fuel_type": "Electric"},
                "ev":           {"fuel_type": "Electric"},
                "petrol":       {"fuel_type": "Petrol"},
                "diesel":       {"fuel_type": "Diesel"},
                "hybrid":       {"fuel_type": "Hybrid"},
                "cng":          {"fuel_type": "CNG"},
                "suv":          {"body_style": "SUV"},
                "sedan":        {"body_style": "Sedan"},
                "hatchback":    {"body_style": "Hatchback"},
                "off-road":     {"road_condition": "Off-Road / Rough"},
                "highway":      {"road_condition": "Highway / Long Distance"},
                "city":         {"road_condition": "City / Traffic"},
                "pre-owned":    {"condition": "Pre-Owned"},
                "preowned":     {"condition": "Pre-Owned"},
                "used":         {"condition": "Pre-Owned"},
                "cpo":          {"condition": "Pre-Owned"},
                "certified":    {"condition": "Pre-Owned"},
                "second hand":  {"condition": "Pre-Owned"},
                "older":        {"condition": "Pre-Owned"},
                "old":          {"condition": "Pre-Owned"},
            }

            # If user says "luxury" / "premium" / "high-end", raise budget tier significantly
            LUXURY_WORDS = ["luxury", "premium", "high-end", "expensive"]
            if any(w in prompt_lower for w in LUXURY_WORDS):
                current_budget_str = profile.get('budget', '')
                nums = re.findall(r'\d+(?:\.\d+)?', current_budget_str)
                current_budget_val = float(nums[0]) if nums else 5.0
                # If user's budget is low (< 15L), upgrade it to a premium tier (30L)
                if current_budget_val < 15:
                    profile['budget'] = '\u20b9 30 Lakh'
                elif current_budget_val < 30:
                    profile['budget'] = '\u20b9 60 Lakh'
                # else keep as-is — just re-filter toward luxury options

            # If user says "brand new" / "new car", raise budget if it's clearly CPO territory
            NEW_CAR_WORDS = ["brand new", "new car", "fresh", "new"]
            if any(w in prompt_lower for w in NEW_CAR_WORDS):
                current_budget_str = profile.get('budget', '')
                nums = re.findall(r'\d+(?:\.\d+)?', current_budget_str)
                current_budget_val = float(nums[0]) if nums else 5.0
                # Under ₹6L is CPO territory; nudge budget to ₹8L to get brand new options
                if current_budget_val < 6:
                    profile['budget'] = '\u20b9 8 Lakh'

            # Apply keyword-based profile overrides
            for kw, overrides in REFINEMENT_MAP.items():
                if kw in prompt_lower:
                    for field, val in overrides.items():
                        if val is not None:
                            profile[field] = val
                        # val=None means "clear this field" so search re-picks via budget tier

            # Also run the regex extractor to pick up explicit numbers / distances
            extract_profile_data(prompt, profile, overwrite=True)

            # Re-run the search with updated profile
            results = perform_web_search(profile, refinement_prompt=prompt)
            st.session_state['recommendations'] = results['candidates']
            # Stay in results_displayed — user may want to keep refining

            cards_md = ""
            for i, c in enumerate(results['candidates'], 1):
                cards_md += (
                    f"### \U0001f48e Option {i}: {c['name']}\n"
                    f"**Price Guide:** {c['price']}\n\n"
                    f"![{c['name']}]({c['image']})\n\n"
                    f"*{c['description']}*\n\n"
                    f"\U0001f517 **[View Official Page \u2192 Open in Browser]({c['link']})**\n\n"
                    f"---\n\n"
                )

            return (
                f"Absolutely! I've refined your search based on your preferences.\n\n"
                f"Here are your updated curated selections:\n\n"
                f"{cards_md}"
                f"Which of these speaks to you? Or tell me how to refine further!"
            )

        # --- Commitment detection (user picked a specific car) ---
        selected = detect_commitment(prompt, recs)
        if selected:
            st.session_state['selected_model'] = selected
            st.session_state['step'] = 'conversion'

            cta_md = (
                f"## \U0001f3c6 READY TO OWN IT?\n"
                f"Your search is complete. The signature **{selected['name']}** aligns perfectly with your requirements.\n\n"
                f"\U0001f4b0 **Estimated Price:** {selected['price']}\n\n"
                f"\U0001f449 **[Click Here \u2192 Official Manufacturer Page \u0026 Book Test Drive]({selected['link']})**\n\n"
                f"*Official link — click to open in your browser.*"
            )

            return (
                f"Exceptional choice! Transitioning your consultation to the purchase stage.\n\n"
                f"{cta_md}"
            )

        # --- Generic nudge when we can't interpret the intent ---
        model_names = ', '.join([c['name'].split()[-1] for c in recs])   # last word = model name
        return (
            f"I\'d love to help! You can:\n"
            f"- **Select a model** — just say its name (e.g., *{recs[0]['name'].split()[-1]}* or *{recs[-1]['name'].split()[-1]}*)\n"
            f"- **Refine your search** — say things like *\"luxury\"*, *\"brand new\"*, *\"electric\"*, *\"SUV\"* etc.\n"
            f"- **Reset completely** — use the **\U0001f504 Reset Consultation** button in the sidebar."
        )
            
    else:
        selected = st.session_state['selected_model']
        ai_response = (
            f"You have committed to the **{selected['name']}**. "
            "Please click the link in the Action Funnel above to proceed with the official booking or test drive. "
            "If you would like to start a new search, please click **🔄 Reset Consultation** in the sidebar."
        )
        return ai_response

# ==================================================
# ✨ MAIN EXECUTION FLOW (The Streamlit UI)
# ==================================================
def main():
    # 1. Setup Session State
    initialize_state()
    
    # 2. Loading Screen Logic (Runs once on startup)
    if "loading_done" not in st.session_state:
        render_spinning_wheel()
        time.sleep(3)
        st.session_state['loading_done'] = True
        st.rerun()
        
    # 3. Main Interface Layout
    # Inject Custom CSS
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    
    # Render Sidebar
    display_profile_summary()
    
    # Main Header
    st.title("✨ AI Auto Advisor")
    st.markdown("*(Your personal luxury automotive concierge)*")
    st.markdown("---")
    
    # Render Chat History using standard Streamlit chat bubbles
    for msg in st.session_state['messages']:
        with st.chat_message(msg['role']):
            if 'search_metadata' in msg and msg['search_metadata']:
                meta = msg['search_metadata']
                with st.status(f"🔍 **WebSearch:** `{meta['query']}`", state="complete"):
                    st.json(meta['results'])
            st.markdown(msg['content'])
            
    # Chat Input
    if prompt := st.chat_input("Compose your response here..."):
        # Append User message
        st.session_state['messages'].append({"role": "user", "content": prompt})
        
        # Clear latest search metadata before run
        st.session_state['latest_search_metadata'] = None
        
        # Get AI Response
        with st.spinner("Concierge is processing..."):
            ai_response = handle_user_message(prompt)
            
        # Append AI response
        msg_dict = {"role": "assistant", "content": ai_response}
        if st.session_state.get('latest_search_metadata'):
            msg_dict['search_metadata'] = st.session_state['latest_search_metadata']
            
        st.session_state['messages'].append(msg_dict)
        st.rerun()

if __name__ == "__main__":
    main()