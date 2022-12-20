import random

def combination():
    f = open('ingredients_after_change.txt', 'r')
    ingredients = []
    for line in f:
        add = line.split(';')
        ingredients += add
    print(*random.sample(ingredients, 5), sep=', ')

combination()