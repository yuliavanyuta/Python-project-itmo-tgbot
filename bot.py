import telebot
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib
import io
from monitor import monitor_schedule
from crypto_data import update_crypto_data
from create_buttons import create_crypto_buttons
from create_buttons import create_mode_buttons

matplotlib.use('agg')

# Токен бота
API_TOKEN = ''
bot = telebot.TeleBot(API_TOKEN)

# Флаг скринера
screener = False

# Список криптовалют, которые будут отображаться в боте
crypto_list = [
    {'name': 'Bitcoin', 'ticker': 'BTCUSDT'},
    {'name': 'Ethereum', 'ticker': 'ETHUSDT'},
    {'name': 'Binance Coin', 'ticker': 'BNBUSDT'},
    {'name': 'Cardano', 'ticker': 'ADAUSDT'},
    {'name': 'Dogecoin', 'ticker': 'DOGEUSDT'},
    {'name': 'Polkadot', 'ticker': 'DOTUSDT'},
    {'name': 'Chainlink', 'ticker': 'LINKUSDT'},
    {'name': 'Litecoin', 'ticker': 'LTCUSDT'},
    {'name': 'Ripple', 'ticker': 'XRPUSDT'},
]

# Словарь данных о криптовалюте, которые будут отображаться в боте
crypto_data = {}


# Приветствие бота
@bot.message_handler(commands=['start'])
def send_hello(message):
    response = "Hello, I am the bot which can output cryptocurrency rates and track market changes." \
               "\nAll information is taken from Binance website."
    bot.send_message(message.chat.id, response, reply_markup=create_mode_buttons())


# Добавляем обработчик для отлова всех сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global screener

    # Режим для вывода курса криптовалют
    if message.text == "CurrencyTracker":
        screener = False
        bot.send_message(message.chat.id, "Mode: CurrencyTracker", reply_markup=create_crypto_buttons(crypto_list))
    # Режим для сканирования рынка
    elif message.text == "Screener":
        screener = True
        monitor_schedule(message, crypto_list, crypto_data, bot, screener)
        bot.send_message(message.chat.id, "Mode: Screener")
    # Выбор режима бота
    elif message.text == "Choose Mode":
        screener = False
        bot.send_message(message.chat.id, "Let's switch mode!", reply_markup=create_mode_buttons())
    # Выводим курс крипты
    else:
        for crypto in crypto_list:
            if message.text == crypto['name']:
                update_crypto_data(crypto['ticker'], crypto_data)
                current_crypto_data = crypto_data[crypto['ticker']]
                # Получаем данные за последние 6 дней
                last_6_days_data = current_crypto_data[
                    current_crypto_data['open_time'] > datetime.now() - timedelta(days=7)]
                # Рисуем график изменения курса
                plt.plot(last_6_days_data['open_time'], last_6_days_data['open'])
                plt.title(f'{crypto["name"]} rate for the last 6 days')
                plt.xlabel(r'Date')
                plt.ylabel(r'Rate, USD')
                plt.grid(True)
                # Сохраняем график в буфер обмена
                buffer = io.BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                # Отправляем изображение и текущий курс
                bot.send_photo(message.chat.id, photo=buffer.getvalue())
                dollar = '💵'
                bot.send_message(message.chat.id,
                                 f'{crypto["name"]} - {current_crypto_data.iloc[-1]["close"]:.2f} USD ' + dollar * 3)
                # Очищаем график для следующего вывода
                plt.clf()
                # Выходим из цикла после отправки сообщения
                break


if __name__ == "__main__":
    # Загружаем информацию о криптовалюте
    for crypto in crypto_list:
        update_crypto_data(crypto['ticker'], crypto_data)

    # Запускаем бота
    bot.polling()
