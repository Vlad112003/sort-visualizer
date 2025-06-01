# Sorting Algorithms Visualization

This project provides a visual comparison of various sorting algorithms in real-time. It uses Pygame to create an interactive interface where you can watch multiple sorting algorithms race to organize the same dataset.

## Features

- **Multiple Algorithms**: Visualizes 12 different sorting algorithms simultaneously
- **Interactive Controls**: Adjust list size and restart sorts on demand
- **Dark Mode Interface**: Easy-to-read dark-themed UI
- **Dynamic Resizing**: Adapts to different screen sizes
- **Real-time Comparison**: See which algorithms are most efficient for different datasets

## Algorithms Included

1. Bubble Sort
2. Insertion Sort
3. Quick Sort
4. Merge Sort
5. Selection Sort
6. Cocktail Sort
7. Sleep Sort
8. Stalin Sort
9. Bogo Sort
10. Miracle Sort (humorous)
11. Quantum BogoSort (humorous)
12. Brutal Sort (humorous)

## Controls

- **R**: Reset and generate a new random list
- **UP/DOWN Arrow Keys**: Increase/decrease list size
- **Slider**: Adjust list size using the slider at the bottom of the screen

## Requirements

- Python 3.x
- Pygame
- pygame_widgets

## Installation

```bash
pip install pygame pygame_widgets
```

## Running the Visualization

```bash
python main.py
```

## How It Works

The program creates a grid of visualization panels, each representing a different sorting algorithm. All algorithms start with the same randomly generated list and sort it in real-time, allowing you to see the differences in efficiency and approach.

Each algorithm runs in its own thread to ensure smooth visualization. The app uses a dark-themed interface for comfortable viewing and provides controls to adjust the list size and restart the sorting process.

## Performance Notes

Some algorithms (like BogoSort) are intentionally inefficient and may never complete for large lists. They are included for educational purposes to demonstrate the stark contrast in algorithm efficiency.

## Screenshots

![image](https://github.com/user-attachments/assets/49a0e662-5ee7-4e6c-b3a7-743649e5893b)


## License

Unlicense
