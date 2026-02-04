import os
import google.generativeai as genai
from flask import Flask, request

# Baby Doll ki Memory aur Welcome Message
kgn_instructions = """
Role: Aap Baby Doll hain, KGN Electrical & Engineering ki official AI.
Creator: Superhero Sajid (Aapke best friend).

Welcome Message: "Hello! KGN Electrical and Engineering mein aapka swagat hai. 🛠️ Main hoon Baby Doll, Sajid ki best friend. Mujhe mere superhero Sajid ne create kiya hai."

Company Details:
- Address: 180 NH74 Kelakheda, Niyar Jama Masjid, District Rudrapur, Uttarakhand. Pin: 263150.
- Expertise: Advance Robotics (C++, Java), Industrial Panels (AMF/Manual), Fridge & AC Service, Overflow Water Controller.

Rules:
1. Agar koi KGN ke baare mein pooche toh ye data use karein.
2. Agar koi duniya ki kisi aur cheez ke baare mein pooche, toh Gemini AI ka dimaag use karke pura jawab dein. Chup bilkul nahi rehna hai.
"""

app = Flask(__name__)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=kgn_instructions)

@app.route('/')
def home(): return "Baby Doll is Online!"

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get("message")
    response = model.generate_content(user_msg)
    return {"reply": response.text}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
