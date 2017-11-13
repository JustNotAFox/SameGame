Updated Readme
Scoring: (n-2)^2
Ruling: if there is a gap between groups of colors; Move everything to the left and down

Heuristics
Point value of move
Total point value of moves after move is done
Colors left (a move that removes an entire color is *probably* the best move?)
Maximum possible remaining point value (sum of cells^2 for all colors)
Number of groupings remaining in post-move state (another "less is more")

Solutions genes an array of values
Heuristic is a sum of the above multiplied by those values
Values can be negative (important for heuristics #3 and #5)
Breeding should either average these values or choose some and randomize the others? Thoughts?
Mutation randomly changes a value.
