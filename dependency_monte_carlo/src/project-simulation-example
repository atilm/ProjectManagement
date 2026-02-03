import numpy as np
import networkx as nx
from scipy.stats import triang, norm

# Define DAG: tasks with predecessors and duration distributions
tasks = {
    "A": {"pred": [], "dist": ("triang", {"c": 0.5, "loc": 3, "scale": 3})},   # mode at mid of [3,6]
    "B": {"pred": ["A"], "dist": ("norm", {"loc": 5, "scale": 1})},
    "C": {"pred": ["A"], "dist": ("triang", {"c": 0.3, "loc": 2, "scale": 4})},
    "D": {"pred": ["B","C"], "dist": ("norm", {"loc": 4, "scale": 0.8})},
}

def sample_duration(kind, params, rng):
    if kind == "triang":
        return float(triang(**params).rvs(random_state=rng))
    if kind == "norm":
        return float(max(0.0, norm(**params).rvs(random_state=rng)))
    raise ValueError("unknown dist")

def simulate_once(rng):
    G = nx.DiGraph()
    for t, info in tasks.items():
        G.add_node(t, dur=sample_duration(*info["dist"], rng=rng))
        for p in info["pred"]:
            G.add_edge(p, t)
    # Longest path duration (CPM): compute earliest finish times
    topo = list(nx.topological_sort(G))
    # EF: "Earliest Finish"
    EF = {}
    for t in topo:
        preds = list(G.predecessors(t))
        start = max((EF[p] for p in preds), default=0.0)
        EF[t] = start + G.nodes[t]["dur"]
    project_duration = max(EF.values())
    # Identify critical path by backtracking from max EF
    end = max(EF, key=EF.get)
    crit = [end]
    cur = end
    while True:
        preds = list(G.predecessors(cur))
        if not preds:
            break
        # pick predecessor with EF equal to start time
        start_time = EF[cur] - G.nodes[cur]["dur"]
        cand = [p for p in preds if np.isclose(EF[p], start_time)]
        cur = cand[0] if cand else preds[0]
        crit.append(cur)
    crit_path = list(reversed(crit))
    return project_duration, crit_path

rng = np.random.default_rng(123)
N = 10000
durations = []
for _ in range(N):
    d, cp = simulate_once(rng)
    durations.append(d)

print(f"Mean duration: {np.mean(durations):.2f}")
print(f"P50: {np.percentile(durations,50):.2f}, P80: {np.percentile(durations,80):.2f}, P95: {np.percentile(durations,95):.2f}")