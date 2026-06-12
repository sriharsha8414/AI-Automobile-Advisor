import re
import json
import requests

OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3"

def is_ollama_available():
    try:
        r = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=3)
        return r.status_code == 200
    except:
        return False

def build_ollama_system_prompt(pref, lang, user_info=None, matched_vehicles=None):
    prompt = f"""You are AutoMatch Advisor, an AI vehicle recommendation assistant. You help users find the perfect vehicle (Two Wheeler or Four Wheeler) in India.

Current settings:
- Vehicle Preference: {pref}
- Language: {lang}
"""
    if user_info and user_info.get("name"):
        prompt += f"""
User Info:
- Name: {user_info.get('name', 'N/A')}
- Phone: {user_info.get('phone', 'N/A')}
- Vehicle Preference: {user_info.get('vehicle_type', 'N/A')}
- Fuel Preference: {user_info.get('fuel_type', 'N/A')}
"""
    if matched_vehicles:
        prompt += "\nMatching vehicles from database:\n"
        for v in matched_vehicles:
            prompt += f"- {v['name']}: {v['price']}, Type: {v['type']}, Pros: {v['pros']}, Cons: {v['cons']}\n"
    else:
        prompt += "\nAvailable vehicles:\n"
        for v in VEHICLES.get(pref, []):
            prompt += f"- {v['name']}: {v['price']}, Type: {v['type']}\n"

    prompt += """

Response guidelines:
1. Be conversational, friendly, and helpful like ChatGPT
2. If language is 'hi', respond in Hindi. If 'te', respond in Telugu. Otherwise English.
3. When recommending vehicles, mention their pros, cons, and price clearly
4. Ask follow-up questions to understand user needs better
5. Keep responses concise but informative
6. Use bullet points for lists"""
    return prompt

def ollama_chat(messages, timeout=180):
    try:
        payload = {
            "model": OLLAMA_MODEL,
            "messages": messages,
            "stream": False,
            "options": {"temperature": 0.7, "num_predict": 1024}
        }
        r = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json=payload,
            timeout=timeout
        )
        if r.status_code == 200:
            data = r.json()
            return data.get("message", {}).get("content", "")
        return None
    except Exception as e:
        print(f"Ollama error: {e}")
        return None

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

