# AI Problem Solving

## Live Demo Links
- [Tic-Tac-Toe AI](https://SOMUREX.github.io/AI_problemSolving_-RA2411026050204-RA2411026050183-/tictactoe.html)
- [Sudoku CSP Solver](https://SOMUREX.github.io/AI_problemSolving_-RA2411026050204-RA2411026050183-/sudoku.html)
- [logistics](logistics_tsp.py)
# 1. tic tac toe
# 2. sudoku csp solver

## ALGORITHMS USED:
-tic tac toe:
-1. Minimax Algorithm

-AI explores ALL possible moves
-Picks the best move assuming opponent also plays perfectly
-Guarantees unbeatable AI

-2. Alpha-Beta Pruning

-Improved version of Minimax
-Skips unnecessary branches that won't affect the result
-Much faster — explores fewer nodes
-Same result as Minimax but more efficient

-sudoku csp solver:
-1. Backtracking Search

-Try a number → if invalid → go back and try next number

-2. MRV Heuristic (Minimum Remaining Values)

-Always pick the cell with fewest possible values first
-Makes solving much faster
