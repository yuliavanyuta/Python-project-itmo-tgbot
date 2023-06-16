from crypto_data import update_crypto_data
import time


# Функция для мониторинга криптовалют
def monitor_crypto(message, crypto_list, crypto_data, bot):
    global screener
    # Если флаг Screener = True, то начинаем мониторинг
    if screener:
        for crypto in crypto_list:
            # Получаем текущий курс криптовалюты из словаря crypto_data
            current_rate = crypto_data[crypto['ticker']]['close'].iloc[-1]
            # Обновляем данные по криптовалюте
            update_crypto_data(crypto['ticker'], crypto_data)
            # Получаем новый курс криптовалюты
            new_rate = crypto_data[crypto['ticker']]['close'].iloc[-1]
            # Если курс изменился, отправляем сообщение
            if new_rate != current_rate:
                change = round(((new_rate - current_rate) / current_rate) * 100, 2)
                if change >= 0:
                    change = "+" + str(change)
                text = f"{crypto['name']}: {new_rate} ({change}% change)"
                bot.send_message(chat_id=message.chat.id, text=text)
    # Если флаг Screener = False, то ничего не делаем
    else:
        pass


# Добавляем таймер для мониторинга каждую минуту
def monitor_schedule(message, crypto_list, crypto_data, bot, screener):
    while True:
        monitor_crypto(message, crypto_list, crypto_data, bot, screener)
        time.sleep(180)
