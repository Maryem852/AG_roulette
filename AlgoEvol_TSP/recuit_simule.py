import random
import math


def calculer_distance_totale(solution, matrice_distances):
    distance_totale = 0
    for i in range(len(solution) - 1):
        distance_totale += matrice_distances[solution[i]][solution[i + 1]]
    distance_totale += matrice_distances[solution[-1]][solution[0]]
    return distance_totale


def generer_voisin(solution):

    i, j = random.sample(range(len(solution)), 2)
    voisin = solution[:]
    voisin[i], voisin[j] = voisin[j], voisin[i]
    return voisin


def recuit_simule(matrice_distances, temperature_initiale, refroidissement, iterations):
    solution_actuelle = list(range(len(matrice_distances)))
    random.shuffle(solution_actuelle)

    meilleure_solution = solution_actuelle[:]
    meilleure_distance = calculer_distance_totale(solution_actuelle, matrice_distances)

    temperature = temperature_initiale

    for _ in range(iterations):
        voisin = generer_voisin(solution_actuelle)

        distance_actuelle = calculer_distance_totale(solution_actuelle, matrice_distances)
        distance_voisin = calculer_distance_totale(voisin, matrice_distances)


        delta=distance_voisin-distance_actuelle

        if delta<0 or random.random()<math.exp(-delta / temperature):
            solution_actuelle = voisin


        if distance_voisin < meilleure_distance:
            meilleure_solution = voisin[:]
            meilleure_distance = distance_voisin

        temperature *= refroidissement

        if temperature <= 0.00001:
            break

    return meilleure_solution, meilleure_distance

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




matrice_distances = [
    [0, 2, 2, 7, 15, 2, 5, 7, 6, 5],
    [2, 0, 10, 4, 7, 3, 7, 15, 8, 2],
    [2, 10, 0, 1, 4, 3, 3, 4, 2, 3],
    [7, 4, 1, 0, 2, 15, 7, 7, 5, 4],
    [15, 7, 4, 2, 0, 7, 3, 2, 2, 7],
    [2, 3, 3, 15, 7, 0, 1, 7, 2, 10],
    [5, 7, 3, 7, 3, 1, 0, 1, 2, 10],
    [7, 15, 4, 7, 2, 7, 1, 0, 1, 15],
    [6, 8, 2, 5, 2, 2, 2, 1, 0, 15],
    [5, 2, 3, 4, 7, 10, 3, 15, 15, 0]
]


temperature_initiale = 100
refroidissement = 0.99
iterations = 1000

meilleure_solution, meilleure_distance = recuit_simule(
    matrice_distances, temperature_initiale, refroidissement, iterations
)

print("Meilleure solution trouvée (Recuit simulé):", meilleure_solution)
print("Distance minimale:", meilleure_distance)
afficher_solution(meilleure_solution, matrice_distances)

