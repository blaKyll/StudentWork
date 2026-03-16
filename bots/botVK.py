from vkbottle.bot import Bot,Message
TOKEN="vk1.a.EMNAr0rxz7XCtIgTMDD66tgdeRtzsOjfgXnPFcFRewD4fc2RINbou7v1UNHmvsnUyr3ZPdtr0ECWDoJEJpOQjS2C3eTt_uWPswhGWJY9DXnki7shb-mXoL2WyXjKNwgT-fBcc8MxSFp-1jTvoEGSobsQSwxVkCq4aj-5wyuEXYLAUTm6JSdptHnwr8-79Fd22W9A7TCKn9C2OwYNzhAdTg"

bot=Bot(TOKEN)
@bot.on.message(text="/start")
#команда /start
async def start_handler(message:Message):
    await message.answer("привет я твой первый бот в вк")
#Ответ на любое сообщение "Привет"
@bot.on.message(text="Привет")
async def hi_handler(message:Message):
    user_id=message.from_id
    await message.answer(f"И тебе привет id пользователя {user_id}")

#Обработка остального текста
@bot.on.message()
async def any_message(message:Message):
    text=message.text
    user_id=message.from_id
    if text:
        await message.answer(f"Ты написал {text}")
if __name__=="__main__":
    print("бот запущен")
    bot.run_forever()