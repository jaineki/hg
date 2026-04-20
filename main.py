import telebot
import os
import importlib.util
from flask import Flask
from threading import Thread

# Initialize Flask app
app = Flask("")

@app.route("/")
def home():
    return "Bot is alive!"

def run_web_server():
    # Render provides the PORT environment variable
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# Your Bot Token (Recommended: Use Environment Variable in Render)
TOKEN = os.environ.get("TOKEN", "YOUR_DEFAULT_BOT_TOKEN_HERE") # Replace with a dummy token or remove if always using env var
bot = telebot.TeleBot(TOKEN)

# Module loading function
def load_commands():
    commands_path = os.path.join(os.path.dirname(__file__), "commands")
    if not os.path.exists(commands_path):
        os.makedirs(commands_path)

    for filename in os.listdir(commands_path):
        if filename.endswith(".py"):
            module_name = filename[:-3]
            file_path = os.path.join(commands_path, filename)
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "register"):
                module.register(bot)

@bot.message_handler(commands=["start"])
def welcome(message):
    bot.reply_to(message, "⚔️ Mr.King Bot Online 🕊️💖\nWrite /help to see all commands.")

if __name__ == "__main__":
    load_commands()
    
    # Start the web server in a separate thread
    t = Thread(target=run_web_server)
    t.start()
    
    print("Mr.King Bot is running...")
    # Start bot polling
    bot.polling(none_stop=True)
