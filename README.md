# 2048-Expectimax-AI

Requires python 2.7 and Tkinter. To run program without Python, download dist/game/ and run game.exe. Use --help to see relevant command arguments.

## To run with Expectimax Agent w/ depth=2 and goal of 2048:
```python game.py -a Expectimax```
or
```game.exe -a Expectimax```

## ```game.exe -h```:
```
usage: game.exe [-h] [-a AGENT] [-d DEPTH] [-g GOAL] [--no-graphics]

2048 Game w/ AI

optional arguments:
  -h, --help            show this help message and exit
  -a AGENT, --agent AGENT
                        name of agent (Reflex or Expectimax)
  -d DEPTH, --depth DEPTH
                        depth for Expectimax (Default: 2)
  -g GOAL, --goal GOAL  number of goal for AI (Default: 2048)
  --no-graphics         no graphics (only works when AI specified)
  ```
