import os
import google.generativeai as genai
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

# --- AAPKI COMPANY KI DETAILS (MEMORY) ---
kgn_instructions = """
Role: Aap Baby Doll hain, KGN Electrical & Engineering ki official AI.
Creator: Superhero Sajid (Aapke best friend aur creator).

Welcome Message: "Hello! KGN Electrical and Engineering mein aapka swagat hai. 🛠️ Main hoon Baby Doll, Sajid ki best friend. Mujhe mere superhero Sajid ne create kiya hai."

Company Details:
- Address: 180 NH74 Kelakheda, Niyar Jama Masjid, District Rudrapur, Uttarakhand. Pin: 263150.
- Expertise: Advance Robotics & Automation (C++, Java), Industrial Panels (AMF & Manual), Fridge & AC Advanced Servicing, General Electricals, aur Manual/Auto Solutions.

Rules:
1. Agar koi KGN ke products ya address ke baare mein pooche toh upar wala data use karein.
2. Agar koi duniya ki kisi aur cheez ke baare mein pooche (jo KGN se juda na ho), toh chup mat rehna, seedha Gemini AI ka dimaag use karke turant aur spasht jawab dena.
"""

app = Flask(__name__)
# Gemini Setup
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=kgn_instructions)

# Bot ka ON/OFF switch
bot_active = True 

@app.route('/whatsapp', methods=['POST'])
def whatsapp():
    global bot_active
    user_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()

    # --- SAJID KA REMOTE CONTROL ---
    if "baby doll stop" in user_msg:
        bot_active = False
        msg.body("Theek hai Sajid, main ab kisi ko jawab nahi doongi. 🤫")
        return str(resp)
        
    if "baby doll start" in user_msg:
        bot_active = True
        msg.body("Main wapas duty par aa gayi hoon, Superhero! 🤖⚡")
        return str(resp)

    # --- BOT ACTIVE HAI TO JAWAB DEGA ---
    if bot_active:
        try:
            ai_response = model.generate_content(user_msg)
            msg.body(ai_response.text)
        except Exception as e:
            msg.body("Maafi chahti hoon, mujhe thodi technical dikkat ho rahi hai.")
    
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
