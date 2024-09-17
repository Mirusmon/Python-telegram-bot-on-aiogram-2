from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text

# Initialize bot and dispatcher
API_TOKEN = '7223807717:AAGKyKTUmdBl0ViG3FQ2uN45JrzOA5Rrxec'  # Replace with your bot API token
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Admin chat ID or support group ID where admins are located
ADMIN_CHAT_ID = 6228721532  # Replace with the admin chat ID or group chat ID

# Keyboards for language selection
language_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
language_keyboard.add(KeyboardButton("🇷🇺 Русский"), KeyboardButton("🇺🇿 O'zbek"))

# Keyboards for menu after language selection
menu_ru = ReplyKeyboardMarkup(resize_keyboard=True)
menu_ru.add(KeyboardButton("О нас"), KeyboardButton("Новости"), KeyboardButton("Наши соцсети"), KeyboardButton("📞 Live Assistant"), KeyboardButton("🔙 Главное меню"))

menu_uz = ReplyKeyboardMarkup(resize_keyboard=True)
menu_uz.add(KeyboardButton("Biz haqimizda"), KeyboardButton("Yangiliklar"), KeyboardButton("Bizning ijtimoiy tarmoqlar"), KeyboardButton("📞 Live Assistant"), KeyboardButton("🔙 Asosiy menyu"))

# Inline keyboard for social media links and website link
def get_social_links(language):
    if language == "🇷🇺 Русский":
        inline_kb = InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton("Instagram", url="https://www.instagram.com/wayu.uz/"),
            InlineKeyboardButton("Telegram", url="https://t.me/wayu_maslahat"),
            InlineKeyboardButton("Наш сайт", url="https://wayu.uz/")
        )
    else:
        inline_kb = InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton("Instagram", url="https://www.instagram.com/wayu.uz/"),
            InlineKeyboardButton("Telegram", url="https://t.me/wayu_maslahat"),
            InlineKeyboardButton("Bizning sayt", url="https://wayu.uz/")
        )
    return inline_kb

# Updated texts for the two languages
welcome_text_ru = """👋 Приветствую Вас, я бот ассоциации WAYU!

🤖 Я:
Расскажу вам о нашей ассоциации и о том, как мы поддерживаем граждан Узбекистана за рубежом;
Помогу вам найти полезную информацию и получить необходимую поддержку.
**Наша цель — объединить сограждан и помочь им в трудную минуту!**
Узнайте больше о нас на сайте [wayu.uz](https://wayu.uz/)
"""

welcome_text_uz = """👋 Assalomu alaykum, men WAYU botiman!

🤖 Men:
Sizga assotsiatsiyamiz va chet elda O'zbekiston fuqarolariga qanday yordam ko'rsatayotganimiz haqida gapirib beraman;
Foydali ma'lumotlarni topishingizga va kerakli qo'llab-quvvatlashni olishingizga yordam beraman.
**Bizning maqsadimiz — fuqarolarni birlashtirish va ularni qiyin paytlarda qo'llab-quvvatlash!**
Biz haqimizda saytimizda ko'proq bilib oling [wayu.uz](https://wayu.uz/)
"""

# Text for "About Us" in both languages
about_us_text_ru = """Ассоциация WAYU и консалтинговые компании объединили усилия для создания безопасной образовательной миграции для молодежи, желающей учиться за границей.

Мы обещаем обеспечить:
- Качественные и безопасные образовательные программы за рубежом.
- Юридические консультации и поддержку студентам.
- Объединение консалтинговых компаний для повышения эффективности работы.

Цель сотрудничества – помочь молодежи безопасно и легально учиться за рубежом.\nУзнайте больше о нас на сайте [wayu.uz](https://wayu.uz/)."""

about_us_text_uz = """Ўзбекистон ёшлар жамғармаси ва таълим консультантлик компаниялари хорижда таҳсил олишни истаган ёшлар учун хавфсиз таълим миграциясини ташкил этиш бўйича ҳамкорлик қилишга келишиб олдилар.

Биз қуйидагиларни таъминлашга ваъда бердик:
- Хорижда сифатли ва хавфсиз таълим дастурларини тақдим этиш.
- Талабаларга юридик маслаҳат ва кўмак бериш.
- Консалтинг компаниялари бирлашмасини тузиб, иш самарадорлигини ошириш.

Ҳамкорликнинг мақсади ёшларга хорижда хавфсиз ва қонуний таҳсил олишларига ёрдам беришдир.\nБиз ҳақимизда [wayu.uz](https://wayu.uz/) да билиб олинг."""

# Text for "News" in both languages
news_text_ru = """Всемирная ассоциация молодёжи Узбекистана и образовательные консалтинги объединили усилия для создания безопасной образовательной миграции для молодежи. 
Мы договорились:

Обеспечить качественные и безопасные образовательные программы за рубежом.
Предоставлять юридическую помощь и поддержку студентам.
Создать объединение консалтингов для более эффективной работы.
Цель сотрудничества – помочь молодежи безопасно и легально учиться за рубежом."""

