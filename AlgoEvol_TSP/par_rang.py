import random
import matplotlib.pyplot as plt


# ================================
#   Fonctions de base
# ================================
def calculer_distance_totale(solution, matrice):
    d = 0
    for i in range(len(solution) - 1):
        d += matrice[solution[i]][solution[i + 1]]
    d += matrice[solution[-1]][solution[0]]
    return d


# --- Sélection par rang ---
def selection_rang(population, matrice):
    # Trier les individus selon leur distance (meilleur premier)
    population_triee = sorted(population, key=lambda x: calculer_distance_totale(x, matrice))
    n = len(population_triee)

    # Attribuer des probabilités inverses au rang
    proba = [(n - i) / sum(range(1, n + 1)) for i in range(n)]

    # Tirage aléatoire basé sur ces probabilités
    seuil = random.random()
    cumul = 0
    for i in range(n):
        cumul += proba[i]
        if seuil <= cumul:
            return population_triee[i][:]
    return population_triee[-1][:]


# ================================
#   Fonctions de croisement
# ================================
def crossover_1_point(p1, p2):
    point = random.randint(1, len(p1) - 2)
    enfant = p1[:point] + [v for v in p2 if v not in p1[:point]]
    return enfant


def crossover_2_point(p1, p2):
    a, b = sorted(random.sample(range(len(p1)), 2))
    segment = p1[a:b]
    enfant = [v for v in p2 if v not in segment]
    enfant[a:a] = segment
    return enfant


def crossover_uniforme(p1, p2):
    enfant = []
    for i in range(len(p1)):
        if random.random() < 0.5:
            gene = p1[i]
        else:
            gene = p2[i]
        if gene not in enfant:
            enfant.append(gene)
    for v in p1:
        if v not in enfant:
            enfant.append(v)
    return enfant


# ================================
#   Mutation
# ================================
def mutation_swap(individu):
    i, j = random.sample(range(len(individu)), 2)
    individu[i], individu[j] = individu[j], individu[i]


# ================================
#   Paramètres de l'AG
# ================================
matrice = [
    [0, 2, 2, 7, 15, 2, 5, 7, 6, 5],
    [2, 0, 10, 4, 7, 3, 7, 15, 8, 2],
    [2, 10, 0, 1, 4, 3, 3, 4, 2, 3],
    [7, 4, 1, 0, 2, 15, 7, 7, 5, 4],
    [15, 7, 4, 2, 0, 7, 3, 2, 2, 7],
    [2, 3, 3, 15, 7, 0, 1, 7, 2, 10],
    [5, 7, 3, 7, 3, 1, 0, 1, 2, 7],
    [7, 15, 4, 7, 2, 7, 1, 0, 1, 2],
    [6, 8, 2, 5, 2, 2, 2, 1, 0, 15],
    [5, 2, 3, 4, 7, 10, 7, 2, 15, 0]
]

nb_villes = len(matrice)
taille_population = 10
nb_generations = 200
p_croisement = 0.8
p_mutation = 0.2

# ================================
#   Initialisation de la population
# ================================
population = []
for _ in range(taille_population):
    ind = list(range(nb_villes))
    random.shuffle(ind)
    population.append(ind)

# ================================
#   Boucle principale AG
# ================================
for gen in range(nb_generations):
    nouvelle_population = []
    while len(nouvelle_population) < taille_population:
        parent1 = selection_rang(population, matrice)
        parent2 = selection_rang(population, matrice)

        # Croisement aléatoire parmi les 3 types
        if random.random() < p_croisement:
            type_cross = random.choice([1, 2, 3])
            if type_cross == 1:
                enfant = crossover_1_point(parent1, parent2)
            elif type_cross == 2:
                enfant = crossover_2_point(parent1, parent2)
            else:
                enfant = crossover_uniforme(parent1, parent2)
        else:
            enfant = parent1[:]

        # Mutation
        if random.random() < p_mutation:
            mutation_swap(enfant)

        nouvelle_population.append(enfant)

    population = sorted(nouvelle_population, key=lambda x: calculer_distance_totale(x, matrice))[:taille_population]

# ================================
#   Résultat final
# ================================
meilleur = min(population, key=lambda x: calculer_distance_totale(x, matrice))
meilleure_distance = calculer_distance_totale(meilleur, matrice)

print("🏆 Meilleure solution trouvée :", meilleur)
print("🚗 Distance minimale :", meilleure_distance)

# ================================
#   Affichage du trajet optimal
# ================================
coords = {
    0: (0, 0), 1: (2, 3), 2: (5, 1), 3: (7, 5), 4: (9, 2),
    5: (4, 7), 6: (1, 6), 7: (8, 8), 8: (3, 9), 9: (6, 0)
}

x = [coords[v][0] for v in meilleur] + [coords[meilleur[0]][0]]
y = [coords[v][1] for v in meilleur] + [coords[meilleur[0]][1]]

plt.figure(figsize=(6, 5))
plt.plot(x, y, '-o', color='blue')
for i, v in enumerate(meilleur):
    plt.text(coords[v][0] + 0.1, coords[v][1] + 0.1, f"Ville {v}", fontsize=9)
plt.title("Trajet optimal trouvé (AG avec sélection par rang)")
plt.xlabel("X")
plt.ylabel("Y")
plt.grid(True)
plt.show()
