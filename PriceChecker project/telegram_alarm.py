import telebot
from data_base import DataServer

with DataServer() as db:
    query = f"SELECT * FROM telegram_data"
    mycursor = db.cursor()
    mycursor.execute(query)
    for i in mycursor:
        token, chat_id = i[0], i[1]

bot = telebot.TeleBot(token)
chat_id = chat_id


def alert_message(name, price, percent, link):
    if float(percent) < float(0):
        percent_message = f"Price dropped by {format(percent, '.2f')}% !"
    if float(percent) > float(0):
        percent_message = f"Price increased by {format(percent, '.2f')}% !"
    if float(percent) == float(0):
        percent_message = f"\nNothing changed: {format(percent, '.2f')}% !"

    bot.send_message(str(chat_id),
                     str(name) + ": " + str(f"{price:,}") + "\n" + str(percent_message) + "\nLink: " + str(link))


if __name__ == '__main__':
    pass
