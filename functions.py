import numpy as np
import time
import psutil
import threading
import matplotlib.pyplot as plt


def extract_movie_names(input_file, output_file):
    with open(input_file, 'r',encoding='utf-8') as infile, open(output_file, 'w',encoding='utf-8') as outfile:
     
        for line in infile:
           
            parts = line.split(',')
            if len(parts) > 1:
                movie_name_with_year = parts[1].strip()  
                movie_name = movie_name_with_year.split(' (')[0]  
                outfile.write(movie_name + '\n')  
 
def read_titles(file_path):
    titles = []
    with open(file_path, 'r',encoding='utf-8') as file:
        titles = file.readlines()
    return titles

def print_result(algo_name, best_match, start_time, score=None):
    print(algo_name)
    print("BEST MATCH: ", best_match.strip())
    if score is not None:
        print("SCORE: ", score)
    print("---execution time: %s seconds ---" % (time.time() - start_time))
    print("")




def monitor_resources(process, stop_event, cpu_samples, memory_samples):
    """Continuously monitor and collect CPU and memory usage while the stop_event is not set."""
    while not stop_event.is_set():
        
        cpu_samples.append(process.cpu_percent(interval=0.1))
        memory_samples.append(process.memory_info().rss)
        time.sleep(0.05)  

def calculate_resources(func, *args):
    process = psutil.Process()
    cpu_samples = []
    memory_samples = []
    stop_event = threading.Event()

    monitor_thread = threading.Thread(target=monitor_resources, args=(process, stop_event, cpu_samples, memory_samples))
    monitor_thread.start()

    start_time = time.time()
    result = func(*args)
    end_time = time.time()

    stop_event.set()
    monitor_thread.join()

    execution_time = end_time - start_time
    avg_cpu_used = sum(cpu_samples) / len(cpu_samples) if cpu_samples else 0.0
    peak_memory_used = max(memory_samples) if memory_samples else 0
    return avg_cpu_used, peak_memory_used


def compare_algorithms(results):
    """
    Compare algorithms based on execution time, resource usage, and score.
    `results` is a list of dictionaries containing stats for each algorithm.
    """
    sorted_by_time = sorted(results, key=lambda x: x['execution_time'])
    sorted_by_cpu = sorted(results, key=lambda x: x['cpu_used'])
    sorted_by_memory = sorted(results, key=lambda x: x['memory_used'])
    sorted_by_score = sorted(results, key=lambda x: x['score'], reverse=True)

    print("Ranking by Execution Time:")
    for i, res in enumerate(sorted_by_time):
        print(f"{i+1}. {res['algorithm']}: {res['execution_time']}s")

    print("\nRanking by CPU Usage:")
    for i, res in enumerate(sorted_by_cpu):
        print(f"{i+1}. {res['algorithm']}: {res['cpu_used']}%")

    print("\nRanking by Memory Usage:")
    for i, res in enumerate(sorted_by_memory):
        print(f"{i+1}. {res['algorithm']}: {res['memory_used']} MB")


    return {
        'time': sorted_by_time,
        'cpu': sorted_by_cpu,
        'memory': sorted_by_memory,
        'score': sorted_by_score
    }


def plot_algorithm_performance(results):
    """
    Plot the performance of algorithms based on RAM usage, execution time, and CPU usage.
    `results` is a list of dictionaries containing the results for each algorithm.
    """
    algorithms = [res['algorithm'] for res in results]
    execution_times = [res['execution_time'] for res in results]
    cpu_usages = [res['cpu_used'] for res in results]
    memory_usages = [res['memory_used'] for res in results]

    plt.figure(figsize=(10, 6))
    plt.barh(algorithms, execution_times, color='skyblue')
    plt.title("Execution Time (s)")
    plt.xlabel("Time (seconds)")
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.barh(algorithms, cpu_usages, color='salmon')
    plt.title("CPU Usage (%)")
    plt.xlabel("CPU Usage (%)")
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.barh(algorithms, memory_usages, color='lightgreen')
    plt.title("Memory Usage (MB)")
    plt.xlabel("Memory Usage (MB)")
    plt.tight_layout()
    plt.show()