# TrioincApp
This is a discord application made with python using Nextcord. 

To make this work on your local pc you have to make a folder called "Config" inside the config folder you make a Config.Json
Inside that you have to write something like this.. 

{
    "TOKEN": "YOUR_APPLICATION_TOKEN",

    "SQLSERVER_HOST": "localhost",
    "SQLSERVER_USER": "sa",
    "SQLSERVER_PASSWORD": "YOUR_PASSWORD",
    "SQLSERVER_DATABASE": "YOUR_DATABASE_NAME"
}

sa for me is the System Administrator. So you have to give it permissions inside SSMS. 

Rember to have python 3.12.6 installed on your computer also, and change in your IDE to that version or else nextcord isn't working. 