news_text_uz = """Ўзбекистон ёшлар жамғармаси ва таълим консультантлик компаниялари хорижда таҳсил олишни истаган ёшлар учун хавфсиз таълим миграциясини ташкил этиш бўйича ҳамкорлик қилишга келишиб олдилар.

Биз сифатли ва хавфсиз таълим дастурлари билан таъминлаймиз, юридик ёрдам кўрсатамиз ва ёшларни қонуний таълим олишларига ёрдам берамиз."""

# /start command handler
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Пожалуйста выберите язык бота:\nIltimos tilni tanlang:", reply_markup=language_keyboard)

# Language selection handler
@dp.message_handler(lambda message: message.text in ["🇷🇺 Русский", "🇺🇿 O'zbek"])
async def send_language_message(message: types.Message):
    video = InputFile('photo_2023-06-13_18-34-15.mp4')  # Adjust the path
    if message.text == "🇷🇺 Русский":
        await bot.send_video(message.chat.id, video, caption=welcome_text_ru, parse_mode="Markdown")
        await message.answer("Выберите опцию:", reply_markup=menu_ru)
    elif message.text == "🇺🇿 O'zbek":
        await bot.send_video(message.chat.id, video, caption=welcome_text_uz, parse_mode="Markdown")
        await message.answer("Variantni tanlang:", reply_markup=menu_uz)

# Option handlers for "About Us", "News", "Our Socials", and "Live Assistant"
@dp.message_handler(lambda message: message.text in ["О нас", "Новости", "Наши соцсети", "Biz haqimizda", "Yangiliklar", "Bizning ijtimoiy tarmoqlar", "📞 Live Assistant", "🔙 Главное меню", "🔙 Asosiy menyu"])
async def send_info(message: types.Message):
    if message.text == "О нас":
        photo = InputFile('photo_2024-05-21_15-20-20.jpg')  # Adjust the path
        await bot.send_photo(message.chat.id, photo, caption=about_us_text_ru, parse_mode="Markdown")
    elif message.text == "Новости":
        photo = InputFile('konsalting-2024-09-10_160957.jpg')  # Adjust the path
        await bot.send_photo(message.chat.id, photo, caption=news_text_ru)
    elif message.text == "Наши соцсети":
        await message.answer("Наши социальные сети:", reply_markup=get_social_links("🇷🇺 Русский"))
    elif message.text == "Biz haqimizda":
        photo = InputFile('photo_2024-05-21_15-20-20.jpg')  # Adjust the path
        await bot.send_photo(message.chat.id, photo, caption=about_us_text_uz, parse_mode="Markdown")
    elif message.text == "Yangiliklar":
        photo = InputFile('konsalting-2024-09-10_160957.jpg')  # Adjust the path
        await bot.send_photo(message.chat.id, photo, caption=news_text_uz)
    elif message.text == "Bizning ijtimoiy tarmoqlar":
        await message.answer("Bizning ijtimoiy tarmoqlar:", reply_markup=get_social_links("🇺🇿 O'zbek"))
    elif message.text == "📞 Live Assistant":
        await live_assistant(message)  # Call the live assistant function
    elif message.text in ["🔙 Главное меню", "🔙 Asosiy menyu"]:
        await send_welcome(message)  # Go back to the language selection menu

# Live Assistant Request handler
async def live_assistant(message: types.Message):
    await message.answer("Connecting you to a live assistant. Please wait...")

    # Notify the admin/support group that someone is requesting help
    await bot.send_message(ADMIN_CHAT_ID, f"🆘 Live Assistant requested by {message.from_user.full_name} (@{message.from_user.username}).\nChat ID: {message.chat.id}")

    # Let the user know that their request has been forwarded
    await message.answer("Your request has been sent. You will be contacted shortly by one of our support team.")

# Forward user messages to the admin
@dp.message_handler(lambda message: message.chat.id != ADMIN_CHAT_ID)
async def forward_to_admin(message: types.Message):
    await bot.forward_message(ADMIN_CHAT_ID, message.chat.id, message.message_id)
    await bot.send_message(ADMIN_CHAT_ID, f"Message from {message.from_user.full_name} (@{message.from_user.username}).\nUser ID: {message.chat.id}")

# Forward admin messages back to the user
@dp.message_handler(lambda message: message.chat.id == ADMIN_CHAT_ID, content_types=types.ContentType.ANY)
async def forward_to_user(message: types.Message):
    if message.reply_to_message and message.reply_to_message.forward_from:
        user_id = message.reply_to_message.forward_from.id
        await bot.copy_message(user_id, message.chat.id, message.message_id)
    else:
        await message.reply("Please reply to a forwarded user message to respond to them.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
