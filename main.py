import pygame
import random
import math
import threading
import time
import pygame_widgets
from pygame_widgets.slider import Slider

pygame.init()


class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BLUE = 0, 0, 255
    PURPLE = 128, 0, 128
    BACKGROUND_COLOR = (30, 30, 30)  # dark mode background

    GRADIENTS = [
        (100, 100, 100),  # darker gradients for dark mode
        (130, 130, 130),
        (160, 160, 160)
    ]

    FONT = pygame.font.SysFont('jetbrains-mono', 30)
    LARGE_FONT = pygame.font.SysFont('jetbrains-mono', 40)
    SMALL_FONT = pygame.font.SysFont('jetbrains-mono', 20)

    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst, position=(0, 0), scale=1.0):
        self.width = width
        self.height = height
        self.position = position
        self.scale = scale
        self.window = None  # will be set by the main window
        self.set_list(lst.copy())
        self.sorting_complete = False
        self.algo_name = ""
        self.color_positions = {}  # Store positions to highlight

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst) if lst else 0
        self.max_val = max(lst) if lst else 1

        # dynamic adjustment of block width based on list length
        self.block_width = round((self.width - self.SIDE_PAD) / max(1, len(lst)))
        self.block_height = math.floor((self.height - self.TOP_PAD) / max(1, (self.max_val - self.min_val)))
        self.start_x = self.SIDE_PAD // 2


def draw(window, algo_infos, slider=None):
    window.fill(DrawInformation.BACKGROUND_COLOR)

    # draw the visualization for each algorithm
    for info in algo_infos:
        draw_algo(window, info)

    # draw control text
    controls_font = DrawInformation.SMALL_FONT
    controls = controls_font.render("R - Reset | UP/DOWN - Change List Size", 1, DrawInformation.WHITE)
    window.blit(controls, (10, window.get_height() - 30))

    # draw information about list size
    if slider:
        size_text = controls_font.render(f"List Size: {int(slider.getValue())}", 1, DrawInformation.WHITE)
        window.blit(size_text, (slider.getX() + slider.getWidth() + 10, slider.getY() + 5))

    pygame.display.update()


def draw_algo(window, draw_info):
    x_offset, y_offset = draw_info.position

    # draw algorithm name and status
    algo_name = draw_info.algo_name
    status = "Complete" if draw_info.sorting_complete else "Sorting..."
    title = draw_info.FONT.render(f"{algo_name} - {status}", 1,
                                  draw_info.GREEN if draw_info.sorting_complete else draw_info.RED)
    window.blit(title, (x_offset + draw_info.width / 2 - title.get_width() / 2, y_offset + 5))

    # draw the list
    draw_list(window, draw_info)


def draw_list(window, draw_info, color_positions={}):
    lst = draw_info.lst
    x_offset, y_offset = draw_info.position

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width + x_offset
        y = y_offset + draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in draw_info.color_positions:
            color = draw_info.color_positions[i]

        pygame.draw.rect(window, color, (x, y, draw_info.block_width, draw_info.height - y + y_offset))


def generate_starting_list(n, min_val, max_val):
    lst = []
    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
    return lst


def bubble_sort(draw_info, lst, stop_event):
    lst = lst.copy()
    draw_info.lst = lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            if stop_event.is_set():
                return

            num1 = lst[j]
            num2 = lst[j + 1]

            # Highlight the elements being compared
            draw_info.color_positions = {
                j: DrawInformation.RED,
                j + 1: DrawInformation.GREEN
            }

            if num1 > num2:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]

            time.sleep(0.01)

    # Clear the color positions when done
    draw_info.color_positions = {}
    draw_info.sorting_complete = True


def insertion_sort(draw_info, lst, stop_event):
    lst = lst.copy()
    draw_info.lst = lst

    for i in range(1, len(lst)):
        if stop_event.is_set():
            return

        current = lst[i]
        j = i

        # Highlight the current element
        draw_info.color_positions = {i: DrawInformation.GREEN}

        while j > 0 and lst[j - 1] > current:
            if stop_event.is_set():
                return

            # Highlight the elements being compared
            draw_info.color_positions = {
                j: DrawInformation.GREEN,
                j - 1: DrawInformation.RED
            }

            lst[j] = lst[j - 1]
            j -= 1
            time.sleep(0.01)

        lst[j] = current
        # Highlight the final position
        draw_info.color_positions = {j: DrawInformation.GREEN}
        time.sleep(0.01)

    # Clear the color positions when done
    draw_info.color_positions = {}
    draw_info.sorting_complete = True


