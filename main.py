#importation de l'os afin de lancer le bot
import os
#importation de discord
import discord
#importation de modules complémentaire de discord : commands est nécéssaire et tasks est pour faire des boucle
from discord.ext import commands, tasks
#importation du fichier permettant l'host h24
from keep_alive import keep_alive
#importation de cycle pour faire le changement automatique de status
from itertools import cycle
#importation pour générer des nombre aléatoire(commande de)
import random
# Pour la base de données
import pymongo
# pour la commande help
from pretty_help import DefaultMenu, PrettyHelp
# Pour plus tard / commande mute
from asyncio import sleep
# pour les footers des embeds
from datetime import datetime

#importation des cogs
import commands.moderation as moderation
import commands.autres as autres
import commands.economy as economy
import commands.zone_de_test as zone_de_test

# on se connecte à la database
client = pymongo.MongoClient(os.environ['DB'])
db = client.db_name

# Pour créer ou supprimer eco
#db.create_collection("eco")
#db.drop_collection("eco")
#print(db.list_collection_names())
eco = db.eco

from routes.utils import app
from quart import Quart, redirect, url_for, render_template, request
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
app = Quart(__name__)

app.secret_key = os.environ.get("session")
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"
app.config["DISCORD_CLIENT_ID"] = os.environ.get("CLIENT_ID")
app.config["DISCORD_CLIENT_SECRET"] = os.environ.get("CLIENT_SECRET")
app.config["DISCORD_REDIRECT_URI"] = os.environ.get("RI")
app.config["DISCORD_BOT_TOKEN"] = os.environ.get("token")
discordd = DiscordOAuth2Session(app)

@app.route("/")
async def home():
	logged = ""
	lst = []
	data = {}
	balance = 0
	if await discordd.authorized:
		logged = True
		user = await discordd.fetch_user()

		check = eco.find_one({"id": user.id})			
		# si l'utilisateur n'a pas de compte
		if check is None:
			#on lui fait un compte
			create_eco(user,eco)
			check = eco.find_one({"id": user.id})		
		# on stock son solde
		balance = check['money']
	return await render_template("index.html", logged=logged, balance=balance)

@app.route("/login/")
async def login():
	return await discordd.create_session(scope=["identify", "guilds"])

@app.route("/logout/")
async def logout():
	discordd.revoke()
	return redirect(url_for(".home"))

@app.route("/me/")
@requires_authorization
async def me():
  user = await discordd.fetch_user()
  return redirect(url_for(".home"))

@app.route("/callback/")
async def callback():
  await discordd.callback()
  try:
    return redirect(bot.url)
  except:
    return redirect(url_for(".me"))

@app.errorhandler(Unauthorized)
async def redirect_unauthorized(e):
  bot.url = request.url
  return redirect(url_for(".login"))

######### Activer ou Désactiver features ##########
changement_status_activation = True
kick_activation = True
delete_activation =True
commands_activation = True
bal_activation = True
work_activation = True
pay_activation = True
bet_activation = True
dice_activation = True
daily_activation = True
add_money_activation = True
remove_money_activation = True
set_money_activation = True
get_all_data_activation = True
reset_user_account_activation = True

#Tous les status que vas prendre le bot
status = cycle([
    'Status 1', 'Status 2',
    'Status 3', 'Status 4',
    'Status 5'
])

#Définition du bot
prefix='-'
default_intents = discord.Intents.default()
default_intents.members = True
bot = commands.Bot(command_prefix=prefix,
                   intents=default_intents,
                   description='Paltube')




#Lorsque le bot se lance
@bot.event
async def on_ready():
  # Si le changement de status est activé
  if (changement_status_activation):
    #on charge la boucle du changement de status
    change_status.start()
  
  #on prévient dans la console que le bot a été connecté ainsi que son nom d'utilisateur
  print("Nous avons été connectée en tant que {0.user}".format(bot))

# Si le changement de status est activé
if(changement_status_activation):
  #Boucle pour le changement de status
  @tasks.loop(seconds=10)
  async def change_status():
    # changement de status du bot
    await bot.change_presence(activity=discord.Game(next(status)))

#### Help command
menu = DefaultMenu('◀️', '▶️', '❌')
bot.help_command = PrettyHelp(navigation=menu, color=discord.Colour.blue())


# Appel de la fonction permettant d'host h24
#keep_alive()
bot.loop.create_task(app.run_task('0.0.0.0'))

# Lancement du bot
bot.add_cog(moderation.Moderation(bot,kick_activation,delete_activation,prefix))

bot.add_cog(autres.Autres(bot,prefix,commands_activation))

bot.add_cog(economy.Economy(bot,eco,prefix,bal_activation, work_activation,pay_activation,bet_activation,daily_activation,add_money_activation,remove_money_activation,set_money_activation,get_all_data_activation,reset_user_account_activation))

bot.add_cog(zone_de_test.Zone_de_test(bot,prefix, dice_activation))

bot.run(os.environ['TOKEN'])