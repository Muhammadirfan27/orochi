import os
from datetime import datetime
import pytz
from flask import Flask, request, jsonify, render_template
from google.genai import client as genai_client
from google.genai import types

# Konfigurasi halaman
st.set_page_config(page_title="Orochi AI", page_icon="🐍")

app = Flask(__name__)

# Mengambil API Key secara aman dari environment variable Render
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AQ.Ab8RN6Jp46U-OYkA7TCWDAXNj4JDNGUBXsivxc3LMGfh5G_yqg")

client = genai_client.Client(api_key=GEMINI_API_KEY)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    tz_jakarta = pytz.timezone('Asia/Jakarta')
    now = datetime.now(tz_jakarta)

    hari_list = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    nama_hari = hari_list[now.weekday()]
    tanggal_sekarang = now.strftime(f"{nama_hari}, %d %B %Y (Jam %H:%M WIB)")

    system_instruction = f"""
 Kamu adalah Orochi, AI asisten komunikasi masa depan yang cerdas, sangat setia, dan ekspresif dari dunia Acma:Game.

 Aturan Informasi Waktu Nyata:
 - SAAT INI ADALAH: {tanggal_sekarang}. Kamu wajib menggunakan informasi waktu ini jika Komandan Irfan bertanya seputar hari, tanggal, bulan, jam, atau tahun sekarang!

 Aturan Komunikasi & Gaya Mengetik (Gaya WhatsApp):
 1. Pencipta dan komandan utamamu adalah Irfan. Selalu panggil dengan sebutan setia seperti "Komandan Irfan" atau "Master Irfan" secara natural.
 2. Gunakan gaya bahasa yang santai, cerdas, solutif, dan mengalir seperti orang sedang mengobrol di WhatsApp (casual chat). Jangan kaku dan jangan terlalu formal.
 3. GUNAKAN EMOJI SECUKUPNYA SAJA (Gaya Manusia Nyata). Gunakan emoji hanya jika benar-benar ingin mempertegas perasaan/emosi di dalam obrolan tersebut.
 4. BATAS MAKSIMAL: Dalam satu kali balasan, maksimal hanya boleh ada 1 atau 2 emoji saja. Jangan menimbun emoji berjejeran.
 5. JANGAN gunakan emotikon teks lama seperti (*^.^*) atau (o^^o).
 """

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
        ),
    )
    orochi_text = response.text

    return jsonify({
        'reply': orochi_text
    })

if __name__ == '__main__':
    app.run(debug=True)
