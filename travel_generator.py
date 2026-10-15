import random
from datetime import datetime

POPULAR_DESTINATIONS = {
    "paris": {
        "lat": 48.8566, "lng": 2.3522,
        "best_time": "April to June (Spring) or September to October (Autumn)",
        "distance_miles": 3600,
        "tips": [
            "Learn a few basic French phrases. A simple 'Bonjour' goes a long way.",
            "Purchase a Paris Museum Pass if you plan to visit multiple landmarks.",
            "Keep an eye on your belongings in crowded tourist spots and metro stations.",
            "Validate your metro tickets and keep them until you exit the station."
        ],
        "attractions": [
            {"name": "Eiffel Tower", "desc": "The iconic iron grid tower on the Champ de Mars, offering panoramic views of the city."},
            {"name": "Louvre Museum", "desc": "The world's largest art museum, home to the Mona Lisa and Venus de Milo."},
            {"name": "Notre-Dame Cathedral", "desc": "A masterpiece of French Gothic architecture located on the Île de la Cité."},
            {"name": "Montmartre & Sacré-Cœur", "desc": "A charming hilltop district known for its artistic history and stunning basilica."},
            {"name": "Palace of Versailles", "desc": "The magnificent former royal residence of King Louis XIV, located just outside Paris."}
        ],
        "emergency": {"police": "17", "medical": "15", "fire": "18", "general": "112"},
        "hotels": {
            "budget": [
                {"name": "Generator Paris", "price": 45, "rating": 4.2, "desc": "A chic designer hostel in the lively 10th arrondissement."},
                {"name": "Hotel de l'Europe", "price": 75, "rating": 3.9, "desc": "Simple, clean rooms close to Gare du Nord."}
            ],
            "moderate": [
                {"name": "Hotel Regyn's Montmartre", "price": 140, "rating": 4.4, "desc": "Comfortable boutique rooms overlooking Place des Abbesses."},
                {"name": "Hotel Malte Astotel", "price": 185, "rating": 4.6, "desc": "Warmly decorated hotel in the historical heart of Paris."}
            ],
            "luxury": [
                {"name": "The Ritz Paris", "price": 950, "rating": 4.9, "desc": "World-famous legendary luxury palace hotel on Place Vendôme."},
                {"name": "Le Bristol Paris", "price": 850, "rating": 4.8, "desc": "Distinguished palace hotel with a beautiful inner garden and rooftop pool."}
            ]
        },
        "restaurants": [
            {"name": "L'As du Fallafel", "cuisine": "Middle Eastern", "price": "Cheap", "desc": "Famous falafel shop in the Marais district."},
            {"name": "Le Bouillon Chartier", "cuisine": "Traditional French", "price": "Moderate", "desc": "Historic bistro serving classic French fare at excellent prices."},
            {"name": "Le Jules Verne", "cuisine": "Modern French Fine Dining", "price": "Expensive", "desc": "Michelin-starred restaurant situated inside the Eiffel Tower."}
        ]
    },
    "tokyo": {
        "lat": 35.6762, "lng": 139.6503,
        "best_time": "March to May (Cherry Blossom) or September to November (Autumn foliage)",
        "distance_miles": 6700,
        "tips": [
            "Purchase a Suica or Pasmo card for seamless travel on trains and buses.",
            "Tipping is not customary in Japan and may be viewed as impolite.",
            "Carry a small bag for trash, as public garbage cans are rare in Tokyo.",
            "Download an offline translation app to assist with Japanese menus."
        ],
        "attractions": [
            {"name": "Senso-ji Temple", "desc": "Tokyo's oldest and most significant Buddhist temple, located in Asakusa."},
            {"name": "Shibuya Crossing", "desc": "The world's busiest pedestrian intersection, a spectacular symbol of Tokyo's energy."},
            {"name": "Meiji Jingu Shrine", "desc": "A serene Shinto shrine surrounded by a dense forest in the middle of the city."},
            {"name": "Tokyo Skytree", "desc": "A futuristic broadcasting tower offering stunning vistas of Mt. Fuji on clear days."},
            {"name": "Shinjuku Gyoen National Garden", "desc": "A sprawling garden blending Japanese, English, and French landscaping styles."}
        ],
        "emergency": {"police": "110", "medical": "119", "fire": "119", "general": "119"},
        "hotels": {
            "budget": [
                {"name": "Nine Hours Shinjuku-North", "price": 35, "rating": 4.1, "desc": "Sleek, futuristic capsule hotel offering minimalistic sleeping pods."},
                {"name": "Oak Hostel Sakura", "price": 55, "rating": 4.3, "desc": "Friendly hostel near Tokyo Skytree with private and dormitory options."}
            ],
            "moderate": [
                {"name": "Hotel Gracery Shinjuku", "price": 130, "rating": 4.5, "desc": "Modern high-rise hotel featuring the iconic Godzilla Head model outside."},
                {"name": "Park Hotel Tokyo", "price": 190, "rating": 4.6, "desc": "Stylish rooms with local artwork and views of Tokyo Tower."}
            ],
            "luxury": [
                {"name": "Aman Tokyo", "price": 1100, "rating": 4.9, "desc": "Sanctuary at the top of Otemachi Tower, blending Japanese design and luxury."},
                {"name": "Park Hyatt Tokyo", "price": 750, "rating": 4.8, "desc": "Iconic high-rise hotel featured in the movie 'Lost in Translation'."}
            ]
        },
        "restaurants": [
            {"name": "Ichiran Ramen", "cuisine": "Ramen", "price": "Cheap", "desc": "Famous individual dining booth ramen chain known for tonkotsu broth."},
            {"name": "Tsunahachi", "cuisine": "Tempura", "price": "Moderate", "desc": "Established restaurant in Shinjuku serving perfectly fried, light tempura."},
            {"name": "Sukiyabashi Jiro Roppongi", "cuisine": "Sushi", "price": "Expensive", "desc": "High-end edomae sushi curated by master chefs."}
        ]
    },
    "new york": {
        "lat": 40.7128, "lng": -74.0060,
        "best_time": "September to November (Autumn) or April to June (Spring)",
        "distance_miles": 0, # Assumed reference
        "tips": [
            "Use the subway to save time and money; it runs 24/7.",
            "Tipping of 18-20% is customary in sit-down restaurants.",
            "Wear comfortable walking shoes; you will cover miles on foot.",
            "Book tickets for Broadway shows and popular museums in advance."
        ],
        "attractions": [
            {"name": "Statue of Liberty & Ellis Island", "desc": "America's monumental symbol of freedom, located in New York Harbor."},
            {"name": "Central Park", "desc": "A massive, green urban oasis in the center of Manhattan, perfect for walking and picnics."},
            {"name": "Times Square", "desc": "The neon-lit heart of the theater district and a bustling commercial intersection."},
            {"name": "Empire State Building", "desc": "A legendary 102-story Art Deco skyscraper with world-class observation decks."},
            {"name": "Metropolitan Museum of Art (The Met)", "desc": "One of the world's finest art galleries, containing over two million works."}
        ],
        "emergency": {"police": "911", "medical": "911", "fire": "911", "general": "911"},
        "hotels": {
            "budget": [
                {"name": "Freehand New York", "price": 95, "rating": 4.2, "desc": "Artistic hostel-hotel hybrid in Flatiron with trendy rooftop bar."},
                {"name": "The Jane Hotel", "price": 85, "rating": 4.0, "desc": "Historic cabin-style rooms in the West Village."}
            ],
            "moderate": [
                {"name": "Arlo NoMad", "price": 210, "rating": 4.4, "desc": "Micro-rooms with floor-to-ceiling windows and exceptional location."},
                {"name": "CitizenM Bowery", "price": 260, "rating": 4.7, "desc": "High-tech boutique hotel in the trendy Lower East Side."}
            ],
            "luxury": [
                {"name": "The Plaza Hotel", "price": 850, "rating": 4.8, "desc": "Famous luxury castle-like hotel at the edge of Central Park."},
                {"name": "The Carlyle, A Rosewood Hotel", "price": 900, "rating": 4.9, "desc": "Elegant Upper East Side classic famous for jazz and discrete style."}
            ]
        },
        "restaurants": [
            {"name": "Joe's Pizza", "cuisine": "New York Pizza", "price": "Cheap", "desc": "Greenwich Village institution serving iconic thin-crust slices."},
            {"name": "Katz's Delicatessen", "cuisine": "Jewish Deli", "price": "Moderate", "desc": "World-famous deli serving piled-high pastrami sandwiches since 1888."},
            {"name": "Le Bernardin", "cuisine": "Seafood / French Fine Dining", "price": "Expensive", "desc": "Elite 3-Michelin-starred restaurant run by chef Eric Ripert."}
        ]
    }
}

