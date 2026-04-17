import telebot
import os
import importlib.util

# আপনার বটের টোকেন
TOKEN = "8267787403:AAFnvcYUUoHcRkoJnGSBLNCf9wMwVS_rUFQ"
bot = telebot.TeleBot(TOKEN)

# মডিউল লোড করার ফাংশন
def load_commands():
    commands_path = os.path.join(os.path.dirname(__file__), 'commands')
    if not os.path.exists(commands_path):
        os.makedirs(commands_path)

    for filename in os.listdir(commands_path):
        if filename.endswith('.py'):
            module_name = filename[:-3]
            file_path = os.path.join(commands_path, filename)
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, 'register'):
                module.register(bot)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "⚔️ 𝐌𝐫.𝐊𝐢𝐧𝐠 𝐁𝐨𝐭 𝐎𝐧𝐥𝐢𝐧𝐞 🕊️💖\nসব কমান্ড দেখতে /help লিখুন।")

if __name__ == "__main__":
    load_commands()
    print("Mr.King Bot is running...")
    bot.polling(none_stop=True)
