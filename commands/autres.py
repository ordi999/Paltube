import discord
from datetime import datetime

class Autres(discord.ext.commands.Cog):
	""" Autres commandes """
	####### commande commands : Affiche les commandes faites et à faires
	def __init__(self,bot,prefix,commands_activation):
		self.bot = bot
		self.commands_activation = commands_activation
		self.prefix = prefix
	@discord.ext.commands.command(
	name="commands",
	brief="Affiche la liste des commandes",
	help="utilisez cette commande afin de connaitre la liste des commandes du bot !")
	async def commands(self, ctx):
		if self.commands_activation:
			# Création d'un Embed avec un titre, une redirection et une couleur (0xff1a1a:rouge)
			embed=discord.Embed(title="Liste des commandes à faire",
			url="http://paltube.great-site.net/accueil.html", color=0xff1a1a,timestamp = datetime.utcnow())

			# Ajout de la catégorie Facile avec tous les commandes faciles
			embed.add_field(name="__Facile__", value="-modération\n-dé\n-traduction\n-auto modération\n-join leave message(image perso style mee6)\n-Minecraft command\n-weather\n-anniv\n-programmation évent date et heure\n-prefix\n-akinator\n-~~help~~ : **Fait par ordi999**\n-status qui permet de changer le status via une commande\n-Activation\n-Changelog (Commande qui permet d'y accéder)\n-~~status automatic change~~ : **Fait par ordi999**", inline=False)

			# Ajout de la catégorie Moyen avec tous les commandes Moyennes
			embed.add_field(name="__Moyen__", value="-ticket/modmail\n-activer/désactivé fonction du bot\n-gif style koya\n-leveling (a lie avec economy)\n-giveaway\n-web scraping (Paul)\n-web dashboard\n-economy + gambling + trade\n-mini jeux\n-rôle automatique\n-leaderboard\n-log\n-poll\n-member count / serveur count", inline=False)

			# Ajout de la catégorie Difficile avec tous les commandes Difficiles
			embed.add_field(name="__Difficile __", value="-rpg (Lucas principalement)\n-chatbot \n-musique", inline=False)

			# Ajout de la catégorie Modération avec tous les commandes de modération
			embed.add_field(name="__Modération __", value="-ban / temp ban / unban\n-~~kick~~ : **Fait par ordi999**\n-mute / temp mute / unmute\n-~~delete message~~ : **Fait par ordi999** \n-warn\n-slowmode", inline=False)
			
			#Ajout d'un footer affichant le pseudo de la personne ayant demandé la commande
			embed.set_footer(text="Commande demandé par : " + ctx.author.display_name)
			# Envoit de l'embed dans le channel
			await ctx.send(embed=embed)
		else:
			# si la commande est désactivé, on fait un embed pour prévenir l'utilisateur
			embed=discord.Embed(title="__Commande désactivée !__", description="La commande **commands** est désactivé 😥", color=0xff1a1a,timestamp = datetime.utcnow())
			embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
			embed.add_field(name="__Comment la réactiver ?__", value="Il vous suffit d'aller dans le code du bot puis de mettre la valeur de **commands_activation** à True au lieu de False 😉", inline=False)
			embed.set_footer(text="Commande demandé par : " + ctx.author.display_name)
			# on ajoute une réaction au message de l'utilisateur
			await ctx.message.add_reaction("❌")
			# on envoit le embed
			await ctx.send(embed=embed, delete_after=10)
			await ctx.message.delete(delay = 2)
	@commands.error
	async def commands_error(self,ctx, error):
		embed=discord.Embed(title="__ERREUR__", description="Il y a eu une erreur !", color=0xff1a1a,timestamp = datetime.utcnow())
		embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
		embed.add_field(name="__Besoin d'aide ?__", value="Utilisez la commande **"+self.prefix+"help commands **", inline=False)
		embed.set_footer(text="Commande demandé par : " + ctx.author.display_name)
		# on ajoute une réaction au message de l'utilisateur
		await ctx.message.add_reaction("❌")
		# on envoit le embed
		await ctx.send(embed=embed, delete_after=5)
		await ctx.message.delete(delay = 2)