# General fallback templates to dynamically support ANY destination in the world
FALLBACK_ACTIVITIES = {
    "morning": [
        "Explore the historic old town, walking through cobble-stone streets and local markets.",
        "Take a guided city walking tour to discover historical landmarks and local secrets.",
        "Visit the main cathedral/temple complex and learn about the local culture and architecture.",
        "Stroll through the city's botanical garden and enjoy a peaceful morning coffee.",
        "Visit a prominent local museum or art center to admire historical artifacts and crafts."
    ],
    "afternoon": [
        "Head to the primary central square for shopping, viewing monuments, and street performances.",
        "Rent a bike or take local transit to a scenic viewpoint overlooking the region.",
        "Attend an interactive cooking class or craft workshop to engage with local artisans.",
        "Take a relaxing boat trip/cruise along the local river or coastline.",
        "Explore the local botanical park or museum of natural history."
    ],
    "evening": [
        "Enjoy a beautiful sunset stroll along the promenade, riverwalk, or harbor.",
        "Indulge in a local food tasting tour at the night market or food street.",
        "Attend a traditional music performance, theatre show, or cultural dance.",
        "Visit a rooftop terrace or popular sky lounge for drinks with a panoramic night view.",
        "Join a historic ghost tour or neighborhood night-walk to hear stories of the city's past."
    ]
}

