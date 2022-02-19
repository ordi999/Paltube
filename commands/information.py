import discord

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