import discord
from datetime import datetime
import random

class Zone_de_test(discord.ext.commands.Cog):
	""" Commandes en test """
	def __init__(self,bot,prefix,dice_activation):
		self.bot = bot
		self.prefix = prefix
		self.dice_activation = dice_activation
	@discord.ext.commands.command(
	name="dice",
	brief="Permet de lancer des dés",
	help="Permet de lancer des dés !")
	async def dice(self,ctx, number_of_de: int,face: int):
		if self.dice_activation:
			#pouvoir mettre plusieur de de différente face à la fois

			embed=discord.Embed(title="Dice",
			description=f"Vous avez lancé {number_of_de} dés à {face} face",color=discord.Colour.blue(),timestamp = datetime.utcnow())
			embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/9/9c/Purple_d20.png")
			
			for i in range(0,number_of_de):
				embed.add_field(name=f"Résultat: {i+1}",value=f"La valeur total de votre lancé n°{i+1} est de {random.randint(1,int(face))}.",inline=False)
			embed.add_field(name=f"Résultat Final:",value=f"La Valeur Total est de .",inline=False)
			embed.set_footer(text="Commande demandé par : " + ctx.author.display_name)
			await ctx.send(embed=embed)
		else:
			# si la commande est désactivé, on fait un embed pour prévenir l'utilisateur
			embed=discord.Embed(title="__Commande désactivée !__", description="La commande **dice** est désactivé 😥", color=0xff1a1a,timestamp = datetime.utcnow())
			embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
			embed.add_field(name="__Comment la réactiver ?__", value="Il vous suffit d'aller dans le code du bot puis de mettre la valeur de **dice_activation** à True au lieu de False 😉", inline=False)
			embed.set_footer(text="Commande demandé par : " + ctx.author.display_name)
			# on ajoute une réaction au message de l'utilisateur
			await ctx.message.add_reaction("❌")
			# on envoit le embed
			await ctx.send(embed=embed, delete_after=10)
			await ctx.message.delete(delay = 2)