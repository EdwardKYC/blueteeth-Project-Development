from src.dependencies import get_db
from src.rasp.models import Rasp
from src.rasp.constants import CardinalDirection, RelativeDirection
from .node_manager import NodeManager, Node
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
        return self.node_manager.get_all_node()

    def _get_facing(self, is_x_axis: bool, is_positive: bool) -> CardinalDirection:
        if is_x_axis:
            return CardinalDirection.WEST if is_positive else CardinalDirection.EAST
        else:
            return CardinalDirection.SOUTH if is_positive else CardinalDirection.NORTH

    def _connect_rasps(self):
        for node in self.get_all_nodes():
            self._find_and_connect(node, is_x_axis=True, is_positive=True)
            self._find_and_connect(node, is_x_axis=True, is_positive=False)
            self._find_and_connect(node, is_x_axis=False, is_positive=True)
            self._find_and_connect(node, is_x_axis=False, is_positive=False)

    def _find_and_connect(self, current_node: Node, is_x_axis: bool, is_positive: bool, do_add_edge: bool = True):
        candidates = []

        for other_node in self.get_all_nodes():
            if current_node.node_id == other_node.node_id:
                continue
            if self._is_valid_connection(current_node, other_node, is_x_axis, is_positive):
                distance = current_node.calculate_distance(other_node)
                candidates.append((other_node, distance))

        if candidates:
            closest_node, distance = min(candidates, key=lambda item: item[1])
            if not do_add_edge:
                return closest_node
            else:
                self.edge_manager.add_edge(current_node.node_id, closest_node.node_id, weight=distance)
                self.edge_manager.add_edge(closest_node.node_id, current_node.node_id, weight=distance)

    def _is_valid_connection(self, current_node: Node, other_node: Node, is_x_axis: bool, is_positive: bool):
        dx = other_node.x - current_node.x
        dy = other_node.y - current_node.y

        if abs(dx) + abs(dy) > 1:
            return False

        if is_x_axis:
            return dy == 0 and ((dx >= 0 and is_positive) or (dx <= 0 and not is_positive))
        else:
            return dx == 0 and ((dy >= 0 and is_positive) or (dy <= 0 and not is_positive))

    def _calculate_direction(self, current_node: Node, next_node: Node) -> RelativeDirection | None:
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
        current_facing_index = facing_cycle.index(current_facing)
        direction_index = relative_cycle.index(direction)
        index = (direction_index - current_facing_index) % 4
        return relative_cycle[index]

    def _build_from_database(self):
        rasps = self.db.query(Rasp).all()
        for rasp in rasps:
            if rasp.status == "online":
                self.node_manager.add_node(
                    rasp.id, rasp.cord_x, rasp.cord_y, CardinalDirection[rasp.facing]
                )
        self._connect_rasps()

    def get_edges(self, node: Node) -> List[Tuple[Node, int]]:
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
        return self.node_manager.get_node(node.node_id) is not None

    def find_path(self, x: int, y: int) -> List[Tuple[str, RelativeDirection]]:
        start_node = Node("StartingDevice", x, y, None)
        directions = []
        distances = {start_node.node_id: 0}
        prev_node = {}
        visited = set()
        queue = [(0, start_node)]

        for is_x_axis, is_positive in [
            (True, True), (True, False), (False, True), (False, False)
        ]:
            neighbor: Node = self._find_and_connect(start_node, is_x_axis, is_positive, do_add_edge=False)
            if neighbor:
                distance = start_node.calculate_distance(neighbor)
                self.edge_manager.add_edge(start_node.node_id, neighbor.node_id, weight=distance)
                self.edge_manager.add_edge(neighbor.node_id, start_node.node_id, weight=distance)

        while queue:
            cost, current = heapq.heappop(queue)
            if current.node_id in visited:
                continue
            visited.add(current.node_id)

            for neighbor, weight in self.get_edges(current):
                if neighbor.node_id in visited:
                    continue
                new_cost = cost + weight
                if neighbor.node_id not in distances or new_cost < distances[neighbor.node_id]:
                    distances[neighbor.node_id] = new_cost
                    prev_node[neighbor.node_id] = current
                    heapq.heappush(queue, (new_cost, neighbor))

        for node_id, prev in prev_node.items():
            direction = self._calculate_direction(self.node_manager.get_node(node_id), prev)
            print(f"node_id: {node_id}, prev: {prev.node_id}, direction: {direction}")
            if direction is not None:
                directions.append((node_id, direction))

        return directions
