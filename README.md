# A Chess engine work in progress
A simple react app using chessboardjsx and chess.js. Can play either by input moves in the browser; from and to, or by letting the engine do the work. Client will request best move from server based on current board position. The server does it's magic and returns the best move to the client.

If you end up with a interesting position and don't want to forget it, make sure to save it to the database by clicking the `save position` button.

All saved positions in the database can be requested by clicking the `load positions`. The board will then fetch all the saved positions and you can load them into the board with a simple click.

Enjoy

![Alt text](../img/screenshot.png)
### TODOS

- Predict more moves in the future in engine
- pruning of minmax tree
- Ent passant
- Better 
- Certain king moves are buggy
- Make better database keys and rows
- Save games in database? openings mby?
