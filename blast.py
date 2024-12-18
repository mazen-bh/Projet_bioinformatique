import numpy as np

def create_kmers(P, k):
    kmers = set()
    for i in range(len(P) - k + 1):
        kmers.add(P[i:i + k])
    return kmers

def find_matches(kmersP, T, k):
    matches = []
    for i in range(len(T) - k + 1):
        kmer = T[i:i + k]
        if kmer in kmersP:
            matches.append(i)
    return matches

def score_matches(P, T, matches):
    best_score = -float('inf')
    best_match = ""
    
    for start in matches:
        match_segment = T[start:start + len(P)]
        # Simple score based on character matching
        score = sum(1 for a, b in zip(P, match_segment) if a == b)
        
        if score > best_score:
            best_score = score
            best_match = match_segment
    
    return best_match, best_score

def find_best_match(P, titles, k=3):
    kmersP = create_kmers(P, k)
    best_match = ""
    best_score = -float('inf')
    
    for title in titles:
        title = title.lower().strip()
        matches = find_matches(kmersP, title, k)
        if matches:
            match, score = score_matches(P, title, matches)
            if score > best_score:
                best_match = match
                best_score = score

    return best_match, best_score
