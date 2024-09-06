# Flappy Bird with Python and Pygame

A Python-based recreation of the classic **Flappy Bird** game, featuring pixel-perfect collision detection using masks for precise gameplay.

## Video Demo
https://youtu.be/J3siykNyf14

## Features
- **Pixel-perfect collision detection:** Achieved with Pygame masks for accuracy.
- **Neural network integration:** Uses the NEAT algorithm to evolve bird behavior and enhance gameplay.
- **Dynamic background and scrolling floor:** Provides a smooth visual experience.
- **Configurable parameters:** Easily adjust bird and pipe properties through the code.

## Getting Started
### Prerequisites
- Python 3.x
- Pygame library
- NEAT-Python library

### Installation
1. Install the required dependencies:
    ```bash
    pip install pygame neat-python
    ```
2. Download or clone the repository:
    ```bash
    git clone https://github.com/ElioCheng/Flappy_Bird.git
    ```
3. Run the game:
    ```bash
    python flappy_bird.py
    ```

### Configuring NEAT
To modify the neural network configurations, edit the `config-feedforward.txt` file included in the project.

## Gameplay
- **Bird Movement:** The bird will jump whenever you press the spacebar or when controlled by the neural network.
- **Avoid Pipes:** Navigate the bird through gaps between pipes to keep it alive.
- **Scoring:** The game tracks your score based on the number of pipes passed.
