import telebot#импорт библиотека для телеграм бота
from datetime import datetime, timedelta#импорт для работы с датой и временем

TOKEN = "8611918803:AAGnldhtcZJyN5qeKg6wcZiWfQm0f_dfyD4"#токен бота

bot = telebot.TeleBot(TOKEN)#создание экземпляра токена

zapis = {}#словарь
temp_data = {}#словарь

def get_time_slots():
    slots = []#список временных слотов
    tomorrow = datetime.now() + timedelta(days=1)#завтрашняя дата
    for hour in range(9, 18):#цикл по времени
        time_str = tomorrow.strftime(f"%d.%m.%y {hour}:00")#формат даты
        slots.append(time_str)#добавление слота в список
    return slots
#обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):#
    bot.send_message(message.chat.id, "Привет! Я бот для записи\n\nКоманды:\n/book - записаться\n/myrecord - моя запись\n/cancel - отмена \n/all - показать")
#обработчик команды /book
@bot.message_handler(commands=['book'])
def book(message):
    chat_id = message.chat.id#id chat
    msg = bot.send_message(chat_id, "Введите ваше имя")#запрос имени
    bot.register_next_step_handler(msg, get_name)#следующий шаг - get_name

def get_name(message):
    chat_id = message.chat.id
    name = message.text#полученное имя
    temp_data[chat_id] = {'name': name}#сохраняем имя временно
    slots = get_time_slots()#полученное имя
    free_slots = []#список свободных слотов
    
    for slot in slots:
        if slot not in zapis:#если слот не занят
            free_slots.append(slot)#добавляем в свободные
    
    if not free_slots:#если нет свободных
        bot.send_message(chat_id, "Извините, на завтра нет свободного времени")
        return
    #создаем клавиатуру с кнопками по времени
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = []
    for slot in free_slots[:8]:#берем первые 8 слотов
        buttons.append(telebot.types.KeyboardButton(slot))#создаем кнопку
    markup.add(*buttons)#добавляем кнопки в клавиатуру
    #отправляем сообщение с выбором
    msg = bot.send_message(chat_id, f"Приятно познакомиться, {name}!\nВыберите свободное время", reply_markup=markup)
    bot.register_next_step_handler(msg, get_time)#след. шаг get_time

def get_time(message):
    chat_id = message.chat.id
    selected_time = message.text#выбранное время
    
    if selected_time in zapis:# Если время уже занято
        bot.send_message(chat_id, "Это время уже занято! Начните заново /book", reply_markup=telebot.types.ReplyKeyboardRemove())
        return
    
    name = temp_data[chat_id]['name']# Получаем имя из временных данных
    zapis[selected_time] = name# Сохраняем запись (время -> имя)    
    
    bot.send_message(chat_id,
                     f"Имя: {name}\n"
                     f"Время: {selected_time}\n\n"
                     f"Ждем Вас!", 
                     reply_markup=telebot.types.ReplyKeyboardRemove())
    del temp_data[chat_id]# Удаляем временные данные
# Обработчик команды /myrecord (проверка своей записи)
@bot.message_handler(commands=['myrecord'])
def my_record(message):
    chat_id = message.chat.id
    user_name = message.from_user.first_name# Имя пользователя Telegram
    found = False # Флаг, найдена ли запись
    
    for time, name in zapis.items():# Поиск по всем записям
        if name == user_name: # Если имя совпадает
            bot.send_message(chat_id, f"Ваша запись: {time}")
            found = True
            break
    
    if not found:# Если запись не найдена
        bot.send_message(chat_id, "У вас нет активных записей")
# Обработчик команды /cancel (отмена записи)
@bot.message_handler(commands=['cancel'])
def cancel(message):
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    to_delete = None # Время для удаления
    
    for time, name in zapis.items(): # Поиск записи пользователя
        if name == user_name:
            to_delete = time
            break
    
    if to_delete:
        del zapis[to_delete]
        bot.send_message(chat_id, " Ваша запись отменена")
    else:
        bot.send_message(chat_id, "У вас нет активных записей")
# Обработчик команды /all (для администратора)
@bot.message_handler(commands=['all'])
def all(message):
    if message.from_user.id == 1831591310:# Проверка ID администратора (нужно заменить на свой ID)
        if zapis:
            text = "📋 Все записи:\n\n"
            for time, name in sorted(zapis.items()):  # Сортируем по времени
                text += f"👤 {name} - {time}\n"
            bot.send_message(message.chat.id, text)
        else:
            bot.send_message(message.chat.id, "Записей нет")
    else:
        bot.send_message(message.chat.id, "У вас нет доступа")  # Для обычных пользователей

print("Бот запущен...")# Сообщение о запуске
bot.polling(none_stop=True)# Запуск бота в режиме постоянного опроса