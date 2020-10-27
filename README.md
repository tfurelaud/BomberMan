# Bomber Man #

This is a simple "Bomber Man" game written in Python 3, based on the *PyGame* library.

![Bomber Man Snapshot](snap0.png?raw=true "snapshot")

## Rules ##

This game is similar to a classic "Bomber Man". This is a *standalone* version of the game for a single player. In this version, a single character (or player) starts the game with an initial amount of 50 health points. Each fruit brings a character with 10 extra health points, while each bomb blast removes 10 health points. A character is dead when its health points reach zero. A character gets immunity for a while after he's hit by a bomb blast. After a character drops a bomb, he is disarmed for a while.

To play, just use the following keys:
  * use *arrows* to move the current character
  * press *space* to drop a bomb at current position, that will explode after a delay of 5 seconds
  * press *escape* to quit the game

The implementation of this game follows a simple MVC architecture (Model/View/Controller).


## Download & Install ##

First clone the project available on GitHUB under GPL:

```
  git clone https://github.com/tfurelaud/BomberMan
```

To install Python (root privilege required):

```
  $ sudo apt get install python3 pip3
```

To install the *PyGame* library (user privilege enough):

```
  $ pip3 install pygame
```

To start the game:

```
  $ ./bomber.py
```

By default, the map "maps/map0" is used, but you can generate you own map (*mymap*) and use it as follows:

```
  $ ./bomber.py maps/mymap
```

## Launch the game

### Server side

```
  ./bomber_server.py <port utilisé> <maps>
```
(ex: <port> = 7777 et <map> = maps/map0)
  

If a permission error prevents you from starting the server, run this command:
```
  chmod a + x bomber_server.py
```

### Client side

If the server is on the same PC :
```
  ./bomber_client.py localhost <port> <nickname>
```
(ex: <port> = 7777 et <nickname> = player1)
  
else if the server is on an other PC:
```
  ./bomber_client.py <adresseIP> <port>
```

If a permission error prevents you from starting the client, run this command:
```
  chmod a+x bomber_client.py
```


