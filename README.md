# Clemont and it's Requirements
- Clemont is a powerful and fast bot built to work directly with Clembot.
- Clemont offers users with private raid notifications and allows them to set a max distance
- A fully functioning version of Clembot must be running on the server.
- Python 3.5+ is required, the bot **will not** work on Python 2.
- MySQL must be installed before continuing. I used MariaDB. https://downloads.mariadb.org/

# Building a Database
- Programmed to be used with MySQL only.
-     CREATE DATABASE clemont CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-     CREATE TABLE notifications (
        `user_id` VARCHAR(60) NOT NULL DEFAULT '0',
        `poke_id` INT NOT NULL DEFAULT '0',
        `lat` VARCHAR(45) NOT NULL DEFAULT '0',
        `lon` VARCHAR(45) NOT NULL DEFAULT '0',
        `distance` INT NOT NULL DEFAULT '0'
        );
- Database is now created and ready.

# Creating your config.py file
- Open config.py in a text editor like Notepad++
- cleambot_search_term should be left untouched. 
- clembot_id is found by right-clicking Clembot and clicking 'Copy id'
- Fill out the database information so the bot can connect to the database we created.
- Your config.py file is now ready. 

# Running Clemont!
- To run Clemont, simply run the line below and you're ready to go. 
-     python3 clemont.py
- Run //commands to see a list of commands once the bot is live.
