class EdgeManager:
    def __init__(self):
        self.edges = {}  # 邊集合 {node_id: [(neighbor_node_id, weight)]}

    def add_edge(self, from_node_id, to_node_id, weight=1):
        """添加邊"""
        if from_node_id not in self.edges:
            self.edges[from_node_id] = []

        self.edges[from_node_id].append((to_node_id, weight))

    def get_neighbors(self, node_id):
        """獲取節點的所有鄰居"""
        return self.edges.get(node_id, [])