import matplotlib.pyplot as plt  # For visualizing memory layout
import random


class Hole:
    def __init__(self, start, size): # constructor
        self.start = start  # Starting address of the hole
        self.size = size    # Size of the hole (free memory)

# ----------------------------------------------------------------------------


class Process:
    def __init__(self, name, size): # constructor
        self.name = name    # Identifier for the process
        self.size = size    # Amount of memory the process needs
        self.start = None   # To be set when the process is allocated a hole

# ----------------------------------------------------------------------------


def first_fit(memory_holes, processes):
 
    allocated = []      
    waiting_queue = []  

    for process in processes:
        allocated_flag = False
        
        for hole in memory_holes:
            if process.size <= hole.size:
                
                process.start = hole.start
                allocated.append(process)
                
                hole.start += process.size
                hole.size -= process.size
                allocated_flag = True
                break
        if not allocated_flag:
            waiting_queue.append(process)  
        print_memory_state(memory_holes, allocated, waiting_queue)
    return allocated, memory_holes, waiting_queue  

# ----------------------------------------------------------------------------


def best_fit(memory_holes, processes):

    allocated = []          
    waiting_queue = []      

    for process in processes:              
        allocated_flag = False             
        suitable_holes = [hole for hole in memory_holes if hole.size >= process.size]
        

        if suitable_holes:                  
            best_hole = min(suitable_holes, key = lambda h : h.size)
            

            process.start = best_hole.start  
            allocated.append(process)        

            best_hole.start += process.size  
            best_hole.size -= process.size   
            allocated_flag = True            

        if not allocated_flag:               
            waiting_queue.append(process)    

        print_memory_state(memory_holes, allocated, waiting_queue)
        

    return allocated, memory_holes, waiting_queue
    


# ----------------------------------------------------------------------------


def worst_fit(memory_holes, processes):
      
    allocated = []
    waiting_queue = []

    for process in processes:
        allocated_flag = False
        suitable_holes = [hole for hole in memory_holes if hole.size >= process.size]

        if suitable_holes:
            
            worst_hole = max(suitable_holes, key=lambda h: h.size)
            process.start = worst_hole.start
            allocated.append(process)

            worst_hole.start += process.size
            worst_hole.size -= process.size
            allocated_flag = True

        if not allocated_flag:
            waiting_queue.append(process)

        print_memory_state(memory_holes, allocated, waiting_queue)

    return allocated, memory_holes, waiting_queue

# ----------------------------------------------------------------------------


def print_memory_state(holes, allocated, waiting):
    """
    Print current allocation status:
      - Which processes are allocated (with start and size)
      - Which holes remain (with start and size)
      - Which processes are waiting
    """
    print("\n--- Memory State ---")
    print("Allocated Partitions:")
    for p in allocated:
        print(f"{p.name} | Start: {p.start} | Size: {p.size}")
    print("Free Holes:")
    for h in holes:
        if h.size > 0:
            print(f"Hole | Start: {h.start} | Size: {h.size}")
    print("Waiting Queue:")
    for p in waiting:
        print(f"{p.name} | Size: {p.size}")
    print("---------------------")

# ----------------------------------------------------------------------------

def plot_memory(allocated, holes, algorithm_name):

    """
    Visualize memory as a horizontal bar:
      - Allocated processes in skyblue
      - Free holes in lightgrey
      - Labels show name and size
    """
    fig, ax = plt.subplots(figsize=(10, 3))
    segments = [*allocated, *holes]
    # Sort segments by starting address
    segments.sort(key=lambda x: x.start)

    y = 0
    for seg in segments:
        color = 'skyblue' if isinstance(seg, Process) else 'lightgrey'
        label = f"{seg.name} ({seg.size})" if isinstance(seg, Process) else f"Hole ({seg.size})"
        ax.broken_barh([(seg.start, seg.size)], (y, 10), facecolors=color, edgecolor='black')
        ax.text(seg.start + seg.size / 2, y + 5, label,
                ha='center', va='center', fontsize=9, weight='bold')

    ax.set_ylim(0, 15)
    ax.set_xlim(0, max(s.start + s.size for s in segments) + 20)
    ax.set_xlabel('Memory Address')
    ax.set_yticks([])
    ax.set_title(f'Memory Allocation - {algorithm_name}')
    ax.grid(True, axis='x', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

# ----------------------------------------------------------------------------

def main():
    # 1. Input memory holes manually
    memory_holes = []
    num_holes = int(input("Enter number of memory holes: "))  # Built-in input for user interaction
    for i in range(num_holes):
        start = int(input(f"Start address of hole {i+1}: "))
        size = int(input(f"Size of hole {i+1}: "))
        memory_holes.append(Hole(start, size))

    # 2. Choose process input mode
    mode = input("Choose process input mode (manual/random): ").strip().lower()

    processes = []
    if mode == 'manual':
        # Manual entry of process names and sizes
        num_processes = int(input("Enter number of processes: "))
        for i in range(num_processes):
            name = input(f"Enter name of process {i+1}: ")
            size = int(input(f"Enter size of process {i+1}: "))
            processes.append(Process(name, size))
    elif mode == 'random':
        # Generate random process sizes within specified bounds
        num_processes = int(input("Enter number of processes: "))
        min_size = int(input("Enter minimum process size: "))
        max_size = int(input("Enter maximum process size: "))
        for i in range(num_processes):
            name = "P" + str(i + 1)
            size = random.randint(min_size, max_size)
            processes.append(Process(name, size))
        print("\nGenerated Random Processes:")
        for p in processes:
            print(f"{p.name} | Size: {p.size}")
    else:
        print("Invalid input mode. Exiting.")
        return

    # 3. Choose allocation algorithm
    algo_choice = input("Choose allocation algorithm (first/best/worst): ").strip().lower()

    if algo_choice == "first":
        allocated, remaining_holes, waiting = first_fit(memory_holes, processes)
    elif algo_choice == "best":
        allocated, remaining_holes, waiting = best_fit(memory_holes, processes)
    elif algo_choice == "worst":
        allocated, remaining_holes, waiting = worst_fit(memory_holes, processes)
    else:
        print("Invalid algorithm choice. Exiting.")
        return


    # 4. Compute total external fragmentation
    total_fragmentation = sum(hole.size for hole in remaining_holes if hole.size > 0)
    print(f"\nTotal Fragmentation: {total_fragmentation}")

    # 5. Plot final memory map
    plot_memory(allocated, remaining_holes, algo_choice.capitalize())

# ----------------------------------------------------------------------------


if __name__ == "__main__":
    main()
