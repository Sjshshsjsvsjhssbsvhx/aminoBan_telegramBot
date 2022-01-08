from os import path
import script, json
import telebot as tb

token: str = str()

#init telegram bot config file
if path.isfile("conf.json") == True:
    is_true_token: str = str()
    while (is_true_token != "Y") or (is_true_token != "N"):
        is_true_token = str(input('Start bot with current token: "Y"/"N": ')).upper()
        if is_true_token == "Y":
            with open("conf.json", "r", encoding= "utf-8") as File:
                data: dict = json.load(File)
                token = data.get("token")
        elif is_true_token == "N":
            token = input("Telegram bot TOKEN: ")
            with open("conf.json", "w", encoding= "utf-8") as File:
                json.dump(
                            {"token": token},
                            File
                        )
else:
    token = input("Telegram bot TOKEN: ")
    with open("conf.json", "w", encoding= "utf-8") as File:
        json.dump(
                    {"token": token},
                    File
                )

#init bot
amino = script.Amino()

bot = tb.TeleBot(token)

@bot.message_handler(commands= 'start')
def init_bot(message) -> None:
    bot.reply_to(message, "Successfully inited")

@bot.message_handler(commands= 'help')
def help_command(message) -> None:
    bot.reply_to(message, '''
        Забанить участника: ban (link) (причина)\n
        Разбанить участника: unban (link) (причина)\n\n
        Пример:\n
        ban http://aminoapps.com/p/tscygh пидор\n
        unban http://aminoapps.com/p/tscygh уже не пидор\n\n
        Наличие причины не обязательно. Пример:\n
        ban http://aminoapps.com/p/tscygh\n
        unban http://aminoapps.com/p/tscygh
    ''')

#echo
@bot.message_handled(func= lambda message: True)
def echo(message) -> None:
    text: str = message.text
    command: list[str] = text.split()
    if (len(command) == 2) or (len(command) == 3):
        link: str = command[1]
        reason: str = str()
        result: bool = bool()
        if len(command) == 3:
            reason: str = command[2]
        if command[0] == "ban":
            result = amino.ban(link, reason)
        elif command[0] == "unban":
            result = amino.unban(link, reason)
        if result == True:
            bot.reply_to(message, "Успешно")
        elif result == False:
            bot.reply_to(message, "Провал")

bot.infinity_polling()
