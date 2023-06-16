import telebot


# Функция для создания кнопок с именованием криптовалют
def create_crypto_buttons(crypto_list):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=3)
    buttons = []
    for crypto in crypto_list:
        buttons.append(telebot.types.KeyboardButton(crypto['name']))
    buttons.append(telebot.types.KeyboardButton('Choose Mode'))
    markup.add(*buttons)
    return markup

# Функция для создания кнопок выбора режима
def create_mode_buttons():
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    buttons = [telebot.types.KeyboardButton("CurrencyTracker"), telebot.types.KeyboardButton("Screener")]
    markup.add(*buttons)
    return markup