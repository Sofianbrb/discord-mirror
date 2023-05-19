# discord-mirror
Welcome abroad!

This is a simple discord mirror bot to send back every message from a channel to another one using webhook. It works like this: 

1- The selfbot account will listen to messages from a predefined list. When one of them is sent to a channel in the list, 
2- It retrieves the message content (Text, embeds, images...)
3- And send them back to specified webhook(s). Because yes, you can have several webhooks for a single channel.

This program is entirely written in python on the main.py file (Has comments if you want to look at it). Data is on the data.json file.


HOW TO USE THE BOT:

1-
    Install the discord python library for selfbots by using this command: pip install discord.py-self
    
2- Get the user discord token
    This can be done by logging into the discord account on the web, entering the developper tools menu by pressing simultaneously Ctrl+Shift+I, going into the "Network" tab, reload the page by clicking on F5 or Ctrl+R, type /api in the "Network" search field, go into "Library" within the results and copy what's next "authorization" in the "headers" section. This is the token of the discord account, which will serve us in this program to retrieve messages.
    (Source: https://www.androidauthority.com/get-discord-token-3149920/)
    To add the account token/authorized users, just launch the script and it will ask you for these informations. Or go and modify them in the json file if you want to.

3- Configure the program
    This can be done in two ways:

        1- This way is the fastest and the most beginner friendly, as the program will add automatically the data in the correct format in data.json (Pretty much no risk of errors). 
        Launch the program, it'll ask for basic data and after that, you can use the commands below...
            Add a webhook to a channel:
                By sending a message in this format `>addwebhook {channelid} {webhookurl} {webhook response url}`, the bot will automatically add the channel to the database. Here's some explanations about the command:
                    1- "channelid": the ID of the channel you want to send back messages from. Channel ID can be retrieved by doing a right click on the channel, and click on "Copy Channel ID". (Developper Mode needs to be activated in the settings of Discord, Advanced, Developper mode.)
                    2- "webhookurl": the URL of the webhook that will send back the messages from the "channel id" channel. 
                    3- "webhook response url": (OPTIONAL) This is meant to send back a response about your command. It's to be sure that everything went well. (Not using the discord account to avoid getting banned by Discord, even if it's unlikely...). NOTE: it can be any webhook url, not specifically the same as webhookurl.

            Remove a channel:
                By sending a message in this format `>removechannel {channelid} {webhookurl} {webhook response url}`. Same arguments as before, no need to explain them.
                NOTE: this is NOT same as >removewebhook. >removechannel will delete an entire channel of the database, including every webhook in it.

            Remove a webhook off of a channel:
                By sending a message in this format `>removewebhook {channelid} {webhookurl} {webhook reponse url}`.
                    1- "channelid": the ID of the channel you want to remove a webhook of. 
                    2- "webhookurl": the url of the webhook you want to remove of the channelid.
                    3- "webhook response url": (OPTIONAL) the webhook that'll send you back the response.

            List the webhooks linked to a channel:
                By sending a message in this format `>listchannels {channelid} {webhook response url}
                    1- "channelid": the ID of the channel you want to get linked webhooks from.
                    2- "webhook response url": the webhook that'll send back the list. VERY IMPORTANT, without it you won't be able to view the list unless you go into the json file.

            Refresh the channels inside the program (In case it didn't do it before):
                By sending a message in this format `>refresh {webhook response url}
                    (Webhook response url is optional, but it lets you know if it did refresh or not.)

            Add a user to the list of authorized users
                By sending a message in this format `>adduser {userid} {webhook response url}
                    1- "userid": The ID of the user you want to add to the list
                    2- "webhook response url": (OPTIONAL) a webhook you want a response to come from if you want. 
            
            remove a user off of the list of authorized users  
                By sending a message in this format `>removeuser {userid} {webhook response url} (Same arguments as the command above)
                NOTE: anyone with authorizations can add/remove anyone. This is a BASIC program, there is no complex system in there.

        2- Do it manually by modifying the data.json file. 

HOW IS THE DATA.JSON FILE CONSTRUCTED (SEE data_example.json FOR BETTER UNDERSTANDING):

    1- STRING "account": has the token of the account that is listening to the messages.
    2- OBJECT "channels": has the channels that are being followed.
    3- ARRAY "channelid": contains the ID of one channel. The list attached to it contains every webhook that'll send back the messages of this specific channel id. Multiple arrays can be put under the "channels" object.
    3- ARRAY "authorized_users": contains the list of the users ID that are being able to use the commands. 


If you need any more informations about this project, you can contact me on Discord Bird そ#2911 for fast response, or github will do it fine too.

ATTENTION: self bots are a violation of discord TOS and can get you account banned for it. In theory, using your account only for listening (Which is what this account does) wouldn't get you account banned, because Discordc can't know it, I still suggest you create a new account to listen to messages. 

Don't forget the star if you liked this project 💫