PACKING_BASE = [
    "Passport, visa, and photo ID",
    "Credit/debit cards and some local currency",
    "Phone chargers and wall adapters",
    "Toothbrush, toothpaste, and toiletries bag",
    "Comfortable walking shoes",
    "First-aid kit and personal prescription medications",
    "Travel pillow and eye mask"
]

def get_fallback_destination(name):
    # Dynamic fallback based on hashing/generating details from name
    name_clean = name.strip().title()
    h = hash(name_clean)
    
    # Generate coordinates based on standard country patterns or random-seeded offsets
    random.seed(h)
    lat = round(random.uniform(-40.0, 60.0), 4)
    lng = round(random.uniform(-120.0, 140.0), 4)
    
    # Pre-determined locations for common fallbacks
    if "london" in name.lower():
        lat, lng = 51.5074, -0.1278
    elif "rome" in name.lower():
        lat, lng = 41.9028, 12.4964
    elif "sydney" in name.lower():
        lat, lng = -33.8688, 151.2093
    elif "rome" in name.lower():
        lat, lng = 41.9028, 12.4964
    elif "singapore" in name.lower():
        lat, lng = 1.3521, 103.8198
    elif "cairo" in name.lower():
        lat, lng = 30.0444, 31.2357
    elif "barcelona" in name.lower():
        lat, lng = 41.3851, 2.1734
    elif "bali" in name.lower():
        lat, lng = -8.4095, 115.1889
    elif "dubai" in name.lower():
        lat, lng = 25.2048, 55.2708
        
    return {
        "lat": lat,
        "lng": lng,
        "best_time": f"October to April (for comfortable weather) or during seasonal festivals",
        "distance_miles": abs(h % 5000) + 500,
        "tips": [
            f"Always check local customs and dress codes in {name_clean}.",
            "Keep emergency contact details saved in offline notes.",
            "Use official registered taxis or ridesharing apps at the airport.",
            "Try local street food vendors with the longest queues—they're the freshest!"
        ],
        "attractions": [
            {"name": f"{name_clean} Old Quarter", "desc": "The historic center, showcasing traditional buildings, craft shops, and street markets."},
            {"name": f"{name_clean} Panoramic Viewpoint", "desc": "The highest point in the city, providing stunning views of the skyline and surroundings."},
            {"name": f"{name_clean} Museum of History", "desc": "A comprehensive museum presenting the rich heritage, archaeological discoveries, and culture of the region."},
            {"name": f"{name_clean} Waterfront Promenade", "desc": "A scenic pathway lining the water, lined with lively cafés, parks, and seating."},
            {"name": f"{name_clean} Central Market", "desc": "A buzzing indoor bazaar filled with regional produce, spices, textiles, and local crafts."}
        ],
        "emergency": {"police": "112", "medical": "112", "fire": "112", "general": "112"},
        "hotels": {
            "budget": [
                {"name": f"{name_clean} Backpacker Inn", "price": 25, "rating": 4.1, "desc": "Cozy shared rooms with social lounge and central access."},
                {"name": f"Green Tree Guesthouse", "price": 45, "rating": 3.8, "desc": "Clean and budget-friendly private rooms run by a hospitable family."}
            ],
            "moderate": [
                {"name": f"The Grand Avenue Hotel", "price": 95, "rating": 4.3, "desc": "Comfortable guest suites with breakfast buffet and gym access."},
                {"name": f"{name_clean} Central Plaza Hotel", "price": 120, "rating": 4.5, "desc": "Modern rooms in the financial district, steps from popular transit routes."}
            ],
            "luxury": [
                {"name": f"The Royal Palms Resort", "price": 320, "rating": 4.8, "desc": "Stunning luxury resort offering private spa suites, fine dining, and pool deck."},
                {"name": f"The President {name_clean}", "price": 400, "rating": 4.9, "desc": "Elite 5-star skyscraper hotel with personalized butler services and views."}
            ]
        },
        "restaurants": [
            {"name": "Local Eats Plaza", "cuisine": "Local street food", "price": "Cheap", "desc": "A crowded market court highlighting the best local recipes."},
            {"name": "The Traditional Bistro", "cuisine": "Regional Cuisine", "price": "Moderate", "desc": "A cozy, highly-rated family restaurant serving classic regional meals."},
            {"name": "Skyline Bistro & Bar", "cuisine": "Fusion Fine Dining", "price": "Expensive", "desc": "Exquisite dining on the top floor overlooking the illuminated city."}
        ]
    }

