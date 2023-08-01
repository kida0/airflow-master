import random

def select_fruit():
    fruit = ["APPLE", "BANANA", "ORANGE", "AVOCADO"]
    rand_int = random.randint(0, len(fruit)-1)
    print(fruit[rand_int])
    