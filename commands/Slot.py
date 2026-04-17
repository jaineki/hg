import json
import os
import random
from datetime import datetime

# কনফিগারেশন ফাইলের পাথ
CONFIG_PATH = "cache/slot_config.json"

def register(bot):
    # স্মার্ট অ্যামাউন্ট পার্সার (1M, 1K ইত্যাদি বুঝতে পারে)
    def parse_smart_amount(amount_str):
        if not amount_str: return 0
        amount_str = str(amount_str).lower().strip()
        units = {'k': 1000, 'm': 1000000, 'b': 1000000000, 't': 1000000000000}
        
        unit = amount_str[-1]
        if unit in units:
            try:
                return int(float(amount_str[:-1]) * units[unit])
            except:
                return 0
        try:
            return int(amount_str)
        except:
            return 0

    # নাম্বার ফরম্যাটার (1000 কে 1K বানায়)
    def format_number(num):
        if num >= 1000000000000: return f"{num / 1000000000000:.1f}T"
        if num >= 1000000000: return f"{num / 1000000000:.1f}B"
        if num >= 1000000: return f"{num / 1000000:.1f}M"
        if num >= 1000: return f"{num / 1000:.1f}K"
        return "{:,}".format(num)

    # কনফিগারেশন লোড বা তৈরি
    def get_config():
        if not os.path.exists("cache"): os.makedirs("cache")
        if not os.path.exists(CONFIG_PATH):
            default = {"winRate": 0.65, "maxBet": 200000000}
            with open(CONFIG_PATH, "w") as f: json.dump(default, f)
            return default
        with open(CONFIG_PATH, "r") as f: return json.load(f)

    @bot.message_handler(commands=['slot'])
    def handle_slot(message):
        admin_uid = 61588626550420 # বসের ইউআইডি
        user_id = message.from_user.id
        args = message.text.split()
        config = get_config()

        # --- অ্যাডমিন কন্ট্রোল ---
        if len(args) > 2 and user_id == admin_uid:
            if args[1] == "limit":
                new_limit = parse_smart_amount(args[2])
                config["maxBet"] = new_limit
                with open(CONFIG_PATH, "w") as f: json.dump(config, f)
                return bot.reply_to(message, f"✅ | 𝐒𝐥𝐨𝐭 𝐥𝐢𝐦𝐢𝐭 𝐮𝐩𝐝𝐚𝐭𝐞𝐝 𝐭𝐨: ${format_number(new_limit)}")
            
            if args[1] == "win":
                try:
                    new_rate = float(args[2])
                    config["winRate"] = new_rate / 100
                    with open(CONFIG_PATH, "w") as f: json.dump(config, f)
                    return bot.reply_to(message, f"✅ | 𝐒𝐥𝐨𝐭 𝐰𝐢𝐧 𝐫𝐚𝐭𝐞 𝐮𝐩𝐝𝐚𝐭𝐞𝐝 𝐭𝐨: {new_rate}%")
                except: pass

        # --- গেম লজিক ---
        if len(args) < 2:
            return bot.reply_to(message, ">🎀 ( 𝐒𝐥𝐨𝐭 𝐌𝐚𝐜𝐡𝐢𝐧𝐞 )\n━━━━━━━━━━━━━━━━━━\n⚠️ | 𝐁𝐚𝐛𝐲, 𝐞𝐧𝐭𝐞𝐫 𝐚𝐧 𝐚𝐦𝐨𝐮𝐧𝐭! (𝐄𝐱: 𝟏𝐌)")

        bet_amount = parse_smart_amount(args[1])
        if bet_amount <= 0:
            return bot.reply_to(message, "⚠️ | 𝐁𝐚𝐛𝐲, 𝐞𝐧𝐭𝐞𝐫 𝐚 𝐯𝐚𝐥𝐢𝐝 𝐚𝐦𝐨𝐮𝐧𝐭!")
        
        if bet_amount > config["maxBet"]:
            return bot.reply_to(message, f"❌ | 𝐁𝐚𝐛𝐲, 𝐭𝐡𝐞 𝐦𝐚𝐱𝐢𝐦𝐮𝐦 𝐬𝐥𝐨𝐭 𝐥𝐢𝐦𝐢𝐭 𝐢𝐬 ${format_number(config['maxBet'])}!")

        # স্লট সিম্বল
        symbols = ["🍒", "💎", "⭐", "💰", "👑", "🍀"]
        is_win = random.random() < config["winRate"]
        
        footer = "━━━━━━━━━━━━━━━━━━\n• 𝐄𝐧𝐣𝐨𝐲 𝐛𝐛𝐲🐉 [ 💛 | 💛 | 💛 ]"

        if is_win:
            win_sym = random.choice(symbols)
            s1 = s2 = s3 = win_sym
            win_money = bet_amount # 2x রিটার্ন (বেট + উইন)
            
            res_msg = (
                f">🎀\n━━━━━━━━━━━━━━━━━━\n"
                f"🏆 | 𝐘𝐨𝐮 𝐰𝐨𝐧: ${format_number(bet_amount + win_money)} (𝟐𝐱)\n"
                f"🎰 | [ {s1} | {s2} | {s3} ]\n{footer}"
            )
        else:
            s1 = random.choice(symbols)
            s2 = random.choice(symbols)
            s3 = random.choice(symbols)
            # যদি ভুল করে ৩টা মিলে যায় হারার সময়, তবে একটা বদলে দাও
            if s1 == s2 == s3: s3 = "💔"
            
            res_msg = (
                f">🎀\n━━━━━━━━━━━━━━━━━━\n"
                f"💀 | 𝐘𝐨𝐮 𝐥𝐨𝐬𝐭: ${format_number(bet_amount)}\n"
                f"🎰 | [ {s1} | {s2} | {s3} ]\n{footer}"
            )

        bot.reply_to(message, res_msg)
