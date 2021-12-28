#Telegram Spammer
___
A script for sending spam with a lot of telegrams accounts with proxies with telethon sessions
___
###How use:
___

git clone "https://github.com/BulatXam/TelegramSpam"

pip install -r requirements.txt

___

Fill in the csv file proxies.csv in base dir:

proxy_type:
<ul> 
  <li>1-socks4</li> 
  <li>2-socks5</li> 
  <li>3-http/https</li> 
</ul>

___

Add telethon sessions in directory "sessions"

___
By writing `python manage.py <command_name> --help`  ou will get a brief documentation of the command
___

Write command in command line:

`python manage.py add_clients`

You have added clients to the database and now you can work with them

___

We will write this command to write additional information about our customers to the database

`python manage.py edit_clients`

___

To pair the participants of the desired chat, enter:

`python manage.py parse_chat <chat_username> <50>`

50 - how many users 1 added client will write to in private messages

___

To start spam:

`python manage.py spam_send <text>`

___

This script will be further refined and improved