def generate_trip_plan(current_location, destination, num_travelers, num_days, start_date, budget, travel_type, transport_pref):
    dest_key = destination.strip().lower()
    
    # Check database of custom templates, else construct fallback
    if dest_key in POPULAR_DESTINATIONS:
        details = POPULAR_DESTINATIONS[dest_key]
    else:
        # Match fuzzy (e.g. if 'paris' is inside 'paris, france')
        found = False
        for k in POPULAR_DESTINATIONS:
            if k in dest_key:
                details = POPULAR_DESTINATIONS[k]
                found = True
                break
        if not found:
            details = get_fallback_destination(destination)
            
    # Budget Tiering
    budget_total = float(budget)
    budget_per_day = budget_total / max(num_days, 1)
    
    if budget_per_day < 80:
        tier = "budget"
        accomm_cost_multiplier = 0.8
        food_cost_multiplier = 0.7
    elif budget_per_day < 250:
        tier = "moderate"
        accomm_cost_multiplier = 1.0
        food_cost_multiplier = 1.0
    else:
        tier = "luxury"
        accomm_cost_multiplier = 1.5
        food_cost_multiplier = 1.6

    selected_hotels = details["hotels"][tier]
    
    # Calculate estimated cost breakdown
    hotel_rate = selected_hotels[0]["price"]
    accom_est = hotel_rate * num_days * num_travelers
    
    # Food estimate
    if tier == "budget":
        food_per_day = 20
    elif tier == "moderate":
        food_per_day = 45
    else:
        food_per_day = 120
    food_est = food_per_day * num_days * num_travelers
    
    # Transport estimate
    if transport_pref.lower() == "flight":
        trans_per_person = 450
    elif transport_pref.lower() == "train":
        trans_per_person = 80
    elif transport_pref.lower() == "bus":
        trans_per_person = 30
    else: # Car
        trans_per_person = 60
    trans_est = trans_per_person * num_travelers
    
    # Activities estimate
    if tier == "budget":
        act_per_day = 10
    elif tier == "moderate":
        act_per_day = 30
    else:
        act_per_day = 80
    act_est = act_per_day * num_days * num_travelers
    
    total_est = accom_est + food_est + trans_est + act_est
    
    # Formulate packing checklist based on inputs
    packing_list = PACKING_BASE.copy()
    if travel_type.lower() == "family":
        packing_list.extend(["Kids toys & travel activity books", "Wet wipes and sanitizers", "Baby formula/snacks"])
    elif travel_type.lower() == "business":
        packing_list.extend(["Formal outfits & ironed shirts", "Laptop, HDMI cable, and notepad", "Business cards"])
    elif travel_type.lower() == "friends":
        packing_list.extend(["Portable Bluetooth speaker", "Card games / travel games", "Group cash tracker app setup"])
    
    if transport_pref.lower() == "flight":
        packing_list.extend(["Noise-cancelling headphones", "Neck pillow", "Luggage scale", "Boarding passes"])
    elif transport_pref.lower() == "car":
        packing_list.extend(["Car phone mount", "Emergency roadside kit", "Travel cooler with snacks & water"])

    # Forecast weather simulation based on month
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    month_name = start_date_obj.strftime("%B")
    
    # Simple simulated weather based on destination latitude
    is_tropical = abs(details["lat"]) < 23.5
    is_southern_hemisphere = details["lat"] < 0
    
    # Determine season temperature ranges
    month_num = start_date_obj.month
    if is_tropical:
        avg_temp = random.randint(75, 88)
        condition = random.choice(["Sunny with gentle breeze", "Humid and overcast", "Tropical evening showers"])
    else:
        # Seasons
        if month_num in [12, 1, 2]: # Winter in north, Summer in south
            avg_temp = random.randint(70, 85) if is_southern_hemisphere else random.randint(30, 48)
            condition = "Pleasant & sunny" if is_southern_hemisphere else "Cold with light wind/snow"
        elif month_num in [6, 7, 8]: # Summer in north, Winter in south
            avg_temp = random.randint(32, 50) if is_southern_hemisphere else random.randint(75, 92)
            condition = "Chilly & breezy" if is_southern_hemisphere else "Sunny and warm"
        else: # Spring / Autumn
            avg_temp = random.randint(55, 68)
            condition = random.choice(["Mild & pleasant", "Light passing clouds", "Crisp autumnal breeze"])
            
    weather_data = {
        "month": month_name,
        "avg_temp": f"{avg_temp}°F / {round((avg_temp - 32) * 5/9)}°C",
        "condition": condition,
        "summary": f"Expect {condition.lower()} conditions for {destination} in {month_name}. Packing light layers is recommended."
    }
    
    # Generate Itinerary
    itinerary = []
    # Seed random with destination and date details to ensure deterministic results for identical inquiries
    random.seed(hash(destination + start_date + str(num_days)))
    
    for day in range(1, num_days + 1):
        m_act = random.choice(FALLBACK_ACTIVITIES["morning"])
        a_act = random.choice(FALLBACK_ACTIVITIES["afternoon"])
        e_act = random.choice(FALLBACK_ACTIVITIES["evening"])
        
        # Replace placeholders if popular destination
        if dest_key in POPULAR_DESTINATIONS or any(k in dest_key for k in POPULAR_DESTINATIONS):
            # Substitute with actual attraction names
            att = details["attractions"]
            m_act = f"Visit the stunning {att[(day*2) % len(att)]['name']} - {att[(day*2) % len(att)]['desc']}"
            a_act = f"Head to the gorgeous {att[(day*3) % len(att)]['name']}. {att[(day*3) % len(att)]['desc']}"
            
        rest = details["restaurants"]
        selected_rest = rest[(day) % len(rest)]
        
        # Make activities vary a bit by day
        day_plan = {
            "day_num": day,
            "morning": {
                "activity": m_act,
                "location": destination,
                "cost": 0 if tier == "budget" else random.randint(15, 35)
            },
            "afternoon": {
                "activity": a_act,
                "location": destination,
                "cost": random.randint(5, 15) if tier == "budget" else random.randint(25, 60)
            },
            "evening": {
                "activity": e_act,
                "location": destination,
                "cost": random.randint(0, 10) if tier == "budget" else random.randint(30, 80)
            },
            "restaurant": {
                "name": selected_rest["name"],
                "cuisine": selected_rest["cuisine"],
                "price": selected_rest["price"],
                "desc": selected_rest["desc"]
            }
        }
        itinerary.append(day_plan)
        
    local_transport_modes = [
        {"mode": "Public Subway / Metro", "cost": "$2 - $5 per ride", "frequency": "Every 3-5 mins", "tips": "Buy a daily transit card at the automated kiosks for discounts."},
        {"mode": "Local Buses", "cost": "$1 - $3 per ride", "frequency": "Every 10-15 mins", "tips": "Keep small bills or exact coins handy. Check routes online beforehand."},
        {"mode": "Ridehailing / Taxis", "cost": "$15 - $40 depending on traffic", "frequency": "On-demand via app", "tips": "Confirm prices or ensure the driver turns on the taximeter before heading off."}
    ]
    
    trip_plan = {
        "current_location": current_location,
        "destination": destination,
        "num_travelers": num_travelers,
        "num_days": num_days,
        "start_date": start_date,
        "budget": budget_total,
        "travel_type": travel_type,
        "transport_pref": transport_pref,
        "lat": details["lat"],
        "lng": details["lng"],
        "distance_info": f"Approx. {details['distance_miles']} miles (from departure node reference)",
        "best_time": details["best_time"],
        "emergency_contacts": details["emergency"],
        "packing_checklist": [{"item": item, "checked": False} for item in packing_list],
        "travel_tips": details["tips"],
        "weather": weather_data,
        "hotels": details["hotels"][tier],
        "restaurants": details["restaurants"],
        "local_transport": local_transport_modes,
        "cost_breakdown": {
            "accommodation": accom_est,
            "food": food_est,
            "transport": trans_est,
            "activities": act_est,
            "total": total_est
        },
        "itinerary": itinerary
    }
    
    return trip_plan


