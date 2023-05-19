import discord
import json
import asyncio
import time
import requests

# Global variable for the list of the channels we will be listening to.
channels_to_listen_to = [] 

# Get the list of the users that are allowed to add/remove channels by commands
def get_authorized_users():
	with open('data.json', 'r') as f:
		data = json.load(f)
	return data['authorized_users']

# Add a user ID to the list of authorized users
def add_authorized_user(user_id):
	try:
		user_id = int(user_id)
		with open('data.json', 'r') as f:
			data = json.load(f)
		if user_id not in data['authorized_users']:
			data['authorized_users'].append(user_id)
			with open('data.json', 'w') as f:
				json.dump(data, f)
			print("User ID added to database.")
			authorized_users = get_authorized_users() # Update the authorized_users variable
		else:
			print("User ID already in database.")
	except Exception as e:
		senderror = input("Sorry, there was an error when adding the user ID to the database. Do you want to print the error? (y/n) ")
		if senderror.lower() == 'y':
			print(e)
		else:
			pass

# Get the token of the account that'll be used to listen to messages.
def get_account_token():
	with open('data.json', 'r') as f:
		data = json.load(f)
	return data['account_token']

# Add the account token to the database
def add_account_token(token):
	try:
		with open('data.json', 'r') as f:
			data = json.load(f)
		data['account_token'] = token
		with open('data.json', 'w') as f:
			json.dump(data, f)
		print("\n✅ Account token is valid and has been added to database.\n")
		time.sleep(2) #I'm adding a 2 seconds wait time because I don't want the user to miss the message, as there'll be an error showing up (Meningfull error, but still an error.)
	except Exception as e:
		senderror = input("Sorry, there was an error when adding the account token to the database. Do you want to print the error? (y/n) ")
		if senderror.lower() == 'y':
			print(e)
		else:
			pass

# Function to check if the token is valid. Will just connect and disconnect. If everything goes well, it returns true. Else, false.
async def check_token_validity(token):
	try:
		bot = discord.Client()
		await bot.login(token)
		await bot.close()
		return True
	except discord.LoginFailure:
		return False
	except :
		return False

# Function to refresh the list of channels we're listening to.
def refresh_channels_list():
	global channels_to_listen_to
	with open("data.json", "r") as jsonfile:
		data = json.load(jsonfile)
	channels = data['channels']
	channels_to_listen_to = []
	for channel in channels:
		channels_to_listen_to.append(channel)

# Function to add a webhook to a channel in the database.
def add_webhook_to_channel(channel_id, webhook_url):
	with open('data.json', 'r') as f:
		data = json.load(f)

	# Firstly we check if the channel is already in the database. If it is, we'll just return a message saying that it's already in the database.
	# The JSON is built like this: channels: {"channel_id": [webhook(s) here]}
	# So we need to extract every channel_id and put them in a list.
	channel_ids = []
	for channelid in data['channels']:
		channel_ids.append(channelid)
	
	# Now we can check if the channel is in this list. If it is, that means that the channel is already in the database, so we don't need to add it but we will just append the webhook.
	# And if it's not, we'll add it to the database and then add the webhook.
	if channel_id in channel_ids:
		
		# The channel is already in the database. But hey, maybe the webhook is already in it? So we'll check that.
		# We'll extract the list of webhooks (No need to take them one by one, they're already a list.)
		webhooks = data['channels'][channel_id]
		if webhook_url in webhooks:
			# The webhook is already in the database. So we'll just return a message saying that it's already in the database.
			return "This webhook is already attached to this channel."
		else:
			# The webhook is not in the database. So we'll add it.
			data['channels'][channel_id].append(webhook_url)
			with open('data.json', 'w') as f:
				json.dump(data, f)
				refresh_channels_list()
			return "Webhook added to database."
		
	elif channel_id not in channel_ids:

		# We will need to add the channel to the database. And because it's a brand new channel, we don't need to check if the webhook is already in it. We'll just add it.
		data['channels'][channel_id] = [webhook_url]
		with open('data.json', 'w') as f:
			json.dump(data, f)
		refresh_channels_list()
		return "Channel and webhook added to database."

	else:
		# There was an error. We'll just return a message saying that there was an error.
		return "Sorry, there was an error."

