import numpy as np
import smithwaterman
from operator import itemgetter
import math

def create_kmers(P):
    kmers = {}
    for i in range(len(P)-k+1):
        kmer = P[i:i+k]
        if(kmer in kmers):
            kmers[kmer].append(i)
        else:
            kmers[kmer] = [i]
            
    return kmers

def find_hotspots(kmers, T):
    hotspots = {}
    for i in range(len(T)-k+1):
        kmer = T[i:i+k]
        if(kmer in kmers.keys()):
            if(kmer in hotspots):
                hotspots[kmer].append(i)
            else:
                hotspots[kmer] = [i]
    return hotspots

def create_dotmatrix(len_P, len_T, hotspots, kmers):
    dotmatrix = np.zeros((len_P, len_T))
    for kmer in hotspots:
        for i in hotspots[kmer]:
            for j in kmers[kmer]:
                for n in range(k):
                    dotmatrix[j+n, i+n] = 1
    return dotmatrix

def score_diago(start, end, P, T):
    score = 0
    i = start[0]
    j = start[1]
    endPlus1 = (end[0] + 1, end[1] + 1)

    while((i,j) != endPlus1):
        score += smithwaterman.score(P[i], T[j])
        i+=1
        j+=1
    return score

def create_diagos(P, T, dotmatrix):
    len_T = len(T)
    len_P = len(P)
    diago_coords = {}
    
    #lire la première moitié de la matrice en diagonale
    i = len_P
    while i >= 0:
        start = None
        end = None

        x = i
        y = 0
        while x < len_P and y < len_T:
            if dotmatrix[x,y] != 0:
                if start is None:
                    start = (x,y)
                else:
                    end = (x,y)

            x += 1
            y += 1

        if(start is not None and end is not None):
            diago_coords[(start,end)] = score_diago(start, end, P, T)
        i -=1

    #lire la 2eme moitié de la matrice en diagonale
    j = 0
    while j < len_T:
        start = None
        end = None

        x = 0
        y = j
        while x < len_P and y < len_T:
            if dotmatrix[x,y] != 0:
                if start is None:
                    start = (x,y)
                else:
                    end = (x,y)

            x += 1
            y += 1

        if(start is not None and end is not None):
            diago_coords[(start,end)] = score_diago(start, end, P, T)
        j += 1
    return diago_coords

def create_super_diagos(diagos, P, T):
    #identifier les voisin à distance raisonable de chq séquence
    superdiagos = {}
    for d in diagos.keys():
        for other in diagos.keys():
            if(other != d):
                x1 = d[1][0]
                y1 = d[1][1]
                x2 = other[0][0]
                y2 = other[0][1]
                if(x2 >= x1 and y2 >= y1):
                    dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
                    if(dist <= maxdistance):
                        superdiagos[d] = other

                x1 = d[1][0]
                y1 = d[1][1]
                x2 = other[0][0]
                y2 = other[0][1]
                if(x2 >= x1 and y2 >= y1):
                    dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
                    if(dist <= maxdistance):
                        superdiagos[d] = other

    #À l'aide des voisins de chacun, reconstruire les super-diagos
    result = {}
    for key in superdiagos:
        voisin = superdiagos[key]
        score = diagos[key] + diagos[voisin]
        while voisin in superdiagos:
            voisin = superdiagos[voisin]
            score += diagos[voisin]
        result[(key[0], voisin[1])] = score

    diagos.update(result) 

def init(words):
    currentIndex = 0
    T_dict = {}
    T = ""
    i = 0
    for word in words:
        T += word.lower()
        newIndex = currentIndex + len(word)
        for n in range(currentIndex, newIndex):
            T_dict[n] = i
        currentIndex = newIndex
        i += 1
    return T, T_dict

def find_best_match(P, words):
    T, T_dict = init(words) 
    len_T = len(T)
    len_P = len(P)

    kmers = create_kmers(P)
    hotspots = find_hotspots(kmers, T)
    dotmatrix = create_dotmatrix(len_P, len_T, hotspots, kmers)
    diagos = create_diagos(P, T, dotmatrix)
    best_diagos = dict(sorted(diagos.items(), key = itemgetter(1), reverse = True)[:diagosToKeep])
    create_super_diagos(best_diagos, P, T)
    best_diagos = dict(sorted(best_diagos.items(), key = itemgetter(1), reverse = True)[:superDiagosToKeep])

    bestmatch = ""
    bestscore = -math.inf
    for diago in best_diagos:
        score = smithwaterman.distance(P, T[diago[0][1]:diago[1][1]+1])
        if(score > bestscore):
            bestmatch = words[T_dict[diago[0][1]]].strip()
            bestscore = score
    
    return bestmatch

##### CONFIG #####
k = 3           # Kmer size
diagosToKeep = 1000
superDiagosToKeep = 10
maxdistance = 5 # distance euclidienne maximale pour lier 2 diagos