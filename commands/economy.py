import discord
from datetime import datetime, timedelta
import random


from commands.functions import create_eco


# Catégories économie
class Economy(discord.ext.commands.Cog):
	""" Toutes les commandes en rapport avec l'économie """
	# permet de récupérer les informations utile pour les commandes
	def __init__(self,bot,eco,prefix,bal_activation, work_activation,pay_activation,bet_activation,daily_activation,add_money_activation, remove_money_activation,set_money_activation,get_all_data_activation, reset_user_data_activation,coinflip_activation,reward_activation, slots_activation):
		self.bot = bot
		self.eco = eco
		self.prefix = prefix
		self.bal_activation = bal_activation
		self.work_activation = work_activation
		self.pay_activation = pay_activation
		self.bet_activation = bet_activation
		self.daily_activation = daily_activation
		self.add_money_activation = add_money_activation
		self.remove_money_activation = remove_money_activation
		self.set_money_activation = set_money_activation
		self.get_all_data_activation = get_all_data_activation
		self.reset_user_data_activation = reset_user_data_activation
		self.coinflip_activation = coinflip_activation
		self.reward_activation = reward_activation
		self.slots_activation = slots_activation
	# commande bal pour savoir son solde ou celui de quelqu'un
	@discord.ext.commands.command(
	name="bal",
	brief="Permet de consulter votre solde ou celui de quelqu'un d'autre",
	help="utilisez cette commande afin de connaitre votre solde ou celui de quelqu'un d'autre !")
	async def balance(self, ctx, user: discord.Member = None):
		# si la commande est activée
		if self.bal_activation:
			# on récupère le nom de l'utilisateur ayant envoyé le message
			author = ctx.author
			
			# on vérifie s'il veut savoir ses informations ou celle de quelqu'un d'autre
			if user is None:
				# on stock le dictionnaire contenant les infos de l'utilisateur
				check = self.eco.find_one({"id": author.id})
				
				# si l'utilisateur n'a pas de compte
				if check is None:
					#on lui cré un compte
					create_eco(ctx.author,self.eco)
					check = self.eco.find_one({"id": author.id})
				
				# on stock son solde
				balance = check['money']
				
				# on lui envoie un message avec son solde
				embed = discord.Embed(
					title = "Ton solde !",
					description = f"**Solde :** {balance}€",
					color = discord.Colour.random(),
					timestamp = datetime.utcnow()
				)
				embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
				# on utilise la fonction reply
				await ctx.message.reply(embed=embed)
				return
			# s'il veut savoir les informations du compte de quelqu'un d'autre
			else:
				# on stock le dictionnaire contenant les infos de l'utilisateur
				check = self.eco.find_one({"id": user.id})
				
				# si l'utilisateur n'a pas de compte
				if check is None:
					#on lui fait un compte
					create_eco(user,self.eco)
					check = self.eco.find_one({"id": user.id})
				
				# on stock son solde
				balance = check['money']
				
				# on envoit son solde
				embed = discord.Embed(
					title = f"Solde de {user.name} !",
					description = f"**Solde :** {balance}€",
					color = discord.Colour.random(),
					timestamp = datetime.utcnow()
				)
				embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
				await ctx.message.reply(embed=embed)
				return
		else:
			# si la commande est désactivé, on fait un embed pour prévenir l'utilisateur
			embed=discord.Embed(title="__Commande désactivée !__", description="La commande **bal** est désactivé 😥", color=0xff1a1a,timestamp = datetime.utcnow())
			embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
			embed.add_field(name="__Comment la réactiver ?__", value="Il vous suffit d'aller dans le code du bot puis de mettre la valeur de **bal_activation** à True au lieu de False 😉", inline=False)
			embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
			# on ajoute une réaction au message de l'utilisateur
			await ctx.message.add_reaction("❌")
			# on envoit le embed
			await ctx.send(embed=embed, delete_after=10)
			await ctx.message.delete(delay = 2)
	@balance.error
	async def balance_error(self,ctx, error):
		#sinon on vérifie si c'est un mauvais argument, si oui, on crée un embed
		if isinstance(error, discord.ext.commands.BadArgument):
			embed=discord.Embed(title="__ERREUR__", description="Veuillez mettre un **utilisateur** valide !", color=0xff1a1a,timestamp = datetime.utcnow())
		else:
			embed=discord.Embed(title="__ERREUR__", description="Il y a eu une erreur !", color=0xff1a1a,timestamp = datetime.utcnow())
		embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
		embed.add_field(name="__Besoin d'aide ?__", value="Utilisez la commande **"+self.prefix+"help bal **", inline=False)
		embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
		# on ajoute une réaction au message de l'utilisateur
		await ctx.message.add_reaction("❌")
		# on envoit le embed
		await ctx.send(embed=embed, delete_after=5)
		await ctx.message.delete(delay = 2)

	# Commande work pour gagner de l'argent
	@discord.ext.commands.command(
		name="work",
		brief="Permet de travailler pour gagner un salaire (cooldown de 10 secondes)",
		help="utilisez cette commande afin de travailler et ainsi gagner un salaire ! (cooldown de 10 secondes)")
	# on met un cooldown de 10 secondes
	@discord.ext.commands.cooldown(1, 10, discord.ext.commands.BucketType.user)
	async def work(self,ctx):
		# si la commande est activée
		if self.work_activation:
			# on récupère le nom de l'utilisateur ayant envoyer le message
			user = ctx.author
			
			# on stock le dictionnaire contenant les infos de l'utilisateur
			check = self.eco.find_one({"id": user.id})
			
			# si l'utilisateur n'a pas de compte
			if check is None:
				# on lui fait un compte
				create_eco(user,self.eco)
				check = self.eco.find_one({"id": user.id})
			
			# on cré une liste de métiers
			job_names = ["🧑🏻‍ géologue 👩🏻‍🦰","👨‍🌾 Fermier(e) 👩‍🌾", "👮‍♂️ Policier(e) 👮‍♀️", "🦹‍♂️ Criminel(le) 🦹‍♀️", "🚕 Taxi 🚕", "👨‍🔧 Mécanicien(ne) 👩‍🔧", "👨‍🎤 Chanteur(se) 👩‍🎤", "👨‍💻 Informaticien(ne) 👩‍💻", "👨‍✈️ Pilote 👩‍✈️"]
			# on en choisit un
			job = random.choice(job_names)
			
			# on choisir aléatoirement la somme gagné
			amount = random.randint(1, 10)
			# on calcule son nouveau solde
			newBal = check['money'] + amount
			
			# on met à jour son solde sur la database
			self.eco.update_one({"id": user.id}, {"$set": {"money": newBal}})
			
			# on envoie un message pour lui dire combien il a gagné
			embed = discord.Embed(
				title = "Tu as fini de travailler !",
				description = f"Tu as travaillé en tant que **{job}** et tu as gagné **{amount}€** !",
				color = discord.Colour.random(),timestamp = datetime.utcnow()
			)
			embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
			await ctx.message.reply(embed=embed)
			return
		else:
			# si la commande est désactivé, on fait un embed pour prévenir l'utilisateur
			embed=discord.Embed(title="__Commande désactivée !__", description="La commande **work** est désactivé 😥", color=0xff1a1a,timestamp = datetime.utcnow())
			embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
			embed.add_field(name="__Comment la réactiver ?__", value="Il vous suffit d'aller dans le code du bot puis de mettre la valeur de **work_activation** à True au lieu de False 😉", inline=False)
			embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
			# on ajoute une réaction au message de l'utilisateur
			await ctx.message.add_reaction("❌")
			# on envoit le embed
			await ctx.send(embed=embed, delete_after=10)
			await ctx.message.delete(delay = 2)
	@work.error
	async def work_error(self,ctx, error):
		# si c'est à cause du cooldown
		if isinstance(error, discord.ext.commands.CommandOnCooldown):
			await ctx.message.reply(f"Il y a un cooldown, veuillez encore attendre {format(error.retry_after, '.2f')} secondes", delete_after = 3)
			await ctx.message.delete(delay = 2)
			return
		else:
			embed=discord.Embed(title="__ERREUR__", description="Il y a eu une erreur !", color=0xff1a1a,timestamp = datetime.utcnow())
		embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
		embed.add_field(name="__Besoin d'aide ?__", value="Utilisez la commande **"+self.prefix+"help work **", inline=False)
		embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
		# on ajoute une réaction au message de l'utilisateur
		await ctx.message.add_reaction("❌")
		# on envoit le embed
		await ctx.send(embed=embed, delete_after=5)
		await ctx.message.delete(delay = 2)
	
	# Commande pay pour donner de l'argent à quelqu'un
	@discord.ext.commands.command(
		name="pay",
		brief="Permet de donner de l'argent à un autre utilisateur ayant un compte",
		help="utilisez cette commande afin de donner de l'argent à un autre utilisateur ayant un compte !")
	async def pay(self,ctx, user: discord.Member, amount:int):
		# Si la commande est activée
		if(self.pay_activation):
			# on récupère le nom de l'utilisateur ayant envoyer le message
			author = ctx.author
			# Si on tente de se donner de l'argent
			if user == author:
				# on prévient que c'est impossible
				await ctx.message.reply("Tu ne peux pas te donner de l'argent à toi-même",delete_after = 5)	
				await ctx.message.delete(delay = 2)
				return
			# si la somme est négative ou nulle
			if amount <= 0:
				# on prévient que c'est impossible
				await ctx.message.reply("Il faut mettre une somme valide",delete_after = 5)	
				await ctx.message.delete(delay = 2)
				return
			# on stock le dictionnaire contenant les infos de l'utilisateur
			check = self.eco.find_one({"id": author.id})
			
			# si l'utilisateur n'a pas de compte
			if check is None:
				# on lui fait un compte
				create_eco(author,self.eco)
				check = self.eco.find_one({"id": author.id})

			
			# on stock le dictionnaire contenant les infos de l'utilisateur à qui il veut envoyer de l'argent
			check2 = self.eco.find_one({"id": user.id})

			# si cet utilisateur n'a pas de compte
			if check2 is None:
				# on lui fait un compte
				create_eco(user,self.eco)
				check2 = self.eco.find_one({"id": user.id})

			# on stock son solde 
			balance = check['money']
				# on vérifie que l'utilisateur a sufisamment de d'argent sur son compte 
			if balance >= amount:
				# si oui, on stock l'argent de l'utilisateur qui va recevoir l'argent
				balance2 = check2['money']
				# on retire l'argent du compte de l'utilisateur qui a envoyer l'argent
				self.eco.update_one({"id": author.id}, {"$set": {"money": balance - amount}})

				# on ajoute l'argent au compte de l'utilisateur qui va recevoir cette argent
				self.eco.update_one({"id": user.id}, {"$set": {"money": balance2 + amount}})

				# on fait un message pour dire que le paiement a été réussi
				embed = discord.Embed(
					title = "Paiement réussi 🤑",
					description = f"Vous avez donné **{amount}€** à **{user.mention}** !  🎉",
					color = discord.Colour.random(),timestamp = datetime.utcnow())
				embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
				await ctx.message.reply(embed=embed)
				return

			# si l'utilisateur n'a pas asser d'argent
			else:
				# on le prévient
				await ctx.message.reply("Vous n'avez pas assez d'argent ")
				return
		else:
			# si la commande est désactivé, on fait un embed pour prévenir l'utilisateur
			embed=discord.Embed(title="__Commande désactivée !__", description="La commande **pay** est désactivé 😥", color=0xff1a1a,timestamp = datetime.utcnow())
			embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
			embed.add_field(name="__Comment la réactiver ?__", value="Il vous suffit d'aller dans le code du bot puis de mettre la valeur de **pay_activation** à True au lieu de False 😉", inline=False)
			embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
			# on ajoute une réaction au message de l'utilisateur
			await ctx.message.add_reaction("❌")
			# on envoit le embed
			await ctx.send(embed=embed, delete_after=10)
			await ctx.message.delete(delay = 2)
	@pay.error
	async def pay_error(self,ctx, error):
		#sinon on vérifie si c'est un mauvais argument, si oui, on crée un embed
		if isinstance(error, discord.ext.commands.BadArgument):
			embed=discord.Embed(title="__ERREUR__", description="Veuillez mettre un **utilisateur** valide !", color=0xff1a1a,timestamp = datetime.utcnow())
		#sinon on vérifie si c'est un manque d'argument, si oui, on crée un embed
		elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
			embed=discord.Embed(title="__ERREUR__", description="Veuillez mettre le **bon** nombre d'argument(s) !", color=0xff1a1a,timestamp = datetime.utcnow())
		else:
			embed=discord.Embed(title="__ERREUR__", description="Il y a eu une erreur !", color=0xff1a1a,timestamp = datetime.utcnow())
		embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
		embed.add_field(name="__Besoin d'aide ?__", value="Utilisez la commande **"+self.prefix+"help pay **", inline=False)
		embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
		# on ajoute une réaction au message de l'utilisateur
		await ctx.message.add_reaction("❌")
		# on envoit le embed
		await ctx.send(embed=embed, delete_after=5)
		await ctx.message.delete(delay = 2)
	
	# Commande bet pour parier de l'argent
	@discord.ext.commands.command(
		name="bet",
		brief="Permet de parier une somme pour tenter de gagner plus \nVoici les pourcentages : \n- 2% -> x12\n- 4% -> x8\n- 6% -> x4\n- 8% -> x2\nTotal : 20% de gagner !",
		help="Permet de parier une somme pour tenter de gagner plus \nVoici les pourcentages : \n- 2% -> x12\n- 4% -> x8\n- 6% -> x4\n- 8% -> x2\nTotal : 20% de gagner !")
	async def bet(self,ctx,  amount:int):
		# si la commande est activée
		if self.bet_activation:
			# on récupère le nom de l'utilisateur ayant envoyer le message
			user = ctx.author
			
			# on stock le dictionnaire contenant les infos de l'utilisateur
			check = self.eco.find_one({"id": user.id})
			
			# si l'utilisateur n'a pas de compte
			if check is None:
				# on lui en fait un
				create_eco(user,self.eco)
				check = self.eco.find_one({"id": user.id})
			
			# si la somme pariée est négative ou nulle
			if amount <= 0:
				# on prévient que c'est impossible
				await ctx.message.reply("Il faut mettre une somme valide")
				return
			#on récupére son solde
			balance = check['money']
			# on vérifie s'il a l'argent nécéssaire
			if balance >= amount:
				# si oui on supprime l'argent qu'il a parié
				self.eco.update_one({"id": user.id}, {"$set": {"money": balance - amount}})

				rand = random.randint(1, 50)
				# 2% de chance de gagner
				if rand == 1:
					# s'il gagne on lui donne 12 fois sa mise
					embed = discord.Embed(title="WIN", description = f"Vous aviez misé **{amount}€** et vous avez gagné 12 fois cette somme, ce qui vous fait un total de **{amount * 12}€** !",color = discord.Colour.green())

					embed.set_thumbnail(url = "https://media.istockphoto.com/vectors/big-win-banner-vector-id611088484?k=20&m=611088484&s=170667a&w=0&h=rpQcUoJUxaI2cT7UYTx0MM1Ww7iyEppHzyPisqsoSQ8=")

					self.eco.update_one({"id": user.id}, {"$set": {"money": balance + (amount*12)}})
						
					await ctx.message.reply(embed=embed)
				elif rand == 2 or rand == 3:
						# s'il gagne on lui donne 8 fois sa mise
					embed = discord.Embed(title="WIN", description = f"Vous aviez misé **{amount}€** et vous avez gagné 8 fois cette somme, ce qui vous fait un total de **{amount * 8}€** !",color = discord.Colour.green())

					embed.set_thumbnail(url = "https://media.istockphoto.com/vectors/big-win-banner-vector-id611088484?k=20&m=611088484&s=170667a&w=0&h=rpQcUoJUxaI2cT7UYTx0MM1Ww7iyEppHzyPisqsoSQ8=")

					self.eco.update_one({"id": user.id}, {"$set": {"money": balance + (amount*8)}})
						
					await ctx.message.reply(embed=embed)
				elif rand == 4 or rand == 5 or rand == 6:
					# s'il gagne on lui donne 4 fois sa mise
					embed = discord.Embed(title="WIN", description = f"Vous aviez misé **{amount}€** et vous avez gagné 4 fois cette somme, ce qui vous fait un total de **{amount * 4}€** !",color = discord.Colour.green())

					embed.set_thumbnail(url = "https://img.freepik.com/free-vector/you-win-lettering-pop-art-text-banner_185004-60.jpg?size=626&ext=jpg")

					self.eco.update_one({"id": user.id}, {"$set": {"money": balance + (amount*4)}})
						
					await ctx.message.reply(embed=embed)
				elif rand == 7 or rand == 8 or rand == 9 or rand == 10:
					# s'il gagne on lui donne 2 fois sa mise
					embed = discord.Embed(title="WIN", description = f"Vous aviez misé **{amount}€** et vous avez gagné 2 fois cette somme, ce qui vous fait un total de **{amount * 2}€** !",color = discord.Colour.green())

					embed.set_thumbnail(url = "https://img.freepik.com/free-vector/you-win-lettering-pop-art-text-banner_185004-60.jpg?size=626&ext=jpg")

					self.eco.update_one({"id": user.id}, {"$set": {"money": balance + (amount*2)}})
						
					await ctx.message.reply(embed=embed)
				else:
					# il a perdu et on le prévient
					embed = discord.Embed(title="LOSE", description = f"Vous aviez misé **{amount}€** et vous avez les avez perdu 😢\n Retentez encore une fois, vous aurez surement plus de chance !",color = discord.Colour.purple())
					embed.set_thumbnail(url = "https://pixelartmaker-data-78746291193.nyc3.digitaloceanspaces.com/image/34c586ac41db5ac.png")
					await ctx.message.reply(embed=embed)
			else:
				# on le prévient
				await ctx.message.reply("Vous n'avez pas assez d'argent ")
				return
		else:
			# si la commande est désactivé, on fait un embed pour prévenir l'utilisateur
			embed=discord.Embed(title="__Commande désactivée !__", description="La commande **bet** est désactivé 😥", color=0xff1a1a,timestamp = datetime.utcnow())
			embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
			embed.add_field(name="__Comment la réactiver ?__", value="Il vous suffit d'aller dans le code du bot puis de mettre la valeur de **bet_activation** à True au lieu de False 😉", inline=False)
			embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
			# on ajoute une réaction au message de l'utilisateur
			await ctx.message.add_reaction("❌")
			# on envoit le embed
			await ctx.send(embed=embed, delete_after=10)
			await ctx.message.delete(delay = 2)
	
	@bet.error
	async def bet_error(self,ctx, error):
		#sinon on vérifie si c'est un mauvais argument, si oui, on crée un embed
		if isinstance(error, discord.ext.commands.BadArgument):
			embed=discord.Embed(title="__ERREUR__", description="Veuillez mettre un **utilisateur** valide !", color=0xff1a1a,timestamp = datetime.utcnow())
		#sinon on vérifie si c'est un manque d'argument, si oui, on crée un embed
		elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
			embed=discord.Embed(title="__ERREUR__", description="Veuillez mettre le **bon** nombre d'argument(s) !", color=0xff1a1a,timestamp = datetime.utcnow())
		else:
			embed=discord.Embed(title="__ERREUR__", description="Il y a eu une erreur !", color=0xff1a1a,timestamp = datetime.utcnow())
		embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
		embed.add_field(name="__Besoin d'aide ?__", value="Utilisez la commande **"+self.prefix+"help bet **", inline=False)
		embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
		# on ajoute une réaction au message de l'utilisateur
		await ctx.message.add_reaction("❌")
		# on envoit le embed
		await ctx.send(embed=embed, delete_after=5)
		await ctx.message.delete(delay = 2)

	@discord.ext.commands.command(
		name="daily",
		brief="Permet de gagner de l'argent tous les jours, si vous l'utilisez plusieurs jours consécutif, vous gagnerez plus d'argent !",
		help="Permet de gagner de l'argent tous les jours, si vous l'utilisez plusieurs jours consécutif, vous gagnerez plus d'argent !") 
	async def daily(self,ctx):
		if self.daily_activation:
			# on récupère l'utilisateur
			user = ctx.author

			# on stock le dictionnaire contenant les infos de l'utilisateur
			check = self.eco.find_one({"id": user.id})
			
			# si l'utilisateur n'a pas de compte
			if check is None:
				# on lui en fait un
				create_eco(user,self.eco)
				check = self.eco.find_one({"id": user.id})
			
			# on récupère son solde
			balance = check['money']

			# on récupère son daily_streak
			streak = check["daily_streak"]
			# on récupère la dernière fois qu'il a utilisé la commande
			last_daily = check["last_daily"]
			# on récupère son meilleur daily-streak
			best = check["best_daily_streak"]

			# on récupère la date actuelle
			now = datetime.fromtimestamp(float(str(datetime.now().timestamp())))

			# on regarde s'il n'a pas fait son daily streak à temps
			if now-last_daily > timedelta(hours=48):
				# dans ce cas on reset son daily_streak
				streak = 1
			# Sinon s'il tente de la refaire avant la fin du cooldown / PS : On utilise pas le cooldown de discord car si le bot est redémaré le cooldown est reset
			elif now-last_daily < timedelta(hours=24):
				# on récupère le temps en seconde restant
				temps = (24*60*60) - (now-last_daily).total_seconds()
				# on regarde si c'est un temps en heure si oui on le convertit
				if(temps/3600 <=24 and temps/3600>=1):
					temps = str(int(temps/3600)) + " heures et " + str(int((temps%3600)/60)) + " minutes"
				# on regarde si c'est un temps en minutes si oui on le convertit
				elif(temps/60 <60 and temps/60>=1):
					temps = str(int(temps/60)) + " minutes et " + str(int(temps%60)) + " secondes"
				else:
				# sinon c'est un temps en seconde, on le convertit
					temps =  str(int(temps)) + " secondes"
				# on prévient qu'il y a encore un cooldown
				await ctx.message.reply(f"Il y a un cooldown, veuillez encore attendre {temps}", delete_after = 5)
				await ctx.message.delete(delay = 2)
				# on stop la fonction ici
				return
			# sinon si l'utilisateur a respecté le délai du daily_streak
			else:
				# on augmente son daily_streak de 1
				streak += 1
			# si son daily streak est supérieur
			if streak > best:
				# on sauvegarde le nouveau meilleur daily streak
				best = streak
				# on l'update
				self.eco.update_one({"id": user.id}, {"$set": {"best_daily_streak": best}})
			
			# on calcule la récompense
			daily = 90 + (streak * 10)

			# on update les données
			self.eco.update_one({"id": user.id}, {"$set": {"money": balance + daily}})
			self.eco.update_one({"id": user.id}, {"$set": {"daily_streak": streak}})
			self.eco.update_one({"id": user.id}, {"$set": {"last_daily": now}})

			# on prévient l'utilisateur qu'il a recu son daily streak
			embed=discord.Embed(title="__Daily reward__", description=f"Vous avez récupéré votre récompense de **{daily}€** et vous avez atteint un combo de **{streak} jours** d'affilés !", color=discord.Colour.green(),timestamp = datetime.utcnow())
			embed.add_field(name="__Meilleur combo__", value=f"Votre meilleur combo est de **{best} jours** d'affilés !", inline=False)
			embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
			await ctx.message.add_reaction("✅")
			await ctx.message.reply(embed=embed)
		else:
			# si la commande est désactivé, on fait un embed pour prévenir l'utilisateur
			embed=discord.Embed(title="__Commande désactivée !__", description="La commande **daily** est désactivé 😥", color=0xff1a1a,timestamp = datetime.utcnow())
			embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
			embed.add_field(name="__Comment la réactiver ?__", value="Il vous suffit d'aller dans le code du bot puis de mettre la valeur de **daily_activation** à True au lieu de False 😉", inline=False)
			embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
			# on ajoute une réaction au message de l'utilisateur
			await ctx.message.add_reaction("❌")
			# on envoit le embed
			await ctx.send(embed=embed, delete_after=10)
			await ctx.message.delete(delay = 2)
	
	@daily.error
	async def daily_error(self,ctx, error):
		# on crée l'erreur
		embed=discord.Embed(title="__ERREUR__", description="Il y a eu une erreur !", color=0xff1a1a,timestamp = datetime.utcnow())
		embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
		embed.add_field(name="__Besoin d'aide ?__", value="Utilisez la commande **"+self.prefix+"help daily **", inline=False)
		embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
		# on ajoute une réaction au message de l'utilisateur
		await ctx.message.add_reaction("❌")
		# on envoit le embed
		await ctx.send(embed=embed, delete_after=5)
		await ctx.message.delete(delay = 2)

	@discord.ext.commands.command(
		name="add_money",
		brief="Permet d'ajouter de l'argent à quelqu'un ! (nécéssite la permission de kick)",
		help="Permet d'ajouter de l'argent à quelqu'un ! (nécéssite la permission de kick)")
	@discord.ext.commands.has_permissions(kick_members=True)
	async def add_money(self,ctx,user: discord.Member, amount:int):
		# si la commande est activée
		if self.add_money_activation:
			
			# si la somme est négative ou nulle
			if amount <= 0:
				# on prévient que c'est impossible
				await ctx.message.reply("Il faut mettre une somme valide", delete_after = 5)	
				await ctx.message.delete(delay = 2)
				return

			# on stock le dictionnaire contenant les infos de l'utilisateur
			check = self.eco.find_one({"id": user.id})
			
			# si l'utilisateur n'a pas de compte
			if check is None:
				# on lui fait un compte
				create_eco(user,self.eco)
				check = self.eco.find_one({"id": user.id})
			
			balance = check["money"]

			# on met à jour son solde sur la database
			self.eco.update_one({"id": user.id}, {"$set": {"money": balance + amount}})
			
			# on envoie un message pour lui dire combien il a gagné
			embed = discord.Embed(
				title = "__Réussite__",
				description = f"Vous avez bien rajouté **{amount}€** sur le compte de {user.mention} !",
				color = discord.Colour.random(),timestamp = datetime.utcnow()
			)
			embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
			
			await ctx.message.reply(embed=embed)
			return
		else:
			# si la commande est désactivé, on fait un embed pour prévenir l'utilisateur
			embed=discord.Embed(title="__Commande désactivée !__", description="La commande **add_money** est désactivé 😥", color=0xff1a1a,timestamp = datetime.utcnow())
			embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
			embed.add_field(name="__Comment la réactiver ?__", value="Il vous suffit d'aller dans le code du bot puis de mettre la valeur de **add_money_activation** à True au lieu de False 😉", inline=False)
			embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
			# on ajoute une réaction au message de l'utilisateur
			await ctx.message.add_reaction("❌")
			# on envoit le embed
			await ctx.send(embed=embed, delete_after=10)
			await ctx.message.delete(delay = 2)
	@add_money.error
	async def add_money_error(self,ctx, error): 
		#on vérifie si c'est un manque de permission, si oui, on crée un embed
		if isinstance(error, discord.ext.commands.MissingPermissions):
			embed=discord.Embed(title="__ERREUR__", description="Vous avez besoin de la permission de **kick** afin d'ajouter de l'argent !", color=0xff1a1a,timestamp = datetime.utcnow())
		#sinon on vérifie si c'est un mauvais argument, si oui, on crée un embed
		elif isinstance(error, discord.ext.commands.BadArgument):
			embed=discord.Embed(title="__ERREUR__", description="Veuillez mettre un **utilisateur** valide !", color=0xff1a1a,timestamp = datetime.utcnow())
		#sinon on vérifie si c'est un manque d'argument, si oui, on crée un embed
		elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
			embed=discord.Embed(title="__ERREUR__", description="Veuillez mettre le **bon** nombre d'argument(s) !", color=0xff1a1a,timestamp = datetime.utcnow())
		else:
			embed=discord.Embed(title="__ERREUR__", description="Il y a eu une erreur !", color=0xff1a1a,timestamp = datetime.utcnow())
		embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
		embed.add_field(name="__Besoin d'aide ?__", value="Utilisez la commande **"+self.prefix+"help add_money **", inline=False)
		embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
		# on ajoute une réaction au message de l'utilisateur
		await ctx.message.add_reaction("❌")
		# on envoit le embed
		await ctx.send(embed=embed, delete_after=5)
		await ctx.message.delete(delay = 2)

	@discord.ext.commands.command(
		name="remove_money",
		brief="Permet de retirer de l'argent à quelqu'un ! (nécéssite la permission de kick)",
		help="Permet de retirer de l'argent à quelqu'un ! (nécéssite la permission de kick)")
	@discord.ext.commands.has_permissions(kick_members=True)
	async def remove_money(self,ctx,user: discord.Member, amount:int):
		# si la commande est activée
		if self.remove_money_activation:
			
			# on stock le dictionnaire contenant les infos de l'utilisateur
			check = self.eco.find_one({"id": user.id})
			
			# si l'utilisateur n'a pas de compte
			if check is None:
				# on lui fait un compte
				create_eco(user,self.eco)
				check = self.eco.find_one({"id": user.id})
			
			balance = check["money"]

			# si la somme finale est négative ou nulle
			if balance - amount < 0:
				# on prévient que c'est impossible
				await ctx.message.reply("L'utilisateur ne peut pas avoir un solde négatif !", delete_after = 5)	
				await ctx.message.delete(delay = 2)
				return

			# on met à jour son solde sur la database
			self.eco.update_one({"id": user.id}, {"$set": {"money": balance - amount}})
			
			# on envoie un message pour lui dire combien il a gagné
			embed = discord.Embed(
				title = "__Réussite__",
				description = f"Vous avez bien retiré **{amount}€** du compte de {user.mention} !",
				color = discord.Colour.random(),timestamp = datetime.utcnow()
			)
			embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
			await ctx.message.reply(embed=embed)
			return
		else:
			# si la commande est désactivé, on fait un embed pour prévenir l'utilisateur
			embed=discord.Embed(title="__Commande désactivée !__", description="La commande **remove_money** est désactivé 😥", color=0xff1a1a,timestamp = datetime.utcnow())
			embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
			embed.add_field(name="__Comment la réactiver ?__", value="Il vous suffit d'aller dans le code du bot puis de mettre la valeur de **remove_money_activation** à True au lieu de False 😉", inline=False)
			embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
			# on ajoute une réaction au message de l'utilisateur
			await ctx.message.add_reaction("❌")
			# on envoit le embed
			await ctx.send(embed=embed, delete_after=10)
			await ctx.message.delete(delay = 2)
	@remove_money.error
	async def remove_money_error(self,ctx, error): 
		#on vérifie si c'est un manque de permission, si oui, on crée un embed
		if isinstance(error, discord.ext.commands.MissingPermissions):
			embed=discord.Embed(title="__ERREUR__", description="Vous avez besoin de la permission de **kick** afin d'ajouter de l'argent !", color=0xff1a1a,timestamp = datetime.utcnow())
		#sinon on vérifie si c'est un mauvais argument, si oui, on crée un embed
		elif isinstance(error, discord.ext.commands.BadArgument):
			embed=discord.Embed(title="__ERREUR__", description="Veuillez mettre un **utilisateur** valide !", color=0xff1a1a,timestamp = datetime.utcnow())
		#sinon on vérifie si c'est un manque d'argument, si oui, on crée un embed
		elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
			embed=discord.Embed(title="__ERREUR__", description="Veuillez mettre le **bon** nombre d'argument(s) !", color=0xff1a1a,timestamp = datetime.utcnow())
		else:
			embed=discord.Embed(title="__ERREUR__", description="Il y a eu une erreur !", color=0xff1a1a,timestamp = datetime.utcnow())
		embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
		embed.add_field(name="__Besoin d'aide ?__", value="Utilisez la commande **"+self.prefix+"help remove_money **", inline=False)
		embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
		# on ajoute une réaction au message de l'utilisateur
		await ctx.message.add_reaction("❌")
		# on envoit le embed
		await ctx.send(embed=embed, delete_after=5)
		await ctx.message.delete(delay = 2)

	@discord.ext.commands.command(
		name="set_money",
		brief="Permet de définir le solde de quelqu'un ! (nécéssite la permission de kick)",
		help="Permet de définir le solde de quelqu'un ! (nécéssite la permission de kick)")
	@discord.ext.commands.has_permissions(kick_members=True)
	async def set_money(self,ctx,user: discord.Member, amount:int):
		# si la commande est activée
		if self.remove_money_activation:
			
			# on stock le dictionnaire contenant les infos de l'utilisateur
			check = self.eco.find_one({"id": user.id})
			
			# si l'utilisateur n'a pas de compte
			if check is None:
				# on lui fait un compte
				create_eco(user,self.eco)
				check = self.eco.find_one({"id": user.id})

			# si la somme finale est négative ou nulle
			if amount < 0:
				# on prévient que c'est impossible
				await ctx.message.reply("L'utilisateur ne peut pas avoir un solde négatif !", delete_after = 5)	
				await ctx.message.delete(delay = 2)
				return

			# on met à jour son solde sur la database
			self.eco.update_one({"id": user.id}, {"$set": {"money": amount}})
			
			# on envoie un message pour lui dire combien il a gagné
			embed = discord.Embed(
				title = "__Réussite__",
				description = f"Vous avez bien définit à **{amount}€** le solde de {user.mention} !",
				color = discord.Colour.random(),timestamp = datetime.utcnow()
			)
			embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
			await ctx.message.reply(embed=embed)
			return
		else:
			# si la commande est désactivé, on fait un embed pour prévenir l'utilisateur
			embed=discord.Embed(title="__Commande désactivée !__", description="La commande **set_money** est désactivé 😥", color=0xff1a1a,timestamp = datetime.utcnow())
			embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
			embed.add_field(name="__Comment la réactiver ?__", value="Il vous suffit d'aller dans le code du bot puis de mettre la valeur de **set_money_activation** à True au lieu de False 😉", inline=False)
			embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
			# on ajoute une réaction au message de l'utilisateur
			await ctx.message.add_reaction("❌")
			# on envoit le embed
			await ctx.send(embed=embed, delete_after=10)
			await ctx.message.delete(delay = 2)
	@set_money.error
	async def set_money_error(self,ctx, error): 
		#on vérifie si c'est un manque de permission, si oui, on crée un embed
		if isinstance(error, discord.ext.commands.MissingPermissions):
			embed=discord.Embed(title="__ERREUR__", description="Vous avez besoin de la permission de **kick** afin d'ajouter de l'argent !", color=0xff1a1a,timestamp = datetime.utcnow())
		#sinon on vérifie si c'est un mauvais argument, si oui, on crée un embed
		elif isinstance(error, discord.ext.commands.BadArgument):
			embed=discord.Embed(title="__ERREUR__", description="Veuillez mettre un **utilisateur** valide !", color=0xff1a1a,timestamp = datetime.utcnow())
		#sinon on vérifie si c'est un manque d'argument, si oui, on crée un embed
		elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
			embed=discord.Embed(title="__ERREUR__", description="Veuillez mettre le **bon** nombre d'argument(s) !", color=0xff1a1a,timestamp = datetime.utcnow())
		else:
			embed=discord.Embed(title="__ERREUR__", description="Il y a eu une erreur !", color=0xff1a1a,timestamp = datetime.utcnow())
		embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
		embed.add_field(name="__Besoin d'aide ?__", value="Utilisez la commande **"+self.prefix+"help set_money **", inline=False)
		embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
		# on ajoute une réaction au message de l'utilisateur
		await ctx.message.add_reaction("❌")
		# on envoit le embed
		await ctx.send(embed=embed, delete_after=5)
		await ctx.message.delete(delay = 2)

	@discord.ext.commands.command(
		name="get_all_data",
		brief="Permet de récupérer toutes les informations de quelqu'un ! (nécéssite la permission de kick)",
		help="Permet de récupérer toutes les informations de quelqu'un ! (nécéssite la permission de kick)")
	@discord.ext.commands.has_permissions(kick_members=True)
	async def get_all_data(self,ctx,user: discord.Member):
		# si la commande est activée
		if self.get_all_data_activation:
			
			# on stock le dictionnaire contenant les infos de l'utilisateur
			check = self.eco.find_one({"id": user.id})
			
			# si l'utilisateur n'a pas de compte
			if check is None:
				# on lui fait un compte
				create_eco(user,self.eco)
				check = self.eco.find_one({"id": user.id})

			embed = discord.Embed(
				title = f"__Information de {user}__",
				color = discord.Colour.random(),timestamp = datetime.utcnow()
			)
			embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)

			for elt in check:
				embed.add_field(name=f"**{elt}**", value=check[elt], inline=False)
			
			await ctx.message.reply(embed=embed)
			return
		else:
			# si la commande est désactivé, on fait un embed pour prévenir l'utilisateur
			embed=discord.Embed(title="__Commande désactivée !__", description="La commande **get_all_data** est désactivé 😥", color=0xff1a1a,timestamp = datetime.utcnow())
			embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
			embed.add_field(name="__Comment la réactiver ?__", value="Il vous suffit d'aller dans le code du bot puis de mettre la valeur de **get_all_data_activation** à True au lieu de False 😉", inline=False)
			embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
			# on ajoute une réaction au message de l'utilisateur
			await ctx.message.add_reaction("❌")
			# on envoit le embed
			await ctx.send(embed=embed, delete_after=10)
			await ctx.message.delete(delay = 2)
	
	@get_all_data.error
	async def get_all_data_error(self,ctx, error): 
		#on vérifie si c'est un manque de permission, si oui, on crée un embed
		if isinstance(error, discord.ext.commands.MissingPermissions):
			embed=discord.Embed(title="__ERREUR__", description="Vous avez besoin de la permission de **kick** afin d'ajouter de l'argent !", color=0xff1a1a,timestamp = datetime.utcnow())
		#sinon on vérifie si c'est un mauvais argument, si oui, on crée un embed
		elif isinstance(error, discord.ext.commands.BadArgument):
			embed=discord.Embed(title="__ERREUR__", description="Veuillez mettre un **utilisateur** valide !", color=0xff1a1a,timestamp = datetime.utcnow())
		#sinon on vérifie si c'est un manque d'argument, si oui, on crée un embed
		elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
			embed=discord.Embed(title="__ERREUR__", description="Veuillez mettre le **bon** nombre d'argument(s) !", color=0xff1a1a,timestamp = datetime.utcnow())
		else:
			embed=discord.Embed(title="__ERREUR__", description="Il y a eu une erreur !", color=0xff1a1a,timestamp = datetime.utcnow())
		embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
		embed.add_field(name="__Besoin d'aide ?__", value="Utilisez la commande **"+self.prefix+"help get_all_data **", inline=False)
		embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
		# on ajoute une réaction au message de l'utilisateur
		await ctx.message.add_reaction("❌")
		# on envoit le embed
		await ctx.send(embed=embed, delete_after=5)
		await ctx.message.delete(delay = 2)

	@discord.ext.commands.command(
		name="reset_user_data",
		brief="Permet de reset toutes les informations de quelqu'un ! (nécéssite la permission de kick)",
		help="Permet de reset toutes les informations de quelqu'un ! (nécéssite la permission de kick)")
	@discord.ext.commands.has_permissions(kick_members=True)
	async def reset_user_data(self,ctx,user: discord.Member):
		# si la commande est activée
		if self.reset_user_data_activation:
			
			# on stock le dictionnaire contenant les infos de l'utilisateur
			check = self.eco.find_one({"id": user.id})
			
			# si l'utilisateur n'a pas de compte
			if check is not None:
				# on lui fait un compte
				self.eco.delete_one({"id": user.id})

			create_eco(user,self.eco)

			embed = discord.Embed(
				title = f"__Reset de {user}__",description=f"Le compte de {user.mention} a bien été reset",
				color = discord.Colour.random(),timestamp = datetime.utcnow()
			)
			embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
			
			await ctx.message.reply(embed=embed)
			return
		else:
			# si la commande est désactivé, on fait un embed pour prévenir l'utilisateur
			embed=discord.Embed(title="__Commande désactivée !__", description="La commande **reset_user_data** est désactivé 😥", color=0xff1a1a,timestamp = datetime.utcnow())
			embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
			embed.add_field(name="__Comment la réactiver ?__", value="Il vous suffit d'aller dans le code du bot puis de mettre la valeur de **reset_user_data_activation** à True au lieu de False 😉", inline=False)
			embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
			# on ajoute une réaction au message de l'utilisateur
			await ctx.message.add_reaction("❌")
			# on envoit le embed
			await ctx.send(embed=embed, delete_after=10)
			await ctx.message.delete(delay = 2)
	
	@reset_user_data.error
	async def reset_user_data_error(self,ctx, error): 
		#on vérifie si c'est un manque de permission, si oui, on crée un embed
		if isinstance(error, discord.ext.commands.MissingPermissions):
			embed=discord.Embed(title="__ERREUR__", description="Vous avez besoin de la permission de **kick** afin d'ajouter de l'argent !", color=0xff1a1a,timestamp = datetime.utcnow())
		#sinon on vérifie si c'est un mauvais argument, si oui, on crée un embed
		elif isinstance(error, discord.ext.commands.BadArgument):
			embed=discord.Embed(title="__ERREUR__", description="Veuillez mettre un **utilisateur** valide !", color=0xff1a1a,timestamp = datetime.utcnow())
		#sinon on vérifie si c'est un manque d'argument, si oui, on crée un embed
		elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
			embed=discord.Embed(title="__ERREUR__", description="Veuillez mettre le **bon** nombre d'argument(s) !", color=0xff1a1a,timestamp = datetime.utcnow())
		else:
			embed=discord.Embed(title="__ERREUR__", description="Il y a eu une erreur !", color=0xff1a1a,timestamp = datetime.utcnow())
		embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
		embed.add_field(name="__Besoin d'aide ?__", value="Utilisez la commande **"+self.prefix+"help reset_user_data **", inline=False)
		embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
		# on ajoute une réaction au message de l'utilisateur
		await ctx.message.add_reaction("❌")
		# on envoit le embed
		await ctx.send(embed=embed, delete_after=5)
		await ctx.message.delete(delay = 2)
	
	@discord.ext.commands.command(
		name="coinflip",
		brief="Permet de parier une somme sur un lancer de pièce, si la pièce tombe sur la face choisis, tu double l'argent parié !",
		help="Permet de parier une somme sur un lancer de pièce, si la pièce tombe sur la face choisis, tu double l'argent parié ! (arg = 'face' ou 'pile')")
	async def coinflip(self,ctx, amount: int, arg: str):
		if self.coinflip_activation:
			arg = arg.lower()
			random_arg = random.choice(["pile", "face"])
			
			if amount <= 0:
				# on prévient que c'est impossible
				await ctx.message.reply("Il faut mettre une somme valide")
				return

			user = ctx.author

			check = self.eco.find_one({"id": user.id})
			
			# si l'utilisateur n'a pas de compte
			if check is None:
				# on lui fait un compte
				create_eco(user,self.eco)
				check = self.eco.find_one({"id": user.id})

			embed = discord.Embed(
				colour=discord.Color.from_rgb(244, 182, 89),timestamp = datetime.utcnow()
			)

			if arg not in ["pile", "face"]:
				await ctx.message.reply("Il faut mettre un **argument** valide (**face** ou **pile**)",delete_after = 5)
				await ctx.message.delete(delay = 2)
				return

			balance = check['money']
			if balance >= amount:
				if arg == random_arg:
					self.eco.update_one({"id": user.id}, {"$set": {"money": balance + amount}})

					embed.add_field(name="Coinflip", value=f"Tu as **gagné** le coinflip ! \n\nTu as doublé ta mise de **{amount}€**")
					embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
					await ctx.message.reply(embed=embed)
				else:
					self.eco.update_one({"id": user.id}, {"$set": {"money": balance - amount}})

					embed.add_field(name="Coinflip", value=f"Tu as **perdu** le coinflip ! \n\nTu as perdu ta mise de **{amount}€**")
					embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
					await ctx.message.reply(embed=embed)
			else:
				await ctx.message.reply("Vous n'avez pas assez d'argent ",delete_after=5)
				await ctx.message.delete(delay = 2)
		else:
			# si la commande est désactivé, on fait un embed pour prévenir l'utilisateur
			embed=discord.Embed(title="__Commande désactivée !__", description="La commande **coinflip** est désactivé 😥", color=0xff1a1a,timestamp = datetime.utcnow())
			embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
			embed.add_field(name="__Comment la réactiver ?__", value="Il vous suffit d'aller dans le code du bot puis de mettre la valeur de **coinflip_activation** à True au lieu de False 😉", inline=False)
			embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
			# on ajoute une réaction au message de l'utilisateur
			await ctx.message.add_reaction("❌")
			# on envoit le embed
			await ctx.send(embed=embed, delete_after=10)
			await ctx.message.delete(delay = 2)
	
	@coinflip.error
	async def coinflip_error(self,ctx, error): 
		#on vérifie si c'est un mauvais argument, si oui, on crée un embed
		if isinstance(error, discord.ext.commands.BadArgument):
			embed=discord.Embed(title="__ERREUR__", description="Veuillez mettre une **somme** valide !", color=0xff1a1a,timestamp = datetime.utcnow())
		#sinon on vérifie si c'est un manque d'argument, si oui, on crée un embed
		elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
			embed=discord.Embed(title="__ERREUR__", description="Veuillez mettre le **bon** nombre d'argument(s) !", color=0xff1a1a,timestamp = datetime.utcnow())
		else:
			embed=discord.Embed(title="__ERREUR__", description="Il y a eu une erreur !", color=0xff1a1a,timestamp = datetime.utcnow())
		embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
		embed.add_field(name="__Besoin d'aide ?__", value="Utilisez la commande **"+self.prefix+"help coinflip **", inline=False)
		embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
		# on ajoute une réaction au message de l'utilisateur
		await ctx.message.add_reaction("❌")
		# on envoit le embed
		await ctx.send(embed=embed, delete_after=5)
		await ctx.message.delete(delay = 2)
	

	@discord.ext.commands.command(
		name="reward",
		brief="Permet de gagner de l'argent toutes les heures !",
		help="Permet de gagner de l'argent toutes les heures !") 
	@discord.ext.commands.cooldown(1, 3600, discord.ext.commands.BucketType.user)
	async def reward(self,ctx):
		if self.reward_activation:
			# on récupère l'utilisateur
			user = ctx.author

			# on stock le dictionnaire contenant les infos de l'utilisateur
			check = self.eco.find_one({"id": user.id})
			
			# si l'utilisateur n'a pas de compte
			if check is None:
				# on lui en fait un
				create_eco(user,self.eco)
				check = self.eco.find_one({"id": user.id})
			
			# on récupère son solde
			balance = check['money']

			# on update les données
			self.eco.update_one({"id": user.id}, {"$set": {"money": balance + 50}})

			# on prévient l'utilisateur qu'il a recu son daily streak
			embed=discord.Embed(title="__Reward__", description=f"Vous avez récupéré votre récompense de **50€** ! \n\n Revenez dans 1h afin de récupérer une nouvelle récompense", color=discord.Colour.green(),timestamp = datetime.utcnow())
			embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
			await ctx.message.add_reaction("✅")
			await ctx.message.reply(embed=embed)
		else:
			# si la commande est désactivé, on fait un embed pour prévenir l'utilisateur
			embed=discord.Embed(title="__Commande désactivée !__", description="La commande **reward** est désactivé 😥", color=0xff1a1a,timestamp = datetime.utcnow())
			embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
			embed.add_field(name="__Comment la réactiver ?__", value="Il vous suffit d'aller dans le code du bot puis de mettre la valeur de **reward_activation** à True au lieu de False 😉", inline=False)
			embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
			# on ajoute une réaction au message de l'utilisateur
			await ctx.message.add_reaction("❌")
			# on envoit le embed
			await ctx.send(embed=embed, delete_after=10)
			await ctx.message.delete(delay = 2)
	
	@reward.error
	async def reward_error(self,ctx, error):
		if isinstance(error, discord.ext.commands.CommandOnCooldown):
			temps = error.retry_after
			if(temps/60 <60 and temps/60>=1):
					temps = str(int(temps/60)) + " minutes et " + str(int(temps%60)) + " secondes"
			else:
				# sinon c'est un temps en seconde, on le convertit
				temps =  str(int(temps)) + " secondes"
			# on prévient qu'il y a encore un cooldown
			await ctx.message.reply(f"Il y a un cooldown, veuillez encore attendre {temps}", delete_after = 5)
			await ctx.message.delete(delay = 2)
		else:
			# on crée l'erreur
			embed=discord.Embed(title="__ERREUR__", description="Il y a eu une erreur !", color=0xff1a1a,timestamp = datetime.utcnow())
		embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
		embed.add_field(name="__Besoin d'aide ?__", value="Utilisez la commande **"+self.prefix+"help reward **", inline=False)
		embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
		# on ajoute une réaction au message de l'utilisateur
		await ctx.message.add_reaction("❌")
		# on envoit le embed
		await ctx.send(embed=embed, delete_after=5)
		await ctx.message.delete(delay = 2)

	@discord.ext.commands.command(
		name="slots",
		brief="Ceci est une machine à sous, vous pouvre gagner plus ou moins d'argent !",
		help="Ceci est une machine à sous, vous pouvre gagner plus ou moins d'argent !") 
	async def slots(self, ctx, money: int):
		if self.slots_activation:
			user = ctx.author
			
			random_slots_data = ["", "", "",
								"", "", "",
								"", "", ""]

			for i in range(len(random_slots_data)):
				random_slots_data[i] = random.choice([":tada:", ":cookie:", ":large_blue_diamond:",":money_with_wings:", ":moneybag:", ":cherries:"])
			

			check = self.eco.find_one({"id": user.id})

			# si l'utilisateur n'a pas de compte
			if check is None:
				# on lui en fait un
				create_eco(user,self.eco)
				check = self.eco.find_one({"id": user.id})
				
			# on récupère son solde
			balance = check['money']
			
			#r = await economy.get_user(ctx.message.author.id)
			embed = discord.Embed()

			if balance >= money:

				embed = discord.Embed(title="Slots", description=f"""{random_slots_data[0]} | {random_slots_data[1]} | {random_slots_data[2]}
				{random_slots_data[3]} | {random_slots_data[4]} | {random_slots_data[5]}
				{random_slots_data[6]} | {random_slots_data[7]} | {random_slots_data[8]}""",colour=discord.Color.from_rgb(244, 182, 89),timestamp = datetime.utcnow())

				embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)

				embed.add_field(name = "Récompense",value=":tada: -> x2\n:cookie: -> x2\n:large_blue_diamond: -> x2\n:money_with_wings: -> x2\n:moneybag: -> x2\n:cherries: -> x2",inline = False)

				if random_slots_data[3] == random_slots_data[4] and random_slots_data[5] == random_slots_data[3]:
					#await economy.add_money(ctx.message.author.id, "bank", money_multi)
					embed.add_field(name="Tu as gagné",value=f"{random_slots_data[3]} -> 15$ x2",inline = False)
				else:
					#await economy.remove_money(ctx.message.author.id, "bank", money)
					embed.add_field(name="Tu as perdu",value=f"{random_slots_data[3]} -> 15$ x2",inline = False)

				await ctx.message.reply(embed=embed)

			else:
				await ctx.message.reply("Vous n'avez pas assez d'argent ",delete_after=5)
				await ctx.message.delete(delay = 2)
		else:
			# si la commande est désactivé, on fait un embed pour prévenir l'utilisateur
			embed=discord.Embed(title="__Commande désactivée !__", description="La commande **slots** est désactivé 😥", color=0xff1a1a,timestamp = datetime.utcnow())
			embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
			embed.add_field(name="__Comment la réactiver ?__", value="Il vous suffit d'aller dans le code du bot puis de mettre la valeur de **slots_activation** à True au lieu de False 😉", inline=False)
			embed.set_footer(text="Commande demandé par : " + ctx.author.display_name, icon_url=ctx.message.author.avatar_url)
			# on ajoute une réaction au message de l'utilisateur
			await ctx.message.add_reaction("❌")
			# on envoit le embed
			await ctx.send(embed=embed, delete_after=10)
			await ctx.message.delete(delay = 2)