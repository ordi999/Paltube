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


# on se connecte à la database
client = pymongo.MongoClient(os.environ['DB'])
db = client.db_name

# Pour créer ou supprimer eco
#db.create_collection("eco")
#db.drop_collection("eco")
#print(db.list_collection_names())
eco = db.eco

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
keep_alive()

# Lancement du bot
bot.add_cog(moderation.Moderation(bot,kick_activation,delete_activation,prefix))

bot.add_cog(autres.Autres(bot,prefix,commands_activation))

bot.add_cog(economy.Economy(bot,eco,prefix,bal_activation, work_activation,pay_activation,bet_activation,daily_activation,add_money_activation,remove_money_activation,set_money_activation,get_all_data_activation))

bot.add_cog(zone_de_test.Zone_de_test(bot,prefix, dice_activation))

bot.run(os.environ['TOKEN'])