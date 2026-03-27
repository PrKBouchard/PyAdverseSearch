import time
import matplotlib.pyplot as plt
from PyAdverseSearch.classes.negamax import NegamaxSolver
from PyAdverseSearch.classes.node import Node

class AIvsAIBenchmark:
    def __init__(self, game_generator, solver1, solver2):
        self.game_generator = game_generator
        self.solver1 = solver1
        self.solver2 = solver2
        self.results = {"AI_1_wins": 0, "AI_2_wins": 0, "draws": 0}

    def play_single_game(self, ai1_starts=True):
        game = self.game_generator(ai1_starts)
        state = game.state
        
        while not game.is_terminal(state):
            current_solver = self.solver1 if state.player == 'MAX' else self.solver2
            
            root_node = Node(state=state)
            best_board = current_solver.get_best_move(root_node)
            
            successors = state._generate_successors()
            state = next((s for s in successors if s.board == best_board), None)
            
            if state is None: break

        winner = game.winner_function(state)
        if winner == 'MAX': self.results["AI_1_wins"] += 1
        elif winner == 'MIN': self.results["AI_2_wins"] += 1
        else: self.results["draws"] += 1

    def run_tournament(self, num_games=10):
        print(f"Starting : {num_games} games...")
        for i in range(num_games):
            # Alternate who starts to keep it fair
            self.play_single_game(ai1_starts=(i % 2 == 0))
            print(f"Game {i+1}/{num_games} finished.")
        
        self.report()

    def report(self):
        print("\n--- RESULTS ---")
        for key, val in self.results.items():
            print(f"{key.replace('_', ' ').upper()}: {val}")
           
    
    def plot_results(self):
        """Generates a bar chart and a pie chart of the results."""
        labels = ['AI 1 (MAX)', 'AI 2 (MIN)', 'Draws']
        counts = [self.results["AI_1_wins"], self.results["AI_2_wins"], self.results["draws"]]
        colors = ['#4CAF50', '#F44336', '#9E9E9E'] # Green, Red, Grey

        # Create a figure with two subplots: Bar and Pie
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # 1. Bar Chart
        bars = ax1.bar(labels, counts, color=colors)
        ax1.set_title('Tournament Match Wins')
        ax1.set_ylabel('Number of Games')
        ax1.bar_label(bars, padding=3)

        # 2. Pie Chart
        # Only show labels for categories with at least 1 result
        ax2.pie(counts, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
        ax2.set_title('Win Distribution %')

        plt.tight_layout()
        print("Opening graph window...")
        plt.show()

    def report(self):
        print("\n" + "="*20)
        print("   FINAL RESULTS   ")
        print("="*20)
        for key, val in self.results.items():
            print(f"{key.replace('_', ' ').upper():<12}: {val}")
        
        if sum(self.results.values()) > 0:
            self.plot_results()