# Application d'une métaheuristique sur le problème de nurse rostering
> *AGRÉ Antoine, ALLAGLO Giovanni, BENAICHA Khaoula, COLY François Xavier, YU Guo*
>
>**INSA Hauts-de-France, FISE 5A ICy, Module : Métaheuristiques**

Le but de ce projet est d'étudier des approches métaheuristiques au problème NP-difficile de nurse rostering, d'en implémenter une, et de la confronter aux instances proposées par *Curtois et Qu (2014)*[^1].

## Exécution

Le package peut être exécuté de la façon suivante :

```cmd
py -m nurse_rostering
```

ce qui exécutera le point d'entrée `__main__.py` et lancera une batterie de tests.

## Solution

Notre solution est basée sur l'article de *Rahimian et al. (2017)*[^2], qui décrit une métaheuristique hybride basée sur l'algorithme Variable Neighborhood Search (VNS) utilisant la programmation linéaire en nombre entiers (Integer Programming, IP) comme fonction de shaking.

1. Générer une solution initiale en utilisant un algorithme à définir
2. Utiliser une fonction de recherche locale à définir pour améliorer la solution initiale
3. Exploitation et exploration par le IP solver à partir de cette solution, en gardant toujours la meilleure solution trouvée
4. Retour à 2. tant que le critère d'arrêt n'est pas rencontré
5. Utiliser la recherche locale pour améliorer une dernière fois la solution

## Références

[^1]: Curtois, T., Qu, R. (2014). *Computational results on new staff scheduling benchmark instances* (Technical Report). ASAP Research Group, School of Computer Science, University of Nottingham.
[^2]: Rahimian, E., Akartunalı, K., Levine, J. (2017). A hybrid Integer Programming and Variable Neighbourhood Search algorithm to solve Nurse Rostering Problems. *European Journal of Operational Research*, 258 (2017), 411–423. https://doi.org/10.1016/j.ejor.2016.09.030