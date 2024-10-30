import numpy as np
import math

def create_kmers(P, k):
    """Crée un ensemble de k-mers à partir de la séquence de requête P."""
    kmers = set()
    for i in range(len(P) - k + 1):
        kmers.add(P[i:i + k])
    return kmers

def find_hotspots(kmers, T):
    """Trouve les hotspots dans la séquence cible T en fonction des k-mers de P."""
    hotspots = {}
    for i in range(len(T) - len(next(iter(kmers))) + 1):
        kmer = T[i:i + len(next(iter(kmers)))]
        if kmer in kmers:
            if kmer not in hotspots:
                hotspots[kmer] = []
            hotspots[kmer].append(i)
    return hotspots

def score_diago(start, end, P, T):
    score = 0
    i, j = start
    len_P = len(P)
    len_T = len(T)
    
    # S'assurer que nous ne dépassons pas les limites de P et T
    while i < len_P and j < len_T and (i, j) != (end[0] + 1, end[1] + 1):
        score += 1 if P[i] == T[j] else 0
        i += 1
        j += 1
    return score


def find_best_match(P, titles):
    k = 3
    best_match = ""
    best_score = -float("inf")

    for title in titles:
        title = title.strip().lower()
        
        # Création des kmers
        kmers = create_kmers(P, k)
        
        # Identification des hotspots
        hotspots = find_hotspots(kmers, title)

        # Calcul du score en diagonale
        scores = []
        for kmer, positions in hotspots.items():
            for start_pos in positions:
                end_pos = (start_pos + k - 1, start_pos + k - 1)
                score = score_diago((0, start_pos), end_pos, P, title)
                scores.append(score)

        current_score = max(scores, default=0)
        
        # Mise à jour du meilleur score
        if current_score > best_score:
            best_score = current_score
            best_match = title
    
    return best_match, best_score
