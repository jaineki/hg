import requests
import os
import time

def register(bot):
    # এপিআই বেস ইউআরএল সংগ্রহ
    def get_base_url():
        try:
            res = requests.get("https://raw.githubusercontent.com/mahmudx7/HINATA/main/baseApiUrl.json")
            return res.json().get("mahmud")
        except:
            return "https://api.samir.pw"

    # ১. কমান্ড দিয়ে ডাউনলোড করার অপশন (/alldl)
    @bot.message_handler(commands=['alldl', 'download'])
    def handle_command_dl(message):
        args = message.text.split()
        if len(args) > 1:
            process_download(message, args[1])

    # ২. অটোমেটিক লিঙ্ক ডিটেক্টর (কোনো কমান্ড ছাড়া লিঙ্ক দিলেই কাজ করবে)
    @bot.message_handler(func=lambda m: m.text and any(x in m.text for x in ["facebook.com", "tiktok.com", "instagram.com", "youtube.com", "youtu.be"]))
    def auto_link_dl(message):
        process_download(message, message.text.strip())

    # ৩. মূল ডাউনলোড এবং অটো-ডিলিট প্রসেস
    def process_download(message, url):
        # ক্যাশ ফোল্ডার নিশ্চিত করা
        if not os.path.exists("cache"):
            os.makedirs("cache")
            
        # ফাইলের একটি ইউনিক নাম তৈরি
        file_path = f"cache/video_{int(time.time())}.mp4"
        
        try:
            bot.send_chat_action(message.chat.id, 'upload_video')
            
            # এপিআই থেকে ভিডিও লিঙ্ক আনা
            base = get_base_url()
            api_url = f"{base}/api/download/video?link={url}"
            res = requests.get(api_url).json()
            video_url = res.get('result', {}).get('url') or res.get('url')

            if video_url:
                # ভিডিও ফাইলটি লোকাল স্টোরেজে ডাউনলোড করা (যাতে পাঠানো সহজ হয়)
                video_data = requests.get(video_url).content
                with open(file_path, 'wb') as f:
                    f.write(video_data)
                
                # ভিডিও পাঠানো
                with open(file_path, 'rb') as video_file:
                    bot.send_video(
                        message.chat.id, 
                        video_file, 
                        caption="✅ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐂𝐨𝐦𝐩𝐥𝐞𝐭𝐞 ⚔️\n🕊️💖 𝐒𝐲𝐬𝐭𝐞𝐦 𝐁𝐲: 𝐌𝐫.𝐊𝐢𝐧𝐠"
                    )
            else:
                bot.reply_to(message, "❌ এই লিঙ্কের ভিডিও খুঁজে পাওয়া যায়নি।")
                
        except Exception as e:
            bot.reply_to(message, "⚠️ ডাউনলোড করতে সমস্যা হয়েছে।")
        
        finally:
            # ফাইল পাঠানো শেষ হলে বা এরর আসলেও ফাইলটি সিস্টেম থেকে ডিলিট করা
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"🧹 Temporary file {file_path} deleted successfully.")
                except Exception as del_error:
                    print(f"Error deleting file: {del_error}")
