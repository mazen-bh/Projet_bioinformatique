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

        ### FASTA +smith waterman ###
        start_time = time.time()
        bestmatch = fasta_smith_waterman.find_best_match(P, titles)
        bestscore = smithwaterman.distance(P, bestmatch)  # Calculate score based on Smith-Waterman
        print_result(" FASTA + SMITH-WATERMAN", bestmatch, start_time, bestscore)

        ### JACCARD + smith waterman ###
        start_time = time.time()
        bestmatch = jaccard_smith_waterman.find_best_match(P, titles)
        bestscore = smithwaterman.distance(P, bestmatch)  # Calculate score based on Smith-Waterman
        print_result("JACCARD + SMITH-WATERMAN", bestmatch, start_time, bestscore)
        

        ### FASTA SEUL ###
        start_time = time.time()
        bestmatch, bestscore = fasta.find_best_match(P, titles)
        print_result("FASTA SEUL", bestmatch, start_time, bestscore)

        ### JACCARD SEUL ###
        start_time = time.time()
        bestmatch, bestscore = jaccard.find_best_match(P, titles)
        print_result("JACCARD SEUL", bestmatch, start_time, bestscore)

        ### BLAST SEUL ###
        start_time = time.time()
        bestmatch, bestscore = blast.find_best_match(P, titles)
        print_result("BLAST SEUL", bestmatch, start_time, bestscore)

        print("")

if __name__ == "__main__":
    main()
