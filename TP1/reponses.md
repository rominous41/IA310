1-list comprehensions non maitrisées. On modifie l'état interne de l'agent attaqué par le lycanthrope pour le marquer comme contaminé. Nous avons vu en cours qu'un agent peut interagir avec les autres agents, et c'est ce qui est fait pour la contamination. Cette méthode correspond donc bien à la définition d'agent vue en cours

Je n'ai pas réussi à supprimer les agents après leur mort dans le jeu. J'ai donc utilisé une variable interne dead pour les faire virtuellement disparaître (invisible et sans interaction)

2-Le système semble converger vers uniquement des lycanthropes en environ 2000 itérations. La présence ou l'absence d'apothicaire ne modifie pas ce résultat (qualitativement, l'apothicaire ne rencontre jamais de lycanthrope non transformé.). Les 2 chasseurs ont un trop faible impact pour contenir la contagion. En effet, ils sont contaminés par les loups-garous qu'ils abattent. L'augmentation du nombre d'apothicaires et de chasseurs réduit la vitesse de propagation voir a une éradication des loups garou (scénario avec 5 loups garou 10 apothicaires et 10 chasseurs).

3-fonctions lambda non maitrisées. La courbe obtenue confirme bien l'observation précédente (la disparition de la population saine au profit des loups-garous)
![standard configuration](https://user-images.githubusercontent.com/62742264/149177813-8b0b538b-69c5-4aec-981e-449932c583e1.png)

4- Etude de l'impact du role de l'apothicaire (sans chasseur). On remarque que l'augmentation du ration d'apothicaire dans la population diminue marginalement la vitesse de contamination (les guérisons sont des événements rares)
![half cleric](https://user-images.githubusercontent.com/62742264/149177642-552fbcb3-77d8-4fac-a2fe-5ac50cd79b66.png)
Etude du chasseur (pas d'apothicaire) : Les chasseurs seuls ne peuvent pas endiguer la propagation. En effet, un chasseur contaminant un loup-garou est automatiquement contaminé, ce qui empêche la restauration du taux de population saine.
![half hunter](https://user-images.githubusercontent.com/62742264/149177704-4310723b-1db1-4fec-b81d-7c5359ac91bf.png)

5-La portée des interactions est cruciale. En effet des chasseurs ayant une meilleure portée pourraient abattre les loups-garous sans être contaminé et ainsi obtenir un meilleur contrôle la population. La probabilité de transformation du loup-garou est aussi à prendre en compte. En effet la probabilité qu'un apothicaire soigne un villageois serait augmentée si la transformation était moins probable

6-D'après les expériences, précédentes, le chasseur ne pourra tuer que quelques loups-garous avant de se transformer, car la probabilité de guérison est faible même avec une grande proportion d'apothicaire. On peut donc s'attendre à une légère baisse de la population globale puis à une victoire des loup garous en 2000 à 3000 itérations.

7-On observe une victoire dans tous les cas des loups-garous au bout des 1000 itérations. La variation du nombre d'apothicaires n'a pas d'influence sur le résultat. Par contre cette méthode ne nous permet pas de comparer les vitesses de propagation et de vérifier si une augmentation du nombre d'apothicaires diminue la vitesse de transmission
