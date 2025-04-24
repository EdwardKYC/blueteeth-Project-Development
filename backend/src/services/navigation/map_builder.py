from src.dependencies import get_db
from src.rasp.models import Rasp
from src.rasp.constants import CardinalDirection, RelativeDirection
from .node_manager import NodeManager, Node
from .edge_manager import EdgeManager

from typing import List, Tuple
from sqlalchemy.orm import Session
from collections import deque

class MapGraph:
    def __init__(self, db: Session):
        self.node_manager = NodeManager()
        self.edge_manager = EdgeManager()
        self.db = db
        self._build_from_database()

    def get_all_nodes(self) -> List[Node]:
        """返回所有節點"""
        return self.node_manager.get_all_node()
    
    def _get_facing(self, is_x_axis: bool, is_positive: bool) -> CardinalDirection:
        """根據邏輯返回對應的 facing"""
        if is_x_axis:
            return CardinalDirection.WEST if is_positive else CardinalDirection.EAST
        else:
            return CardinalDirection.SOUTH if is_positive else CardinalDirection.NORTH

    def _connect_rasps(self):
        """根據 facing 和位置自動連接節點"""
        for node in self.get_all_nodes():
            self._find_and_connect(node, is_x_axis=True, is_positive=True)
            self._find_and_connect(node, is_x_axis=True, is_positive=False)
            self._find_and_connect(node, is_x_axis=False, is_positive=True)
            self._find_and_connect(node, is_x_axis=False, is_positive=False)

    def _find_and_connect(self, current_node: Node, is_x_axis: bool, is_positive: bool, do_add_edge: bool = True):
        """尋找符合 facing 條件的節點並連接"""
        candidates = []

        for other_node in self.get_all_nodes():
            if current_node.node_id == other_node.node_id:
                continue

            if self._is_valid_connection(current_node, other_node, is_x_axis, is_positive):
                distance = current_node.calculate_distance(other_node)
                candidates.append((other_node, distance))

        # 連接距離最近的節點
        if candidates:
            closest_node, distance = min(candidates, key=lambda item: item[1])
            if not do_add_edge:
                return closest_node
            else:
                self.edge_manager.add_edge(current_node.node_id, closest_node.node_id, weight=distance)
                self.edge_manager.add_edge(closest_node.node_id, current_node.node_id, weight=distance)

    def _is_valid_connection(self, current_node: Node, other_node: Node, is_x_axis: bool, is_positive: bool):
        """檢查兩個節點是否符合連接條件"""
        if is_x_axis:
            return current_node.y == other_node.y and (
                (other_node.x >= current_node.x and is_positive) or
                (other_node.x <= current_node.x and not is_positive)
            )
        else:
            return current_node.x == other_node.x and (
                (other_node.y >= current_node.y and is_positive) or
                (other_node.y <= current_node.y and not is_positive)
            )
        
    def _calculate_direction(self, current_node: Node, next_node: Node) -> RelativeDirection | None:
        """計算從 current_node 到 next_node 的方向"""
        if current_node.x < next_node.x:
            target_direction = RelativeDirection.RIGHT
        elif current_node.x > next_node.x:
            target_direction = RelativeDirection.LEFT
        elif current_node.y < next_node.y:
            target_direction = RelativeDirection.UP
        elif current_node.y > next_node.y:
            target_direction = RelativeDirection.DOWN
        else:
            return None
        
        return self._adjust_facing(target_direction, current_node.facing)
    
    def _adjust_facing(self, direction: RelativeDirection, current_facing: CardinalDirection) -> RelativeDirection:
        facing_cycle = [
            CardinalDirection.SOUTH,
            CardinalDirection.EAST,
            CardinalDirection.NORTH,
            CardinalDirection.WEST,
        ]
        relative_cycle = [
            RelativeDirection.DOWN,
            RelativeDirection.RIGHT,
            RelativeDirection.UP,
            RelativeDirection.LEFT,
        ]

        # 計算 facing 與目標 direction 的最短轉向
        current_facing_index = facing_cycle.index(current_facing)
        direction_index = relative_cycle.index(direction)

        index = (direction_index - current_facing_index) % 4
        return relative_cycle[index]
        
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
    
    def find_path(self, x: int, y: int) -> List[Tuple[str, RelativeDirection]]:
        start_node = Node("StartingDevice", x, y, None)
        
        directions = []
        visited = set()
        queue = deque([start_node])

        for is_x_axis, is_positive in [
            (True, True), (True, False), (False, True), (False, False)
        ]:
            neighbor = self._find_and_connect(start_node, is_x_axis, is_positive, do_add_edge=False)
            if neighbor and neighbor.node_id not in visited:
                direction = self._calculate_direction(neighbor, start_node)
                if direction is not None:
                    directions.append((neighbor.node_id, direction))
                visited.add(neighbor.node_id)
                queue.append(neighbor)

        while queue:
            current = queue.popleft()
            visited.add(current.node_id)

            for neighbor_id, _ in self.edge_manager.get_neighbors(current.node_id):
                if neighbor_id in visited:
                    continue
                visited.add(neighbor_id)
                neighbor = self.node_manager.get_node(neighbor_id)
                if neighbor:
                    direction = self._calculate_direction(neighbor, current)
                    if direction is not None:
                        directions.append((neighbor.node_id, direction))
                    queue.append(neighbor)

        return directions