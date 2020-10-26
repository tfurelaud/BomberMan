#################################################
#---------- COMMENT LANCER NOTRE JEU? ----------#
#################################################

Côté serveur :
 - Pour lancer un serveur écrire :
./bomber_server.py <port utilisé> <maps>
(ex: <port> = 7777 et <map> = maps/map0)

Si une erreur de permission vous empêche de lancer le serveur, lancer cette commande:
chmod a+x bomber_server.py


Côté client :
 - Pour se connecter à un serveur sur la même machine taper :
./bomber_client.py localhost <port> <nickname>
(ex: <port> = 7777 et <nickname> = player1)

	      - Pour se connecter sur une autre machine taper :
./bomber_client.py <adresseIP> <port>

Si une erreur de permission vous empêche de lancer le serveur, lancer cette commande:
chmod a+x bomber_client.py

##################################################
#---------- COMMENT JOUER À NOTRE JEU? ----------#
##################################################

- Pour se déplacer, utilisez les flèches directionnelles du clavier.
- Pour lâcher des bombes, utilisez espace.
- Pour se déconnecter du serveur et quitter le jeu, appuyez sur la touche 'Échap' ou sur la croix de fermeture.
- Pour ferme le serveur, appuyez sur 'Ctrl' + 'C' sur le terminal du serveur.
- Pour tuer un adversaire il faut que ses points de vie soient à 0. Chacun des joueurs perd 10 points de vie quand il est dans l'explosion d'une bombe et en gagne 10 quand il mange un fruit. Chaque joueur apparait avec un total de 50 points de vie.
- Attention lorsque vous quittez le jeu, votre statut de jeu(point de vie, position,...) est effacé, car quitter est considéré comme un abandon.

