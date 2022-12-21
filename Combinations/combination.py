import random
import csv

def combination():
    f = open('ingredients2.csv', 'r')
    ingredients = list(f.readline().split(";"))[:]
    final_ingredients = []
    spisok = []
    for i in range(0, 588):
        spisok.append(list(int(x) for x in f.readline().split(";"))[:])
    first_ingredient = random.randint(0, 587)
    if max(spisok[first_ingredient]) < 10:
        while max(spisok[first_ingredient]) < 10:
            first_ingredient = random.randint(0, 588)
    final_ingredients.append(first_ingredient)
    final_ingredients.append(spisok[first_ingredient].index(max(spisok[first_ingredient])))
    #print(ingredients[first_ingredient], ingredients[final_ingredients[1]])
    last_ingredient = final_ingredients[1]
    while len(final_ingredients) < 5:
        flag = True
        add_ingredient = spisok[last_ingredient].index(max(spisok[last_ingredient]))
        ost = spisok[last_ingredient]
        while flag:
            n = 0
            for i in range(0, len(final_ingredients)):
                if spisok[add_ingredient][final_ingredients[i]] > 0:
                   n += 1
            if add_ingredient in final_ingredients or n != len(final_ingredients):
                ost[add_ingredient] = 0
                add_ingredient = spisok[last_ingredient].index(max(ost))
            else:
                flag = False
                final_ingredients.append(spisok[last_ingredient].index(max(ost)))
        last_ingredient = final_ingredients[-1]
    for elem in final_ingredients:
        print(ingredients[elem])

combination()