def get_input(prompt):
    return input(prompt)

def get_process_details(num_processes, include_priority=False):
    processes = []
    for i in range(num_processes):
        process_id = get_input(f"Enter Process ID for process {i+1}: ")
        burst_time = int(get_input(f"Enter Burst Time for process {i+1}: "))
        priority = None
        if include_priority:
            priority = int(get_input(f"Enter Priority for process {i+1}: "))
        processes.append({
            "id": process_id,
            "burst_time": burst_time,
            "priority": priority
        })
    return processes

def calculate_average_times(waiting_times, turnaround_times):
    avg_waiting_time = sum(waiting_times) / len(waiting_times)
    avg_turnaround_time = sum(turnaround_times) / len(turnaround_times)
    return avg_waiting_time, avg_turnaround_time

def fcfs(processes):
    waiting_times = [0] * len(processes)
    turnaround_times = [0] * len(processes)
    order_of_execution = []
    
    current_time = 0
    for i, process in enumerate(processes):
        order_of_execution.append(process['id'])
        waiting_times[i] = current_time
        current_time += process['burst_time']
        turnaround_times[i] = current_time
    
    avg_waiting_time, avg_turnaround_time = calculate_average_times(waiting_times, turnaround_times)
    return avg_waiting_time, avg_turnaround_time, order_of_execution

def sjf(processes):
    # Sort processes by burst time
    processes.sort(key=lambda x: x['burst_time'])
    
    waiting_times = [0] * len(processes)
    turnaround_times = [0] * len(processes)
    order_of_execution = []
    
    current_time = 0
    for i, process in enumerate(processes):
        order_of_execution.append(process['id'])
        waiting_times[i] = current_time
        current_time += process['burst_time']
        turnaround_times[i] = current_time
    
    avg_waiting_time, avg_turnaround_time = calculate_average_times(waiting_times, turnaround_times)
    return avg_waiting_time, avg_turnaround_time, order_of_execution

def priority_scheduling(processes):
    # Sort processes by priority (assuming lower number means higher priority)
    processes.sort(key=lambda x: x['priority'])
    
    waiting_times = [0] * len(processes)
    turnaround_times = [0] * len(processes)
    order_of_execution = []
    
    current_time = 0
    for i, process in enumerate(processes):
        order_of_execution.append(process['id'])
        waiting_times[i] = current_time
        current_time += process['burst_time']
        turnaround_times[i] = current_time
    
    avg_waiting_time, avg_turnaround_time = calculate_average_times(waiting_times, turnaround_times)
    return avg_waiting_time, avg_turnaround_time, order_of_execution

def round_robin(processes, time_quantum):
    waiting_times = [0] * len(processes)
    turnaround_times = [0] * len(processes)
    order_of_execution = []
    
    remaining_burst_times = [p['burst_time'] for p in processes]
    current_time = 0
    while True:
        done = True
        for i, process in enumerate(processes):
            if remaining_burst_times[i] > 0:
                done = False
                order_of_execution.append(process['id'])
                if remaining_burst_times[i] > time_quantum:
                    current_time += time_quantum
                    remaining_burst_times[i] -= time_quantum
                else:
                    current_time += remaining_burst_times[i]
                    waiting_times[i] = current_time - process['burst_time']
                    remaining_burst_times[i] = 0
                    turnaround_times[i] = current_time
        if done:
            break
    
    avg_waiting_time, avg_turnaround_time = calculate_average_times(waiting_times, turnaround_times)
    return avg_waiting_time, avg_turnaround_time, order_of_execution

def display_results(algorithm_name, avg_waiting_time, avg_turnaround_time, order_of_execution):
    print(f"\nResults for {algorithm_name}:")
    print(f"Average Waiting Time: {avg_waiting_time:.2f}")
    print(f"Average Turnaround Time: {avg_turnaround_time:.2f}")
    print(f"Order of Execution: {' -> '.join(order_of_execution)}")

def main():
    num_cores = int(get_input("Number of CPU cores: "))
    compare_algorithms = get_input("Do you want to compare multiple scheduling algorithms? (yes/no): ").lower()

    algorithms = []
    if compare_algorithms == "yes":
        algorithms = get_input("Select the scheduling algorithm(s) (comma-separated):\n"
                               "1. First Come First Serve\n"
                               "2. Shortest Job First\n"
                               "3. Priority Scheduling\n"
                               "4. Round Robin\n").split(", ")
    else:
        algorithms.append(get_input("Select the scheduling algorithm:\n"
                                    "1. First Come First Serve\n"
                                    "2. Shortest Job First\n"
                                    "3. Priority Scheduling\n"
                                    "4. Round Robin\n"))

    num_processes = int(get_input("Enter the number of processes: "))
    time_quantum = None
    include_priority = "3" in algorithms
    processes = get_process_details(num_processes, include_priority)

    if "4" in algorithms:
        time_quantum = int(get_input("Enter the time quantum for Round Robin: "))

    results = []
    for algorithm in algorithms:
        if algorithm == "1":
            avg_waiting_time, avg_turnaround_time, order_of_execution = fcfs(processes)
            display_results("First Come First Serve", avg_waiting_time, avg_turnaround_time, order_of_execution)
            results.append(("First Come First Serve", avg_waiting_time))
        elif algorithm == "2":
            avg_waiting_time, avg_turnaround_time, order_of_execution = sjf(processes)
            display_results("Shortest Job First", avg_waiting_time, avg_turnaround_time, order_of_execution)
            results.append(("Shortest Job First", avg_waiting_time))
        elif algorithm == "3":
            avg_waiting_time, avg_turnaround_time, order_of_execution = priority_scheduling(processes)
            display_results("Priority Scheduling", avg_waiting_time, avg_turnaround_time, order_of_execution)
            results.append(("Priority Scheduling", avg_waiting_time))
        elif algorithm == "4":
            avg_waiting_time, avg_turnaround_time, order_of_execution = round_robin(processes, time_quantum)
            display_results("Round Robin", avg_waiting_time, avg_turnaround_time, order_of_execution)
            results.append(("Round Robin", avg_waiting_time))

    if compare_algorithms == "yes":
        results.sort(key=lambda x: x[1])  # Sort by average waiting time
        print("\nOrder of effectiveness based on average waiting time:")
        for result in results:
            print(f"{result[0]}: {result[1]:.2f}")
        print(f"\nBest algorithm: {results[0][0]}")

if __name__ == "__main__":
    main()