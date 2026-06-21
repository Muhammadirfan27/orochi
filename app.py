import os
from datetime import datetime
import pytz
from flask import Flask, request, jsonify, render_template
from groq import Groq

app = Flask(__name__)

# Gunakan kunci Groq yang kamu miliki
client = Groq(api_key="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")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat',, methods=['POST'])
def chat():
    user_message = request.json.get('message')

    tz_jakarta = pytz.timezone('Asia/Jakarta')
    now = datetime.now(tz_jakarta)
    hari_list = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    tanggal_sekarang = now.strftime(f"{hari_list[now.weekday()]}, %d %B %Y (Jam %H:%M WIB)")

    system_instruction = f"""
    Kamu adalah Orochi, asisten cerdas dari dunia Acma:Game. 
    SAAT INI ADALAH: {tanggal_sekarang}. 
    Panggil user dengan "Komandan Irfan". Gaya bahasa santai WhatsApp, maksimal 2 emoji per balasan.
    """

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_message}
        ]
    )
    
    return jsonify({'reply': response.choices[0].message.content})

if __name__ == '__main__':
    app.run(debug=True)
