from src.rasp.constants import CardinalDirection

class Node:
    def __init__(self, node_id: str, x: int, y: int, facing: CardinalDirection):
        self.node_id = node_id
        self.x = x
        self.y = y
        self.facing = facing

    def calculate_distance(self, other_node) -> int:
        """計算到其他節點的曼哈頓距離"""
        return abs(self.x - other_node.x) + abs(self.y - other_node.y)
    
    def __lt__(self, other: "Node") -> bool:
        """Define comparison for priority queue (heapq)"""
        # Compare based on `node_id` to ensure consistent behavior
        return self.node_id < other.node_id