from datetime import datetime, timedelta

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
			"last_daily": datetime.fromtimestamp(float(str(datetime.now().timestamp()))) - timedelta(days = 1),
			"best_daily_streak":0
		}
		eco.insert_one(insert)