TRANSLATIONS = {
    "hi": {
        "greeting": "नमस्ते! AutoMatch सलाहकार में आपका स्वागत है। मैं आपकी कैसे मदद कर सकता हूँ?",
        "greeting_tw": "नमस्ते! मैं आपका AutoMatch दो-पहिया सलाहकार हूँ। कृपया अपनी पसंद बताएं - बजट, वाहन प्रकार, या कोई सवाल पूछें।",
        "greeting_fw": "नमस्ते! मैं आपका AutoMatch चार-पहिया सलाहकार हूँ। कृपया अपनी पसंद बताएं - बजट, वाहन प्रकार, या कोई सवाल पूछें।",
        "how_can_i_help": "मैं आपकी कैसे मदद कर सकता हूँ? कृपया अपना नाम, फ़ोन नंबर, और वाहन संबंधी जानकारी साझा करें।",
        "ask_name": "कृपया अपना नाम बताएं:",
        "ask_phone": "कृपया अपना फ़ोन नंबर बताएं:",
        "ask_vehicle": "कृपया अपनी पसंद का वाहन बताएं (दो-पहिया या चार-पहिया):",
        "ask_fuel": "कृपया अपनी पसंद का ईंधन प्रकार बताएं (पेट्रोल, डीज़ल, या इलेक्ट्रिक):",
        "thanks": "आपका स्वागत है! अगर और मदद चाहिए तो कृपया पूछें।",
        "goodbye": "धन्यवाद! अगर फिर कभी वाहन चुनने में मदद चाहिए तो ज़रूर आएं। शुभ दिन!",
        "welcome": "आपका स्वागत है, {name}! आपका फ़ोन नंबर {phone} दर्ज कर लिया गया है। आप {vehicle} और {fuel} में रुचि रखते हैं। मैं आपकी कैसे मदद कर सकता हूँ?",
        "ev_vs_petrol": "ईवी बनाम पेट्रोल तुलना",
        "fuel_types": {"petrol": "पेट्रोल", "diesel": "डीज़ल", "electric": "इलेक्ट्रिक"},
        "vehicle_types": {"bike": "बाइक", "scooter": "स्कूटर", "car": "कार", "suv": "एसयूवी", "hatchback": "हैचबैक"},
    },
    "te": {
        "greeting": "నమస్కారం! AutoMatch సలహాదారుకి స్వాగతం. నేను మీకు ఎలా సహాయం చేయగలను?",
        "greeting_tw": "నమస్కారం! నేను మీ AutoMatch రెండు-చక్రాల సలహాదారుని. దయచేసి మీ ప్రాధాన్యతను తెలపండి - బడ్జెట్, వాహనం రకం, లేదా ఏదైనా ప్రశ్న అడగండి.",
        "greeting_fw": "నమస్కారం! నేను మీ AutoMatch నాలుగు-చక్రాల సలహాదారుని. దయచేసి మీ ప్రాధాన్యతను తెలపండి - బడ్జెట్, వాహనం రకం, లేదా ఏదైనా ప్రశ్న అడగండి.",
        "how_can_i_help": "నేను మీకు ఎలా సహాయం చేయగలను? దయచేసి మీ పేరు, ఫోన్ నంబర్ మరియు వాహన వివరాలను తెలపండి.",
        "ask_name": "దయచేసి మీ పేరు తెలపండి:",
        "ask_phone": "దయచేసి మీ ఫోన్ నంబర్ తెలపండి:",
        "ask_vehicle": "దయచేసి మీకు నచ్చిన వాహనం తెలపండి (రెండు-చక్రాలు లేదా నాలుగు-చక్రాలు):",
        "ask_fuel": "దయచేసి మీకు నచ్చిన ఇంధన రకం తెలపండి (పెట్రోల్, డీజిల్, లేదా ఎలక్ట్రిక్):",
        "thanks": "మీకు స్వాగతం! మరింత సహాయం కావాలంటే అడగండి.",
        "goodbye": "ధన్యవాదాలు! మళ్ళీ వాహనాన్ని ఎంచుకోవడంలో సహాయం కావాలంటే రండి. శుభ దినం!",
        "welcome": "స్వాగతం, {name}! మీ ఫోన్ నంబర్ {phone} నమోదు చేయబడింది. మీరు {vehicle} మరియు {fuel} పై ఆసక్తి కలిగి ఉన్నారు. నేను మీకు ఎలా సహాయం చేయగలను?",
        "ev_vs_petrol": "ఈవీ vs పెట్రోల్ పోలిక",
        "fuel_types": {"petrol": "పెట్రోల్", "diesel": "డీజిల్", "electric": "ఎలక్ట్రిక్"},
        "vehicle_types": {"bike": "బైక్", "scooter": "స్కూటర్", "car": "కారు", "suv": "ఎస్‌యువి", "hatchback": "హ్యాచ్‌బ్యాక్"},
    }
}

def fuzzy_match(word, keywords):
    word = word.lower()
    for kw in keywords:
        if kw in word or word in kw:
            return True
        if len(kw) > 3 and len(word) > 3:
            if kw[0] == word[0] and kw[-1] == word[-1]:
                common = len(set(kw) & set(word))
                longer = max(len(kw), len(word))
                if common / longer > 0.7:
                    return True
    return False

def parse_budget(text):
    multipliers = {"thousand": 0.001, "thousands": 0.001, "k": 0.001}
    lakh_multipliers = {"lakh": 1.0, "lakhs": 1.0, "lac": 1.0, "lacs": 1.0}
    crore_multipliers = {"crore": 100.0, "crores": 100.0, "cr": 100.0}

    numbers = re.findall(r"[-+]?\d*\.?\d+", text)
    if not numbers:
        return None

    budget = float(numbers[0])

    for word, mult in crore_multipliers.items():
        if word in text:
            return budget * mult
    for word, mult in lakh_multipliers.items():
        if word in text:
            return budget * mult
    for word, mult in multipliers.items():
        if word in text:
            return budget * mult

    if budget > 1000:
        budget = budget / 100000.0

    return budget

