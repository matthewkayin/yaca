# Yet Another Chess AI
This chess AI isn't very smart, but I wanted to see if I could make one so I did. The result is a player vs CPU chess game developed in pygame. I didn't want to google any chess AI theory when developing this, I just wanted to give it my best attempt given what I figured would be a good approach to the problem. Based on some CS theory classes I figured game trees would be a good approach, so I had the AI consider a move, score the value of the board at that position, then choose among the moves that resulted in the highest scoring board from the AI's perspective (I've since learned that this is pretty much how stockfish works, it's just that stockfish is much more complex and has far more precise values for weighting different pieces). 

Things that contribute the AI's board scoring:
 - Capturing another piece gives points
 - Checkmating the player gives points
 - Putting the player in check gives points
 - Putting the player's pieces under threat of capture gives points
 - Putting AI pieces in a position that they could be captured next turn loses points
 - Losing AI pieces loses points

What I would have liked to do going forward with this is to work on having the AI think three moves ahead. The idea was to just expand the game tree that I'm building two layers down. So for each possible AI move, we guess the response player move, and then from that build another tree of possible AI moves. 
The initial move's score becomes the score of the best possible second move that the AI makes. As I was messing around with this idea, I saw that it was becoming particularly slow especially in python, so I was likely going to need to impliment some sort of tree pruning to improve efficiency (i.e. only expand to the second move on a subset of the initial moves that are clearly better than the rest). Unfortunately I got stuck on this idea because of the recursive logic of this approach: if we use the same logic to guess the player's move as we use to predict the AI's move, then we would end up in an endless recursive of trees. So we either need to only guess the player's move at one depth or we need to find some other way to try to approximate where the player would move. However I've never developed this project that far so the current state it's in is just one level of decision making. 

If you want to run this project, you'll need python3 installed with the pygame library downloaded. I plan on putting a windows exe here in the future so that you don't need to do that.
