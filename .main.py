import os
import telebot
import requests
import io
from flask import Flask

# التوكن الخاص بك مدمج وجاهز
TOKEN = "8921597972:AAFCE0IuUktQfz_M5hm8w4jMb_BYUF0zAQQ"
bot = telebot.TeleBot(TOKEN)

# إنشاء سيرفر وهمي صغير لكي يقبله موقع Render المجاني
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Alive!"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً بك! 🚀\nاكتب لي أي وصف باللغة الإنجليزية وسأصنع لك الصورة فوراً وبحرية مطلقة وبدون توقف.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_prompt = message.text
    bot.reply_to(message, "⚡ جاري توليد صورتك الآن بسرعة فائقة...")
    try:
        clean_prompt = requests.utils.quote(user_prompt)
        API_URL = f"https://pollinations.ai{clean_prompt}?width=512&height=512&nologo=true&private=true"
        response = requests.get(API_URL, timeout=20)
        
        if response.status_code == 200:
            bio = io.BytesIO(response.content)
            bio.name = 'image.png'
            bot.send_photo(message.chat.id, photo=bio)
        else:
            bot.reply_to(message, "❌ فشل السيرفر في الاستجابة، حاول مجدداً.")
    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ: {str(e)}")

if __name__ == "__main__":
    # تشغيل البوت والسيرفر معاً
    import threading
    threading.Thread(target=bot.infinity_polling).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