def detect_intent(text):
    text_lower = text.lower().strip()

    greeting_words = ("hi", "hello", "hey", "hola", "greetings", "good morning", "good evening", "good afternoon", "namaste", "namaskaram", "help", "start", "sup", "yo", "wasup")
    if text_lower in greeting_words or any(text_lower.startswith(g + " ") for g in ("hi", "hello", "hey", "good morning", "good evening")):
        return "greeting"

    comparison_kw = ("ev vs", "versus", "comparison", "petrol vs", "electric vs", "ev or petrol", "petrol or electric", "ev and petrol", "compare", "difference between", "vs", "vs.")
    if any(kw in text_lower for kw in comparison_kw):
        return "comparison"

    thanks_kw = ("thanks", "thank you", "thx", "thankyou", "thanks a lot", "appreciate it", "धन्यवाद", "శుభం")
    if text_lower in thanks_kw or any(kw in text_lower for kw in thanks_kw):
        return "thanks"

    goodbye_kw = ("bye", "goodbye", "see you", "cya", "exit", "quit", "अलविदा", "వెళ్ళొస్తాను")
    if text_lower in goodbye_kw or any(text_lower.startswith(g + " ") for g in ("bye", "goodbye")):
        return "goodbye"

    return "query"

def detect_cross_category(text, pref):
    text_lower = text.lower()

    two_wheeler_kw = ("bike", "scooter", "motorcycle", "two wheeler", "2 wheeler", "2-wheeler",
                      "ola", "activa", "raider", "r15", "royal enfield", "classic 350",
                      "yamaha", "honda activa", "tvs", "commuter", "cruiser",
                      "sports bike", "motorbike", "scooty", "gear", "helmet",
                      "बाइक", "स्कूटर", "మోటార్ సైకిల్")

    four_wheeler_kw = ("car", "suv", "hatchback", "sedan", "four wheeler", "4 wheeler",
                       "4-wheeler", "nexon", "swift", "xuv", "creta", "tiago",
                       "tata nexon", "maruti", "mahindra", "hyundai",
                       "compact suv", "mid-size suv", "sedan", "mpv", "muv",
                       "petrol car", "diesel car", "electric car", "family car",
                       "sports car", "hatch", "suvs", "crossover", "pickup",
                       "कार", "ఎస్‌యువి", "కారు")

    if pref == "Two Wheeler" and any(kw in text_lower for kw in four_wheeler_kw):
        return "four_wheeler"
    if pref == "Four Wheeler" and any(kw in text_lower for kw in two_wheeler_kw):
        return "two_wheeler"
    return None

def get_vehicle_filters(text):
    text_lower = text.lower()
    filters = []

    ev_kw = ("ev", "electric", "electric vehicle", "electrical", "battery", "इलेक्ट्रिक", "ఎలక్ట్రిక్")
    suv_kw = ("suv", "suvs", "sport utility", "off-road", "offroad", "off road", "एसयूवी", "ఎస్‌యువి")
    hatchback_kw = ("hatchback", "hatch", "5-door", "five door", "हैचबैक", "హ్యాచ్‌బ్యాక్")
    sedan_kw = ("sedan", "saloon", "4-door", "four door", "notchback")
    scooter_kw = ("scooter", "scooty", "scooters", "moped", "vespa", "स्कूटर", "స్కూటర్")
    bike_kw = ("bike", "bikes", "motorcycle", "motorcycles", "commuter", "street", "motorbike", "बाइक", "బైక్")
    cruiser_kw = ("cruiser", "cruising", "thump", "retro", "classic")
    sports_kw = ("sports", "sport", "racing", "fast", "speed", "performance", "track", "r15")

    if any(kw in text_lower for kw in ev_kw): filters.append("ev")
    if any(kw in text_lower for kw in suv_kw): filters.append("suv")
    if any(kw in text_lower for kw in hatchback_kw): filters.append("hatchback")
    if any(kw in text_lower for kw in sedan_kw): filters.append("sedan")
    if any(kw in text_lower for kw in scooter_kw): filters.append("scooter")
    if any(kw in text_lower for kw in bike_kw): filters.append("bike")
    if any(kw in text_lower for kw in cruiser_kw): filters.append("cruiser")
    if any(kw in text_lower for kw in sports_kw): filters.append("sports")

    return filters

def matches_vehicle(vehicle, filters):
    if not filters:
        return True
    combined = (vehicle["name"] + " " + vehicle["type"]).lower()
    return any(f in combined for f in filters)

