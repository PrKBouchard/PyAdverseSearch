import matplotlib.pyplot as plt

class SearchProfiler:
    def __init__(self, solver):
        self.solver = solver
        self.history = []

    def capture_metrics(self, move_name):
        stats = {
            "move": move_name,
            "nodes": self.solver.nodes_visited,
            "cutoffs": self.solver.cutoffs,
            "cache_size": len(self.solver.transposition_table)
        }
        self.history.append(stats)
        
        self.solver.nodes_visited = 0
        self.solver.cutoffs = 0

    def plot(self):
        moves = [h["move"] for h in self.history]
        nodes = [h["nodes"] for h in self.history]
        cutoffs = [h["cutoffs"] for h in self.history]

        fig, ax1 = plt.subplots(figsize=(10, 6))

        ax1.set_xlabel('Move Number')
        ax1.set_ylabel('Nodes Visited', color='tab:blue')
        ax1.plot(moves, nodes, color='tab:blue', marker='o', label='Nodes')
        
        ax2 = ax1.twinx()
        ax2.set_ylabel('Cutoffs', color='tab:red')
        ax2.plot(moves, cutoffs, color='tab:red', linestyle='--', marker='x', label='Cutoffs')

        plt.title("Search Complexity per Move")
        fig.tight_layout()
        plt.show()