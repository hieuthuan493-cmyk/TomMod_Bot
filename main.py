import time

print("Bot Telegram dang khoi dong...")

# Vong lap giu bot chay 24/7 tren Railway
while True:
    print("Bot van dang hoat dong tot...")
    time.sleep(60)
  
import os
import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Thiết lập logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Danh sách 100 câu chửi kết hợp câu của mày và các câu nặng đô (50 câu đuôi =))=йки, 50 câu đuôi 😂😂)
SPAM_MESSAGES = [
    # 50 câu đầu đuôi =))=йки
    "Địt mẹ con mẹ đĩ mẹ đồ vào =))=йки",
    "Đụ má mày cái thứ chó chết này =))=йки",
    "Con đĩ mẹ mày cái đồ súc sinh ăn cứt =))=йки",
    "Địt mẹ con mẹ đĩ mẹ đồ vào mặt lồn =))=йки",
    "Thứ lồn què nhà mày sinh ra mày chỉ để làm rác =))=йки",
    "Địt mẹ mày cái loại mặt lồn ăn hại =))=йки",
    "Bà cha mày cái đồ chó đẻ ngu si =))=йки",
    "Địt mẹ con mẹ đĩ mẹ đồ vào cái loại súc vật =))=йки",
    "Cái loại đĩ bợm nhà mày chỉ đáng bú cu =))=йки",
    "Mẹ kiếp nhà mày cái thứ súc vật đú đởn =))=йки",
    "Đụ con mẹ mày cái đồ cặn bã hạ đẳng =))=йки",
    "Địt mẹ con mẹ đĩ mẹ đồ vào nghe cho rõ =))=йки",
    "Thứ con hoang bú cu thiên hạ =))=йки",
    "Địt mẹ cái mồm thối tha của mày =))=йки",
    "Cái loại đầu buồi giẻ rách nhà mày =))=йки",
    "Địt mẹ con mẹ đĩ mẹ đồ vào thứ rác rưởi =))=йки",
    "Con đĩ mẹ mày bú liếm đéo có liêm sỉ =))=йки",
    "Đụ má mày cái thứ não cứt vô ơn =))=йки",
    "Thứ chó hoang rách việc thích sủa bậy =))=йки",
    "Địt mẹ con mẹ đĩ mẹ đồ vào cái đồ ăn hại =))=йки",
    "Địt mẹ mày cái loại mặt dày bốc cứt =))=йки",
    "Bà cha mày cái đồ đĩ chó ăn hại =))=йки",
    "Cái loại súc sinh đầu đất nhà mày =))=йки",
    "Địt mẹ con mẹ đĩ mẹ đồ vào loại hạ cấp =))=йки",
    "Đụ con mẹ mày cái thứ rác rưởi hạ cấp =))=йки",
    "Thứ lồn cái nhà mày đẻ ra mày đúng phí cơm =))=йки",
    "Địt mẹ cái quân vô học bú đít thiên hạ =))=йки",
    "Địt mẹ con mẹ đĩ mẹ đồ vào cái quân khốn nạn =))=йки",
    "Mẹ kiếp nhà mày cái đồ chó ngậm máu phun người =))=йки",
    "Đụ má mày cái loại ăn bám bú cu =))=йки",
    "Thứ con đĩ mẹ mày cái đồ đầu tôm não cá =))=йки",
    "Địt mẹ con mẹ đĩ mẹ đồ vào thứ bất hiếu =))=йки",
    "Địt con mẹ mày cái quân bất hiếu ăn cứt =))=йки",
    "Cái loại súc vật lai tạp vô tích sự =))=йки",
    "Đụ má cái mồm chó gặm xương của mày =))=йки",
    "Địt mẹ con mẹ đĩ mẹ đồ vào cái mồm thối =))=йки",
    "Thứ đĩ bợm rẻ rách bú liếm thiên hạ =))=йки",
    "Địt mẹ mày cái loại hèn hạ mạt hạng =))=йки",
    "Bà cha mày cái đồ chó hoang đói khát =))=йки",
    "Địt mẹ con mẹ đĩ mẹ đồ vào cái loại mày =))=йки",
    "Cái loại mặt lồn trơ trẽn vô sỉ =))=йки",
    "Đụ con mẹ mày cái thứ đầu buồi giẻ rách =))=йки",
    "Thứ chó đẻ ăn hại đái khai =))=йки",
    "Địt mẹ con mẹ đĩ mẹ đồ vào đồ súc sinh =))=йки",
    "Địt mẹ mày cái loại súc sinh mọc đuôi =))=йки",
    "Mẹ kiếp nhà mày cái quân đĩ thõa lăng loàn =))=йки",
    "Đụ má mày cái thứ não tàn bú cứt =))=йки",
    "Địt mẹ con mẹ đĩ mẹ đồ vào cái loại chó =))=йки",
    "Thứ con hoang vô thừa nhận nhà mày =))=йки",
    "Địt mẹ mày cái loại mặt dày vô liêm sỉ =))=йки",

    # 50 câu sau đuôi 😂😂
    "Địt mẹ con mẹ đĩ mẹ đồ vào cho khôn ra 😂😂",
    "Đụ má mày cái loại chó đẻ ngu lâu 😂😂",
    "Con đĩ mẹ mày cái đồ súc sinh ăn cứt 😂😂",
    "Địt mẹ con mẹ đĩ mẹ đồ vào cái loại mặt lồn 😂😂",
    "Thứ lồn què nhà mày chỉ đáng bú cu 😂😂",
    "Địt mẹ mày cái loại mặt lồn ăn hại 😂😂",
    "Bà cha mày cái đồ chó rách vô tích sự 😂😂",
    "Địt mẹ con mẹ đĩ mẹ đồ vào cái đồ ăn bám 😂😂",
    "Cái loại đĩ bợm nhà mày sinh ra thừa thãi 😂😂",
    "Mẹ kiếp nhà mày cái thứ cặn bã hạ đẳng 😂😂",
    "Đụ con mẹ mày cái đồ súc vật đú đởn 😂😂",
    "Địt mẹ con mẹ đĩ mẹ đồ vào cái quân rác rưởi 😂😂",
    "Thứ con hoang chuyên đi bú liếm 😂😂",
    "Địt mẹ cái mồm chó ngậm cứt của mày 😂😂",
    "Cái loại đầu buồi giẻ rách thích sủa 😂😂",
    "Địt mẹ con mẹ đĩ mẹ đồ vào nghe cho thấm 😂😂",
    "Con đĩ mẹ mày cái đồ não cứt vô ơn 😂😂",
    "Đụ má mày cái thứ chó hoang đói khát 😂😂",
    "Thứ mặt dày hèn hạ mạt hạng nhà mày 😂😂",
    "Địt mẹ con mẹ đĩ mẹ đồ vào cái đồ ngu 😂😂",
    "Địt mẹ mày cái loại đĩ cái bợm đời 😂😂",
    "Bà cha mày cái đồ chó chết tiệt 😂😂",
    "Cái loại súc sinh đầu đất ăn hại 😂😂",
    "Địt mẹ con mẹ đĩ mẹ đồ vào loại súc vật 😂😂",
    "Đụ con mẹ mày cái thứ rác rưởi hôi hám 😂😂",
    "Thứ lồn cái nhà mày đẻ ra phí gạo 😂😂",
    "Địt mẹ cái quân vô học bú đít thiên hạ 😂😂",
    "Địt mẹ con mẹ đĩ mẹ đồ vào cái quân đốn mạt 😂😂",
    "Mẹ kiếp nhà mày cái đồ chó ngậm máu 😂😂",
    "Đụ má mày cái loại ăn bám bú cu suốt ngày 😂😂",
    "Thứ con đĩ mẹ mày cái đồ đầu tôm 😂😂",
    "Địt mẹ con mẹ đĩ mẹ đồ vào cái đồ hèn 😂😂",
    "Địt con mẹ mày cái quân bất hiếu đốn mạt 😂😂",
    "Cái loại súc vật lai tạp đáng vứt sọt rác 😂😂",
    "Đụ má cái mồm chó thối tha của mày 😂😂",
    "Địt mẹ con mẹ đĩ mẹ đồ vào cái mõm thối 😂😂",
    "Thứ đĩ bợm rẻ rách không ai thèm nhìn 😂😂",
    "Địt mẹ mày cái loại hèn hạ bẩn thỉu 😂😂",
    "Bà cha mày cái đồ chó hoang rách việc 😂😂",
    "Địt mẹ con mẹ đĩ mẹ đồ vào cái loại khốn 😂😂",
    "Cái loại mặt lồn trơ trẽn hết thuốc chữa 😂😂",
    "Đụ con mẹ mày cái thứ đầu buồi ăn hại 😂😂",
    "Thứ chó đẻ chuyên đi phá làng phá xóm 😂😂",
    "Địt mẹ con mẹ đĩ mẹ đồ vào cái loại chó ghẻ 😂😂",
    "Địt mẹ mày cái loại súc sinh mọc đuôi 😂😂",
    "Mẹ kiếp nhà mày cái quân đĩ thõa mặt dày 😂😂",
    "Đụ má mày cái thứ não tàn chuyên bú cứt 😂😂",
    "Địt mẹ con mẹ đĩ mẹ đồ vào ăn cứt tiếp đi 😂😂",
    "Thứ con hoang vô thừa nhận đáng khinh 😂😂",
    "Địt mẹ mày cái loại vô liêm sỉ hết nấc 😂😂"
]

