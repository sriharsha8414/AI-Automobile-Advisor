import re

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

    greeting_words = ("hi", "hello", "hey", "hola", "greetings", "good morning", "good evening", "good afternoon", "namaste", "help", "start", "sup", "yo", "wasup")
    if text_lower in greeting_words or any(text_lower.startswith(g + " ") for g in ("hi", "hello", "hey", "good morning", "good evening")):
        return "greeting"

    comparison_kw = ("ev vs", "versus", "comparison", "petrol vs", "electric vs", "ev or petrol", "petrol or electric", "ev and petrol", "compare", "difference between", "vs", "vs.") 
    if any(kw in text_lower for kw in comparison_kw):
        return "comparison"

    thanks_kw = ("thanks", "thank you", "thx", "thankyou", "thanks a lot", "appreciate it")
    if text_lower in thanks_kw or any(kw in text_lower for kw in thanks_kw):
        return "thanks"

    goodbye_kw = ("bye", "goodbye", "see you", "cya", "exit", "quit")
    if text_lower in goodbye_kw or any(text_lower.startswith(g + " ") for g in ("bye", "goodbye")):
        return "goodbye"

    return "query"


def detect_cross_category(text, pref):
    text_lower = text.lower()

    two_wheeler_kw = ("bike", "scooter", "motorcycle", "two wheeler", "2 wheeler", "2-wheeler",
                      "ola", "activa", "raider", "r15", "royal enfield", "classic 350",
                      "yamaha", "honda activa", "tvs", "commuter", "cruiser",
                      "sports bike", "motorbike", "scooty", "gear", "helmet")

    four_wheeler_kw = ("car", "suv", "hatchback", "sedan", "four wheeler", "4 wheeler",
                       "4-wheeler", "nexon", "swift", "xuv", "creta", "tiago",
                       "tata nexon", "maruti", "mahindra", "hyundai",
                       "compact suv", "mid-size suv", "sedan", "mpv", "muv",
                       "petrol car", "diesel car", "electric car", "family car",
                       "sports car", "hatch", "suvs", "crossover", "pickup")

    if pref == "Two Wheeler" and any(kw in text_lower for kw in four_wheeler_kw):
        return "four_wheeler"
    if pref == "Four Wheeler" and any(kw in text_lower for kw in two_wheeler_kw):
        return "two_wheeler"
    return None


def get_vehicle_filters(text):
    text_lower = text.lower()
    filters = []

    ev_kw = ("ev", "electric", "electric vehicle", "electrical", "battery")
    suv_kw = ("suv", "suvs", "sport utility", "off-road", "offroad", "off road")
    hatchback_kw = ("hatchback", "hatch", "5-door", "five door")
    sedan_kw = ("sedan", "saloon", "4-door", "four door", "notchback")
    scooter_kw = ("scooter", "scooty", "scooters", "moped", "vespa")
    bike_kw = ("bike", "bikes", "motorcycle", "motorcycles", "commuter", "street", "motorbike")
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


def format_recommendation(matched, pref, budget, filters):
    res = f"### <i class=\"fas fa-car\"></i> AutoMatch Advisor Recommendations ({pref})\n\n"
    if budget:
        res += f"Here are the best options matching your budget of **~₹{budget:.2f} Lakh**:\n\n"
    elif filters:
        res += "Here are the best options matching your preference:\n\n"
    else:
        res += "Here are our top recommended options for you:\n\n"

    for v in matched:
        res += build_vehicle_card(v)

    res += "\n\n---\n"
    res += "*Would you like to adjust your budget, or get details on a specific model listed above?*"
    return res


def generate_response(user_input, pref):
    text = user_input.strip()
    text_lower = text.lower()

    intent = detect_intent(text_lower)

    if intent == "greeting":
        examples = "budget (e.g. '1.5 lakh'), vehicle type (e.g. 'SUV', 'scooter'), or compare **EV vs Petrol**."
        return f"Hello! Welcome to **AutoMatch {pref} Advisor**. How can I help you today? Try telling me your {examples}"

    if intent == "thanks":
        return "You're welcome! Feel free to ask if you need more help finding the perfect vehicle. 😊"

    if intent == "goodbye":
        return "Goodbye! Feel free to come back anytime you need help choosing a vehicle. Have a great day! 🚗"

    if intent == "comparison":
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
        return (
            f"You're asking about **{other}**, but your preference is set to **{pref}**. "
            f"Switch to **{switch_to}** in the sidebar, and I'll help you find the perfect {examples_map[switch_to]}!"
        )

    unknown_words = (
        "what is your name", "who are you", "what can you do", "how are you",
        "your name", "capabilities", "features", "about you"
    )
    if any(kw in text_lower for kw in unknown_words):
        return (
            "I'm **AutoMatch Advisor**, your personal vehicle recommendation assistant! 🚗\n\n"
            "I can help you:\n"
            "- Find vehicles within your budget\n"
            "- Recommend specific types (SUV, hatchback, scooter, bike, etc.)\n"
            "- Compare EV vs Petrol vehicles\n"
            "- Suggest the best options based on your needs\n\n"
            f"Currently helping with **{pref}** searches. Try asking: \"suv under 15 lakh\" or \"best scooter\""
        )

    budget = parse_budget(text_lower)
    filters = get_vehicle_filters(text_lower)

    matched = recommend_vehicles(pref, budget, filters)
    return format_recommendation(matched, pref, budget, filters)
