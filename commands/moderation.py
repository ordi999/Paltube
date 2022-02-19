# https://youtu.be/xeBIAOKoaGo
import discord
# pour les footers des embeds
from datetime import datetime

class Moderation(discord.ext.commands.Cog):
	""" Toutes les commandes de Modérations """
	def __init__(self,bot,kick_activation,delete_activation, ban_activation,unban_activation,prefix):
		self.bot = bot
		self.kick_activation = kick_activation
		self.delete_activation = delete_activation
		self.ban_activation = ban_activation
		self.unban_activation = unban_activation
		self.prefix = prefix
	@discord.ext.commands.command(
	name="kick",
	brief="kick un membre du serveur",
	help="utilisez cette commande afin de kick quelqu'un du serveur !")
	###### Commande kick
	#on vérifie si l'utilisateur a la perm de kick
	@discord.ext.commands.has_permissions(kick_members=True)
	async def kick(self,ctx, member: discord.Member, *, reason=None):
		# on vérifie si kick est activé
		if(self.kick_activation):
			# on vérifie si on mentionne le bot
			if self.bot.user.mention == member.mention :
				# Si oui on renvoie un message d'erreur
				embed=discord.Embed(title="__ERREUR__", description="La commande **kick** ne marche pas sur moi 🙃",url="https://youtu.be/dQw4w9WgXcQ", color=0xff1a1a,timestamp = datetime.utcnow())
				embed.set_thumbnail(url="https://www.presse-citron.net/app/uploads/2000/Meme_Rick_Roll_Rick_Astley-Presse-Citron.jpg")
				embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
				# on ajoute une réaction au message de l'utilisateur
				await ctx.message.add_reaction("❌")
				
				await ctx.send(embed=embed, delete_after=5)
				await ctx.message.delete(delay = 2)
			else:
				# Si non, on vérifie s'il y a une raison
				if reason==None:
					#s'il n'y a pas de raison, on donne une valeur à la raison
					reason="Dieu a frappé 🔥"
				# on kick le membre ciblé
				await ctx.guild.kick(member)
				# On fait un embed de confirmation
				embed = discord.Embed(title="__Kick__",description=f"{member.mention} a été kick",colour=discord.Colour.green(),timestamp = datetime.utcnow())
				embed.add_field(name="Par:", value=ctx.author.mention, inline=False)
				embed.add_field(name="raison:", value=reason, inline=False)
				embed.set_thumbnail(url=member.avatar_url)
				# on ajoute une réaction au message de l'utilisateur
				embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
				await ctx.message.add_reaction("✅")
				# on envoit le embed
				await ctx.send(embed=embed)
		else:
			# si la commande est désactivé, on fait un embed pour prévenir l'utilisateur
			embed=discord.Embed(title="__Commande désactivée !__", description="La commande **kick** est désactivé 😥", color=0xff1a1a,timestamp = datetime.utcnow())
			embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
			embed.add_field(name="__Comment la réactiver ?__", value="Il vous suffit d'aller dans le code du bot puis de mettre la valeur de **kick_activation** à True au lieu de False 😉", inline=False)
			embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
			# on ajoute une réaction au message de l'utilisateur
			await ctx.message.add_reaction("❌")
			# on envoit le embed
			await ctx.send(embed=embed, delete_after=10) 
			await ctx.message.delete(delay = 2)
	
	#s'il y a une erreur lors de la commande kick
	@kick.error
	async def kick_error(self,ctx, error): 
		#on vérifie si c'est un manque de permission, si oui, on crée un embed
		if isinstance(error, discord.ext.commands.MissingPermissions):
			embed=discord.Embed(title="__ERREUR__", description="Vous avez besoin de la permission de **kick** !", color=0xff1a1a,timestamp = datetime.utcnow())
		#sinon on vérifie si c'est un mauvais argument, si oui, on crée un embed
		elif isinstance(error, discord.ext.commands.BadArgument):
			embed=discord.Embed(title="__ERREUR__", description="Veuillez mettre un **utilisateur** valide !", color=0xff1a1a,timestamp = datetime.utcnow())
		#sinon on vérifie si c'est un manque d'argument, si oui, on crée un embed
		elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
			embed=discord.Embed(title="__ERREUR__", description="Veuillez mettre le **bon** nombre d'argument(s) !", color=0xff1a1a,timestamp = datetime.utcnow())
		else:
			embed=discord.Embed(title="__ERREUR__", description="Il y a eu une erreur !", color=0xff1a1a,timestamp = datetime.utcnow())
		embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
		embed.add_field(name="__Besoin d'aide ?__", value="Utilisez la commande **"+self.prefix+"help kick **", inline=False)
		embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
		# on ajoute une réaction au message de l'utilisateur
		await ctx.message.add_reaction("❌")
		# on envoit le embed
		await ctx.send(embed=embed, delete_after=5)
		await ctx.message.delete(delay = 2)
	
	##### Commande delete
	@discord.ext.commands.command(
	name="del",
	brief="Permet de supprimer tous les messages ou seulement un certain nombre",
	help="utilisez cette commande afin de supprimer des messages !")
	#permet d'éxécuter ce code uniquement sur un serveur
	@discord.ext.commands.guild_only()
	# on vérifie la permission de modifier les messages
	@discord.ext.commands.has_permissions(manage_messages=True)
	#s'il n'y a pas de nombre de messages à supprimer, on supprime tous les messages
	async def delete(self,ctx, number_of_messages: int = 10000000000):
	# A tester -del desfs / -del -43
	# Voir si c'est possible de surprimer des messages jusqu'à une certaine date
		if(self.delete_activation):
			# Permet de supprimer les messages
			await ctx.channel.purge(limit=number_of_messages + 1)
		else:
			# si la commande est désactivé, on fait un embed pour prévenir l'utilisateur
			embed=discord.Embed(title="__Commande désactivée !__", description="La commande **delete** est désactivé 😥", color=0xff1a1a,timestamp = datetime.utcnow())
			embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
			embed.add_field(name="__Comment la réactiver ?__", value="Il vous suffit d'aller dans le code du bot puis de mettre la valeur de **delete_activation** à True au lieu de False 😉", inline=False)
			embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
			# on ajoute une réaction au message de l'utilisateur
			await ctx.message.add_reaction("❌")
			# on envoit le embed
			await ctx.send(embed=embed, delete_after=10) 
			await ctx.message.delete(delay = 2)
	

	#s'il y a une erreur lors de la commande delete
	
	@delete.error
	async def delete_error(self,ctx, error):
		#on vérifie si c'est un manque de permission, si oui, on crée un embed
		if isinstance(error, discord.ext.commands.MissingPermissions):
			embed=discord.Embed(title="__ERREUR__", description="Vous avez besoin de la permission de **supprimer** des message !", color=0xff1a1a,timestamp = datetime.utcnow())
		#sinon on vérifie si c'est un mauvais argument, si oui, on crée un embed
		elif isinstance(error, discord.ext.commands.BadArgument):
			embed=discord.Embed(title="__ERREUR__", description="Veuillez mettre un **nombre** valide !", color=0xff1a1a,timestamp = datetime.utcnow())
		else:
			embed=discord.Embed(title="__ERREUR__", description="Il y a eu une erreur !", color=0xff1a1a,timestamp = datetime.utcnow())
		embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
		embed.add_field(name="__Besoin d'aide ?__", value="Utilisez la commande **"+self.prefix+"help delete** !", inline=False)
		embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
		# on ajoute une réaction au message de l'utilisateur
		await ctx.message.add_reaction("❌")
		# on envoit le embed
		await ctx.send(embed=embed, delete_after=5)
		await ctx.message.delete(delay = 2)


	@discord.ext.commands.command(
	name="ban",
	brief="Permet de bannir un membre du serveur",
	help="utilisez cette commande afin de bannir quelqu'un du serveur !")
	###### Commande ban
	#on vérifie si l'utilisateur a la perm de ban
	@discord.ext.commands.has_permissions(ban_members=True)
	async def ban(self,ctx, member: discord.Member, *, reason=None):
		# on vérifie si ban est activé
		if(self.ban_activation):
			# on vérifie si on mentionne le bot
			if self.bot.user.mention == member.mention :
				# Si oui on renvoie un message d'erreur
				embed=discord.Embed(title="__ERREUR__", description="La commande **ban** ne marche pas sur moi 🙃",url="https://youtu.be/dQw4w9WgXcQ", color=0xff1a1a,timestamp = datetime.utcnow())
				embed.set_thumbnail(url="https://www.presse-citron.net/app/uploads/2000/Meme_Rick_Roll_Rick_Astley-Presse-Citron.jpg")
				embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
				# on ajoute une réaction au message de l'utilisateur
				await ctx.message.add_reaction("❌")
				
				await ctx.send(embed=embed, delete_after=5)
				await ctx.message.delete(delay = 2)
			else:
				# Si non, on vérifie s'il y a une raison
				if reason==None:
					#s'il n'y a pas de raison, on donne une valeur à la raison
					reason="Dieu a frappé 🔥"
				# on ban le membre ciblé
				await ctx.guild.ban(member)
				# On fait un embed de confirmation
				embed = discord.Embed(title="__Ban__",description=f"{member.mention} a été ban",colour=discord.Colour.green(),timestamp = datetime.utcnow())
				embed.add_field(name="Par:", value=ctx.author.mention, inline=False)
				embed.add_field(name="raison:", value=reason, inline=False)
				embed.set_thumbnail(url=member.avatar_url)
				# on ajoute une réaction au message de l'utilisateur
				embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
				await ctx.message.add_reaction("✅")
				# on envoit le embed
				await ctx.send(embed=embed)
		else:
			# si la commande est désactivé, on fait un embed pour prévenir l'utilisateur
			embed=discord.Embed(title="__Commande désactivée !__", description="La commande **ban** est désactivé 😥", color=0xff1a1a,timestamp = datetime.utcnow())
			embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
			embed.add_field(name="__Comment la réactiver ?__", value="Il vous suffit d'aller dans le code du bot puis de mettre la valeur de **ban_activation** à True au lieu de False 😉", inline=False)
			embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
			# on ajoute une réaction au message de l'utilisateur
			await ctx.message.add_reaction("❌")
			# on envoit le embed
			await ctx.send(embed=embed, delete_after=10) 
			await ctx.message.delete(delay = 2)

	#s'il y a une erreur lors de la commande ban
	@ban.error
	async def ban_error(self,ctx, error): 
		#on vérifie si c'est un manque de permission, si oui, on crée un embed
		if isinstance(error, discord.ext.commands.MissingPermissions):
			embed=discord.Embed(title="__ERREUR__", description="Vous avez besoin de la permission de **ban** !", color=0xff1a1a,timestamp = datetime.utcnow())
		#sinon on vérifie si c'est un mauvais argument, si oui, on crée un embed
		elif isinstance(error, discord.ext.commands.BadArgument):
			embed=discord.Embed(title="__ERREUR__", description="Veuillez mettre un **utilisateur** valide !", color=0xff1a1a,timestamp = datetime.utcnow())
		#sinon on vérifie si c'est un manque d'argument, si oui, on crée un embed
		elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
			embed=discord.Embed(title="__ERREUR__", description="Veuillez mettre le **bon** nombre d'argument(s) !", color=0xff1a1a,timestamp = datetime.utcnow())
		else:
			embed=discord.Embed(title="__ERREUR__", description="Il y a eu une erreur !", color=0xff1a1a,timestamp = datetime.utcnow())
		embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
		embed.add_field(name="__Besoin d'aide ?__", value="Utilisez la commande **"+self.prefix+"help ban **", inline=False)
		embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
		# on ajoute une réaction au message de l'utilisateur
		await ctx.message.add_reaction("❌")
		# on envoit le embed
		await ctx.send(embed=embed, delete_after=5)
		await ctx.message.delete(delay = 2)

	@discord.ext.commands.command(
	name="unban",
	brief="Permet de débannir un membre du serveur (il faut utiliser son ID discord)",
	help="utilisez cette commande afin de débannir quelqu'un du serveur !(il faut utiliser son ID discord)")
	###### Commande unban
	#on vérifie si l'utilisateur a la perm de ban
	@discord.ext.commands.has_permissions(ban_members=True)
	async def unban(self,ctx, member_id):
		# on vérifie si unban est activé
		if(self.unban_activation):
			user = await self.bot.fetch_user(member_id)
			await ctx.guild.unban(user)
			
			embed = discord.Embed(title="__Ban__",description=f"{user.mention} a été déban",colour=discord.Colour.green(),timestamp = datetime.utcnow())
			embed.add_field(name="Par:", value=ctx.author.mention, inline=False)
			embed.set_thumbnail(url=user.avatar_url)
			# on ajoute une réaction au message de l'utilisateur
			embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
			await ctx.message.add_reaction("✅")
				# on envoit le embed
			await ctx.send(embed=embed)
		else:
			# si la commande est désactivé, on fait un embed pour prévenir l'utilisateur
			embed=discord.Embed(title="__Commande désactivée !__", description="La commande **unban** est désactivé 😥", color=0xff1a1a,timestamp = datetime.utcnow())
			embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
			embed.add_field(name="__Comment la réactiver ?__", value="Il vous suffit d'aller dans le code du bot puis de mettre la valeur de **unban_activation** à True au lieu de False 😉", inline=False)
			embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
			# on ajoute une réaction au message de l'utilisateur
			await ctx.message.add_reaction("❌")
			# on envoit le embed
			await ctx.send(embed=embed, delete_after=10) 
			await ctx.message.delete(delay = 2)

	#s'il y a une erreur lors de la commande ban
	@unban.error
	async def unban_error(self,ctx, error): 
		#on vérifie si c'est un manque de permission, si oui, on crée un embed
		if isinstance(error, discord.ext.commands.MissingPermissions):
			embed=discord.Embed(title="__ERREUR__", description="Vous avez besoin de la permission de **ban** !", color=0xff1a1a,timestamp = datetime.utcnow())
		#sinon on vérifie si c'est un mauvais argument, si oui, on crée un embed
		elif isinstance(error, discord.ext.commands.BadArgument):
			embed=discord.Embed(title="__ERREUR__", description="Veuillez mettre un **utilisateur** valide !", color=0xff1a1a,timestamp = datetime.utcnow())
		#sinon on vérifie si c'est un manque d'argument, si oui, on crée un embed
		elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
			embed=discord.Embed(title="__ERREUR__", description="Veuillez mettre le **bon** nombre d'argument(s) !", color=0xff1a1a,timestamp = datetime.utcnow())
		elif isinstance(error,discord.ext.commands.CommandInvokeError):
			embed=discord.Embed(title="__ERREUR__", description="l'utilisateur que vous cherchez n'est pas dans la liste des bannis ! (vérifiez que vous utilisez bien l'ID discord de l'utilisateur que vous souhaitez unban)", color=0xff1a1a,timestamp = datetime.utcnow())
		else:
			embed=discord.Embed(title="__ERREUR__", description="Il y a eu une erreur !", color=0xff1a1a,timestamp = datetime.utcnow())
		embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
		embed.add_field(name="__Besoin d'aide ?__", value="Utilisez la commande **"+self.prefix+"help unban **", inline=False)
		embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
		# on ajoute une réaction au message de l'utilisateur
		await ctx.message.add_reaction("❌")
		# on envoit le embed
		await ctx.send(embed=embed, delete_after=5)
		await ctx.message.delete(delay = 2)