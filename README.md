# sorting algorithms visualization

this project provides a visual comparison of various sorting algorithms in real-time. it uses pygame to create an interactive grid interface where you can watch 12 sorting algorithms simultaneously organize the same dataset.

## features

- **multi-algorithm display**: visualizes 12 different sorting algorithms in a 3×4 grid
- **real-time comparison**: directly compare algorithm efficiency on identical data
- **dynamic visualization**: colored highlights show element comparisons and swaps
- **interactive controls**: adjust list size with slider or keyboard shortcuts
- **responsive design**: automatically adapts to different window sizes
- **dark mode interface**: easy on the eyes with dark-themed UI

## algorithms included

the visualization includes both practical and educational/humorous algorithms:

### practical algorithms
1. **bubble sort**: compares adjacent elements and swaps them if in wrong order
2. **insertion sort**: builds sorted array one element at a time
3. **quick sort**: uses divide-and-conquer with a pivot element
4. **merge sort**: divides array into halves, sorts, then merges
5. **selection sort**: repeatedly finds minimum element from unsorted part
6. **cocktail sort**: bidirectional bubble sort variant

### educational/humorous algorithms
7. **sleep sort**: elements "sleep" proportional to their value
8. **stalin sort**: removes elements that are out of order
9. **bogo sort**: randomly shuffles until sorted (very inefficient)
10. **miracle sort**: waits for list to sort itself by chance
11. **quantum bogosort**: simulates "destroying universe" until finding one with sorted list
12. **brutal sort**: simulates testing all permutations

## controls

- **r key**: reset and generate a new random list
- **up/down arrows**: increase/decrease list size
- **slider**: adjust list size using the slider at the bottom of the screen
- **window resize**: interface automatically adapts to window size

## visual elements

- **colored blocks**: represent values in each list
- **red/green highlights**: show elements being compared or swapped
- **algorithm status**: displays "sorting..." or "complete" for each algorithm
- **progress visualization**: watch each algorithm work through the data in real-time

## requirements

- python 3.x
- pygame
- pygame_widgets

## installation

```bash
pip install pygame pygame_widgets
```

## running the visualization

```bash
python main.py
```

## how it works

the program creates a 3×4 grid of visualization panels, each representing a different sorting algorithm. all algorithms start with the same randomly generated list and sort it in real-time, allowing you to see the differences in efficiency and approach.

each algorithm runs in its own thread to ensure smooth visualization. the app uses a dark-themed interface for comfortable viewing and provides controls to adjust the list size and restart the sorting process.

## performance notes

- some algorithms (like bogosort) are intentionally inefficient and may never complete for large lists
- for demonstration purposes, some inefficient algorithms are given artificial completion conditions
- the sleep sort implementation is scaled to complete faster than a real implementation would
- the humorous algorithms (miracle, quantum bogosort, brutal) are simulations rather than actual implementations

## screenshots

![image](https://github.com/user-attachments/assets/49a0e662-5ee7-4e6c-b3a7-743649e5893b)

## license

unlicense
