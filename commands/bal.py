import json
import os

# ব্যালেন্স ডাটা স্টোর করার ফাইল পাথ
BAL_FILE = "cache/user_balances.json"

def register(bot):
    # ডাটা লোড করার ইন্টারনাল ফাংশন
    def load_user_data():
        if not os.path.exists("cache"):
            os.makedirs("cache")
        
        if not os.path.exists(BAL_FILE):
            with open(BAL_FILE, "w") as f:
                json.dump({}, f)
            return {}
            
        try:
            with open(BAL_FILE, "r") as f:
                return json.load(f)
        except:
            return {}

    @bot.message_handler(commands=['bal', 'balance', 'money'])
    def check_balance(message):
        user = message.from_user
        user_id = str(user.id)
        u_name = user.username
        name = user.first_name

        # অ্যাডমিন ইউজারনেম চেক (আপনার জন্য আনলিমিটেড)
        if u_name == "mr_King1430":
            amount_display = "𝐈𝐧𝐟𝐢𝐧𝐢𝐭𝐲 ♾️"
        else:
            data = load_user_data()
            # নতুন ইউজারদের জন্য ৫০০ টাকা ডিফল্ট বোনাস
            amount = data.get(user_id, 500)
            amount_display = f"৳ {amount}"

        # ফাইনাল মেসেজ ফরম্যাট (কোনো star ব্যবহার করা হয়নি)
        msg = (
            "⚔️ 𝐌𝐫.𝐊𝐢𝐧𝐠 𝐖𝐚𝐥𝐥𝐞𝐭 𝐒𝐲𝐬𝐭𝐞𝐦 🕊️💖\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            f"👤 𝐔𝐬𝐞𝐫: {name}\n"
            f"💰 𝐁𝐚𝐥𝐚𝐧𝐜𝐞: {amount_display}\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "✨ 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐁𝐲: 𝐌𝐫.𝐊𝐢𝐧𝐠"
        )

        try:
            bot.reply_to(message, msg)
        except Exception as e:
            print(f"Error: {e}")
