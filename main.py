import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Lấy Token từ Railway
TOKEN = os.getenv("TOKEN")

# Danh sách câu chửi / spam vô hạn
spam_texts = [
    "Đm mày chết chưa con chó ăn cứt!",
    "Thằng nhà quê rách rưới bố mày gọi đấy!",
    "Bú hộ bố cái đm mày ngu vãi lồn!",
    "Con đĩ mẹ mày sao lại dột thế hả em?",
    "Ăn cứt đá bộ, loại mày chỉ có vứt đi!",
    "Đm thằng mặt lờ này láo nháo à?",
    "Cái loại mày đú đởn ăn hại xã hội!",
    "Bố mày vả cho rụng răng bây giờ con ạ!",
    "Sủa đi em ơi, sủa to lên cho bố nghe nào!",
    "ĐM MÀY NGU NHƯ BÒ LÊN ĐỈNH OLYMPIA!",
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot spam vô hạn đã sẵn sàng! Gõ /spam để bắt đầu xả bão.")

async def spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text("Đang bắt đầu chiến dịch xả bão vô hạn...")
    
    # Vòng lặp vô hạn bắn tin nhắn
    try:
        while True:
            for text in spam_texts:
                await context.bot.send_message(chat_id=chat_id, text=text)
                await asyncio.sleep(1.5)  # Nghỉ 1.5 giây mỗi tin để đỡ bị Telegram ban
    except Exception as e:
        print(f"Lỗi spam: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("spam", spam))
    
    print("Bot Telegram dang khoi dong...")
    app.run_polling()
    
