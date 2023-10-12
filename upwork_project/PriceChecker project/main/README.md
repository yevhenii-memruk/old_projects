# Design for use 
- Hello, to make all set to go just do some conditions!


__Firstly__, we have **telegram_user_data.py** file with info about BOT, we should gain this data, let's get it! Need:
  - TOKEN
  - chat_id 

__Secondly__, we should figure out our version of Google and download **webriver** to use Selenium! Need:
  - version of Google
  - webdriver


## 1. Telegram Alarm:

--> open [Botfather](https://t.me/botfather) (BotFather - use it to create new bot accounts and manage your existing bots) ;

--> head over to BotFather in Telegram and CREATE YOUR BOT ;

--> after creation you get bot TOKEN (save it) ;

--> open telegram_user_data.py file into main repository via Notepad and paste YOUR TOKEN in ( TOKEN = "here" ) ;


> GREAT, half the way is over!


--> paste the following link in your browser - _https://api.telegram.org/bot<API-access-token>/getUpdates?offset=0_ ;

--> delete <API-access-token> from link and paste your bot TOKEN and press ENTER ;

--> press CNTRL+F on this page and write "chat" , then you find your bot_chatID and COPY it(only digits) ;

--> open telegram_user_data.py again and paste YOUR bot_chatID in ( chat_id = 'here' ) ;


## 2. Selenium Web driver 

--> open Google and paste this into search line - _chrome://version_ ;

--> First line - (Google Chrome:	_your version_) ;

--> when you got to know your version of Google, go to next site and find your version: [chromedriver](https://chromedriver.storage.googleapis.com/index.html) ; 

--> choose version for your type of system and download file ; 

--> extract file into main directory of project ;

> THAT IT, CONGRATULATIONS!
