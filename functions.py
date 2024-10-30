import numpy as np
import time
def extract_movie_names(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
      
        for line in infile:
            
            parts = line.split(',')
            if len(parts) > 1:
                movie_name_with_year = parts[1].strip()  
                movie_name = movie_name_with_year.split(' (')[0]  
                outfile.write(movie_name + '\n')  

def read_titles(file_path):
    titles = []
    with open(file_path, 'r') as file:
        titles = file.readlines()
    return titles

def print_result(algo_name, best_match, start_time, score=None):
    print(algo_name)
    print("BEST MATCH: ", best_match.strip())
    if score is not None:
        print("SCORE: ", score)
    print("---execution time: %s seconds ---" % (time.time() - start_time))
    print("")