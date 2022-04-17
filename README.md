# cutlinks_bot
## бот для создания коротких ссылок и мультиссылок. 
## Презентация проекта http://cutlinks.ru/2223. 
## Сайт проекта http://cutlinks.ru. 
## Бот можно найти по этой ссылке https://t.me/cutlinksbot. 
  
## Правила работы:
Для дебага:
Необходимо поменять TOKEN = '<ваш токен для дебага>' 
Раскомментить следующую строку
'''
#updater.start_polling()
'''

И закомментить следущую строку
'''
updater.start_webhook(listen="0.0.0.0",
                      port=int(PORT),
                      url_path=TOKEN,
                      webhook_url='https://sleepy-island-02101.herokuapp.com/' + TOKEN)
'''

Деплоится проект на heroku (спрашивать artemsteshenko)
