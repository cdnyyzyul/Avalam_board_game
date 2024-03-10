# Avalam_board_game

Avalam is a two-player game with win, null and loss conditions- a zero-sum game. Like most adversarial agents, we need to understand key aspects of the game to build an agent:
- Initial state - The initial state of the board has opposing color pawns arranged diagonally. 
![alt text](http:images/next.png)
- Viable actions - Pawns can be stacked on to adjacent pawns but it is illegal to stack more than 5 pawns.
- Every Avalam player can move his/her opponent’s pawns.
- Terminal state - The game ends when no legal moves are allowed.


# step to play

-	Open a terminal: 
    - (avalam) PS D:\game> python random_player.py --bind localhost --port 8000
-	Open a second terminal:
    - (avalam) PS D:\game> python greedy_player.py --bind localhost --port 8010
-	Open a third terminal:
    -  (avalam) PS D:\game> python game.py http://localhost:8000 http://localhost:8010 --time 900 --no-gui

