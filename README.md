## Sudoku Solver
I figured that the real way to beat sudoku would be to create an algorithmic approach that can beat arbitrary puzzles.

In its current state, this program can beat all but the most difficult puzzles.  One constraint I imposed upon myself was to avoid brute-force approaches if at all possible.  I imagine if I implement a guess-and-check algorithm, this will be able to solve all puzzles.  This was mostly an exercise for me in formalizing logic.  

I have a few different stages saved here (I know, version control...).
 
* dumb_complete.py stores only the code responsible for representing a puzzle.  This was actually the most difficult part of the project.  I find that good organization is essential to writing code.  If you're interested in writing the algorithms to solve the puzzle yourself, you could start with this as a way to represent the puzzle.
* sample.py has some sample games written in there, with each given square represented by its row number, column number and value.  Mimic this structure to add new games.
* sudoku.py has the most recent version of the game with the algorithms included.  It's fairly well documented, so you should be able to understand what each function does.

If I were going to properly release this program, I'd refactor it so the representation data is stored separately from the puzzle logic.  I'd also implement a guess-and-check process that counts how many times it had to guess, so at least I could see how many guesses it took, and if there is indeed a unique solution.
