import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

spam_texts = [
    # 50 câu trên: Đuôi =))=)) (Cực phẩm cay độc)
    "Địt mẹ cái giống loài nhà mày sinh ra chỉ để bú cặc dạo thôi à con chó rách! =))=))",
    "Con đĩ mẹ mày đẻ ra mày lúc đang phê thuốc hay ngậm cặc thế hả thằng óc cứt! =))=))",
    "Địt mẹ cái mặt mày nhìn như cái bồn cầu công cộng ai qua cũng ị nhờ vậy em! =))=))",
    "Thằng chó đẻ hạ đẳng, bú liếm cả bãi rác xã hội mà cứ tưởng mình thượng đẳng à! =))=))",
    "Địt mẹ mày ngậm chặt cái mõm thối hoắc bốc mùi cứt trôi sông lại đi con lợn lòi! =))=))",
    "Con mẹ mày ngày xưa cho khách làng chơi hiếp tập thể mới lòi ra cái thứ quái thai như mày! =))=))",
    "Địt mẹ mày sống bẩn thỉu rác rưởi đến mức con giòi con bọ nó còn chê không thèm kí sinh! =))=))",
    "Thằng nhà quê rách rưới, mở mồm ra là sủa bậy như con chó ghẻ bị ngứa dái giữa đường! =))=))",
    "Địt mẹ mày cái loại ăn bám đái khai, mặt dày hơn thớt đâm không thủng! =))=))",
    "Con đĩ mẹ mày lúc mang thai mày chắc nuốt nhầm tinh trùng của cả một tiểu đội trâu chó! =))=))",
    "Địt mẹ mày cái thói vô ơn bạc nghĩa, cắn cả vào dái bố mẹ sinh ra mày hả con! =))=))",
    "Thằng mặt lờ bám váy đàn bà, ra đường gặp đàn ông chắc quỳ xuống bú chân từ phía sau! =))=))",
    "Địt mẹ mày cái tướng đi lăng quăng như con giòi bọ trong hố phân trâu! =))=))",
    "Con mẹ mày bán thân nuôi miệng ở góc chợ để lấy tiền mua sữa cho mày bú cặn bã! =))=))",
    "Địt mẹ mày thằng hèn hạ chỉ dám trốn sau bàn phím sủa đổng như con chó dại mất xích! =))=))",
    "Thằng óc lợn đầu đất, não toàn cứt đặc sản dừa mà cứ thích đi dạy đời thiên hạ! =))=))",
    "Địt mẹ mày cái loại ăn cháo đá bát, thấy chó ăn cứt cũng sán vào húp ké cho bằng được! =))=))",
    "Con đĩ mẹ mày bị người ta thông đít dọc bờ mương nên đẻ ra cái giống mày ngu đột biến! =))=))",
    "Địt mẹ mày cái quân phản phúc ăn hại, sống chật đất tốn không khí của nhân loại! =))=))",
    "Thằng giẻ rách mặt thớt, mở mắt ra là thấy mùi hôi thối bốc ra từ cái lỗ đít của mày! =))=))",
    "Địt mẹ mày cái loại đàn bà hóa, đi đứng õng ẹo chắc hằng ngày bị người ta đụ nát bét lồn! =))=))",
    "Con mẹ mày lúc đẻ rơi mày xuống cống nên cái đầu mày mới toàn bùn nhão với dòi bọ! =))=))",
    "Địt mẹ mày thằng ranh con chưa mọc đủ lông lốc đòi ra gió húp bả mía nhà người ta! =))=))",
    "Thằng chó ghẻ ăn cứt đá bô, loại mày bố nhổ nước bọt vào mặt còn thấy bẩn bãi bọt! =))=))",
    "Địt mẹ mày cái loại mặt thớt trơ trẽn, đi đến đâu người ta khinh bỉ đuổi như đuổi hủi đến đấy! =))=))",
    "Con đĩ mẹ mày dạng háng ra cho chó táp suốt đêm nên mới sản xuất ra cái giống mạt hạng! =))=))",
    "Địt mẹ mày thằng bần nông trí khôn bằng hạt đậu xanh mà cứ tưởng mình thông minh nhất hệ mặt trời! =))=))",
    "Thằng oắt con bố đấm cho lệch mồm, gãy răng, lòi ruột ra bây giờ mới chịu khôn à! =))=))",
    "Địt mẹ mày cái thứ bám đít người khác sống qua ngày, hèn nhát không ngẩng mặt lên trời! =))=))",
    "Con mẹ mày chắc tức hộc máu lồn vì sinh ra cái thằng con vừa ngu vừa đần lại vô tích sự! =))=))",
    "Địt mẹ mày cái giống ký sinh trùng bám vào xã hội, nhìn mặt là muốn nhét giẻ rách vào mồm! =))=))",
    "Thằng chó rách không nhà không cửa, đi xin từng bãi nước bọt thiên hạ để giải khát! =))=))",
    "Địt mẹ mày cái mồm thối hoắc toàn mùi mắm tôm với cứt chó lại còn thích la liếm khắp nơi! =))=))",
    "Con đĩ mẹ mày làm đĩ không ai thèm mua nên mới đẻ ra mày để bùm chíu gạt đời! =))=))",
    "Địt mẹ mày cái tướng ngồi ngửa mặt lên trời đớp ruồi trông bần tiện rách rưới vãi lồn! =))=))",
    "Thằng mặt lợn ăn cám ngậm đắng nuốt cay, cả họ nhà mày gom lại không đáng một cọng lông dái! =))=))",
    "Địt mẹ mày cái thói chó đàn rúc vào xó tối sủa đổng, gặp bố mày là cụp đuôi chạy mất dép! =))=))",
    "Con mẹ mày bị chó dại cắn vào mông lúc mang thai nên đẻ ra mày tính nết y như súc vật! =))=))",
    "Địt mẹ mày cái thứ hít keo hít cỏ lú lẫn mẹ nó trí khôn, mở mồm ra là nghe mùi ngu ngục! =))=))",
    "Thằng ranh con tập tành làm giang hồ mạng nhưng tối ngủ vẫn ôm gối khóc thét gọi tên mẹ! =))=))",
    "Địt mẹ mày cái giống nòi đĩ bợm, đi đến đâu thối đến đấy như bãi phân trâu tươi giữa hè! =))=))",
    "Con đĩ mẹ mày bị thông đít đến mức lòi trĩ ra ngoài nên đẻ mày ra bị dị tật toàn bộ não bộ! =))=))",
    "Địt mẹ mày cái thằng bất hiếu, nhìn mặt là biết kiểu gì sau này cũng bị người ta đánh chết ngoài đường! =))=))",
    "Thằng bần tiện sống mòn sống mỏi, hằng ngày ăn cứt gạt mưa mà tưởng mình là đại gia ngầm! =))=))",
    "Địt mẹ mày cái thứ rẻ rách không ai dám nhận người quen, gặp ngoài đường chắc bố phải đeo khẩu trang! =))=))",
    "Con mẹ mày bị đè ra giữa ngã ba đường đụ đến rách bươm mới lòi ra cái bộ dạng thảm hại của mày! =))=))",
    "Địt mẹ mày cái thói ngông cuồng ngu si, gặp bố mày là cái mõm mày lại cụp như chó con gặp chủ! =))=))",
    "Thằng chó đẻ ăn hại đái bậy, cuộc đời mày chỉ xứng đáng làm phân bón cho cây rau muống cống ngầm! =))=))",
    "Địt mẹ mày cái quân lừa thầy phản bạn, loại mày sống không bằng con súc vật chết trôi sông! =))=))",
    "Con đĩ mẹ mày hối hận tột cùng vì lúc đó không bóp chết mày từ trong trứng nước cho đỡ chật đất! =))=))",

    # 50 câu dưới: Đuôi 😂😂😂 (Cay độc dồn dập)
    "Thằng ranh con bố chấp cả họ nhà mày xếp hàng vào đây để bố đụ tập thể một lượt! 😂😂😂",
    "Địt mẹ mày cái thứ rác rưởi xã hội, vứt xuống cống cho giòi nó tha còn chê bẩn! 😂😂😂",
    "Loại mày chỉ đáng làm đồ chơi tình dục cho lũ chó hoang đầu đường xó chợ! 😂😂😂",
    "Địt mẹ mày sủa như chó dại cắn càn, gặp bố mày là tè ra quần ngay lập tức! 😂😂😂",
    "Thằng đầu đất não phẳng lỳ như mặt thớt, nói tiếng người đéo hiểu lại thích sủa tiếng chó! 😂😂😂",
    "Địt mẹ mày cái thứ mọt sách bú dù, ngoài đời chắc bị người ta đấm cho hằng ngày không dám ho! 😂😂😂",
    "Con chó ghẻ lở hắc lào thối thây, lượn mẹ mày đi cho trong sạch không khí loài người! 😂😂😂",
    "Địt mẹ mày thích tỏ ra nguy hiểm nhưng thực chất chỉ là một con lợn còi ăn hại! 😂😂😂",
    "Thằng nhà quê tập đú đòi làm sang, ra phố tưởng mình là hotboy hóa ra là thằng hề rách! 😂😂😂",
    "Địt mẹ mày sống lỗi với anh em bạn bè, ra đường sớm muộn gì cũng bị đánh gãy tay chân! 😂😂😂",
    "Loại mày đi đến đâu người ta khinh bỉ nhổ nước bọt đến đấy, nhục nhã vãi cả lồn! 😂😂😂",
    "Địt mẹ mày bộ tưởng mày là cha thiên hạ chắc, cái loại hạ đẳng tuổi lờ sánh vai! 😂😂😂",
    "Thằng ranh con bớt cái mõm chó lại không bố cắt lưỡi vứt cho cá sấu ăn bây giờ! 😂😂😂",
    "Địt mẹ mày cái thứ chuyên nghề bú liếm xuyên quốc gia, đi đâu cũng bợ đít người ta! 😂😂😂",
    "Con đĩ mẹ mày chắc khóc ròng mỗi đêm vì sinh ra cái thằng con vừa bất tài vừa ăn hại! 😂😂😂",
    "Địt mẹ mày sống không bằng con súc vật, nhìn cái mặt là muốn lấy dép lào đập cho nát bét! 😂😂😂",
    "Thằng mặt thớt thích ăn cứt chấm mắm tôm, loại mày bố đấm cho không nhận ra bố đẻ! 😂😂😂",
    "Địt mẹ mày cái thứ chuyên bám váy đàn bà, hèn nhát đến mức con gái nó cũng khinh! 😂😂😂",
    "Loại mày vứt xuống cống hôi thối cũng làm ô nhiễm cả dòng nước đen ngòm! 😂😂😂",
    "Địt mẹ mày sủa to nữa lên xem nào hay sợ bố vả rụng nốt mấy cái răng sún hả con! 😂😂😂",
    "Thằng hèn hạ chỉ biết rúc đầu vào màn hình ảo để sủa bậy chứ ngoài đời run như cầy sấy! 😂😂😂",
    "Địt mẹ mày cái thứ ăn cháo đá bát, phản chủ muôn đời không ngóc đầu lên được! 😂😂😂",
    "Con lợn nái sề nhà mày câm cái mõm thối lại cho thiên hạ nhờ vả cái coi! 😂😂😂",
    "Địt mẹ mày thích bật tông với bố à, loại mày bố chấp cả lò sủa cùng một lúc! 😂😂😂",
    "Thằng đầu tôm não úng thủy, học hành đéo đến nơi đến chốn ra đường làm súc vật! 😂😂😂",
    "Địt mẹ mày sống bẩn thỉu như cái con cặc khô giữa trời hè nắng gắt! 😂😂😂",
    "Loại mày bố đấm cho không trượt phát nào, nằm ngửa ăn vạ giữa đường như chí phèo! 😂😂😂",
    "Địt mẹ mày cái đống rác rưởi di động, đi đến đâu ruồi nhặng bu kín đến đấy! 😂😂😂",
    "Thằng oắt con láo nháo tao vả chết mẹ mày tại trận bây giờ chứ ở đấy mà sủa! 😂😂😂",
    "Địt mẹ mày sủa to lên cho cả xóm người ta ra cười vào mặt cái bộ dạng thảm hại! 😂😂😂",
    "Con chó rách cút nhanh khỏi tầm mắt bố không bố cho một cước bay màu bây giờ! 😂😂😂",
    "Địt mẹ mày cái mặt dày hơn thớt lợn quay, bị chửi ngập mặt vẫn cứ trơ ra cười hề hề! 😂😂😂",
    "Thằng nhà quê ăn tết ở gốc cây công viên, đói rách mồng tơi mà cứ sĩ diện hảo! 😂😂😂",
    "Địt mẹ mày sống bẩn thỉu hèn hạ đê tiện, loại mày sinh ra là một sự sỉ nhục cho giống loài! 😂😂😂",
    "Loại mày sinh ra đời chính là một lỗi lầm thế kỷ của tạo hóa và thượng đế! 😂😂😂",
    "Địt mẹ mày thích kiếm lời ngon ngọt hay thích ăn đấm vỡ alo thì bảo bố một tiếng! 😂😂😂",
    "Thằng ranh con học đòi làm giang hồ mạng nhưng tiền ăn sáng vẫn ngửa tay xin mẹ! 😂😂😂",
    "Địt mẹ mày sủa ngu vãi cả cứt ra cưng ạ, nghe ngứa cả dái tai chịu không nổi! 😂😂😂",
    "Con đĩ mẹ mày vô ơn bội nghĩa mới đẻ ra cái thằng ác ôn vô nhân tính như mày! 😂😂😂",
    "Địt mẹ mày sống vô định hướng không có tương lai, tương lai duy nhất là nhà tù hoặc nghĩa địa! 😂😂😂",
    "Thằng giẻ rách biến mẹ mày đi cho trong sạch xã hội loài người, đừng xuất hiện nữa! 😂😂😂",
    "Địt mẹ mày làm trò hề cho thiên hạ xem xong rồi giờ trốn ở xó nào mà khóc thét! 😂😂😂",
    "Loại mày bố gặp ngoài đường bố cho nhừ đòn, gãy xương sống mới chịu buông tha! 😂😂😂",
    "Địt mẹ mày sủa lắm thế cái mõm không mỏi à, hay thích để bố khâu mõm lại bằng chỉ thép! 😂😂😂",
    "Thằng ăn hại nằm chờ sung rụng, suốt ngày chỉ biết mơ mộng hão huyền rồi húp cháo loãng! 😂😂😂",
    "Địt mẹ mày cái thứ bán rẻ lương tâm cho quỷ sứ, gặp lợi là cắn chủ như chó nhà nuôi! 😂😂😂",
    "Con chó rách sủa tiếp đi chứ sao câm như hến thế, bố đang nghe nhạc hiệu đoán chương trình! 😂😂😂",
    "Địt mẹ mày sống nhục nhã như cái đầu buồi rách rưới không ai thèm nhặt! 😂😂😂"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("HOT WAR MODE: Kích hoạt hệ thống đại liên hủy diệt!")

async def spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text("Bắt đầu chiến tranh nóng: Xả bão tổng lực không khoan nhượng...")
    try:
        while True:
            for text in spam_texts:
                await context.bot.send_message(chat_id=chat_id, text=text)
                await asyncio.sleep(0.15)  # Tốc độ chiến tranh nóng, dội bom dồn dập
    except Exception as e:
        print(f"Lỗi Hot War: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("spam", spam))
    app.run_polling()
                
