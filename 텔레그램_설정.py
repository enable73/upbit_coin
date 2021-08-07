import telegram

token = "1916543022:AAGOduTrGMCluQne4Ax_y3NDJrY0_C3atA4"
bot = telegram.Bot(token)
updates = bot.getUpdates()
for u in updates:
    print(u.message)
