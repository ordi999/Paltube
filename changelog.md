# Changelog

## [Futur Changement]
Voir commande -commands du bot

## 2022-02-07
### Ajout
- commande remove_money : Permet aux utilisateurs possédant la permission de kick de retirer de l'argent au solde de quelqu'un
- commande set_money : Permet aux utilisateurs possédant la permission de kick de définir le solde de quelqu'un
- commande get_all_data : Permet aux utilisateurs possédant la permission de kick de savoir toutes les informations contenu dans la base de données à propos de quelqu'un
- commande reset_user_account : Permet aux utilisateurs possédant la permission de kick de reset le compte de quelqu'un

## 2022-02-06
### Ajout
- Commande add_money : Permet aux utilisateurs possédant la permission de kick d'ajouter de l'argent au solde de quelqu'un

## 2022-02-04
### Ajout
- commande bug : permet de report un bug au dev
### Changement
- supression du cooldown de discord pour la commande daily (quand on redémarait le bot, le cooldown était reset)
- remplacement du cooldown de discord par mon propre cooldown (commande daily)

## 2022-02-03
### Ajout
- commande daily : permet de récupérer de l'argent chaque jours (augmente en fonction du nombre de jours consécutifs) avec un cooldown de 24H
### Changement
- Supression de la commande create
- création automatique d'un compte sur la base de donnée eco si l'utilisateur n'a pas de compte

## 2022-02-02
### Ajout
- Ajout des cogs
- Création du fichier autres.py qui contient les autres commandes(commands)
- Création du fichier economy.py qui contient les commandes en rapport avec l'économie (create/work/bal/pay/bet)
- Création du fichier fun.py qui contient les commandes fun (dice : à ajouter une fois finit)
- Création du fichier moderation.py qui contient les commandes de modération (kick/delete)
- Création du fichier zone_de_test.py qui contient les commandes en test (dice)
### Changement
- Ajout d'une supression automatique aux embeds
- Amélioration des commande work/pat/create/bal/bet : ajout de la gestion des erreurs (et mise en place du message pour prévenir du cooldown) / ajout de la possibilité d'activé/désactivé ces commandes
### Importation
- Importation des fichiers Cogs (moderation.py/autres.py/economy.py/fun.py/zone_de_test.py)

## 2022-01-31
### Changement
- amélioration de la commande bet : elle permet maintenant d'obtenir des gains 1 fois sur 5. les gains sont variables

## 2022-01-30
### Ajout
- mise en place de la base de donnée MongoDB
- Commande : create (permet de se créer un compte dans la database) / A améliorer
- Commande : bal (permet de savoir la quantité d'argent dans son compte) / A améliorer
- Commande : work (permet de travailler afin de gagner de l'argent/ Il y a un cooldown de 10 secondes) / A améliorer
- Commande : pay (permet de payer un utilisateur ayant un compte)/ A améliorer
- Commande : bet (permet de parier de l'argent avec une chance de 2% de faire *50 sa mise)/ A améliorer
### Importation
- import pymongo : Pour la base de donnée

## 2022-01-29
### Ajout
- Commande help
### Changement
- Ajout d'un footer et de l'heure d'utilisation aux embeds
### Importation
- from pretty_help import DefaultMenu, PrettyHelp : Pour la commande help
- from datetime import datetime : pour l'heure d'utilisation dans les embeds

## 2022-01-28
### Ajout
- Commande : del (Permet de supprimer des messages si cela est possible)
- Command dice(pour faire lancer des dés) / Il manque encore le dice.error ainsi que plusieurs fonctionalitées
### Importation
- import random : Pour générer des nombres aléatoirement

## 2022-01-27
### Ajout
- Mise en place du changelog
- Mise en place du changement de status automatique
- Commande : commands (permet d'afficher la liste des commandes faites et à faires)
- Commande : kick (Permet de kick un membre du discord si cela est possible)
### Importation
- from itertools import cycle : Pour le changement de status automatique
- from discord.ext import tasks : Pour le changement de status automatique

## 2022-01-26
### Ajout
- Création du projet
- Ajout du fichier keep_alive.py et mise en place de l'host H24
- Token du bot mis dans environement secret pour les variables
- mise en place du message quand le bot est prêt : on_ready
### Importation
- from keep_alive import keep_alive : Pour l'host H24
- import discord : Pour le bot
- from discord.ext import commands : pour le bot
- import os : pour le lancement du bot