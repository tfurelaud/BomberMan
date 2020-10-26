# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

from model import *

import socket
import select
import threading
import pickle
import errno

################################################################################
#                          NETWORK SERVER CONTROLLER                           #
################################################################################

class NetworkServerController:

    def __init__(self, model, port):
        self.model = model
        self.port = port
        self.s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('', port))
        self.s.listen(1)
        self.l = []
        self.player_dictionnaire = {}
        self.modif = False
        threading.Thread(None, self.connect_new_player, None, ()).start()
        self.new_socket = None
        self.crashed_player_dictionnaire = {}
        self.disconnected_player = []

    #connect_new_player nous permet d'attribuer un thread à chaque nouvelle connection accepté
    def connect_new_player(self):
        while(True):
            new_socket, addr = self.s.accept()
            threading.Thread(None, self.gestion_message, None, (new_socket,)).start()

    #gestion_message nous permet de gerer les requêtes envoyés par les clients
    def gestion_message(self, socket):
        while True :
            try:
                message = socket.recv(150)
                if message != b'' and message != b'\n' and message != b' ':

                    #On décode le message
                    message_decode = message.decode()

                    #On split le message en tableau de mot: mot 0 = keyword, mot 1 = pseudo, mot 2 uniquement pour la direction si keymord = DIR
                    message_split = message_decode.split(" ")

                    #Si c'est un nouveau joueur <pseudo>, le client envoi comme message "new_player <pseudo>"
                    if message_split[0] == "new_player":
                        print("Player Connected: " + message_split[1] + "\n")
                        self.player_in_game = message_split[1]
                        self.model.add_character(message_split[1], True)
                        self.player_dictionnaire[message_split[1]] = [socket]
                        map = pickle.dumps([self.model.map.array, self.model.map.width, self.model.map.height])
                        socket.sendall(map)
                        obj = pickle.dumps(self.model.fruits)
                        socket.sendall(obj)
                        obj = pickle.dumps(self.model.characters)
                        socket.sendall(obj)
                        print("Map info send to " + message_split[1] + "\n")
                        self.modif = True

                    #Si un joueur <pseudo> quitte, le client envoi comme  message "QUIT <pseudo>"
                    if message_split[0] =="QUIT":
                        print("Player " + message_split[1] + " leave the game")
                        self.model.kill_character(message_split[1])
                        self.disconnected_player = self.disconnected_player + [message_split[1]]
                        self.modif= True
                        socket.close()

                    #Si un joueur <pseudo> bouge, le client envoi comme  message "DIR <pseudo> <direction>"
                    if message_split[0] == "DIR":
                        self.model.move_character(message_split[1], int(message_split[2]))
                        self.modif = True

                    #Si un joueur <pseudo> drop une bombe, le client envoi comme  message "DROP <pseudo>"
                    if message_split[0] == "DROP":
                        self.model.drop_bomb(message_split[1])
                        self.modif = True
                else:
                    socket.close()
            except:
                socket.close()

    #gestion_event est en charge de s'occuper de l'envoi de mise a jour concernant la map lorsqu'une modification est faite sur celle-ci
    def gestion_event(self):
        socket_delete = None
        #Pour chaque socket, on envoi la MAJ
        for cle in self.player_dictionnaire:
            sockett = self.player_dictionnaire[cle][0]
            try:
                obj = pickle.dumps([self.model.fruits, self.model.characters, self.model.bombs])
                sockett.sendall(obj)
            #Si il n'arrive pas à l'envoyer, alors c'est que le joueur à crash ou s'est déconnecté.
            except:
                #Es ce que le joueur s'est déconnecté proprement ou a-t-il crash?
                disconnected = False
                for x in self.disconnected_player:
                    if x == cle:
                        disconnected = True
                if disconnected == False:
                    print("Player " + cle + " just crash. Waiting for reconnection...")
                    self.model.kill_character(cle)
                    socket_delete = sockett
                    sockett.close()
        if socket_delete != None:
            del self.player_dictionnaire[cle]

    # time event

    def tick(self, dt):
        #On vérifie si il y a eu un event pour pouvoir modifier la map et envoyer la modification à tout le monde. Sinon, on ne fait rien?
        if self.modif == True:
            self.gestion_event()
            self.modif = False
        return True

################################################################################
#                          NETWORK CLIENT CONTROLLER                           #
################################################################################

class NetworkClientController:

    def __init__(self, model, host, port, nickname):
        self.model = model
        self.host = host
        self.port = port
        self.nickname = nickname
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        #Arrivons nous à nous connecter au serveur?
        try:
            self.s.connect((self.host, self.port))
            self.connect=True
            print("\nConnection Status : OK\nConnection Port : " + str(self.port) + "\nNickname : " + str(self.nickname) + "\n")
            message =  "new_player " + str(self.nickname)
            self.s.sendall(b"" + message.encode())

        except:
            self.connect=False
            print('ERROR: Server unreachable... Game closed')
        #On initialise la map du serveur
        map = pickle.loads(self.s.recv(5000))
        self.model.map.array = map[0]
        self.model.map.width = map[1]
        self.model.map.height = map[2]
        fruits_tableau = self.s.recv(1500)
        self.model.fruits = pickle.loads(fruits_tableau)
        character = self.s.recv(1500)
        self.model.characters = pickle.loads(character)
        print("Map receved")
        self.s.setblocking(False)

    # keyboard events
    def keyboard_quit(self):
        print("=> event \"quit\"")
        message = "QUIT " + str(self.nickname)
        self.s.sendall(b"" + message.encode())
        print("Leaving the game...")
        self.model.quit(self.nickname)
        self.s.close()
        return False

    def keyboard_move_character(self, direction):
        print("=> event \"keyboard move direction\" {}".format(DIRECTIONS_STR[direction]))
        message =  "DIR " + str(self.nickname) + " " + str(direction)
        self.s.sendall(b"" + message.encode())
        self.model.move_character(self.nickname,direction)
        return True

    def keyboard_drop_bomb(self):
        print("=> event \"keyboard drop bomb\"")
        message = "DROP " + str(self.nickname)
        self.s.sendall(b"" + message.encode())
        self.model.drop_bomb(self.nickname)
        return True

    def connection_serveur():
        return True

    # time event

    def tick(self, dt):
        #On regarde si on reçoit un message de la part du serveur (reçu uniquement si il y a eu EVENT et donc actualisation de la map)
        try:
            map_event = pickle.loads(self.s.recv(10000))
            self.model.fruits = map_event[0]
            self.model.characters = map_event[1]
            self.model.bombs = map_event[2]
        #Gestion de l'erreur de socket
        except socket.error as e:
            if e.args[0] == errno.EWOULDBLOCK:
                pass
            else:
                print("Socket error: ", e)
        return True