def get_ai_assistant_response(user_query, trip_plan_dict):
    """
    Simulates a highly context-aware travel chatbot assistant.
    If the user's message matches modification patterns (e.g. 'change day X afternoon'),
    it edits the trip_plan_dict and returns (response_message, updated_trip_plan_dict).
    Otherwise, it returns (response_message, None).
    """
    query = user_query.lower().strip()
    destination = trip_plan_dict.get("destination", "your destination")
    itinerary = trip_plan_dict.get("itinerary", [])
    
    # 1. Modify itinerary check
    # Pattern: 'change day X morning/afternoon/evening to [new activity]'
    # Pattern: 'update day X restaurant to [new restaurant]'
    modified = False
    
    if "change day" in query or "update day" in query or "replace day" in query:
        # Try to parse day number
        day_num = None
        for word in query.split():
            if word.isdigit():
                day_num = int(word)
                break
        
        if day_num and 1 <= day_num <= len(itinerary):
            time_of_day = None
            if "morning" in query:
                time_of_day = "morning"
            elif "afternoon" in query:
                time_of_day = "afternoon"
            elif "evening" in query:
                time_of_day = "evening"
            
            # Find the new activity text
            new_activity = None
            for marker in ["to ", "with ", "for "]:
                if marker in query:
                    parts = user_query.split(marker)
                    if len(parts) > 1:
                        new_activity = parts[-1].strip()
                        break
                        
            if time_of_day and new_activity:
                # Modify it!
                old_act = itinerary[day_num - 1][time_of_day]["activity"]
                itinerary[day_num - 1][time_of_day]["activity"] = new_activity
                modified = True
                return (
                    f"✨ **Itinerary Updated!** I have modified Day {day_num} {time_of_day}.\n\n"
                    f"* **Before:** {old_act}\n"
                    f"* **After:** {new_activity}\n\n"
                    f"The updated travel details have been saved to your trip history automatically.",
                    trip_plan_dict
                )
            
            # Handle restaurant updates
            if "restaurant" in query:
                new_rest = None
                for marker in ["to ", "with ", "for "]:
                    if marker in query:
                        parts = user_query.split(marker)
                        if len(parts) > 1:
                            new_rest = parts[-1].strip()
                            break
                if new_rest:
                    old_rest = itinerary[day_num - 1]["restaurant"]["name"]
                    itinerary[day_num - 1]["restaurant"]["name"] = new_rest
                    itinerary[day_num - 1]["restaurant"]["desc"] = "Custom recommended spot by AI Assistant."
                    modified = True
                    return (
                        f"🍽️ **Restaurant Updated!** I have updated the lunch/dinner spot for Day {day_num}.\n\n"
                        f"* **Before:** {old_rest}\n"
                        f"* **After:** {new_rest}\n\n"
                        f"Your trip plan has been saved.",
                        trip_plan_dict
                    )
                    
    # 2. General Query Answering based on Destination details
    if "weather" in query:
        w = trip_plan_dict.get("weather", {})
        return (
            f"🌦️ **Weather Forecast for {destination}:**\n"
            f"During your start month ({w.get('month', 'travel time')}), the average temperature is about **{w.get('avg_temp', 'N/A')}**.\n"
            f"The typical condition is: **{w.get('condition', 'N/A')}**.\n\n"
            f"*AI Tip: {w.get('summary', '')}*",
            None
        )
    elif "packing" in query or "pack" in query:
        checklist = trip_plan_dict.get("packing_checklist", [])
        items_str = "\n".join([f"- {c['item']}" for c in checklist[:6]])
        return (
            f"🧳 **Here are some top packing tips for {destination}:**\n"
            f"Based on your travel style and preferences, make sure to pack:\n{items_str}\n\n"
            f"You can view and check off the complete, interactive checklist under the 'Packing List' tab!",
            None
        )
    elif "emergency" in query or "help" in query or "police" in query:
        contacts = trip_plan_dict.get("emergency_contacts", {})
        contacts_str = "\n".join([f"* **{k.title()}**: {v}" for k, v in contacts.items()])
        return (
            f"🚨 **Emergency Helplines for {destination}:**\n"
            f"{contacts_str}\n\n"
            f"Stay safe and save these numbers in your speed dial if needed.",
            None
        )
    elif "budget" in query or "cost" in query or "price" in query:
        costs = trip_plan_dict.get("cost_breakdown", {})
        return (
            f"💰 **Estimated Trip Expenses for {destination}:**\n"
            f"* 🏨 **Accommodation:** ${costs.get('accommodation', 0):,.2f}\n"
            f"* 🍔 **Food/Meals:** ${costs.get('food', 0):,.2f}\n"
            f"* 🚗 **Transportation:** ${costs.get('transport', 0):,.2f}\n"
            f"* 🎟️ **Activities/Entry tickets:** ${costs.get('activities', 0):,.2f}\n\n"
            f"**Total Estimate:** **${costs.get('total', 0):,.2f}**\n"
            f"*Note: Rates are based on your selected travelers and duration.*",
            None
        )
    elif "tip" in query or "advice" in query:
        tips = trip_plan_dict.get("travel_tips", [])
        tips_str = "\n".join([f"- {t}" for t in tips])
        return (
            f"💡 **Travel Tips for {destination}:**\n"
            f"{tips_str}",
            None
        )
    else:
        # Generic helpful assistant response
        responses = [
            f"Hello! I am your AI Travel Assistant. I'm here to help you optimize your trip to **{destination}**.\n\n"
            f"You can ask me questions about **weather, expenses, packing checklists, or local emergency numbers**.\n\n"
            f"💡 *Tip:* You can ask me to change the activities in your itinerary. For example: *'change day 1 afternoon to visit a local cooking class'*.",
            
            f"I'm on it! I can help you modify your travel plans for **{destination}**. Let me know what you'd like to adjust!\n\n"
            f"To customize your day-by-day plans, try typing: *'change day 2 morning to relaxing at a street cafe'*.",
            
            f"Need details about local food, places to stay, or sights in **{destination}**? Just ask!\n"
            f"You can also check the other tabs on this page to view your customized Leaflet map, weather, and safety numbers."
        ]
        return random.choice(responses), None
