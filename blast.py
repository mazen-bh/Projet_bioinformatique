import numpy as np
import smithwaterman

def create_kmers(P, k):
    """Create k-mers from the query sequence P."""
    kmers = set()
    for i in range(len(P) - k + 1):
        kmers.add(P[i:i + k])
    return kmers

def find_matches(kmersP, T, k):
    """Find all matches of k-mers in the target sequence T."""
    matches = []
    for i in range(len(T) - k + 1):
        kmer = T[i:i + k]
        if kmer in kmersP:
            matches.append(i)
    return matches

def score_matches(P, T, matches):
    """Score the matches found using Smith-Waterman."""
    best_score = -float('inf')
    best_match = ""
    
    for start in matches:
        # Align using Smith-Waterman
        score = smithwaterman.distance(P, T[start:start + len(P)])
        if score > best_score:
            best_score = score
            best_match = T[start:start + len(P)]
    
    return best_match

def find_best_match(P, titles, k=3):
    """Find the best match for query P in the list of titles using BLAST."""
    kmersP = create_kmers(P, k)
    best_match = ""
    best_score = -float('inf')
    
    for title in titles:
        matches = find_matches(kmersP, title.lower(), k)
        if matches:
            match = score_matches(P, title.lower(), matches)
            if match and smithwaterman.distance(P, match) > best_score:
                best_match = match
                best_score = smithwaterman.distance(P, match)

    return best_match
