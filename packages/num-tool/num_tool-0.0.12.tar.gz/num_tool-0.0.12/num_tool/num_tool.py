import random

def random_num_list(a, b, l):
    ls = []
    for i in range(l):
        ls.append(random.randint(a, b))
    return ls