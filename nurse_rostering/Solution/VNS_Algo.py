import time
import random

from model.problem import Problem


class VNS:
    def __init__(self, problem):
        self.problem = problem

    #  Fonction d'évaluation de la solution
    def evaluate(self, solution):
        total_penalty = 0

        for staff_member in self.problem.staff:
                for day in range(self.problem.days_count):
                    # Pénalité pour ne pas assigner un employe à un poste préféré
                    if solution[staff_member.id][day] not in staff_member.shift_wish_penalties[day]:
                        total_penalty += 1

                    # Autres critères d'évaluation

        return total_penalty


    def generate_random_solution(self):
        #  Générer une solution initiale aléatoire
        pass

    def generate_neighbor(self, solution):
        # Générer un voisin en inversant la position de deux éléments dans la séquence
        neighbor = solution[:]
        idx1, idx2 = random.sample(range(len(solution)), 2)
        neighbor[idx1], neighbor[idx2] = neighbor[idx2], neighbor[idx1]
        return neighbor
    
    #  Fonction de la recherche locale (voisinage)
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

    # Fonction de l'algorithme VNS 
    def variable_neighborhood_search(self, max_time, k_max):
        start_time = time.time()
        current_solution = self.generate_random_solution()
        best_solution = current_solution.copy()

        while time.time() - start_time < max_time:
            k = 1
            while k <= k_max:
                new_solution = self.local_search(current_solution, k)
                current_eval = self.evaluate(current_solution)
                new_eval = self.evaluate(new_solution)

                if new_eval < current_eval:
                    current_solution = new_solution.copy()
                    k = 1  # Re-initialize k to 1
                    if new_eval < self.evaluate(best_solution):
                        best_solution = new_solution.copy()
                else:
                    k += 1

        return best_solution



# Exemple d'utilisation
if __name__ == "__main__":
    # Création d'une instance du problème
    problem_instance = Problem(days_count=7)

    # Initialisation de la métaheuristique VNS
    vns = VNS(problem_instance)

    # Paramètres de la VNS
    max_execution_time = 60  # en secondes
    max_k = 5   #max d'iteration

    # Application de la VNS
    best_solution = vns.variable_neighborhood_search(max_execution_time, max_k)

    # Affichage de la solution optimale
    print("Best Solution:", best_solution)
    print("Best Evaluation:", vns.evaluate(best_solution))
