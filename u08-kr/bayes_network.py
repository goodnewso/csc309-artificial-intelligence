"""Unit 8: probabilistic reasoning with a small Bayesian network.

Malaria (M) and typhoid (T) can each cause fever (F). Given that a
patient has a fever, how likely is each disease? Inference by
enumerating every combination. The numbers are for teaching only.
"""
from itertools import product

P_M, P_T = 0.10, 0.03                       # prior probabilities
P_F = {(True, True): 0.98, (True, False): 0.85,   # P(fever | M, T)
       (False, True): 0.80, (False, False): 0.05}


def joint(m, t, f):
    p = (P_M if m else 1 - P_M) * (P_T if t else 1 - P_T)
    pf = P_F[(m, t)]
    return p * (pf if f else 1 - pf)


def query(var, evidence):
    """P(var = True | evidence), summing the joint distribution."""
    num = den = 0.0
    for m, t in product([True, False], repeat=2):
        world = {"M": m, "T": t, "F": True}
        if any(world[k] != v for k, v in evidence.items()):
            continue
        p = joint(m, t, True)
        den += p
        if world[var]:
            num += p
    return num / den


print(f"P(malaria)              = {P_M:.3f}")
print(f"P(malaria | fever)      = {query('M', {'F': True}):.3f}")
print(f"P(typhoid | fever)      = {query('T', {'F': True}):.3f}")
print(f"P(typhoid | fever, malaria) = "
      f"{query('T', {'F': True, 'M': True}):.3f}  (explaining away)")
