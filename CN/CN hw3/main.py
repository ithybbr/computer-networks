import random
import argparse
from matplotlib import pyplot as plt
def simulate_slotted_aloha(num_slots, n, p, logging = False):
    #efficiency_formula = n * p * (1 - p)**(n - 1)
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
    print(f"n={n}, p={p}, efficiency={efficiency}")
    return efficiency
def plotter():
    slots = 100000
    ns = [1, 2, 5, 10, 20, 50, 100]
    ps = [round(x * 0.01, 2) for x in range(0, 101)]
    for n in ns:
        ys = []
        for p in ps:
            ys.append(simulate_slotted_aloha(slots, n, p))
        plt.plot(ps,ys)
    plt.show()
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("num_slots", type = int, help = "total number of slots")
    parser.add_argument("n", type = int, help = "number of nodes in slotted Aloha network")
    parser.add_argument("p", type = float, help = "probability that the node transmits a frame in a slot")
    parser.add_argument("--logging", action = "store_true", help = "prints log")
    args = parser.parse_args()
    simulate_slotted_aloha(args.num_slots, args.n, args.p, args.logging)