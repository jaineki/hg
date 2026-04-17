import os
import time
from yt_dlp import YoutubeDL

def register(bot):
    @bot.message_handler(commands=['sing', 'song'])
    def handle_sing(message):
        args = message.text.split()
        if len(args) < 2:
            return bot.reply_to(message, "⚠️ 𝐆𝐚𝐚𝐧 𝐞𝐫 𝐧𝐚𝐚𝐦 𝐭𝐚 𝐛𝐨𝐥𝐨 𝐛𝐚𝐛𝐲! 🎵")

        query = " ".join(args[1:])
        wait_msg = bot.reply_to(message, f"🔎 𝐖𝐚𝐢𝐭 𝐤𝐨𝐫𝐨 𝐛𝐚𝐛𝐞, '{query}' 𝐤𝐡𝐮𝐣𝐜𝐡𝐢... ✨")

        if not os.path.exists("cache"): os.makedirs("cache")
        file_base = f"cache/song_{int(time.time())}"
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': file_base + '.%(ext)s',
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
            'quiet': True
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([f"ytsearch1:{query}"])
            
            final_file = file_base + ".mp3"
            if os.path.exists(final_file):
                with open(final_file, 'rb') as audio:
                    bot.send_audio(message.chat.id, audio, caption=f"✅ 𝐇𝐞𝐫𝐞 𝐢𝐬 𝐲𝐨𝐮𝐫 𝐦𝐮𝐬𝐢𝐜 𝐛𝐚𝐛𝐲! 🕊️💖")
                os.remove(final_file) # পাঠানোর পর ডিলিট
            
            bot.delete_message(message.chat.id, wait_msg.message_id)
        except Exception as e:
            bot.reply_to(message, "❌ Error hoilo babe! FFmpeg install koro.")
