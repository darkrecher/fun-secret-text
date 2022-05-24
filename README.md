# fun-secret-text

Texte secret se révélant au fur et à mesure que le joueur obtient les clés. Utile pour des jeux d'énigmes, chasse aux trésors, escape room, etc..


## Générateur de puzzle avec des clés inspirés de Harry Potter

C'est dans le dossier `harry_potter_image_key_generator`.

Il faut open-cv : `pip install open-cv`

Et ensuite : `python harry_key_generator.py`

Le script générera les images qui sont dans le sous-dossier generated_images (en 2 fois plus grand, je les ais retaillées pour que ça prenne moins de place).

Il s'agit d'une sorte de puzzle inspiré du jeu Dobble. Chaque groupe de 4 clés a une clé exactement identique avec les 4 groupes adjacents.

Petit exemple :

```

    |-------------|-------------|
    | clé_A clé_B | clé_X clé_Y |
    |             |             |
    | clé_C clé_D | clé_D clé_Z |
    | ----------- | ----------- |
    | clé_E clé_F | clé_Y clé_E |
    |             |             |
    | clé_B clé_G | clé_P clé_Q |
    | ----------- | ----------- |

```

La position des clés dans le groupe de 4 est aléatoire. Dans l'exemple ci-dessus, c'est la "clé_D" qui est en commun aux deux premiers groupe. Elle est en 4ème position dans le premier groupe, et en 3ème dans le deuxième groupe. Ce n'est pas significatif, et ça aurait pu être d'autres possibilités.

Les planches sont disposées comme ceci :

```
    p_00 p_03 p_06 p_09
    p_01 p_04 p_07 p_10
    p_02 p_05 p_08 p_11
```

Pour les planches p_02 p_05 p_08 p_11, les groupes de clés de la première ligne sont des doublons des groupes juste au-dessus (parce que j'ai codé mon script à l'arrache).

Dans les fichiers du dossier "generated_images", ces groupes de clés ont déjà été supprimés.

Et maintenant, vous pouvez découper tous les groupes de 4 clés, vous les mélangez, et ça fait un super puzzle ! Amusez-vous bien !

