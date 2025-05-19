import random
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
def simulate_slotted_aloha(num_slots, n, p, logging = False):
    nodes = {i: 0 for i in range(0, n)}
    successes_numb = 0
    efficiency = 0
    for i in range(1, num_slots + 1):
        hitcount = 0
        hitters = []
        for node in nodes:
            hit = random.random() <= p
            nodes[node] += hit
            hitcount += hit
            if hit: hitters.append(node)
        successes_numb += 1 if hitcount == 1 else 0
        if logging and i % 10 == 0:
            print(f"Slot {i}: {'Success' if hitcount == 1 else 'idle' if hitcount == 0  else 'collision'}")
            for node in nodes:
                print(f"\t Node {node}: {'tx' if node in hitters else 'idle'}, idle_cnt: {i - nodes[node]}, tx_cnt: {nodes[node]}")
    efficiency = successes_numb / num_slots
    if logging:
        print(f"n={n}, p={p}, efficiency={efficiency}")
    return efficiency

def efficiency_formula(n, p):
    return n * p * (1 - p)**(n - 1)

slots = 100000
ns = [1, 2, 5, 10, 20, 50, 100]
ps = [round(x * 0.01, 2) for x in range(0, 101)]
plt.figure(figsize=(16, 10))
for n in ns:
    ys = []
    yst = []
    for p in ps:
        ys.append(simulate_slotted_aloha(slots, n, p))
        yst.append(efficiency_formula(n, p))
    plt.plot(ps,ys, label = f"n={n}-simulation")
    plt.plot(ps, yst, linestyle = 'None', marker = 'o',  markevery = 10, label = f"n={n}-theory")
plt.xlabel("p")
plt.ylabel("Efficiency")
plt.title("Efficiency vs Probability of transmission")
plt.legend()
plt.tight_layout()
plt.show()
