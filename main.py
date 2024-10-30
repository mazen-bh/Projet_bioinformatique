import numpy as np
from operator import itemgetter
import math
import time
import levenshtein
import smithwaterman
import fasta
import jaccard
from functions import read_titles, print_result,extract_movie_names # Import functions 

def main():
    input_file = 'db.txt'  # Input file containing the movie database
    output_file = 'movies.txt'  # Output file where movie names will be stored
    extract_movie_names(input_file, output_file)

    titles = read_titles(output_file)  # Use the output file to read titles
    for P in ["Toy Story" ,"The Story", "Toy Stori", "Toy Store", "Story", "Toy Storry"]:
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
        print_result("LEVENSHTEIN", bestmatch, start_time, bestscore)

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
        print_result("SMITH-WATERMAN", bestmatch, start_time, bestscore)

        ### HOME MADE FASTA ###
        start_time = time.time()
        bestmatch = fasta.find_best_match(P, titles)
        bestscore = smithwaterman.distance(P, bestmatch)  # Calculate score based on Smith-Waterman
        print_result("HOME MADE FASTA + SMITH-WATERMAN", bestmatch, start_time, bestscore)

        ### JACCARD ###
        start_time = time.time()
        bestmatch = jaccard.find_best_match(P, titles)
        bestscore = smithwaterman.distance(P, bestmatch)  # Calculate score based on Smith-Waterman
        print_result("JACCARD + SMITH-WATERMAN", bestmatch, start_time, bestscore)

        print("")

if __name__ == "__main__":
    main()