def stalin_sort(draw_info, lst, stop_event):
    lst = lst.copy()
    draw_info.lst = lst

    i = 1
    while i < len(lst):
        if stop_event.is_set():
            return

        # Highlight the elements being compared
        draw_info.color_positions = {
            i - 1: DrawInformation.GREEN,
            i: DrawInformation.RED
        }

        if lst[i] < lst[i - 1]:
            lst.pop(i)
        else:
            i += 1

        time.sleep(0.05)

    # Clear the color positions when done
    draw_info.color_positions = {}
    draw_info.sorting_complete = True


def bogo_sort(draw_info, lst, stop_event):
    lst = lst.copy()
    draw_info.lst = lst

    def is_sorted(arr):
        return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))

    attempts = 0
    while not is_sorted(lst) and attempts < 100:  # limit attempts to prevent infinite loops
        if stop_event.is_set():
            return

        # Color two random elements to show activity
        if len(lst) > 1:
            i, j = random.sample(range(len(lst)), 2)
            draw_info.color_positions = {
                i: DrawInformation.RED,
                j: DrawInformation.GREEN
            }

        random.shuffle(lst)
        attempts += 1
        time.sleep(0.1)

    # Clear the color positions when done
    draw_info.color_positions = {}
    draw_info.sorting_complete = True


def quick_sort_helper(draw_info, lst, start, end, stop_event):
    if start >= end or stop_event.is_set():
        return

    pivot = lst[end]
    partition_idx = start

    # Highlight the pivot
    draw_info.color_positions = {end: DrawInformation.BLUE}
    time.sleep(0.01)

    for i in range(start, end):
        if stop_event.is_set():
            return

        # Highlight the elements being compared
        draw_info.color_positions = {
            i: DrawInformation.RED,
            partition_idx: DrawInformation.GREEN,
            end: DrawInformation.BLUE  # pivot
        }

        if lst[i] <= pivot:
            lst[i], lst[partition_idx] = lst[partition_idx], lst[i]
            partition_idx += 1
        time.sleep(0.01)

    # Highlight the final pivot position
    draw_info.color_positions = {
        partition_idx: DrawInformation.GREEN,
        end: DrawInformation.RED
    }
    lst[partition_idx], lst[end] = lst[end], lst[partition_idx]
    time.sleep(0.01)

    quick_sort_helper(draw_info, lst, start, partition_idx - 1, stop_event)
    quick_sort_helper(draw_info, lst, partition_idx + 1, end, stop_event)


def quick_sort(draw_info, lst, stop_event):
    lst = lst.copy()
    draw_info.lst = lst

    quick_sort_helper(draw_info, lst, 0, len(lst) - 1, stop_event)

    # Clear the color positions when done
    draw_info.color_positions = {}
    draw_info.sorting_complete = True


def merge_sort_helper(draw_info, lst, left, right, stop_event):
    if left < right and not stop_event.is_set():
        mid = (left + right) // 2

        # Highlight the current range
        for i in range(left, right + 1):
            draw_info.color_positions[i] = DrawInformation.PURPLE
        time.sleep(0.01)

        merge_sort_helper(draw_info, lst, left, mid, stop_event)
        merge_sort_helper(draw_info, lst, mid + 1, right, stop_event)

        merge(draw_info, lst, left, mid, right, stop_event)


def merge(draw_info, lst, left, mid, right, stop_event):
    if stop_event.is_set():
        return

    left_half = lst[left:mid + 1]
    right_half = lst[mid + 1:right + 1]

    # Highlight the merging range
    for i in range(left, right + 1):
        draw_info.color_positions[i] = DrawInformation.PURPLE
    time.sleep(0.01)

    i = j = 0
    k = left

    while i < len(left_half) and j < len(right_half) and not stop_event.is_set():
        # Highlight the elements being compared
        draw_info.color_positions = {
            left + i: DrawInformation.RED if k == left + i else DrawInformation.PURPLE,
            mid + 1 + j: DrawInformation.GREEN if k == mid + 1 + j else DrawInformation.PURPLE
        }

        if left_half[i] <= right_half[j]:
            lst[k] = left_half[i]
            i += 1
        else:
            lst[k] = right_half[j]
            j += 1
        k += 1
        time.sleep(0.01)

    while i < len(left_half) and not stop_event.is_set():
        # Highlight the current element
        draw_info.color_positions[left + i] = DrawInformation.GREEN

        lst[k] = left_half[i]
        i += 1
        k += 1
        time.sleep(0.01)

    while j < len(right_half) and not stop_event.is_set():
        # Highlight the current element
        draw_info.color_positions[mid + 1 + j] = DrawInformation.GREEN

        lst[k] = right_half[j]
        j += 1
        k += 1
        time.sleep(0.01)


