class SearchTracer:
    def __init__(self):
        self.history = []
        self.path_stack = []

    def enter_node(self, node, alpha, beta, color):
        parent_id = self.path_stack[-1] if self.path_stack else None
    
        board = node.state.board
        label = "\n".join(" ".join(cell for cell in row) for row in board)
        
        step = {
            'type': 'entry',
            'id': id(node),
            'parent': parent_id,
            'label': label,          # ← était str(node.state)
            'depth': node.depth,
            'alpha': round(alpha, 2) if alpha not in (float('inf'), float('-inf')) else alpha,
            'beta':  round(beta,  2) if beta  not in (float('inf'), float('-inf')) else beta,
            'color': "MAX" if color == 1 else "MIN",
            'value': None,
            'cutoff': False
        }
        self.history.append(step)
        self.call_stack_push(id(node))

    def report_cutoff(self):
        if not self.path_stack:
            return
        current_id = self.path_stack[-1]
        for step in reversed(self.history):
            if step['id'] == current_id and step['type'] == 'entry':
                step['cutoff'] = True
                break

    def exit_node(self, value):
        node_id = self.call_stack_pop()
        # Find the entry record and update it with the final calculated value
        for step in reversed(self.history):
            if step['id'] == node_id and step['type'] == 'entry':
                step['value'] = value
                break

    def call_stack_push(self, node_id):
        self.path_stack.append(node_id)

    def call_stack_pop(self):
        return self.path_stack.pop()
    
    def report_best_move(self, node_id, value):
        """Marks the chosen best move in history."""
        for step in reversed(self.history):
            if step['id'] == node_id and step['type'] == 'entry':
                step['best_move'] = True
                step['value'] = value
                break