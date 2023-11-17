# Raiden Game

A simple arcade-style shooting game using Pygame.

## File Descriptions:

- `raiden_game.py`: The main game script.
- `player.png`: Image resource for the player's aircraft.
- `enemy.png`: Image resource for enemy aircraft.
- `bullet.png`: Image resource for bullets.

## Game Controls:

- Arrow keys `LEFT` and `RIGHT` to move the player's aircraft.
- `SPACE` to shoot.
- Choose game difficulty at the start: `Easy`, `Medium`, or `Hard`.
- `r` to retry the game after game over.
- `q` to quit the game after game over.

## Game Logic:

- Player tries to avoid being hit by enemy bullets and aircraft.
- Player shoots at enemy aircraft to gain points.
- The game difficulty affects the frequency of enemy spawns and the player's initial lives.

## Dependencies:

- Pygame

To install dependencies:
```bash
pip install pygame


Run the game script:

python raiden_game.py
