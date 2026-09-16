import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Lấy Token từ biến môi trường trên Railway (hoặc thay trực tiếp token bot của mày vào đây)
TOKEN = os.getenv("TOKEN", "8882626353:AAFlup4z-OxSQL-oaeTqndDHkn238WcTrEI")

# Danh sách 100 câu chửi tục / câu spam vô hạn
spam_texts = [
    "Đm mày chết chưa con chó ăn cứt!",
    "Thằng nhà quê rách rưới bố mày gọi đấy!",
    "Bú hộ bố cái đm mày ngu vãi lồn!",
    "Con đĩ mẹ mày sao lại dốt thế hả em?",
    "Ăn cứt đá bô, loại mày chỉ có vứt đi!",
    "Đm thằng mặt lờ này láo nháo à?",
    "Cái loại mày đú đởn ăn hại xã hội!",
    "Bố mày vả cho rụng răng bây giờ con ạ!",
    "Sủa đi em ơi, sủa to lên cho bố nghe nào!",
    "ĐM MÀY NGU NHƯ BÒ LÊN ĐỈNH OLYMPIA!",
    "Thằng mặt thớt này bố gặp là bố đấm!",
    "ĐM MÀY SỐNG CHẬT ĐẤT CHẬT CHỘI VÃI LỒN!",
    "Con mẹ mày sinh mày ra chắc lúc đấy đau bụng!",
    "ĐM LOẠI CHÓ RÁCH ĂN HẠI ĐÁI BẬY!",
    "Bố mày chấp cả họ nhà mày vào sủa cùng đấy!",
    "Thằng mặt dơi hoạ mi này tuổi lờ gì?",
    "ĐM MÀY BỚT BẬT ĐI KHÔNG BỐ VẢ VỠ MỒM!",
    "Loại mày chỉ xứng đáng ăn cứt trâu thôi con ơi!",
    "ĐM THẰNG BÁN NHANG SỐNG DAI THẾ NHỈ?",
    "Bố mày là bố của thiên hạ, quỳ xuống!",
    "ĐM MÀY LÊN ĐỈNH CHƯA HAY VẪN ĐỨNG DƯỚI ĐÁY?",
    "Thằng óc chó này học lớp mấy mà đần thế?",
    "ĐM MÀY CÀ KHỊA NHẦM THẦY RỒI EM ƠI!",
    "Loại mày bố chấp bằng một ngón chân cái!",
    "ĐM MÀY CÒN SỦA LÀ BỐ CÒN KHINH!",
    "Thằng mặt ngựa cút mẹ mày đi cho trong sạch xã hội!",
    "ĐM MÀY ĂN GÌ NGU THẾ HAY ĂN CỨT HEO?",
    "Bố mày chấp cả làng nhà mày ra đây đọ mõm!",
    "ĐM MÀY THÍCH ĐU ĐÊM KHÔNG CON TRAI?",
    "Thằng ranh con tập tòi làm hacker à, cút!",
    "ĐM MÀY CÁI THỨ VÔ GIA CƯ VÔ VẬT!",
    "Bố mày vả phát bay màu khỏi trái đất luôn bây giờ!",
    "ĐM MÀY TỎ RA NGU VÃI LỒN LUÔN Á!",
    "Thằng khốn nạn này ngày nào cũng phải ăn đòn à?",
    "ĐM MÀY HÍT HÀ ĐỦ CHƯA HAY MUỐN THÊM?",
    "Loại mày gặp bố chỉ có nước quỳ lạy xin tha!",
    "ĐM MÀY NÓI NHIỀU VÃI CẢ CỨT!",
    "Thằng mõm nhôm này làm gì có tuổi với bố?",
    "ĐM MÀY CÚT MẸ RA CHỖ KHÁC CHƠI ĐỂ BỐ LÀM VIỆC!",
    "Bố mày khinh cái loại mày đến tận rốn!",
    "ĐM MÀY LẠI CÒN BÀY ĐẶT RA VẺ NGUY HIỂM?",
    "Thằng cặn bã xã hội này sao chưa ai hốt đi nhỉ?",
    "ĐM MÀY CÀ KHỊA BỐ LÀ SAI LẦM CUỘC ĐỜI RỒI!",
    "Loại mày chỉ đáng xách dép cho tổ tiên nhà bố!",
    "ĐM MÀY SỦA TO NỮA LÊN XEM NÀO!",
    "Thằng mặt sẹo này thích ăn đấm không em?",
    "ĐM MÀY CÁI THỨ Ổ KÉN SÂU BỌ!",
    "Bố mày nhổ nước bọt cũng đủ chết đuối nhà mày!",
    "ĐM MÀY ĐỪNG CỐ TỎ RA NGUY HIỂM NỮA!",
    "Thằng ăn hại đái khai này biến đi cho đẹp trời!",
    "ĐM MÀY THÍCH SPAM THÌ CHIỀU LUÔN NHÉ!",
    "Bố mày xả bão cho sập nguồn Telegram luôn bây giờ!",
    "ĐM MÀY ĐỪNG CÓ HÒ HẸN VỚI BỐ!",
    "Thằng ranh con chưa mọc đủ lông cánh!",
    "ĐM MÀY CÁI THỨ ĂN HẠI CHƯA LỚN!",
    "Bố mày chấp cả họ nhà mày bơi vào đây!",
    "ĐM MÀY THÍCH GÂY SỰ À CON CHÓ RÁCH?",
    "Thằng mặt chuột này chỉ giỏi chui rúc góc tối!",
    "ĐM MÀY NGON THÌ RA ĐÂY 1 ĐỐI 1 NÀO!",
    "Bố mày chấp mày gọi cả cụ tổ nhà mày ra luôn!",
    "ĐM MÀY CÁI LOẠI SỐNG LÂU CHẬT ĐẤT!",
    "Thằng bợm nhậu này say khướt rồi à?",
    "ĐM MÀY ĐÁNH RƠI LIÊM SỈ Ở ĐÂU THẾ?",
    "Bố mày lượm được nhưng đéo thèm trả đâu con ạ!",
    "ĐM MÀY CÁI THỨ MẶT DẠY VÔ LIÊM SỈ!",
    "Thằng khốn nạn này bớt sủa bậy lại đi!",
    "ĐM MÀY CÒN LEO LÉO LÀ BỐ CẮT LƯỠI!",
    "Bố mày đấm cho không trượt phát nào bây giờ!",
    "ĐM MÀY THÍCH ĐU ĐƯA KHÔNG EM GÁI?",
    "Thằng bóng lộ này điệu đà vừa thôi con!",
    "ĐM MÀY CÁI THỨ ĂN HẠI ĐÁI KHAI!",
    "Bố mày cho mày một vé về hành tinh của khỉ!",
    "ĐM MÀY SỦA NHỎ THÔI CHO BỐ NGỦ!",
    "Thằng mặt thớt này cút mẹ mày đi!",
    "ĐM MÀY LOẠI NÀY CHỈ ĐỂ LÀM PHÂN BÓN CÂY!",
    "Bố mày chấp hết tất cả các thể loại nhà mày!",
    "ĐM MÀY THÍCH BẬT TAY ĐÔI HÔNG?",
    "Thằng ranh con láo toét bị bố vả cho lệch mặt!",
    "ĐM MÀY CÁI THỨ ĐẦU ĐẤT ĐÍT PHI TỜ!",
    "Bố mày đập nát cái bàn phím của mày bây giờ!",
    "ĐM MÀY THÍCH SPAM VÔ HẠN TỐC ĐỘ 0.1S HẢ?",
    "Thằng đần độn này húp hộ bát cháo hành đi!",
    "ĐM MÀY CÁI LOẠI SỐNG KHÔNG BẰNG CON CÚN!",
    "Bố mày gọi tên mày là con chó ngu nhất năm!",
    "ĐM MÀY CÒN GÁM GÁM LÀ BỐ CHO ĂN ĐÒN!",
    "Thằng rác rưởi này lướt nhanh cho nước nó trong!",
    "ĐM MÀY THÍCH CHỬI NHAU KHÔNG CON TRAI?",
    "Bố mày chấp 3 ngày 3 đêm không nghỉ luôn!",
    "ĐM MÀY CÁI THỨ NGU LÂU DỐT BỀN VỮNG!",
    "Thằng đần này lo học hành đi lại còn đòi làm bot?",
    "ĐM MÀY BIẾN MẸ MÀY ĐI CHO KHUẤT MẮT BỐ!",
    "Bố mày chửi mỏi mồm rồi đấy nhé con giời!",
    "ĐM MÀY CÒN TÁI PHẠM LÀ BỐ ĐỤC VỠ MẶT!",
    "Thằng óc đậu phụ này câm mồm chưa con?",
    "ĐM MÀY LẦN SAU ĐỪNG CÓ DẠY BỐ NỮA NHÉ!",
    "Bố mày là trùm thiên hạ, cút đi con đĩ!",
    "ĐM MÀY SỐNG VÔ DỤNG VÃI LỒN LUÔN!",
    "Thằng khốn nạn này nhận quà spam từ bố đi!",
    "ĐM MÀY CHUẨN BỊ TINH THẦN ĂN BÃO CHƯA?",
    "Bố mày thả bom spam 24/7 ngập mồm mày luôn!",
    "ĐM MÀY XIN VĨNH BIỆT CỤ NHA CON CHÓ NGU!"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot chửi tục 24/7 đã sẵn sàng! Gõ /spam để bắt đầu xả bão!")

async def spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text("Bắt đầu xả bão chửi tục tốc độ 0.1s đây con giời!")
    
    # Vòng lặp spam vô hạn 100 câu chửi
    while True:
        for text in spam_texts:
            try:
                await context.bot.send_message(chat_id=chat_id, text=text)
                await asyncio.sleep(0.1) # Tốc độ 0.1 giây / tin nhắn
            except Exception as e:
                print(f"Lỗi gửi tin nhắn: {e}")
                await asyncio.sleep(1)

def main():
    if TOKEN == "THAY_TOKEN_BOT_VÀO_ĐÂY_NẾU_CHƯA_CÓ_ENV":
        print("CẢNH BÁO: Chưa cấu hình Token Bot Telegram!")
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("spam", spam))
    
    print("Bot đang chạy 24/7...")
    application.run_polling()

if __name__ == '__main__':
    main()
