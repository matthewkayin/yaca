# Yet Another Chess AI
## Introduction
This is a chess AI I wrote in an attempt to answer the question "Can I make a chess AI without googling how to make a chess AI?" You can run it in python3 by downloading the files or you can run the included executable for Windows. If you want to run it in python3 you will need to have the pygame library installed as well.

There are the beginnings of an attempt to make the AI think multiple moves, you can test this out by specifying the "--depth=n" flag, where n is some 2 or greater. (n = 2 means the AI tries to think 2 moves ahead). Warning, this is very slow, read below to see why.

I had never studied AI theory before this, all I knew were game trees. I thought the idea of game trees was interesting, because I figured you could use them to brute force you way into finding the best move in a chess match. 

## How it Works and What I Learned
The AI works by considering an altered board state and then evaluating how good that board state is for it using multiple scoring factors such as the number of enemy pieces captured, the number of allied pieces lost, the number of board squares controlled by allied pieces, and whether allied pieces are currently threatening enemy pieces. The AI will then pick the move which gives it the most favorable board. 

I have later learned that this sort of thing is called an "adveserial search" and that scoring the board is my "heuristic" function. I have also learned about alpha-beta pruning, which would have been nice to use because even going up to a depth of 2 slows down the AI quite a bit. Alpha-beta pruning is designed for that sort of thing because it prunes out paths that it knows aren't optimal, which would make the best-move search much quicker at higher depths.

This AI could be improved in a number of ways by looking at the work of other chess AIs, (more specific weights on pieces, different weights at different times, measures to calm down the aggressive queen, etc.), but for now it enjoys a humble retirement in my github. If you decide to play it, I hope you enjoy.
