from src.dependencies import get_db
from src.rasp.models import Rasp
from src.rasp.constants import CardinalDirection
from src.services.navigation.node import Node
from .node_manager import NodeManager
from .edge_manager import EdgeManager

from typing import List, Tuple
from sqlalchemy.orm import Session
import heapq

class MapGraph:
    def __init__(self, db: Session):
        self.node_manager = NodeManager()
        self.edge_manager = EdgeManager()
        self.db = db
        self._build_from_database()

    def get_all_nodes(self) -> List[Node]:
        """返回所有節點"""
        return self.node_manager.get_all_node()

    def _connect_rasps(self):
        """根據 facing 和位置自動連接節點"""
        for node in self.get_all_nodes():
            self._find_and_connect(node, is_x_axis=True, is_positive=True)
            self._find_and_connect(node, is_x_axis=True, is_positive=False)
            self._find_and_connect(node, is_x_axis=False, is_positive=True)
            self._find_and_connect(node, is_x_axis=False, is_positive=False)

    def _get_facing(self, is_x_axis: bool, is_positive: bool) -> CardinalDirection:
        """根據邏輯返回對應的 facing"""
        if is_x_axis:
            return CardinalDirection.WEST if is_positive else CardinalDirection.EAST
        else:
            return CardinalDirection.SOUTH if is_positive else CardinalDirection.NORTH

    def _find_and_connect(self, current_node: Node, is_x_axis: bool, is_positive: bool):
        """尋找符合 facing 條件的節點並連接"""
        candidates = []

        for other_node in self.get_all_nodes():
            if current_node.node_id == other_node.node_id:
                continue

            if self._is_valid_connection(current_node, other_node, is_x_axis, is_positive):
                distance = current_node.calculate_distance(other_node)
                candidates.append((other_node.node_id, distance))

        # 連接距離最近的節點
        if candidates:
            closest_node, distance = min(candidates, key=lambda item: item[1])
            self.edge_manager.add_edge(current_node.node_id, closest_node, weight=distance)

    def _is_valid_connection(self, current_node: Node, other_node: Node, is_x_axis: bool, is_positive: bool):
        """檢查兩個節點是否符合連接條件"""
        target_facing = self._get_facing(is_x_axis, is_positive)
        if other_node.facing != target_facing:
            return False

        if is_x_axis:
            return current_node.y == other_node.y and (
                (other_node.x > current_node.x and is_positive) or
                (other_node.x < current_node.x and not is_positive)
            )
        else:
            return current_node.x == other_node.x and (
                (other_node.y > current_node.y and is_positive) or
                (other_node.y < current_node.y and not is_positive)
            )
        
    def _build_from_database(self):
        """從資料庫中讀取 Rasp 並自動建立地圖"""
        rasps = self.db.query(Rasp).all()
        for rasp in rasps:
            if rasp.status == "online":
                self.node_manager.add_node(
                    rasp.id, rasp.cord_x, rasp.cord_y, CardinalDirection[rasp.facing]
                )
        self._connect_rasps()

    def get_edges(self, node: Node) -> List[Tuple[Node, int]]:
        """返回某節點的所有鄰居及其邊權重 (Node, weight)"""
        node_id = node.node_id

        if node_id not in self.edge_manager.edges:
            raise ValueError(f"Node {node_id} not found in edges")
        
        neighbors = []
        for neighbor_id, weight in self.edge_manager.get_neighbors(node_id):
            neighbor_node = self.node_manager.get_node(neighbor_id)
            if neighbor_node:
                neighbors.append((neighbor_node, weight))
            else:
                print(f"Warning: Neighbor node {neighbor_id} not found in NodeManager")
        
        return neighbors
    
    def node_exists(self, node: Node):
        """檢查節點是否存在"""
        node_id = node.node_id
        return self.node_manager.get_node(node_id) is not None
    
    def find_closest_node(self, x: int, y: int) -> Node:
        """找到距離 (x, y) 最近的 Rasp"""
        virtual_node = Node("VirtualNode", x, y, None)
        closest_rasp = None
        min_distance = float("inf")

        for node in self.get_all_nodes():
            distance = node.calculate_distance(virtual_node)
            if distance < min_distance:
                closest_rasp = node
                min_distance = distance

        return closest_rasp
    
    def find_shortest_path(self, start_node: Node, target_node: Node) -> List[Node]:
        if not self.node_exists(start_node):
            raise ValueError(f"Start node '{start_node}' does not exist")
        if not self.node_exists(target_node):
            raise ValueError(f"Target node '{target_node}' does not exist")

        """使用 Dijkstra 算法計算最短路徑"""
        queue = [(0, start_node, [])]
        visited = set()

        while queue:
            cost, current, path = heapq.heappop(queue)
            if current in visited:
                continue

            visited.add(current)
            path = path + [current]

            if current == target_node:
                return path

            for neighbor, weight in self.get_edges(current):
                if neighbor not in visited:
                    heapq.heappush(queue, (cost + weight, neighbor, path))

        return None