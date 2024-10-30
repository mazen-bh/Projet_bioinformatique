from operator import itemgetter

def create_kmers(P, k=3):
    return {P[i:i+k] for i in range(len(P)-k+1)}

def jaccard_similarity(kmersP, kmersT):
    intersection_count = len(kmersP.intersection(kmersT))
    union_count = len(kmersP) + len(kmersT) - intersection_count
    return intersection_count / union_count if union_count != 0 else 0

def find_best_match(P, titles):
    bestmatch = ""
    bestscore = -1
    kmersP = create_kmers(P)
    for title in titles:
        title = title.lower().strip()
        kmersT = create_kmers(title)
        score = jaccard_similarity(kmersP, kmersT)
        if score > bestscore:
            bestmatch = title
            bestscore = score
    return bestmatch, bestscore
