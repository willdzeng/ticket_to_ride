# Ticket To Ride Libary
A Game Engine and multiple AIs for Game "Ticket To Ride"

## AI Introducation
### CFAE
Cost Function Action Evaluation AI (CFAE) uses a set of cost function to evaluate each action of each round and select the best
### CFBase
A cost function Base AI which have a set of rules and cost function to make decision in each round
### Adverisrial AI
A AI that eavaluate the routes build by the oppoenets and select the best action to block the routes of the oppoenets
### CFCombined AI
A AI that comibe CFAE and Adversirial AI by using another high-level cost function
### Random
A random AI that does random action each round
## How to play the game

Change whatever AI you want to use and just run 
```
./play_game.py
```
or
```
python play_game.py
```
## How to play as human
In the play_game.py, uncomment
```
p2 = ConsolePlayer("Human")
```
and comment whatever p2 is, and turn on the gui by
```
use_gui = True
```
And you are good to go!

## Main Contributor
Steve Schwarcz 

Jeffrey Twigg

Di Zeng

## Be free to fork and change the code.
## If you have any questions, you can submit them in issue page.
## Thanks
