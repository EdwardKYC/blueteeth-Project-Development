from src.services.navigation.node import Node
from typing import List

class NodeManager:
    def __init__(self):
        self.nodes = {}  # 節點集合 {node_id: Node}

    def add_node(self, node_id, x, y, facing):
        """添加節點"""
        self.nodes[node_id] = Node(node_id, x, y, facing)

    def get_node(self, node_id) -> Node:
        """獲取節點"""
        return self.nodes.get(node_id)
    
    def get_all_node(self) -> List[Node]:
        """獲取所有節點"""
        return list(self.nodes.values())