# Function to remove a channel off of the database
def remove_webhook_from_channel(channel_id, webhook_url):
	with open('data.json', 'r') as f:
		data = json.load(f)
	
	# Firstly we check if the channel is in the database. If it is, we'll remove it. If not, we'll just return a message saying that it's not in the database.
	# The JSON is built like this: channels: {"channel_id": [webhook(s) here]}
	# So we need to extract every channel_id and put them in a list.
	channel_ids = []
	for channel_id in data['channels']:
		channel_ids.append(channel_id)
	
	# Now we can check if the channel is in this list. If it is, that means that the channel is in the database, so we can remove it. If not, we'll just return a message saying that it's not in the database.

	if channel_id in channel_ids:
		# The channel is in the database. So we'll check if the webhook is in it.
		# We'll extract the list of webhooks (No need to take them one by one, they're already a list.)
		webhooks = data['channels'][channel_id]
		if webhook_url in webhooks:
			# The webhook is in the database. So we'll remove it.
			data['channels'][channel_id].remove(webhook_url)
			with open('data.json', 'w') as f:
				json.dump(data, f)
			refresh_channels_list()
			return "Webhook removed from database."
		else:
			# The webhook is not in the database. So we'll return a message saying that it's not in the database.
			return "This webhook is not attached to this channel."

	elif channel_id not in channel_ids:
		# The channel is not in the database. So we'll return a message saying that it's not in the database.
		return "This channel is not in the database."

	else:
		# There was an error. We'll just return a message saying that there was an error.
		return "Sorry, there was an error."

# Function to remove an entire channel off of the database
def remove_channel_from_database(channel_id):
	with open('data.json', 'r') as f:
		data = json.load(f)
	
	# Firstly we check if the channel is in the database. If it is, we'll remove it. If not, we'll just return a message saying that it's not in the database.
	# The JSON is built like this: channels: {"channel_id": [webhook(s) here]}
	# So we need to extract every channel_id and put them in a list.
	channel_ids = []
	for channel_id in data['channels']:
		channel_ids.append(channel_id)

	# Now we can check
	if channel_id in channel_ids:
		# The channel is in the database. So we'll remove it.
		del data['channels'][channel_id]
		with open('data.json', 'w') as f:
			json.dump(data, f)
		refresh_channels_list()
		return "Channel removed from database."
	elif channel_id not in channel_ids:
		# The channel is not in the database. So we'll return a message saying that it's not in the database.
		return "This channel is not in the database."
	else:
		# There was an error. We'll just return a message saying that there was an error.
		return "Sorry, there was an error."

# Function to get the list of webhooks following a channel.
def get_webhooks_list(channel_id):
	with open("data.json", "r") as f:
		data = json.load(f)
	
	return data['channels'][str(channel_id)]

# Ask for and verify that the token is valid in case it was not in the json. If it is in it, it should be valid then.
account_token = get_account_token()
if account_token == None:
	print("No account token found.")
	while True:
		account_token = input("Please enter the account token: ")
		account_token_valid = asyncio.run(check_token_validity(account_token))
		if account_token_valid:
			add_account_token(account_token)
			break
		elif not account_token_valid:
			print("Invalid token. Please try again.")
		else:
			print("An error occurred. Exiting...")
			exit()

authorized_users = get_authorized_users()

# If there are no authorized users, ask the user to add one if they wish to. Else, continue.
if authorized_users == []:
	print("No authorized users found.")
	while True:
		user_id = input("Please add a user ID, or else type in 'None' to continue: ")
		if user_id.lower() == 'none':
			print("No authorized users added. Continuing...")
			break
		elif user_id.lower() != 'none' and user_id.isdigit():
			add_authorized_user((user_id))
			break
		elif user_id.lower() != 'none' and not user_id.isdigit():
			print("Invalid user ID. Please try again.")

client = discord.Client()
@client.event
async def on_ready():
	global channels_to_listen_to
	refresh_channels_list()
	# Print a message to say that the bot is connected and running.
	print(f"""
🌟 Connected! 🌟
⭐ Account token: {account_token}
⭐ Account name: {client.user.name}
⭐ Account discriminator: {client.user.discriminator}
⭐ Account ID: {client.user.id}
💫 Bot is now running...""")

