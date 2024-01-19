# Application d'une métaheuristique sur le problème de nurse rostering

> Le but de ce projet est d'étudier des approches métaheuristiques au problème NP-difficile de nurse rostering, d'en implémenter une, et de la confronter aux instances proposées par *Curtois et Qu (2014)*[^1].

## Solution

Notre solution est basée sur l'article de *Rahimian et al. (2017)*[^2], qui décrit une métaheuristique hybride basée sur l'algorithme Variable Neighborhood Search (VNS) utilisant la programmation linéaire en nombre entiers (Integer Programming, IP) comme fonction de shaking.

1. Générer une solution initiale en utilisant un algorithme à définir
2. Utiliser une fonction de recherche locale à définir pour améliorer la solution initiale
3. Exploitation et exploration par le IP solver à partir de cette solution, en gardant toujours la meilleure solution trouvée
4. Retour à 2. tant que le critère d'arrêt n'est pas rencontré
5. Utiliser la recherche locale pour améliorer une dernière fois la solution

## Génération d'une solution initiale

Greedy algorithm for generating an initial solution

- créer solution vide
- itérer aléatoirement parmi le staff ; on considère 1 planning par staff
- `SetDaysOff()` : bloquer les jours de repos demandés par le staff et empêcher d'assigner un poste à cet endroit
- `AssignWorkDays()` : assigner aléatoirement les jours travaillés
- **Check** : max number of workdays, min and max number of consecutive shift types (including days off),
- `AssignShifts()` : assigner aléatoirement les shifts aux jours travaillés
- **Check** : max number of shift types, avoid blocking shift types
- Pour vérifier les contraintes restantes (max number of worked weekends + min/max total time of assigned shifts) :
- Calculer pénalités $p_1$ et $p_2$
- Si $p_1 + p_2 > 0$ : détruire planning (pour staff actuel) et recommencer
- répéter pour tous les staff


## Références

[^1]: Tim Curtois et Rong Qu : **Computational results on new staff scheduling benchmark
instances.** *ASAP Res. Group, School Comput. Sci., Univ. Nottingham, Nottingham, UK,
Tech. Rep*, 2014
[^2]: Erfan Rahimian, Kerem Akartunalı et John Levine : **A hybrid integer programming
and variable neighbourhood search algorithm to solve nurse rostering problems.** *European
Journal of Operational Research*, 258(2):411–423, 2017.