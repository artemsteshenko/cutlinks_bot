# cutlinks_bot
#### бот для создания коротких ссылок и мультиссылок. 
#### Презентация проекта http://cutlinks.ru/2223. 
#### Презентация проекта https://www.canva.com/design/DAE9a_nyIls/u7W2p-zH8Ev9nUqQS7VMhg/edit?utm_content=DAE9a_nyIls&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton
#### Сайт проекта http://cutlinks.ru. 
#### Бот можно найти по этой ссылке https://t.me/cutlinksbot. 
#### Доска Trello https://trello.com/b/45RgYOjc/cutlinks. 
  
#### Правила работы:
Для дебага:
Необходимо поменять TOKEN = '<ваш токен для дебага>' 
Раскомментить следующую строку
```
#updater.start_polling()
```

И закомментить следущую строку
```
updater.start_webhook(listen="0.0.0.0",
                      port=int(PORT),
                      url_path=TOKEN,
                      webhook_url='https://sleepy-island-02101.herokuapp.com/' + TOKEN)
```

Деплоится проект на heroku (спрашивать artemsteshenko)
