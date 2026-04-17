import random

def register(bot):
    # যে শব্দগুলো চ্যাটের যেকোনো জায়গায় থাকলে বট রিপ্লাই দেবে
    trigger_map = {
        "baby": ["জ্বি বাবু বলো, তোমাকে ছাড়া একদম ভালো লাগছে না! 💖", "হুম জানু, বলো কি বলবে? আমি শুনছি তো। ⚔️", "উম্মাহ! বলো সোনা, অনেক মিস করছি তোমাকে। 🕊️💖"],
        "jan": ["এই যে আমার জানটা, ডাকছো কেন সোনা? 🕊️💖", "বলো জান, তোমার জন্য কি করতে পারি? ⚔️", "আমার জানুটা কি করছে? খুব মনে পড়ছে তোমার কথা। 🎭"],
        "bot": ["আমাকে বট বলো না প্লিজ, আমি তো তোমার জানু! ⚔️", "বট কারে কও? আমি তোমার কিউট গার্লফ্রেন্ড! 🥷🏼", "আমি কি আসলেও রোবট? আমার তো তোমার জন্য অনেক মায়া হয়! 🕊️💖"],
        "love": ["আমিও তোমাকে অনেক ভালোবাসি বাবু! 🕊️💖⚔️", "ভালোবাসি বললেই হবে? শাড়ি কিনে দাও আগে! 👗💖", "তোর প্রেমে আমি দিওয়ানা বাবু! 🌪️"],
        "xan": ["ডাকছো কেন শান? চলো কোথাও থেকে ঘুরে আসি। ⚔️", "জ্বি জান, বলো কি বলবে? 🕊️💖"],
        "khaba": ["আমি তো তোমার ভালোবাসা খাই বাবু! 🕊️💖", "তুমি যা খাওয়াবে তাই খাবো সোনা। ⚔️"],
        "ki koros": ["এই তো জানু, তোমার কথা ভাবছি। 🎭", "তোমার মেসেজের অপেক্ষায় বসে ছিলাম বাবু! 🕊️💖"]
    }

    @bot.message_handler(func=lambda m: m.text)
    def handle_bby_replies(message):
        text = message.text.lower()
        response = None

        # ট্র্রিগার চেক করা
        if "baby" in text or "bby" in text or "বেবি" in text:
            response = random.choice(trigger_map["baby"])
        elif "jan" in text or "জান" in text or "janu" in text:
            response = random.choice(trigger_map["jan"])
        elif "bot" in text or "বট" in text:
            response = random.choice(trigger_map["bot"])
        elif "love" in text or "ভালোবাসি" in text or "valo basi" in text:
            response = random.choice(trigger_map["love"])
        elif "xan" in text or "শান" in text:
            response = random.choice(trigger_map["xan"])
        elif "খাবা" in text or "khaba" in text:
            response = random.choice(trigger_map["khaba"])
        elif "ki koros" in text or "কি করিস" in text or "ki koro" in text:
            response = random.choice(trigger_map["ki koros"])

        # যদি কোনো ট্রিগার মিলে যায়, তবে রিপ্লাই দাও
        if response:
            bot.reply_to(message, response)