def build_vehicle_card(v):
    return (
        '<div class="vehicle-card">\n'
        '<div class="vehicle-header">\n'
        f'<h4 class="vehicle-name">{v["name"]}</h4>\n'
        f'<span class="vehicle-tag">{v["type"]}</span>\n'
        '</div>\n'
        f'<div class="vehicle-price">Estimated Price: <b>{v["price"]}</b></div>\n'
        f'<div class="pros-list"><i class="fas fa-check-circle icon-glow"></i> <b>PROS:</b> {v["pros"]}</div>\n'
        f'<div class="cons-list"><i class="fas fa-times-circle icon-glow"></i> <b>CONS:</b> {v["cons"]}</div>\n'
        '</div>\n'
    )

def recommend_vehicles(pref, budget=None, filters=None):
    candidates = VEHICLES[pref]

    if budget:
        matched = [v for v in candidates if v["budget_val"] <= budget * 1.25 and v["budget_val"] >= budget * 0.5]
        if not matched:
            matched = list(candidates)
        matched.sort(key=lambda x: abs(x["budget_val"] - budget))
    else:
        matched = list(candidates)

    if filters:
        filtered = [v for v in matched if matches_vehicle(v, filters)]
        if filtered:
            matched = filtered

    if not matched:
        matched = candidates[:3]

    return matched[:5]

def format_recommendation(matched, pref, budget, filters, lang="en"):
    if lang == "hi":
        res = f"### <i class=\"fas fa-car\"></i> AutoMatch सलाहकार अनुशंसाएँ ({pref})\n\n"
        if budget:
            res += f"आपके बजट **~₹{budget:.2f} लाख** के अनुसार सबसे अच्छे विकल्प:\n\n"
        elif filters:
            res += "आपकी पसंद के अनुसार सबसे अच्छे विकल्प:\n\n"
        else:
            res += "आपके लिए हमारी शीर्ष अनुशंसाएँ:\n\n"
    elif lang == "te":
        res = f"### <i class=\"fas fa-car\"></i> AutoMatch సలహాదారు సిఫార్సులు ({pref})\n\n"
        if budget:
            res += f"మీ బడ్జెట్ **~₹{budget:.2f} లక్షల** ప్రకారం ఉత్తమ ఎంపికలు:\n\n"
        elif filters:
            res += "మీ ప్రాధాన్యత ప్రకారం ఉత్తమ ఎంపికలు:\n\n"
        else:
            res += "మీ కోసం మా టాప్ సిఫార్సులు:\n\n"
    else:
        res = f"### <i class=\"fas fa-car\"></i> AutoMatch Advisor Recommendations ({pref})\n\n"
        if budget:
            res += f"Here are the best options matching your budget of **~₹{budget:.2f} Lakh**:\n\n"
        elif filters:
            res += "Here are the best options matching your preference:\n\n"
        else:
            res += "Here are our top recommended options for you:\n\n"

    for v in matched:
        res += build_vehicle_card(v)

    if lang == "hi":
        res += "\n\n---\n"
        res += "*क्या आप अपना बजट समायोजित करना चाहेंगे, या ऊपर दिए गए किसी मॉडल के बारे में विस्तृत जानकारी चाहेंगे?*"
    elif lang == "te":
        res += "\n\n---\n"
        res += "*మీరు మీ బడ్జెట్‌ను సర్దుబాటు చేయాలనుకుంటున్నారా, లేదా పైన ఉన్న ఏదైనా మోడల్ గురించి వివరాలు కావాలా?*"
    else:
        res += "\n\n---\n"
        res += "*Would you like to adjust your budget, or get details on a specific model listed above?*"
    return res

def get_greeting(pref, lang="en"):
    if lang == "hi":
        if pref == "Two Wheeler":
            return TRANSLATIONS["hi"]["greeting_tw"]
        return TRANSLATIONS["hi"]["greeting_fw"]
    elif lang == "te":
        if pref == "Two Wheeler":
            return TRANSLATIONS["te"]["greeting_tw"]
        return TRANSLATIONS["te"]["greeting_fw"]
    else:
        if pref == "Two Wheeler":
            return "Hello! I'm your AutoMatch **Two Wheeler** Advisor.\n\n💡 **Try asking:**\n- Scooter under ₹1 lakh\n- Best sports bike\n- EV vs Petrol comparison\n- Reliable daily commuter"
        return "Hello! I'm your AutoMatch **Four Wheeler** Advisor.\n\n💡 **Try asking:**\n- SUV under ₹15 lakh\n- Best hatchback\n- EV vs Petrol comparison\n- Family car with good safety"

