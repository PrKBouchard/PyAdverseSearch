import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

class TreeVisualizer:
    def __init__(self, tracer):
        self.history = tracer.history
        self.index = 0
        self.G = nx.DiGraph()
        
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        plt.subplots_adjust(bottom=0.2)
        
        # Button UI
        ax_next = plt.axes([0.8, 0.05, 0.1, 0.075])
        self.btn_next = Button(ax_next, 'Next >')
        self.btn_next.on_clicked(self.update)

    def _get_pos(self):
        """Génère un layout en arbre centré par profondeur."""
        from collections import defaultdict
        
        # 1. Grouper les noeuds par profondeur
        depth_nodes = defaultdict(list)
        for node_id in self.G.nodes:
            d = self.G.nodes[node_id]['depth']
            depth_nodes[d].append(node_id)
        
        # 2. Calculer les positions centrées
        pos = {}
        for depth, nodes in depth_nodes.items():
            n = len(nodes)
            for i, node_id in enumerate(nodes):
                x = (i - (n - 1) / 2) * 2.5  # espacement de 2.5, centré sur 0
                pos[node_id] = (x, -depth * 3)
        
        return pos

    def update(self, event):
        if self.index < len(self.history):
            step = self.history[self.index]
            node_id = step['id']
            
            # Add node if it's an entry
            if not self.G.has_node(node_id):
                self.G.add_node(node_id, **step)
                if step['parent']:
                    self.G.add_edge(step['parent'], node_id)
            
            # Update attributes (like value or cutoff status)
            self.G.nodes[node_id].update(step)
            
            self.index += 1
            self.render()

    def render(self):
        self.ax.clear()
        pos = self._get_pos()

        visible_nodes = list(self.G.nodes)[-20:]
        subgraph = self.G.subgraph(visible_nodes)
        pos_visible = {n: pos[n] for n in visible_nodes if n in pos}

        # Guard — nothing to draw yet
        if not subgraph.nodes:
            plt.draw()
            return

        colors = []
        for n in subgraph.nodes:
            node = subgraph.nodes[n]
            value = node.get('value')
            color = node.get('color')
            if node.get('best_move'):
                colors.append('gold')
            elif value is None:
                colors.append('skyblue')
            else:
                signed = value if color == 'MAX' else -value
                if signed > 0:   colors.append('lightgreen')
                elif signed < 0: colors.append('salmon')
                else:            colors.append('skyblue')

        labels = {
            n: (
                f"{subgraph.nodes[n]['label']}\n"
                f"{subgraph.nodes[n]['color']} v={subgraph.nodes[n]['value']}"
            )
            for n in subgraph.nodes
        }

        nx.draw(subgraph, pos_visible, labels=labels, with_labels=True,
                node_color=colors, node_size=2000, font_size=7, ax=self.ax)

        best = [n for n in subgraph.nodes if subgraph.nodes[n].get('best_move')]
        title = f"AI chose node {best[0]}" if best else f"Step {self.index} / {len(self.history)}"
        plt.title(title)
        plt.draw()
