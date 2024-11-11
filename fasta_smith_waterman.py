import numpy as np
import smithwaterman
from operator import itemgetter
import math

# Fonction pour créer un dictionnaire de kmers à partir d'une chaîne P
def create_kmers(P):
    kmers = {}
    # Parcours de P pour extraire tous les kmers de taille k
    for i in range(len(P)-k+1):
        kmer = P[i:i+k]
        # Si le kmer est déjà dans le dictionnaire, on ajoute l'indice
        if(kmer in kmers):
            kmers[kmer].append(i)
        else:
            kmers[kmer] = [i]
            
    return kmers

# Fonction pour identifier les "hotspots" dans une chaîne T, où les kmers de P sont trouvés
def find_hotspots(kmers, T):
    hotspots = {}
    # Parcours de T pour rechercher les kmers de P
    for i in range(len(T)-k+1):
        kmer = T[i:i+k]
        if(kmer in kmers.keys()):
            # Ajoute l'indice du kmer à hotspots
            if(kmer in hotspots):
                hotspots[kmer].append(i)
            else:
                hotspots[kmer] = [i]
    return hotspots

# Fonction pour créer une matrice de points (dotmatrix) représentant les alignements des kmers
def create_dotmatrix(len_P, len_T, hotspots, kmers):
    dotmatrix = np.zeros((len_P, len_T))
    # Pour chaque kmer trouvé dans les hotspots
    for kmer in hotspots:
        # Marquer les positions correspondantes dans la dotmatrix
        for i in hotspots[kmer]:
            for j in kmers[kmer]:
                for n in range(k):
                    dotmatrix[j+n, i+n] = 1
    return dotmatrix

# Fonction pour calculer le score d'une diagonale entre deux indices de départ et de fin
def score_diago(start, end, P, T):
    score = 0
    i = start[0]
    j = start[1]
    endPlus1 = (end[0] + 1, end[1] + 1)

    # Calcul du score sur la diagonale en comparant les caractères de P et T
    while((i,j) != endPlus1):
        score += smithwaterman.score(P[i], T[j])  # Utilise l'algorithme de Smith-Waterman pour calculer le score
        i+=1
        j+=1
    return score

# Fonction pour créer les diagonales d'alignement à partir de la dotmatrix
def create_diagos(P, T, dotmatrix):
    len_T = len(T)
    len_P = len(P)
    diago_coords = {}
    
    # Recherche des diagonales dans P en commençant par la fin
    i = len_P
    while i >= 0:
        start = None
        end = None

        x = i
        y = 0
        # Cherche les diagonales où la dotmatrix est non nulle
        while x < len_P and y < len_T:
            if dotmatrix[x,y] != 0:
                if start is None:
                    start = (x,y)
                else:
                    end = (x,y)

            x += 1
            y += 1

        # Si une diagonale est trouvée, on calcule son score
        if(start is not None and end is not None):
            diago_coords[(start,end)] = score_diago(start, end, P, T)
        i -= 1

    # Recherche des diagonales dans T
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

# Fonction pour créer des super-diagonales basées sur les distances entre les diagonales
def create_super_diagos(diagos, P, T):
    superdiagos = {}
    for d in diagos.keys():
        for other in diagos.keys():
            if(other != d):
                # Calcul de la distance entre deux diagonales
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

    # Combinaison des scores des super-diagonales pour obtenir un score global
    result = {}
    for key in superdiagos:
        voisin = superdiagos[key]
        score = diagos[key] + diagos[voisin]
        while voisin in superdiagos:
            voisin = superdiagos[voisin]
            score += diagos[voisin]
        result[(key[0], voisin[1])] = score

    diagos.update(result)  # Met à jour les scores des diagonales

# Fonction pour initialiser la chaîne T et associer chaque indice à un mot
def init(words):
    currentIndex = 0
    T_dict = {}
    T = ""
    i = 0
    # Construction de T et création du dictionnaire des indices
    for word in words:
        T += word.lower()
        newIndex = currentIndex + len(word)
        for n in range(currentIndex, newIndex):
            T_dict[n] = i
        currentIndex = newIndex
        i += 1
    return T, T_dict

# Fonction pour trouver la meilleure correspondance de P dans une liste de mots
def find_best_match(P, words):
    T, T_dict = init(words) 
    len_T = len(T)
    len_P = len(P)

    kmers = create_kmers(P)  # Crée les kmers de P
    hotspots = find_hotspots(kmers, T)  # Trouve les hotspots dans T
    dotmatrix = create_dotmatrix(len_P, len_T, hotspots, kmers)  # Crée la dotmatrix
    diagos = create_diagos(P, T, dotmatrix)  # Crée les diagonales
    best_diagos = dict(sorted(diagos.items(), key = itemgetter(1), reverse = True)[:diagosToKeep])  # Trie et garde les meilleures diagonales
    create_super_diagos(best_diagos, P, T)  # Crée les super-diagonales
    best_diagos = dict(sorted(best_diagos.items(), key = itemgetter(1), reverse = True)[:superDiagosToKeep])  # Trie et garde les meilleures super-diagonales

    bestmatch = ""
    bestscore = -math.inf
    # Recherche la meilleure correspondance en utilisant l'algorithme de Smith-Waterman
    for diago in best_diagos:
        score = smithwaterman.distance(P, T[diago[0][1]:diago[1][1]+1])
        if(score > bestscore):
            bestmatch = words[T_dict[diago[0][1]]].strip()
            bestscore = score
    
    return bestmatch


# Paramètres de configuration
k = 3           
diagosToKeep = 1000  # Nombre de diagonales à garder
superDiagosToKeep = 10  # Nombre de super-diagonales à garder
maxdistance = 5  # Distance maximale pour considérer une super-diagonale