def generate_response(user_input, pref, lang="en", user_info=None, ai_mode="rule"):
    text = user_input.strip()
    text_lower = text.lower()

    if ai_mode == "ollama":
        budget = parse_budget(text_lower)
        filters = get_vehicle_filters(text_lower)
        matched = recommend_vehicles(pref, budget, filters)

        system_prompt = build_ollama_system_prompt(pref, lang, user_info, matched)
        ollama_messages = [
            {"role": "system", "content": system_prompt},
        ]

        ollama_messages.append({"role": "user", "content": user_input})
        response = ollama_chat(ollama_messages)
        if response:
            return response
        fallback = format_recommendation(matched, pref, budget, filters, lang)
        return f"{fallback}\n\n---\n*Note: Ollama is not responding. Showing rule-based recommendations.*"

    intent = detect_intent(text_lower)

    if user_info and user_info.get("awaiting_info"):
        return process_user_info_step(user_input, user_info, lang)

    if intent == "greeting":
        if lang == "hi":
            return TRANSLATIONS["hi"]["greeting"]
        elif lang == "te":
            return TRANSLATIONS["te"]["greeting"]
        if pref == "Two Wheeler":
            return "Hello! I'm your AutoMatch **Two Wheeler** Advisor.\n\n💡 **Try asking:**\n- Scooter under ₹1 lakh\n- Best sports bike\n- EV vs Petrol comparison\n- Reliable daily commuter"
        return "Hello! I'm your AutoMatch **Four Wheeler** Advisor.\n\n💡 **Try asking:**\n- SUV under ₹15 lakh\n- Best hatchback\n- EV vs Petrol comparison\n- Family car with good safety"

    if intent == "thanks":
        if lang == "hi":
            return TRANSLATIONS["hi"]["thanks"]
        elif lang == "te":
            return TRANSLATIONS["te"]["thanks"]
        return "You're welcome! Feel free to ask if you need more help finding the perfect vehicle."

    if intent == "goodbye":
        if lang == "hi":
            return TRANSLATIONS["hi"]["goodbye"]
        elif lang == "te":
            return TRANSLATIONS["te"]["goodbye"]
        return "Goodbye! Feel free to come back anytime you need help choosing a vehicle. Have a great day!"

    if intent == "comparison":
        if lang == "hi":
            return get_ev_vs_petrol_hi()
        elif lang == "te":
            return get_ev_vs_petrol_te()
        return (
            "### <i class=\"fas fa-bolt\"></i> EV vs Petrol Comparison\n\n"
            "<table class='ev-comparison-table'>"
            "<tr><th>Feature</th><th>EV (Electric Vehicle)</th><th>Petrol Vehicle</th></tr>"
            "<tr><td><b>Initial Cost</b></td><td>Higher upfront purchase price</td><td>Lower initial cost</td></tr>"
            "<tr><td><b>Running Cost</b></td><td>Extremely low (~₹0.5 - ₹1 per km)</td><td>Higher (~₹6 - ₹9 per km)</td></tr>"
            "<tr><td><b>Maintenance</b></td><td>Minimal (no engine oil, fewer parts)</td><td>Regular servicing (filters, plugs, oil)</td></tr>"
            "<tr><td><b>Convenience</b></td><td>Needs regular charging</td><td>Refuel in 2 mins anywhere</td></tr>"
            "<tr><td><b>Eco-Friendliness</b></td><td>Zero tailpipe emissions</td><td>CO2 emissions from fuel</td></tr>"
            "<tr><td><b>Range</b></td><td>150-300 km per charge</td><td>500-800 km per tank</td></tr>"
            "</table>"
            "**Recommendation:** Buy an **EV** if your daily run is >40 km inside the city and you have charging access. Choose **Petrol** if you do frequent long highway runs or lack charging infrastructure."
        )

    cross = detect_cross_category(text_lower, pref)
    if cross:
        other = "Four Wheelers" if cross == "four_wheeler" else "Two Wheelers"
        switch_to = "Four Wheeler" if cross == "four_wheeler" else "Two Wheeler"
        examples_map = {
            "Four Wheeler": "car, SUV, or hatchback",
            "Two Wheeler": "bike or scooter"
        }
        if lang == "hi":
            return (
                f"आप **{other}** के बारे में पूछ रहे हैं, लेकिन आपकी प्राथमिकता **{pref}** पर सेट है। "
                f"साइडबार में **{switch_to}** चुनें, और मैं आपको सही वाहन खोजने में मदद करूंगा!"
            )
        elif lang == "te":
            return (
                f"మీరు **{other}** గురించి అడుగుతున్నారు, కానీ మీ ప్రాధాన్యత **{pref}** పై సెట్ చేయబడింది. "
                f"సైడ్‌బార్‌లో **{switch_to}** ఎంచుకోండి, నేను మీకు సరైన వాహనాన్ని కనుగొనడంలో సహాయం చేస్తాను!"
            )
        return (
            f"You're asking about **{other}**, but your preference is set to **{pref}**. "
            f"Switch to **{switch_to}** in the sidebar, and I'll help you find the perfect {examples_map[switch_to]}!"
        )

    unknown_words = (
        "what is your name", "who are you", "what can you do", "how are you",
        "your name", "capabilities", "features", "about you"
    )
    if any(kw in text_lower for kw in unknown_words):
        if lang == "hi":
            return (
                "मैं **AutoMatch सलाहकार** हूँ, आपका व्यक्तिगत वाहन अनुशंसा सहायक!\n\n"
                "मैं आपकी मदद कर सकता हूँ:\n"
                "- आपके बजट के अनुसार वाहन खोजना\n"
                "- विशिष्ट प्रकार (SUV, हैचबैक, स्कूटर, बाइक, आदि) सुझाना\n"
                "- EV बनाम पेट्रोल की तुलना करना\n"
                "- आपकी ज़रूरतों के अनुसार सर्वश्रेष्ठ विकल्प सुझाना"
            )
        elif lang == "te":
            return (
                "నేను **AutoMatch సలహాదారుని**, మీ వ్యక్తిగత వాహన సిఫార్సు సహాయకుడిని!\n\n"
                "నేను మీకు సహాయం చేయగలను:\n"
                "- మీ బడ్జెట్ ప్రకారం వాహనాలను కనుగొనడం\n"
                "- నిర్దిష్ట రకాలను సిఫార్సు చేయడం (SUV, హ్యాచ్‌బ్యాక్, స్కూటర్, బైక్, మొదలైనవి)\n"
                "- EV vs పెట్రోల్ పోలిక\n"
                "- మీ అవసరాలకు అనుగుణంగా ఉత్తమ ఎంపికలను సూచించడం"
            )
        return (
            "I'm **AutoMatch Advisor**, your personal vehicle recommendation assistant!\n\n"
            "I can help you:\n"
            "- Find vehicles within your budget\n"
            "- Recommend specific types (SUV, hatchback, scooter, bike, etc.)\n"
            "- Compare EV vs Petrol vehicles\n"
            "- Suggest the best options based on your needs"
        )

    budget = parse_budget(text_lower)
    filters = get_vehicle_filters(text_lower)

    matched = recommend_vehicles(pref, budget, filters)
    return format_recommendation(matched, pref, budget, filters, lang)

