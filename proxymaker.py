import random
proxies=open("proxies.txt").read().split("\n")
def get_random_proxy():
    return random.choice(proxies)
