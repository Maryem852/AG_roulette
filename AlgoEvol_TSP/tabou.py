import random
from collections import deque

def calculer_distance_totale(solution, matrice_distances):
    distance_totale = 0
    for i in range(len(solution) - 1):
        distance_totale += matrice_distances[solution[i]][solution[i + 1]]
    distance_totale += matrice_distances[solution[-1]][solution[0]]
    return distance_totale

def generer_voisins(solution):
    voisins = []
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            voisin = solution[:]
            voisin[i], voisin[j] = voisin[j], voisin[i]
            voisins.append(voisin)
    return voisins

def tabu_search(matrice_distances, nombre_iterations, taille_tabu):
    nombre_villes = len(matrice_distances)
    solution_actuelle = list(range(nombre_villes))
    random.shuffle(solution_actuelle)

    meilleure_solution = solution_actuelle[:]
    meilleure_distance = calculer_distance_totale(solution_actuelle, matrice_distances)

    tabu_list = deque(maxlen=taille_tabu)

    for _ in range(nombre_iterations):
        voisins = generer_voisins(solution_actuelle)
        voisins = [v for v in voisins if v not in tabu_list]

        if not voisins:
            break

        solution_actuelle = min(voisins, key=lambda x: calculer_distance_totale(x, matrice_distances))
        distance_actuelle = calculer_distance_totale(solution_actuelle, matrice_distances)

        tabu_list.append(solution_actuelle)

        if distance_actuelle < meilleure_distance:
            meilleure_solution = solution_actuelle[:]
            meilleure_distance = distance_actuelle

    return meilleure_solution, meilleure_distance



matrice_distances = [
[0,2,2,7,15,2,5,7,6,5],
[2,0,10,4,7,3,7,15,8,2],
[2,10,0,1,4,3,3,4,2,3],
[7,4,1,0,2,15,7,7,5,4],
[15,7,4,2,0,7,3,2,2,7],
[2,3,3,15,7,0,1,7,2,10],
[5,7,3,7,3,1,0,1,2,7],
[7,15,4,7,2,7,1,0,1,2],
[6,8,2,5,2,2,2,1,0,15],
[5,2,3,4,7,10,7,2,15,0]
]


nombre_iterations = 1000
taille_tabu = 50

import matplotlib.pyplot as plt

def afficher_solution(solution, matrice_distances):
    n = len(matrice_distances)
    # coordonnées aléatoires pour les villes
    coords = [(random.random(), random.random()) for _ in range(n)]

    plt.figure(figsize=(6,6))
    for i, (x, y) in enumerate(coords):
        plt.scatter(x, y, color='blue')
        plt.text(x + 0.02, y + 0.02, str(i), fontsize=9)

    # tracer le trajet
    for i in range(len(solution)):
        x1, y1 = coords[solution[i]]
        x2, y2 = coords[solution[(i + 1) % n]]
        plt.plot([x1, x2], [y1, y2], color='red')

    plt.title("Trajet du voyageur de commerce (Recuit simulé)")
    plt.show()



meilleure_solution, meilleure_distance = tabu_search(matrice_distances, nombre_iterations, taille_tabu)

print("Meilleure solution trouvée (Tabu Search):", meilleure_solution)
print("Distance minimale:", meilleure_distance)
afficher_solution(meilleure_solution, matrice_distances)

