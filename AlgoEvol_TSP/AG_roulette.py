import random
import matplotlib.pyplot as plt

# ---------- FONCTIONS DE BASE ----------
def calculer_distance_totale(solution, matrice):
    d = 0
    for i in range(len(solution) - 1):
        d += matrice[solution[i]][solution[i + 1]]
    d += matrice[solution[-1]][solution[0]]
    return d

def selection_roulette(population, matrice):
    fitness = []
    for indiv in population:
        d = calculer_distance_totale(indiv, matrice)
        fitness.append(1 / (d + 1))

    total_fit = sum(fitness)
    seuil = random.random() * total_fit

    cumul = 0
    for i, indiv in enumerate(population):
        cumul += fitness[i]
        if cumul >= seuil:
            return indiv[:]

    return population[-1][:]

# ---------- 3 TYPES DE CROISEMENTS ----------
def crossover_1_point(p1, p2):
    point = random.randint(1, len(p1) - 2)
    enfant = p1[:point] + [v for v in p2 if v not in p1[:point]]
    return enfant

def crossover_2_point(p1, p2):
    a, b = sorted(random.sample(range(len(p1)), 2))
    milieu = p1[a:b]
    reste = [v for v in p2 if v not in milieu]
    enfant = reste[:a] + milieu + reste[a:]
    return enfant

def crossover_OX(p1, p2):
    a, b = sorted(random.sample(range(len(p1)), 2))
    enfant = [None] * len(p1)
    enfant[a:b] = p1[a:b]
    pos = b
    for v in p2:
        if v not in enfant:
            enfant[pos % len(p1)] = v
            pos += 1
    return enfant

# ---------- MUTATION ----------
def mutation(individu):
    i, j = random.sample(range(len(individu)), 2)
    individu[i], individu[j] = individu[j], individu[i]
    return individu

# ---------- ALGORITHME GÉNÉTIQUE ----------
def algo_genetique(matrice, taille_pop=20, generations=100, Pc=0.8, Pm=0.2):
    nb_villes = len(matrice)

    # Initialisation
    population = []
    for _ in range(taille_pop):
        ind = list(range(nb_villes))
        random.shuffle(ind)
        population.append(ind)

    meilleur_distance = []
    meilleur_indiv = None

    for g in range(generations):
        nouvelle_population = []

        for _ in range(taille_pop):
            # Sélection de deux parents
            p1 = selection_roulette(population, matrice)
            p2 = selection_roulette(population, matrice)

            # Croisement (selon probabilité)
            if random.random() < Pc:
                type_croisement = random.choice(["1point", "2points", "OX"])
                if type_croisement == "1point":
                    enfant = crossover_1_point(p1, p2)
                elif type_croisement == "2points":
                    enfant = crossover_2_point(p1, p2)
                else:
                    enfant = crossover_OX(p1, p2)
            else:
                enfant = p1[:]

            # Mutation (selon probabilité)
            if random.random() < Pm:
                enfant = mutation(enfant)

            nouvelle_population.append(enfant)

        population = nouvelle_population

        # Évaluer le meilleur de la génération
        distances = [calculer_distance_totale(ind, matrice) for ind in population]
        best_gen = min(distances)
        meilleur_distance.append(best_gen)
        meilleur_indiv = population[distances.index(best_gen)]

        print(f"Génération {g+1}: meilleure distance = {best_gen}")

    # Affichage graphique de la convergence
    plt.plot(meilleur_distance)
    plt.xlabel("Génération")
    plt.ylabel("Distance du meilleur individu")
    plt.title("Évolution de la meilleure solution")
    plt.show()

    return meilleur_indiv, meilleur_distance[-1]

# ---------- MATRICE DES DISTANCES ----------
matrice = [
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

# ---------- EXÉCUTION ----------
best, dist = algo_genetique(matrice, taille_pop=20, generations=100, Pc=0.9, Pm=0.2)
print("\nMeilleure solution trouvée :", best)
print("Distance totale :", dist)
