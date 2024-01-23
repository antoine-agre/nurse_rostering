import time
import random

from model.problem import Problem

class VND:
    def __init__(self, problem):
        self.problem = problem

    # Fonction d'évaluation de la solution
    def evaluate(self, solution):
        total_penalty = 0

        for staff_member in self.problem.staff:
            for day in range(self.problem.days_count):
                # Pénalité pour ne pas assigner un employé à un poste préféré
                if solution[staff_member.id][day] not in staff_member.shift_wish_penalties[day]:
                    total_penalty += 1

                # Autres critères d'évaluation

        return total_penalty

    def generate_random_solution(self):
        # Générer une solution initiale aléatoire
        pass

    def generate_neighbor(self, solution):
        # Générer un voisin en inversant la position de deux éléments dans la séquence
        neighbor = solution[:]
        idx1, idx2 = random.sample(range(len(solution)), 2)
        neighbor[idx1], neighbor[idx2] = neighbor[idx2], neighbor[idx1]
        return neighbor

    # Fonction de la recherche locale (voisinage)
    def local_search(self, solution, k_max):
        # Boucle pour effectuer la recherche locale jusqu'à k_max essais
        for k in range(k_max):
            # Générer un voisin de la solution actuelle
            neighbor_solution = self.generate_neighbor(solution)

            # Évaluer la qualité du voisin
            neighbor_quality = self.evaluate(neighbor_solution)

            # Comparer la qualité du voisin avec la solution actuelle
            if neighbor_quality < self.evaluate(solution):
                # Si le voisin est meilleur, mettre à jour la solution actuelle
                solution = neighbor_solution

        # Renvoyer la meilleure solution trouvée pendant la recherche locale
        return solution

    # Fonction de l'algorithme VND
    def variable_neighborhood_descent(self, max_k):
        # Initialisation de la liste pour stocker les solutions
        all_solutions = []
        current_solution = self.generate_random_solution()

        for k in range(1, max_k + 1):
            new_solution = self.local_search(current_solution, k)
            current_eval = self.evaluate(current_solution)
            new_eval = self.evaluate(new_solution)

            if new_eval < current_eval:
                current_solution = new_solution.copy()
                all_solutions.append(current_solution.copy())  # Stocker la nouvelle solution
                #retouner la liste des solutions à chaque fois. Au cas où le nombre d'itération est grand, on garde la liste des solutions
                return all_solutions   

        return current_solution, all_solutions


# Exemple d'utilisation
if __name__ == "__main__":
    # Création d'une instance du problème
    problem_instance = Problem(days_count=7)

    # Initialisation de la métaheuristique VND
    vnd = VND(problem_instance)

    # Paramètre de la VND
    max_k = 5   # max d'itérations pour la recherche locale

    # Application de la VND
    best_solution = vnd.variable_neighborhood_descent(max_k)

    # Affichage de la solution optimale
    print("Best Solution:", best_solution)
    print("Best Evaluation:", vnd.evaluate(best_solution))