def merge_sort(draw_info, lst, stop_event):
    lst = lst.copy()
    draw_info.lst = lst

    merge_sort_helper(draw_info, lst, 0, len(lst) - 1, stop_event)

    # Clear the color positions when done
    draw_info.color_positions = {}
    draw_info.sorting_complete = True


def miracle_sort(draw_info, lst, stop_event):
    # wait for a miracle to happen and the list to sort itself
    lst = lst.copy()
    draw_info.lst = lst

    def is_sorted(arr):
        return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))

    attempts = 0
    while not is_sorted(lst) and attempts < 50:
        if stop_event.is_set():
            return

        # Highlight random elements to show activity
        if len(lst) > 2:
            positions = random.sample(range(len(lst)), min(3, len(lst)))
            draw_info.color_positions = {
                pos: DrawInformation.GREEN if random.random() > 0.5 else DrawInformation.RED
                for pos in positions
            }

        # waiting for the miracle
        time.sleep(0.2)
        attempts += 1

        # simulate small chances of the miracle happening
        if random.random() < 0.01:
            lst.sort()

    # Clear the color positions when done
    draw_info.color_positions = {}
    draw_info.sorting_complete = True


def selection_sort(draw_info, lst, stop_event):
    lst = lst.copy()
    draw_info.lst = lst

    for i in range(len(lst)):
        if stop_event.is_set():
            return

        min_idx = i
        # Highlight current position
        draw_info.color_positions = {i: DrawInformation.BLUE}

        for j in range(i + 1, len(lst)):
            if stop_event.is_set():
                return

            # Highlight the elements being compared
            draw_info.color_positions = {
                i: DrawInformation.BLUE,
                min_idx: DrawInformation.GREEN,
                j: DrawInformation.RED
            }

            if lst[j] < lst[min_idx]:
                min_idx = j

            time.sleep(0.01)

        # Highlight the swap
        draw_info.color_positions = {
            i: DrawInformation.RED,
            min_idx: DrawInformation.GREEN
        }
        lst[i], lst[min_idx] = lst[min_idx], lst[i]
        time.sleep(0.01)

    # Clear the color positions when done
    draw_info.color_positions = {}
    draw_info.sorting_complete = True


def sleep_sort(draw_info, lst, stop_event):
    # sort elements by letting them sleep proportionally to their value
    lst = lst.copy()
    draw_info.lst = lst
    result = []
    n = len(lst)

    # scaling factor for sleep - smaller for demonstration
    scale = 0.05

    def sleep_and_add(val, idx):
        if stop_event.is_set():
            return

        # Highlight the element about to wake up
        draw_info.color_positions[idx] = DrawInformation.RED
        time.sleep(val * scale)

        result.append(val)

        # update the list after each addition
        temp = result.copy() + [0] * (n - len(result))
        for i in range(len(temp)):
            if i < len(lst):
                lst[i] = temp[i]
                # Highlight the newly placed element
                if i == len(result) - 1:
                    draw_info.color_positions[i] = DrawInformation.GREEN

    threads = []
    for idx, val in enumerate(lst):
        t = threading.Thread(target=sleep_and_add, args=(val, idx))
        t.daemon = True
        threads.append(t)

    for t in threads:
        t.start()

    # wait maximum time for all threads to complete
    max_wait = max(lst) * scale + 1
    start_time = time.time()
    while len(result) < n and time.time() - start_time < max_wait:
        if stop_event.is_set():
            return
        time.sleep(0.1)

    # complete the final result
    for i in range(len(result)):
        if i < len(lst):
            lst[i] = result[i]

    # Clear the color positions when done
    draw_info.color_positions = {}
    draw_info.sorting_complete = True


