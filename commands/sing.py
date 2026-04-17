import requests
import os
import time

def register(bot):
    # এপিআই বেস ইউআরএল সংগ্রহ করার ফাংশন
    def get_base_api_url():
        try:
            res = requests.get("https://raw.githubusercontent.com/Mostakim0978/D1PT0/refs/heads/main/baseApiUrl.json")
            return res.json().get("api")
        except:
            return "https://api.samir.pw" # ব্যাকআপ এপিআই

    # /sing অথবা /music কমান্ড
    @bot.message_handler(commands=['sing', 'music', 'play'])
    def handle_sing(message):
        args = message.text.split()
        if len(args) < 2:
            return bot.reply_to(message, "❌ Please provide a song name or link.")

        query = " ".join(args[1:])
        bot.send_chat_action(message.chat.id, 'upload_document')
        
        # ক্যাশ ফোল্ডার তৈরি
        if not os.path.exists("cache"):
            os.makedirs("cache")
        
        file_path = f"cache/music_{int(time.time())}.mp3"

        try:
            base_url = get_base_api_url()
            
            # ১. গান সার্চ করা এবং ভিডিও আইডি বের করা
            search_res = requests.get(f"{base_url}/ytFullSearch?songName={query}").json()
            
            if not search_res or len(search_res) == 0:
                return bot.reply_to(message, "⭕ No results found.")
            
            video_id = search_res[0].get("id")
            title = search_res[0].get("title", "Requested Song")

            # ২. ডাউনলোড লিঙ্ক সংগ্রহ করা (MP3 ফরম্যাট)
            dl_info = requests.get(f"{base_url}/ytDl3?link={video_id}&format=mp3").json()
            download_link = dl_info.get("downloadLink")

            if download_link:
                # ৩. অডিও ফাইলটি ডাউনলোড করে সেভ করা
                audio_data = requests.get(download_link).content
                with open(file_path, 'wb') as f:
                    f.write(audio_data)

                # ৪. টেলিগ্রামে অডিও পাঠানো
                with open(file_path, 'rb') as audio_file:
                    bot.send_audio(
                        message.chat.id, 
                        audio_file, 
                        caption=f"✅ | 𝐇𝐞𝐫𝐞'𝐬 𝐲𝐨𝐮𝐫 𝐫𝐞𝐪𝐮𝐞𝐬𝐭𝐞𝐝 𝐬𝐨𝐧𝐠\n➡️ {title}\n🕊️💖 𝐒𝐲𝐬𝐭𝐞𝐦 𝐁𝐲: 𝐌𝐫.𝐊𝐢𝐧𝐠",
                        title=title
                    )
            else:
                bot.reply_to(message, "❌ Download link not found.")

        except Exception as e:
            bot.reply_to(message, f"❌ Error: {str(e)}")

        finally:
            # অটো-ডিলিট সিস্টেম: ফাইল পাঠানো শেষ হলে ক্যাশ থেকে ডিলিট করা
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except:
                    pass

    # কোনো প্রিফিক্স ছাড়া 'song ' বা 'music ' দিয়ে শুরু করলে ডিটেক্ট করবে
    @bot.message_handler(func=lambda m: m.text and (m.text.lower().startswith("song ") or m.text.lower().startswith("music ")))
    def auto_sing(message):
        msg_text = message.text.lower()
        if msg_text.startswith("song "):
            query = message.text[5:]
        else:
            query = message.text[6:]
            
        if query:
            # সরাসরি কমান্ড হ্যান্ডলারে পাঠানো
            message.text = f"/sing {query}"
            handle_sing(message)
