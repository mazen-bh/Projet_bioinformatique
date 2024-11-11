from operator import itemgetter
import smithwaterman
import math

def create_kmers(P):
    kmers = set({})
    for i in range(len(P)-k+1):
        kmers.add(P[i:i+k])
            
    return kmers

def distance(kmersP, kmersT):
    intersectionCount = len(kmersP.intersection(kmersT))
    unionCount = len(kmersP) + len(kmersT) - intersectionCount
    return (intersectionCount / unionCount) * 1.0  

def find_best_match(P, titles):
    distances = {}
    kmersP = create_kmers(P)
    for title in titles:
        kmersT = create_kmers(title.lower())
        dist = distance(kmersP, kmersT)
        distances[title] = dist
    
    bestmatch = ""
    bestscore = -math.inf
    candidates = dict(sorted(distances.items(), key = itemgetter(1), reverse = True)[:candidatesToKeep])
    for candidate in candidates:
        score = smithwaterman.distance(P, candidate)
        if(score > bestscore):
            bestmatch = candidate
            bestscore = score
    
    return bestmatch


candidatesToKeep = 20
k = 3