def cocktail_sort(draw_info, lst, stop_event):
    lst = lst.copy()
    draw_info.lst = lst
    n = len(lst)
    swapped = True
    start = 0
    end = n - 1

    while swapped:
        swapped = False

        # forward pass
        for i in range(start, end):
            if stop_event.is_set():
                return

            # Highlight the elements being compared
            draw_info.color_positions = {
                i: DrawInformation.RED,
                i + 1: DrawInformation.GREEN
            }

            if lst[i] > lst[i + 1]:
                lst[i], lst[i + 1] = lst[i + 1], lst[i]
                swapped = True
            time.sleep(0.01)

        if not swapped:
            break

        swapped = False
        end -= 1

        # backward pass
        for i in range(end - 1, start - 1, -1):
            if stop_event.is_set():
                return

            # Highlight the elements being compared
            draw_info.color_positions = {
                i: DrawInformation.RED,
                i + 1: DrawInformation.GREEN
            }

            if lst[i] > lst[i + 1]:
                lst[i], lst[i + 1] = lst[i + 1], lst[i]
                swapped = True
            time.sleep(0.01)

        start += 1

    # Clear the color positions when done
    draw_info.color_positions = {}
    draw_info.sorting_complete = True


def quantum_bogosort(draw_info, lst, stop_event):
    # destroy the universe and create a new one where the list is sorted
    lst = lst.copy()
    draw_info.lst = lst

    def is_sorted(arr):
        return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))

    attempts = 0
    while not is_sorted(lst) and attempts < 50:
        if stop_event.is_set():
            return

        # Color random elements to show quantum activity
        if len(lst) > 3:
            positions = random.sample(range(len(lst)), min(5, len(lst)))
            draw_info.color_positions = {
                pos: DrawInformation.RED if random.random() > 0.5 else DrawInformation.GREEN
                for pos in positions
            }

        # simulate universe destruction
        time.sleep(0.3)

        # try to create a new universe with sorted list
        if random.random() < 0.1:  # 10% chance of success
            lst.sort()
            break

        # otherwise, try another random universe
        random.shuffle(lst)
        attempts += 1

    # Clear the color positions when done
    draw_info.color_positions = {}
    draw_info.sorting_complete = True


def brutal_sort(draw_info, lst, stop_event):
    # test all possible permutations until finding a sorted one
    # (actually just simulating for demonstration)
    lst = lst.copy()
    draw_info.lst = lst

    def is_sorted(arr):
        return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))

    # simulate brutal effort
    attempts = 0
    while not is_sorted(lst) and attempts < 30:
        if stop_event.is_set():
            return

        # Highlight random elements to show activity
        if len(lst) > 2:
            i = random.randint(0, len(lst) - 2)
            j = random.randint(i + 1, len(lst) - 1)
            draw_info.color_positions = {
                i: DrawInformation.RED,
                j: DrawInformation.GREEN
            }

        # simulate testing a permutation
        time.sleep(0.1)

        # make some random changes to simulate progress
        if attempts % 3 == 0 and len(lst) > 1:
            # the more we advance, the smarter changes we make
            progress = min(1.0, attempts / 20.0)

            if random.random() < progress:
                # sort a small portion
                start = random.randint(0, len(lst) - 2)
                end = min(start + random.randint(2, 5), len(lst))
                lst[start:end] = sorted(lst[start:end])
            else:
                # random swap
                i = random.randint(0, len(lst) - 1)
                j = random.randint(0, len(lst) - 1)
                lst[i], lst[j] = lst[j], lst[i]

        attempts += 1

        # eventually give up and sort everything
        if attempts >= 50:
            lst.sort()

    # Clear the color positions when done
    draw_info.color_positions = {}
    draw_info.sorting_complete = True


def restart_sorting(algo_infos, original_list, stop_event):
    # stop current threads
    stop_event.set()
    time.sleep(0.1)  # give threads time to stop
    stop_event.clear()

    # reset visualizations
    for info in algo_infos:
        info.set_list(original_list.copy())
        info.sorting_complete = False
        info.color_positions = {}  # Clear color positions

    # create and start new threads with all algorithms
    algorithms = [
        bubble_sort,
        insertion_sort,
        quick_sort,
        merge_sort,
        miracle_sort,
        selection_sort,
        sleep_sort,
        quantum_bogosort,
        cocktail_sort,
        brutal_sort,
        stalin_sort,
        bogo_sort
    ]

    threads = []
    for i, algorithm in enumerate(algorithms):
        if i < len(algo_infos):
            thread = threading.Thread(target=algorithm, args=(algo_infos[i], original_list.copy(), stop_event))
            thread.daemon = True
            thread.start()
            threads.append(thread)

    return threads


