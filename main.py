import numpy as np
from operator import itemgetter
import math
import time
import levenshtein
import smithwaterman
import fasta_smith_waterman
import jaccard_smith_waterman
import jaccard
import fasta
import blast
from functions import read_titles, print_result, extract_movie_names, calculate_resources, compare_algorithms,plot_algorithm_performance  # Import functions

def main():
    input_file = 'db.txt'
    output_file = 'movies.txt'
    extract_movie_names(input_file, output_file)

    titles = read_titles(output_file)

    # List to store results for comparison

    for P in ["Toy Story","toy stori","toe storry"]:  # You can add more test cases here
        results = []
        print(P)
        P = P.lower()

        ### LEVENSHTEIN ###
        start_time = time.time()
        bestmatch = ""
        bestscore = math.inf
        for title in titles:
            title = title.lower()
            score = levenshtein.distance(P, title)
            if score < bestscore:
                bestmatch = title
                bestscore = score
        cpu_used, memory_used = calculate_resources(levenshtein.distance, P, title)
        results.append({
            'algorithm': "LEVENSHTEIN",
            'execution_time': time.time() - start_time,
            'cpu_used': cpu_used,
            'memory_used': memory_used,
            'score': bestscore,
        })
        print_result("LEVENSHTEIN", bestmatch, start_time, bestscore)
        print("CPU USED: ", cpu_used)
        print("MEMORY USED: ", memory_used)

        ### SMITH-WATERMAN ###
        start_time = time.time()
        bestmatch = ""
        bestscore = -math.inf
        for title in titles:
            title = title.lower()
            score = smithwaterman.distance(P, title)
            if score > bestscore:
                bestmatch = title
                bestscore = score
        cpu_used, memory_used = calculate_resources(smithwaterman.distance, P, title)
        results.append({
            'algorithm': "SMITH-WATERMAN",
            'execution_time': time.time() - start_time,
            'cpu_used': cpu_used,
            'memory_used': memory_used,
            'score': bestscore,
        })
        print_result("SMITH-WATERMAN", bestmatch, start_time, bestscore)
        print("CPU USED: ", cpu_used)
        print("MEMORY USED: ", memory_used)

        ### FASTA + SMITH-WATERMAN ###
        start_time = time.time()
        bestmatch = fasta_smith_waterman.find_best_match(P, titles)
        bestscore = smithwaterman.distance(P, bestmatch)
        cpu_used, memory_used = calculate_resources(fasta_smith_waterman.find_best_match, P, title)
        results.append({
            'algorithm': "FASTA + SMITH-WATERMAN",
            'execution_time': time.time() - start_time,
            'cpu_used': cpu_used,
            'memory_used': memory_used,
            'score': bestscore,
        })
        print_result("FASTA + SMITH-WATERMAN", bestmatch, start_time, bestscore)
        print("CPU USED: ", cpu_used)
        print("MEMORY USED: ", memory_used)

        ### JACCARD + SMITH-WATERMAN ###
        start_time = time.time()
        bestmatch = jaccard_smith_waterman.find_best_match(P, titles)
        bestscore = smithwaterman.distance(P, bestmatch)
        cpu_used, memory_used = calculate_resources(jaccard_smith_waterman.find_best_match, P, title)
        results.append({
            'algorithm': "JACCARD + SMITH-WATERMAN",
            'execution_time': time.time() - start_time,
            'cpu_used': cpu_used,
            'memory_used': memory_used,
            'score': bestscore,
        })
        print_result("JACCARD + SMITH-WATERMAN", bestmatch, start_time, bestscore)
        print("CPU USED: ", cpu_used)
        print("MEMORY USED: ", memory_used)

        ### FASTA ###
        start_time = time.time()
        bestmatch, bestscore = fasta.find_best_match(P, titles)
        cpu_used, memory_used = calculate_resources(fasta.find_best_match, P, title)
        results.append({
            'algorithm': "FASTA",
            'execution_time': time.time() - start_time,
            'cpu_used': cpu_used,
            'memory_used': memory_used,
            'score': bestscore,
        })
        print_result("FASTA", bestmatch, start_time, bestscore)
        print("CPU USED: ", cpu_used)
        print("MEMORY USED: ", memory_used)

        ### JACCARD ###
        start_time = time.time()
        bestmatch, bestscore = jaccard.find_best_match(P, titles)
        cpu_used, memory_used = calculate_resources(jaccard.find_best_match, P, title)
        results.append({
            'algorithm': "JACCARD",
            'execution_time': time.time() - start_time,
            'cpu_used': cpu_used,
            'memory_used': memory_used,
            'score': bestscore,
        })
        print_result("JACCARD", bestmatch, start_time, bestscore)
        print("CPU USED: ", cpu_used)
        print("MEMORY USED: ", memory_used)

        ### BLAST ###
        start_time = time.time()
        bestmatch, bestscore = blast.find_best_match(P, titles)
        cpu_used, memory_used = calculate_resources(blast.find_best_match, P, title)
        results.append({
            'algorithm': "BLAST",
            'execution_time': time.time() - start_time,
            'cpu_used': cpu_used,
            'memory_used': memory_used,
            'score': bestscore,
        })
        print_result("BLAST", bestmatch, start_time, bestscore)
        print("CPU USED: ", cpu_used)
        print("MEMORY USED: ", memory_used)

    # After collecting all results, compare and rank algorithms
        print("\nComparing Algorithms:")
        compare_algorithms(results)
        plot_algorithm_performance(results)





if __name__ == "__main__":
    main()
