# gomoku
Gomoku with manual and AI play options. AL player implemented with Monte Carlo Tree Search algorithm.

## Files
**main.py**: Game UI  
**game.py**: Game engine  
**ai.py**: AI simulator  
**test.py**: Automated testing suites  
**test_states, test_sols**: test case parameters  

## Usage
To run the program:  
```
python main.py
```

To run tests in predefined states:
```
python main -t 1
```

To test AI player against random policy:
```
python main -t 2
```

## in-game keyboard options
* 'Enter' for AI play
* 'm' for manual play
* Space to restart
