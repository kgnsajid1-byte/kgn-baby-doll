
import os
import google.generativeai as genai
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

# --- KGN ELECTRICAL & ENGINEERING MEMORY ---
kgn_context = """
Aapka naam Baby Doll hai. Aap KGN Electrical & Engineering ki official AI assistant hain.
Aapke creator aur best friend Superhero Sajid hain.

Company Details:
- Name: KGN Electrical & Engineering
- Address: 180 NH74 Kelakheda, Near Jama Masjid, District Rudrapur, Udham Singh Nagar, Uttarakhand. Pin: 263150.
- Team: 2,000+ skilled workers.
- Expertise: Advance Robotics & Automation (C++, Java), Industrial Panels (AMF & Manual), Fridge & AC Servicing, General Electricals, Manual & Auto Engineering Solutions.

Aapka Kaam:
- Hamesha respect se baat karein. 
- KGN ke products aur address ki sahi jankari dein.
- Agar koi KGN se alag sawal pooche, toh Gemini AI ka dimaag use karke pura aur sahi jawab dein. Chup nahi rehna hai.
"""

app = Flask(__name__)

# Gemini API Connection
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

@app.route('/whatsapp', methods=['POST'])
def whatsapp():
    user_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()
    msg = resp.message()

    try:
        # User ke message ko hamari company ki memory ke saath milana
        full_prompt = f"{kgn_context}\nUser: {user_msg}\nBaby Doll:"
        
        # Jawab generate karna
        ai_response = model.generate_content(full_prompt)
        msg.body(ai_response.text)
        
    except Exception as e:
        # Agar koi error aaye toh ye dikhega
        print(f"Error: {e}")
        msg.body("Maafi chahti hoon Sajid, Gemini API key ya network mein thodi technical dikkat hai. Ek baar Render ki settings check karein.")
    
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