def process_user_info_step(user_input, user_info, lang):
    step = user_info.get("step", 0)
    if step == 0:
        user_info["name"] = user_input.strip()
        user_info["step"] = 1
        if lang == "hi":
            return TRANSLATIONS["hi"]["ask_phone"]
        elif lang == "te":
            return TRANSLATIONS["te"]["ask_phone"]
        return "Please share your phone number:"
    elif step == 1:
        user_info["phone"] = user_input.strip()
        user_info["step"] = 2
        if lang == "hi":
            return TRANSLATIONS["hi"]["ask_vehicle"]
        elif lang == "te":
            return TRANSLATIONS["te"]["ask_vehicle"]
        return "Please tell me your preferred vehicle type (Two Wheeler or Four Wheeler):"
    elif step == 2:
        user_info["vehicle"] = user_input.strip()
        user_info["step"] = 3
        if lang == "hi":
            return TRANSLATIONS["hi"]["ask_fuel"]
        elif lang == "te":
            return TRANSLATIONS["te"]["ask_fuel"]
        return "Please tell me your preferred fuel type (Petrol, Diesel, or Electric):"
    elif step == 3:
        user_info["fuel"] = user_input.strip()
        user_info["step"] = 4
        user_info["awaiting_info"] = False
        name = user_info.get("name", "")
        phone = user_info.get("phone", "")
        vehicle = user_info.get("vehicle", "")
        fuel = user_info.get("fuel", "")
        if lang == "hi":
            return TRANSLATIONS["hi"]["welcome"].format(name=name, phone=phone, vehicle=vehicle, fuel=fuel)
        elif lang == "te":
            return TRANSLATIONS["te"]["welcome"].format(name=name, phone=phone, vehicle=vehicle, fuel=fuel)
        return f"Welcome, {name}! Your phone number {phone} is registered. You're interested in {vehicle} with {fuel}. How can I help you today?"

