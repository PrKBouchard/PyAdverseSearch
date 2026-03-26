from PyAdverseSearch.classes.node import Node
import random

class NegamaxSolver:
    """
    Solveur basé sur l'algorithme Negamax avec élagage Alpha-Beta, 
    recherche de quiescence et table de transposition.
    
    Cette variante simplifiée du Minimax repose sur l'égalité : max(a, b) == -min(-a, -b).
    Elle permet de traiter les deux joueurs avec la même logique de maximisation.
    """


    
    def __init__(self, depth_limit=5, tracer=None):
        """
        Initialise le solveur avec une limite de profondeur de recherche.
        
        :param depth_limit: Profondeur maximale de l'arbre de recherche (nombre de demi-coups).
        """
        self.tracer = tracer
        
        self.depth_limit = depth_limit
        self.transposition_table = {}

        self.nodes_visited = 0
        self.cutoffs = 0



    def get_best_move(self, root_node):
        """
        Détermine le meilleur coup à partir du nœud racine donné.

        Explore tous les enfants du nœud racine en utilisant l'algorithme
        Negamax avec élagage Alpha-Beta, puis sélectionne l'action
        produisant la meilleure valeur d'évaluation.

        :param root_node: Nœud racine représentant l'état actuel du jeu.
        :return: La représentation du plateau (board) correspondant
                au meilleur coup trouvé.
        """
        if root_node.is_terminal():
            raise ValueError("get_best_move appelé sur un état terminal.")

        current_color = 1 if root_node.state.player == 'MAX' else -1
                
        if not root_node.children:
            root_node._expand()
        
        if not root_node.children:
            raise ValueError("Aucun coup légal depuis cet état.")

        best_value = -float('inf')
        best_action = None
        best_child = None
        
        for child in root_node.children:
            value = -self._negamax(
                child,
                self.depth_limit - 1,
                -float('inf'),
                float('inf'),
                -current_color
            )
            
            if value > best_value:
                best_value = value
                best_action = child.state.board
                best_child = child
                
        if self.tracer and best_child is not None:
            self.tracer.report_best_move(id(best_child), best_value)

        return best_action
    
    
    
    def _get_evaluation(self, node, color):
        """
        Évalue numériquement un nœud donné.

        Si le nœud est terminal, retourne sa valeur utilité pondérée
        par la profondeur pour favoriser les victoires rapides et
        retarder les défaites.

        Sinon, utilise la fonction d'évaluation heuristique définie
        dans l'état du jeu si disponible.

        :param node: Nœud à évaluer.
        :param color: 1 pour MAX, -1 pour MIN.
        :return: Score numérique de la position.
        """
        if node.is_terminal():
            return color * (node.utility + (node.depth if node.utility > 0 else -node.depth))
        
        if hasattr(node.state, 'evaluate'):
            return color * node.state.evaluate()
        
        return 0
    
    
    
    def solve(self, game, state, color):
        """
        Évalue la valeur d'un état donné indépendamment de la recherche
        d'un meilleur coup.

        Cette méthode réinitialise la table de transposition afin de garantir
        une recherche propre, puis lance l'algorithme Negamax depuis l'état fourni.

        :param game: Instance du jeu.
        :param state: État à évaluer.
        :param color: 1 si le joueur courant est MAX, -1 si MIN.
        :return: Valeur numérique estimée de l'état.
        """
        self.transposition_table = {}
        
        if state.game is None:
            state.game = game
            
        root_node = Node(state=state, parent=None, depth=0)
        
        return self._negamax(root_node, self.depth_limit, -float('inf'), float('inf'), color)



    def _get_move_score(self, node, color):
        """
        Calcule un score heuristique pour ordonner les coups.

        Cette méthode est utilisée pour améliorer l'efficacité
        de l'élagage Alpha-Beta en explorant d'abord les coups
        potentiellement les plus prometteurs.

        Les positions terminales favorables sont priorisées.

        :param node: Nœud enfant à évaluer.
        :param color: 1 pour MAX, -1 pour MIN.
        :return: Score heuristique utilisé pour le tri des coups.
        """
        if node.is_terminal():
            if node.utility * color > 0:
                return 100000
            else:
                return -100000
        
        return self._get_evaluation(node, color)



    def _negamax(self, node, depth, alpha, beta, color):
        """
        Implémentation récursive de l'algorithme Negamax avec élagage Alpha-Beta.

        Explore récursivement l'arbre des coups possibles en alternant
        les perspectives des joueurs via l'inversion du signe (principe Negamax).

        Inclut :
        - Élagage Alpha-Beta pour réduire l'espace de recherche
        - Table de transposition pour éviter les recalculs
        - Recherche de quiescence lorsque la profondeur maximale est atteinte

        :param node: Nœud courant.
        :param depth: Profondeur restante à explorer.
        :param alpha: Borne inférieure (meilleure valeur garantie pour MAX).
        :param beta: Borne supérieure (meilleure valeur garantie pour MIN).
        :param color: 1 pour MAX, -1 pour MIN.
        :return: Meilleure valeur trouvée pour ce nœud.
        """
        if self.tracer: 
            self.tracer.enter_node(node, alpha, beta, color)
        self.nodes_visited += 1

        state_hash = hash(node.state) if hasattr(node.state, '__hash__') else hash(str(node.state.board))
        
        if state_hash in self.transposition_table:
            entry = self.transposition_table[state_hash]
            if entry['depth'] >= depth:
                return entry['value']

        if node.is_terminal() or depth == 0:
            if depth == 0 and hasattr(node.state, '_possible_captures'):
                return self._quiescence(node, alpha, beta, color)
            return self._get_evaluation(node, color)

        if not node.children:
            node._expand()

        node.children.sort(key=lambda n: self._get_move_score(n, color), reverse=True)

        value = -float('inf')
        for child in node.children:
            score = -self._negamax(child, depth - 1, -beta, -alpha, -color)
            value = max(value, score)
            alpha = max(alpha, value)
            if alpha >= beta:
                if self.tracer: 
                    self.tracer.report_cutoff()
                self.cutoffs += 1
                break

        self.transposition_table[state_hash] = {'value': value, 'depth': depth}
        if self.tracer: 
            self.tracer.exit_node(value)
        return value
    
    
    
    def _quiescence(self, node, alpha, beta, color):
        """
        Effectue une recherche de quiescence pour stabiliser l'évaluation
        en fin de profondeur.

        Permet de limiter l'effet d'horizon en continuant d'explorer
        uniquement les coups tactiques (captures) susceptibles de
        modifier significativement l'évaluation.

        Applique également :
        - Stand pat evaluation
        - Élagage Alpha-Beta
        - Delta pruning pour limiter les explorations inutiles

        :param node: Nœud à analyser.
        :param alpha: Borne inférieure.
        :param beta: Borne supérieure.
        :param color: 1 pour MAX, -1 pour MIN.
        :return: Score stabilisé de la position.
        """
        if hasattr(node.state, '_evaluate'):
            stand_pat = color * node.state._evaluate()
        else:
            stand_pat = color * getattr(node.state, 'utility', 0)

        if stand_pat >= beta: 
            return beta
        
        if alpha < stand_pat: 
            alpha = stand_pat

        delta_margin = 10
        if stand_pat < alpha - delta_margin:
            return alpha

        actions = node.state._possible_actions()
        # random.shuffle(actions)
        captures = [a for a in actions if getattr(a, 'is_capture', False)]
        
        for action in captures:
            new_state = node.state._apply_action(action)
            child_node = Node(state=new_state, parent=node, depth=node.depth + 1)
            
            score = -self._quiescence(child_node, -beta, -alpha, -color)
            
            if score >= beta:
                return beta 
            if score > alpha:
                alpha = score
                
        return alpha