import telebot, threading
from telebot import types
from keep_alive import keep_alive

# Настройки
TOKEN = '8487416892:AAG51pbX5wAhC3XdcUTm4q90Q_0hJDF0XmM'
ADMIN = 5012078381
LINK = "@Sell_Skill"

bot = telebot.TeleBot(TOKEN)
states, media = {}, {}

def report(uid, name):
    if uid not in media: return
    d = media[uid]
    bot.send_message(ADMIN, f"🔔 Заявка: {name} (ID: {uid})")
    alb = [types.InputMediaPhoto(x, caption=(d['txt'] if i==0 else None)) for i, x in enumerate(d['pics'])]
    if alb: bot.send_media_group(ADMIN, alb)
    elif d['txt']: bot.send_message(ADMIN, d['txt'])
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("✅ Да", callback_data=f"y_{uid}"),
           types.InlineKeyboardButton("❌ Нет", callback_data=f"n_{uid}"))
    bot.send_message(ADMIN, "Решение:", reply_markup=kb)
    del media[uid]
    states[uid] = False

@bot.message_handler(commands=['start'])
def start(m):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Да", callback_data="go"), types.InlineKeyboardButton("Нет", callback_data="no"))
    bot.send_message(m.chat.id, "Вступить в METOR?", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data in ["go", "no"])
def join(c):
    if c.data == "no": bot.edit_message_text("Пока!", c.message.chat.id, c.message.message_id)
    else:
        bot.edit_message_text("Пришли скрины: кс/т, свап основы, ник и топливо. Ожидай.", c.message.chat.id, c.message.message_id)
        states[c.from_user.id] = True

@bot.message_handler(func=lambda m: states.get(m.from_user.id), content_types=['photo', 'text'])
def load(m):
    uid = m.from_user.id
    if uid not in media:
        media[uid] = {'pics': [], 'txt': None, 'tmr': None}
        bot.send_message(m.chat.id, "✅ Данные приняты! Ожидай.")
    if m.text: media[uid]['txt'] = m.text
    if m.caption: media[uid]['txt'] = m.caption
    if m.content_type == 'photo': media[uid]['pics'].append(m.photo[-1].file_id)
    if media[uid]['tmr']: media[uid]['tmr'].cancel()
    t = threading.Timer(12.0, report, args=[uid, m.from_user.first_name])
    media[uid]['tmr'] = t
    t.start()

@bot.callback_query_handler(func=lambda c: "_" in c.data)
def ans(c):
    op, uid = c.data.split("_")
    res = f"✅ Одобрено! Лидер: {LINK}" if op == "y" else "❌ Отклонено."
    try:
        bot.send_message(int(uid), res)
        bot.edit_message_text(f"Готово для {uid}", c.message.chat.id, c.message.message_id)
    except: pass

if name == "main":
    keep_alive()
    print("БОТ ЗАПУЩЕН")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
