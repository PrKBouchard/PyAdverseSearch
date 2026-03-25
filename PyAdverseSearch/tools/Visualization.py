import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button


class Visualization:
    def __init__(self, root_node, selection_method):
        self.root_node = root_node
        self.current_node = root_node
        self.visited_nodes = set([root_node])  # Ajouter la racine directement
        self.visited_edges = set()
        self.history = [root_node]  # Liste des étapes parcourues
        self.selection_method = selection_method  # Méthode de sélection des nœuds
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.3)
        self.draw_graph()
        self.create_buttons()

    def draw_graph(self):
        self.ax.clear()
        G = nx.DiGraph()

        # Ajouter toutes les connexions des nœuds visités et leurs enfants
        for node in self.visited_nodes:
            node.expand()  # Générer dynamiquement les enfants si ce n'est pas déjà fait
            for child in node.children:
                G.add_edge(str(node.state), str(child.state))
                if child in self.visited_nodes:
                    self.visited_edges.add((str(node.state), str(child.state)))

        # Marquer les nœuds et arêtes réellement explorés
        node_colors = {n: "green" if any(obj.state == n for obj in self.visited_nodes) else "lightblue" for n in
                       G.nodes}
        edge_colors = {edge: "green" if edge in self.visited_edges else "gray" for edge in G.edges}

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color=[node_colors[n] for n in G.nodes],
                edge_color=[edge_colors[e] for e in G.edges], node_size=2000, font_size=12, width=2, ax=self.ax)
        plt.draw()

    def next_node(self, event):
        if not self.current_node.children:
            self.current_node.expand()  # Générer les enfants si ce n'est pas déjà fait
        if self.current_node.children:
            self.current_node = self.selection_method(self.current_node.children)
            self.history.append(self.current_node)  # Ajouter à l'historique
            self.visited_nodes.add(self.current_node)  # Marquer comme visité
            self.draw_graph()

    def create_buttons(self):
        ax_next = plt.axes([0.8, 0.05, 0.1, 0.075])
        self.btn_next = Button(ax_next, 'Next')
        self.btn_next.on_clicked(self.next_node)


class Node:
    def __init__(self, state, parent=None, depth=0):
        self.state = state
        self.parent = parent
        self.depth = depth
        self.valuation = None
        self.children = []  # Liste des successeurs

    def expand(self):
        """Génère tous les états successeurs et les ajoute comme enfants."""
        if not self.children:  # Éviter de ré-expanser
            for action in self.state.possible_actions():
                new_state = self.state.apply_action(action)
                child_node = Node(new_state, parent=self, depth=self.depth + 1)
                self.children.append(child_node)

    def is_terminal(self):
        """Retourne True si cet état est terminal."""
        return self.state.is_terminal()


# Exemple de fonction de sélection des nœuds
def select_first(children):
    return children[0] if children else None


# Simulation d'un état de jeu
import string

class GameState:
    def __init__(self, name, depth=3):
        self.name = name
        self.depth = depth  # Nombre de niveaux d'expansion

        # Générer dynamiquement 3 nouvelles actions pour chaque état sauf si la profondeur est atteinte
        if self.depth > 0:
            self.actions = [name + c for c in string.ascii_uppercase[:3]]  # Ex: "A" -> ["AB", "AC", "AD"]
        else:
            self.actions = []  # État terminal si la profondeur est atteinte

    def possible_actions(self):
        return self.actions

    def apply_action(self, action):
        return GameState(action, self.depth - 1)  # Réduire la profondeur à chaque expansion

    def is_terminal(self):
        return len(self.actions) == 0

    def __str__(self):
        return self.name



# Création de l'état initial avec des actions possibles
initial_state = GameState("A", 5)
root = Node(initial_state)

vis = Visualization(root, select_first)
plt.show()
