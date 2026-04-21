import random

class Coinflip:

    @classmethod
    def flipcoin(cls, repeats=1):
        if repeats == 1:
            if random.random() < 0.5:
                print("heads")
            else:
                print("tails")

        heads = 0
        tails = 0
        for _ in range(repeats):
            if random.random() < 0.5:
                heads += 1
            else:
                tails += 1

        heads_prob = heads / repeats
        tails_prob = tails / repeats

        print(f"Heads: {heads} ({heads_prob:.2%})")
        print(f"Tails: {tails} ({tails_prob:.2%})")