@client.event
async def on_message(message):
	if message.author.id == client.user.id:	# If the message is from the bot, we will ignore it
		return
	
	global channels_to_listen_to	# Import the list of channels we're listening to.
	if message.content.startswith(">addwebhook"):
		#So the message here is to check if to add a channel to the list of channels we listen to. It's built like this: >addchannel {channelid} {webhookurl} {webhook response url}. More details in the readme file.

		# First thing to do is to check if the user is authorized to add channels. If not, we'll check if there's a response webhook to inform them. If not, we will just ignore this command.
		if message.author.id not in authorized_users:
			#Get the webhook response url if there is one and send back that the user is not authorized to add channels.
			if message.content.split(" ")[3]:
				webhookresponseurl = message.content.split(" ")[3]
				data = {
					"content": f"<@{message.author.id}> Sorry, you are not authorized to add channels."
				}
				headers = {
					"Content-Type": "application/json"
				}
				response=requests.post(webhookresponseurl, json=data, headers=headers)
			return

		# Get the channel ID, webhook URL and webhook response URL from the message
		# I am going to split them in a list, according to spaces.
		words = message.content.split(" ")
		channelid = words[1]
		webhookurl = words[2]
		webhookresponseurl = None
		try:
			webhookresponseurl = words[3]
		except:
			pass

		# Now that we have the informations, we can proceed to add the channel to the database. But first thing is ti check if webhookurl is a valid webhook.
		# This can be done by checking if the webhook has a guild_id for example. If it does, it's a valid webhook. Else, it's not (Webhooks can't exist without a guild. At least, not at the moment.)
		webhookurl_data = requests.get(webhookurl).json()
		# We got the data of the webhook in a json format. Now we can check if it has a guild_id. If yes, we proceed to add it to the database. Else, we'll send a message to the webhook response url if there is one, or just ignore it.
		
		# Check if the webhook has a guild_id
		# By default, we will set it to None (No guild_id). But if we can find a guild_id, we'll set it to that.
		webhookurl_guild_id = None
		try:
			webhookurl_guild_id = webhookurl_data['guild_id']
		except:
			pass
		
		# Now that we have our guild_id, we can do the rest.
		# First thing is to check if the guild_id is None. If it is, we'll send a message to the webhook response url if there is one, or just ignore it. If not, we'll proceed to add the channel to the database.
		if webhookurl_guild_id == None:
			# Send a message to the webhook response url if there is one, or just ignore it.
			if webhookresponseurl:
				data = {
					"content": f"<@{message.author.id}> Invalid webhook URL. Please try again."
				}
				headers = {
					"Content-Type": "application/json"
				}
				response=requests.post(webhookresponseurl, json=data, headers=headers)

		elif webhookurl_guild_id != None:

			# We can finally add the webhook to the database.
			# We will use the function "add_channel_to_database" to do so. Get a look into it to see how it works.
			add_channel_to_database_response = add_webhook_to_channel(channelid, webhookurl)
			# And of course, if there's a response webhook, we'll send a message to it.
			if webhookresponseurl:
				data = {
					"content": f"<@{message.author.id}> {add_channel_to_database_response}"
				}
				headers = {
					"Content-Type": "application/json"
				}
				response=requests.post(webhookresponseurl, json=data, headers=headers)
	
	if message.content.startswith(">removewebhook"):
		# Command to remove a webhook off of a channel. Built as follows: >removechannel {channelid} {webhookurl} {webhook response url}. More details in the readme file.
		
		# First thing to do is to check if the user is authorized to remove channels. If not, we'll check if there's a response webhook to inform them. If not, we will just ignore this command.
		if message.author.id not in authorized_users:
			#Get the webhook response url if there is one and send back that the user is not authorized to add channels.
			if message.content.split(" ")[3]:
				webhookresponseurl = message.content.split(" ")[3]
				data = {
					"content": f"<@{message.author.id}> Sorry, you are not authorized to remove webhooks."
				}
				headers = {
					"Content-Type": "application/json"
				}
				response=requests.post(webhookresponseurl, json=data, headers=headers)
			return

		# Get the channel ID, webhook URL and webhook response URL from the message
		# I am going to split them in a list, according to spaces.
		words = message.content.split(" ")
		channelid = words[1]
		webhookurl = words[2]
		webhookurl_guild_id = None
		if message.content.split(" ")[3]:
			webhookresponseurl = message.content.split(" ")[3]
		else:
			webhookresponseurl = None
		
		# Now that we have the informations, we can proceed to remove the channel from the database. But first thing is ti check if webhookurl is a valid webhook.
		webhookurl_data = requests.get(webhookurl).json()

		# Check if the webhook has a guild_id
		# By default, we will set it to None (No guild_id). But if we can find a guild_id, we'll set it to that.
		webhookurl_guild_id = None
		try:
			webhookurl_guild_id = webhookurl_data['guild_id']
		except:
			pass
		
		# If the guild_id is None, we'll send a message to the webhook response url if there is one, or just ignore it. If not, we'll proceed to remove the channel from the database.
		if webhookurl_guild_id == None:
			# Send a message to the webhook response url if there is one, or just ignore it.
			if webhookresponseurl:
				data = {
					"content": f"<@{message.author.id}> Invalid webhook URL. Please try again."
				}
				headers = {
					"Content-Type": "application/json"
				}
				response=requests.post(webhookresponseurl, json=data, headers=headers)
		
		elif webhookurl_guild_id != None:
			
			# We can finally remove the webhook from the database.
			# We will use the function "remove_channel_from_database" to do so. Get a look into it to see how it works.
			remove_channel_from_database_response = remove_webhook_from_channel(channelid, webhookurl)
			# And of course, if there's a response webhook, we'll send a message to it.
			if webhookresponseurl:
				data = {
					"content": f"<@{message.author.id}> {remove_channel_from_database_response}"
				}
				headers = {
					"Content-Type": "application/json"
				}
				response=requests.post(webhookresponseurl, json=data, headers=headers)
	
	if message.content.startswith(">removechannel"):
		# This command deletes a channel and every webhook linked to it. But it doesn't delete the webhooks from other channels....
		# Built as follows: >removechannel {channelid} {webhook response url}. More details in the readme file.
		
		# First thing to do is to check if the user is authorized to remove channels.
		if message.author.id not in authorized_users:
			#Get the webhook response url if there is one and send back that the user is not authorized to add channels.
			if message.content.split(" ")[2]:
				webhookresponseurl = message.content.split(" ")[2]
				data = {
					"content": f"<@{message.author.id}> Sorry, you are not authorized to remove channels."
				}
				headers = {
					"Content-Type": "application/json"
				}
				response=requests.post(webhookresponseurl, json=data, headers=headers)
			return
	
		# Get the channel ID and webhook response URL from the message
		words = message.content.split(" ")
		channelid = words[1]
		webhookresponseurl = None
		try:
			webhookresponseurl = words[2]
		except:
			pass
		
		# Now that we have the informations, we can proceed to remove the channel from the database.
		# We will use the function "remove_channel_from_database" to do so. Get a look into it to see how it works.
		remove_channel_from_database_response = remove_channel_from_database(channelid)
		# And of course, if there's a response webhook, we'll send a message to it.
		if webhookresponseurl:
			data = {
				"content": f"<@{message.author.id}> {remove_channel_from_database_response}"
			}
			headers = {
				"Content-Type": "application/json"
			}
			response=requests.post(webhookresponseurl, json=data, headers=headers)

	if message.content.startswith(">listchannels"):
		# First thing here is getting the webhook url for the response.
		webhookresponseurl = None
		try:
			webhookresponseurl = message.content.split(" ")[1]
		except:
			return

		# Now we can check if they're authorized to list the channels.
		if message.author.id not in authorized_users:
			data = {
				"content": f"<@{message.author.id}> Sorry, you are not authorized to list the channels."
			}
			headers = {
				"Content-Type": "application/json"
			}
			response=requests.post(webhookresponseurl, json=data, headers=headers)
			return
		
		# Now we can get the list of channels.
		with open("data.json", "r") as f:
			channels = json.load(f)
		channels = channels['channels']
		data = {
			"content": f"<@{message.author.id}> Here is the list of channels I'm listening to:\n ```{channels}```"
		}
		headers = {
			"Content-Type": "application/json"
		}
		response=requests.post(webhookresponseurl, json=data, headers=headers)
	
	if message.content.startswith(">refresh"):
		# First thing here is getting the webhook url for the response.
		webhookresponseurl = None
		try:
			webhookresponseurl = message.content.split(" ")[1]
		except:
			return

		# Now we can check if they're authorized to refresh the channels.
		if message.author.id not in authorized_users:
			if webhookresponseurl:
				data = {
					"content": f"<@{message.author.id}> Sorry, you are not authorized to refresh the channels."
				}
				headers = {
					"Content-Type": "application/json"
				}
				response=requests.post(webhookresponseurl, json=data, headers=headers)
			return
		
		# Now we can get the list of channels.
		with open("data.json", "r") as f:
			channels = json.load(f)
		channels = channels['channels']
		channels_to_listen_to = []
		for channel in channels:
			channels_to_listen_to.append(channel)
		if webhookresponseurl:
			data = {
				"content": f"<@{message.author.id}> Channels refreshed."
			}
			headers = {
				"Content-Type": "application/json"
			}
			response=requests.post(webhookresponseurl, json=data, headers=headers)
	

	# Finally, we can manage the mirroring part. 

	# First step would be to check if the message is from a channel that we're listening to. If not, we'll just ignore it.
	# The channels will be a list of channel IDs we designated when the bot was starting. Whenever we make a change to the channels, it'd automatically update the list.
	# But in case it doesn't, we can use the command >refresh to refresh the list of channels we're listening to.

	if str(message.channel.id) not in channels_to_listen_to:
		return
	
	# Get every webhook that follows this channel by invoking the get_webhook_list function.
	webhooks_list = get_webhooks_list(message.channel.id)
	
	# We will check one by one for raw text (message content), embeds, images/attachments and commands.

	if message.content:
		# We'll send the message content to every webhook.
		for webhook in webhooks_list:
			data = {
				"content": message.content,
				"username": message.author.name,
				"avatar_url": "https://cdn.discordapp.com/attachments/1096418851887009842/1108838934441639976/discord-6832787_960_720.png"
			}
			headers = {
				"Content-Type": "application/json"
			}
			response=requests.post(webhook, json=data, headers=headers)
	
	# We will check if the message has any embeds, and add them to the data dictionary if it does
	if len(message.embeds) > 0:
		dict_embeds = []
		for embed in message.embeds:
			dict_embeds.append(embed.to_dict())
		for webhook in webhooks_list:
			data = {
				"embeds": dict_embeds,
				"username": message.author.name,
				"avatar_url":  "https://cdn.discordapp.com/attachments/1096418851887009842/1108838934441639976/discord-6832787_960_720.png"
			}
			headers = {
				"Content-Type": "application/json"
			}
			response=requests.post(webhook, json=data, headers=headers)

	# We will check if the message has any attachment (Images, videos....)
	if message.attachments:
		for attachment in message.attachments:
			response = requests.get(attachment.url)
			if response.status_code == 200:
				file_data = response.content
				attachment_name = attachment.filename
				payload = {
					'file': (attachment_name, file_data)
				}
				for webhook in webhooks_list:
					requests.post(webhook, files=payload)

	# We will check if the message is a command. If it is, we'll just send relative information to the webhooks.
	if message.interaction:
		data = {
			"username": message.author.name,
			"avatar_url":  "https://cdn.discordapp.com/attachments/1096418851887009842/1108838934441639976/discord-6832787_960_720.png",
			"embeds": [{
				"title": "Command used.",
				"description": f"Command: /{message.interaction.name}\nUser: {message.interaction.user.name}#{message.interaction.user.discriminator}\nBot: {message.author.name}#{message.author.discriminator}",
				"color": 000000
			}]
		}
		headers = {
			"Content-Type": "application/json"
		}
		for webhook in webhooks_list:
			response=requests.post(webhook, json=data, headers=headers)


client.run(account_token)