# Từ điển lưu trạng thái chạy spam cho từng chat_id
active_spammers = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot chửi tục đã sẵn sàng! Gõ /info để bắt đầu xả láng, gõ /stop để dừng lại.")

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if active_spammers.get(chat_id):
        await update.message.reply_text("Bot đang xả láng rồi, muốn dừng thì gõ /stop nhé!")
        return

    active_spammers[chat_id] = True
    await update.message.reply_text("Bắt đầu chiến dịch chửi tục 100 câu tốc độ 0.1s!")
    
    try:
        index = 0
        while active_spammers.get(chat_id, False):
            msg = SPAM_MESSAGES[index % len(SPAM_MESSAGES)]
            await context.bot.send_message(chat_id=chat_id, text=msg)
            index += 1
            await asyncio.sleep(0.1)
    except Exception as e:
        logging.error(f"Lỗi khi gửi tin nhắn: {e}")

async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if active_spammers.get(chat_id):
        active_spammers[chat_id] = False
        await update.message.reply_text("Đã dừng cuộc chiến thành công!")
    else:
        await update.message.reply_text("Bot có đang chạy đâu mà đòi dừng!")

def main():
    token = os.environ.get("TOKEN")
    if not token:
        print("LỖI: Chưa cấu hình biến môi trường TOKEN!")
        return

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info_command))
    app.add_handler(CommandHandler("stop", stop_command))

    print("Bot đang chạy...")
    app.run_polling()

if __name__ == "__main__":
    main()
