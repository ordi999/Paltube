import discord
from datetime import datetime, timedelta
import random

# fonction pour créer un compte
def create_eco(user, eco):
	# on regarde si un compte est déjà éxistant
	check = eco.find_one({"id" : user.id})
	if check == None:
		#s'il n'y a pas de compte on lui en cré un
		insert = {
			"id": user.id,
			"name": user.name,
			"tags": user.discriminator,
			"money": 10,
			"daily_streak": 0,
			"last_daily": datetime.fromtimestamp(float(str(datetime.now().timestamp()))),
			"best_daily_streak":0
		}
		eco.insert_one(insert)


# Catégories économie
class Economy(discord.ext.commands.Cog):
	""" Toutes les commandes en rapport avec l'économie """
	# permet de récupérer les informations utile pour les commandes
	def __init__(self,bot,eco,prefix,bal_activation, work_activation,pay_activation,bet_activation):
		self.bot = bot
		self.eco = eco
		self.prefix = prefix
		self.bal_activation = bal_activation
		self.work_activation = work_activation
		self.pay_activation = pay_activation
		self.bet_activation = bet_activation
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
				embed.set_footer(text="Commande demandée par : " + ctx.author.display_name)
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
				embed.set_footer(text="Commande demandée par : " + ctx.author.display_name)
				await ctx.message.reply(embed=embed)
				return
		else:
			# si la commande est désactivé, on fait un embed pour prévenir l'utilisateur
			embed=discord.Embed(title="__Commande désactivée !__", description="La commande **bal** est désactivé 😥", color=0xff1a1a,timestamp = datetime.utcnow())
			embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
			embed.add_field(name="__Comment la réactiver ?__", value="Il vous suffit d'aller dans le code du bot puis de mettre la valeur de **bal_activation** à True au lieu de False 😉", inline=False)
			embed.set_footer(text="Commande demandée par : " + ctx.author.display_name)
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
		embed.set_footer(text="Commande demandée par : " + ctx.author.display_name)
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
			embed.set_footer(text="Commande demandée par : " + ctx.author.display_name)
			await ctx.message.reply(embed=embed)
			return
		else:
			# si la commande est désactivé, on fait un embed pour prévenir l'utilisateur
			embed=discord.Embed(title="__Commande désactivée !__", description="La commande **work** est désactivé 😥", color=0xff1a1a,timestamp = datetime.utcnow())
			embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
			embed.add_field(name="__Comment la réactiver ?__", value="Il vous suffit d'aller dans le code du bot puis de mettre la valeur de **work_activation** à True au lieu de False 😉", inline=False)
			embed.set_footer(text="Commande demandée par : " + ctx.author.display_name)
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
		embed.set_footer(text="Commande demandée par : " + ctx.author.display_name)
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
				await ctx.message.reply("Tu ne peux pas te donner de l'argent à toi-même")
				return
			# si la somme est négative ou nulle
			if amount <= 0:
				# on prévient que c'est impossible
				await ctx.message.reply("Il faut mettre une somme valide")
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
				em = discord.Embed(
					title = "Paiement réussi 🤑",
					description = f"Vous avez donné **{amount}€** à **{user.mention}** !  🎉",
					color = discord.Colour.random())
				await ctx.message.reply(embed=em)
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
			embed.set_footer(text="Commande demandée par : " + ctx.author.display_name)
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
		embed.set_footer(text="Commande demandée par : " + ctx.author.display_name)
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
			embed.set_footer(text="Commande demandée par : " + ctx.author.display_name)
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
		embed.set_footer(text="Commande demandée par : " + ctx.author.display_name)
		# on ajoute une réaction au message de l'utilisateur
		await ctx.message.add_reaction("❌")
		# on envoit le embed
		await ctx.send(embed=embed, delete_after=5)
		await ctx.message.delete(delay = 2)

	@discord.ext.commands.command(
		name="daily",
		brief="Permet de gagner de l'argent tous les jours, si vous l'utilisez plusieurs jours consécutif, vous gagnerez plus d'argent !",
		help="Permet de gagner de l'argent tous les jours, si vous l'utilisez plusieurs jours consécutif, vous gagnerez plus d'argent !") 
	@discord.ext.commands.cooldown(1, 60*60*24, discord.ext.commands.BucketType.user)
	async def daily(self,ctx):
		user = ctx.author

		# on stock le dictionnaire contenant les infos de l'utilisateur
		check = self.eco.find_one({"id": user.id})
		


		# si l'utilisateur n'a pas de compte
		if check is None:
			# on lui en fait un
			create_eco(user,self.eco)
			check = self.eco.find_one({"id": user.id})
		
		balance = check['money']

		streak = check["daily_streak"]
		last_daily = check["last_daily"]
		best = check["best_daily_streak"]

		now = datetime.fromtimestamp(float(str(datetime.now().timestamp())))
		if now-last_daily > timedelta(hours=48):
			streak = 1
		else:
			streak += 1
		if streak > best:
			best = streak
			self.eco.update_one({"id": user.id}, {"$set": {"best_daily_streak": best}})
		daily = 45 + (streak * 5)

		self.eco.update_one({"id": user.id}, {"$set": {"money": balance + daily}})
		self.eco.update_one({"id": user.id}, {"$set": {"daily_streak": streak}})
		self.eco.update_one({"id": user.id}, {"$set": {"last_daily": now}})

		embed=discord.Embed(title="__Daily reward__", description=f"Vous avez récupéré votre récompense de **{daily}€** et vous avez atteint un combo de **{streak} jours** d'affilés !", color=discord.Colour.green(),timestamp = datetime.utcnow())
		embed.add_field(name="__Meilleur combo__", value=f"Votre meilleur combo est de **{best} jours** d'affilés !", inline=False)
		embed.set_footer(text="Commande demandée par : " + ctx.author.display_name)
		await ctx.message.add_reaction("✅")
		await ctx.message.reply(embed=embed)
	
	@daily.error
	async def daily_error(self,ctx, error):
		# si c'est à cause du cooldown
		if isinstance(error, discord.ext.commands.CommandOnCooldown):
			temps = int(error.retry_after)
			if(temps/3600 <=24 and temps/3600>=1):
				temps = str(int(temps/3600)) + " heures et " + str(int((temps%3600)/60)) + " minutes"
			elif(temps/60 <60 and temps/60>=1):
				temps = str(int(temps/60)) + " minutes et " + str(int(temps%60)) + " secondes"
			else:
				temps =  str(int(temps)) + " secondes"
			await ctx.message.reply(f"Il y a un cooldown, veuillez encore attendre {temps}", delete_after = 5)
			await ctx.message.delete(delay = 2)
			return
		else:
			embed=discord.Embed(title="__ERREUR__", description="Il y a eu une erreur !", color=0xff1a1a,timestamp = datetime.utcnow())
		embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/1/1c/No-Symbol.png")
		embed.add_field(name="__Besoin d'aide ?__", value="Utilisez la commande **"+self.prefix+"help work **", inline=False)
		embed.set_footer(text="Commande demandée par : " + ctx.author.display_name)
		# on ajoute une réaction au message de l'utilisateur
		await ctx.message.add_reaction("❌")
		# on envoit le embed
		await ctx.send(embed=embed, delete_after=5)
		await ctx.message.delete(delay = 2)