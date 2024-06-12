# TicTacToe Game Against AI

A standard 3 by 3 TicTacToe game where human play against trained agent.
The agent was trained using Q-based agent over 5 millions times of playing
the game and updating its Q-table accordingly to the formulas.

## Features
- Two players game
- Agent: X player
- Human: O player
- Movements: Mouse cursor
- Restart: R keyboard or click the restart button

## Code Structuring
 
 The game was implemented by following architectural pattern of 
 Model-View-Controller(MVC). There are console game, graphical game and 
 a unit testing to make the model are working as expected. The code is written
 by following SOLID Object Oriented Principle whenever is possible. 
 There is a doc-string for the functions in the model, `tictactoe.py`, and
 in the graphical game, `graphical_game.py`. It is a normal graphical game with a welcome screen
 and the playing part where user can restart the game anytime they want.
 
 ## Installation
 
 To set up the project locally, clone the repository and run:
 
 ```bash
 pip3 install pygame
 pip3 install numpy
 pip3 install pickle
 pip3 install tqdm
```
 
 ## Contact
 For questions or feedback, feel free to contact me at heanchhinling@gmail.com
 
 
 