def get_ev_vs_petrol_hi():
    return (
        "### <i class=\"fas fa-bolt\"></i> EV बनाम पेट्रोल तुलना\n\n"
        "<table class='ev-comparison-table'>"
        "<tr><th>विशेषता</th><th>EV (इलेक्ट्रिक वाहन)</th><th>पेट्रोल वाहन</th></tr>"
        "<tr><td><b>शुरुआती लागत</b></td><td>अधिक खरीद मूल्य</td><td>कम शुरुआती लागत</td></tr>"
        "<tr><td><b>चलाने का खर्च</b></td><td>बहुत कम (~₹0.5 - ₹1 प्रति किमी)</td><td>अधिक (~₹6 - ₹9 प्रति किमी)</td></tr>"
        "<tr><td><b>रखरखाव</b></td><td>न्यूनतम (कोई इंजन ऑयल नहीं)</td><td>नियमित सर्विसिंग</td></tr>"
        "<tr><td><b>सुविधा</b></td><td>नियमित चार्जिंग चाहिए</td><td>2 मिनट में कहीं भी ईंधन</td></tr>"
        "<tr><td><b>पर्यावरण-मित्रता</b></td><td>शून्य उत्सर्जन</td><td>CO2 उत्सर्जन</td></tr>"
        "<tr><td><b>रेंज</b></td><td>150-300 किमी प्रति चार्ज</td><td>500-800 किमी प्रति टैंक</td></tr>"
        "</table>"
        "**सुझाव:** यदि आपका दैनिक उपयोग शहर में 40 किमी से अधिक है और चार्जिंग की सुविधा है तो **EV** खरीदें। लंबी हाईवे यात्राओं के लिए **पेट्रोल** चुनें।"
    )

def get_ev_vs_petrol_te():
    return (
        "### <i class=\"fas fa-bolt\"></i> ఈవీ vs పెట్రోల్ పోలిక\n\n"
        "<table class='ev-comparison-table'>"
        "<tr><th>లక్షణం</th><th>EV (ఎలక్ట్రిక్ వాహనం)</th><th>పెట్రోల్ వాహనం</th></tr>"
        "<tr><td><b>ప్రారంభ ఖర్చు</b></td><td>అధిక కొనుగోలు ధర</td><td>తక్కువ ప్రారంభ ఖర్చు</td></tr>"
        "<tr><td><b>నడపడం ఖర్చు</b></td><td>చాలా తక్కువ (~₹0.5 - ₹1 ప్రతి కి.మీ)</td><td>ఎక్కువ (~₹6 - ₹9 ప్రతి కి.మీ)</td></tr>"
        "<tr><td><b>నిర్వహణ</b></td><td>కనిష్టం (ఇంజిన్ ఆయిల్ లేదు)</td><td>సాధారణ సర్వీసింగ్</td></tr>"
        "<tr><td><b>సౌలభ్యం</b></td><td>క్రమం తప్పకుండా ఛార్జింగ్ అవసరం</td><td>2 నిమిషాల్లో ఎక్కడైనా ఇంధనం</td></tr>"
        "<tr><td><b>పర్యావరణ అనుకూలత</b></td><td>సున్నా ఉద్గారాలు</td><td>CO2 ఉద్గారాలు</td></tr>"
        "<tr><td><b>రేంజ్</b></td><td>150-300 కి.మీ ప్రతి ఛార్జ్</td><td>500-800 కి.మీ ప్రతి ట్యాంక్</td></tr>"
        "</table>"
        "**సిఫార్సు:** మీ రోజువారీ ప్రయాణం నగరంలో 40 కి.మీ కంటే ఎక్కువ ఉంటే మరియు ఛార్జింగ్ సౌకర్యం ఉంటే **EV** కొనండి. తరచుగా హైవే ప్రయాణాలకు **పెట్రోల్** ఎంచుకోండి."
    )
