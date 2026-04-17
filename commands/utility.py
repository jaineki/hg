import os
import glob

def register(bot):
    @bot.message_handler(commands=['refresh'])
    def clear_cache(message):
        files = glob.glob('cache/*')
        for f in files: os.remove(f)
        bot.reply_to(message, "🧹 𝐒𝐲𝐬𝐭𝐞𝐦 𝐂𝐥𝐞𝐚𝐧𝐞𝐝! ⚔️")