def main():
    # screen setup
    width, height = 1920, 980  # height reduced from 1080 to 980
    window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("Sorting Algorithms Visualization")

    # initial list settings
    n = 100
    min_val = 5
    max_val = 100
    original_list = generate_starting_list(n, min_val, max_val)

    # create slider for list size control
    list_size_slider = Slider(
        window,
        width - 300,
        height - 50,
        200,
        20,
        min=10,
        max=500,
        step=10,
        initial=n
    )

    # configure algorithm visualizations with grid layout
    def update_algo_infos():
        nonlocal algo_infos
        screen_width, screen_height = window.get_size()

        # calculate grid layout for algorithms
        rows, cols = 3, 4
        algo_width = (screen_width - (cols + 1) * 20) // cols
        algo_height = (screen_height - (rows + 1) * 20 - 50) // rows  # account for bottom controls

        algo_infos = []

        # create a grid of algorithm visualizations
        for row in range(rows):
            for col in range(cols):
                x_pos = 20 + col * (algo_width + 20)
                y_pos = 20 + row * (algo_height + 20)
                algo_infos.append(DrawInformation(algo_width, algo_height, original_list, position=(x_pos, y_pos)))

        # set algorithm names
        algorithm_names = [
            "Bubble Sort", "Insertion Sort", "Quick Sort", "Merge Sort",
            "Miracle Sort", "Selection Sort", "Sleep Sort", "Quantum BogoSort",
            "Cocktail Sort", "Brutal Sort", "Stalin Sort", "Bogo Sort"
        ]

        for i, name in enumerate(algorithm_names):
            if i < len(algo_infos):
                algo_infos[i].algo_name = name

        # set window reference for all visualizations
        for info in algo_infos:
            info.window = window

        return algo_infos

    algo_infos = update_algo_infos()

    # create threads for sorting algorithms
    stop_event = threading.Event()
    threads = restart_sorting(algo_infos, original_list, stop_event)

    # main loop
    run = True
    clock = pygame.time.Clock()
    prev_list_size = n

    while run:
        clock.tick(60)
        events = pygame.event.get()

        # update widgets
        pygame_widgets.update(events)

        current_list_size = int(list_size_slider.getValue())

        # check if list size has changed
        if current_list_size != prev_list_size:
            n = current_list_size
            original_list = generate_starting_list(n, min_val, max_val)
            threads = restart_sorting(algo_infos, original_list, stop_event)
            prev_list_size = current_list_size

        for event in events:
            if event.type == pygame.QUIT:
                run = False
                stop_event.set()

            elif event.type == pygame.VIDEORESIZE:
                # update slider position when window is resized
                screen_width, screen_height = window.get_size()
                list_size_slider.setX(screen_width - 300)
                list_size_slider.setY(screen_height - 50)

                # update algorithm visualizations for new window size
                algo_infos = update_algo_infos()
                threads = restart_sorting(algo_infos, original_list, stop_event)

            # add restart capability with 'R' key
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    original_list = generate_starting_list(n, min_val, max_val)
                    threads = restart_sorting(algo_infos, original_list, stop_event)

                # change list size with arrow keys
                elif event.key == pygame.K_UP:
                    n = min(500, n + 10)
                    list_size_slider.setValue(n)
                    original_list = generate_starting_list(n, min_val, max_val)
                    threads = restart_sorting(algo_infos, original_list, stop_event)
                    prev_list_size = n

                elif event.key == pygame.K_DOWN:
                    n = max(10, n - 10)
                    list_size_slider.setValue(n)
                    original_list = generate_starting_list(n, min_val, max_val)
                    threads = restart_sorting(algo_infos, original_list, stop_event)
                    prev_list_size = n

        # draw current state
        draw(window, algo_infos, list_size_slider)

    pygame.quit()


if __name__ == "__main__":
    main()