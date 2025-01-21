from src.rasp.constants import CardinalDirection, RelativeDirection
from src.services.navigation.node import Node
from typing import List, Tuple

class DirectionCalculator:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DirectionCalculator, cls).__new__(cls)
        return cls._instance

    def _calculate_direction(self, current_node: Node, next_node: Node) -> RelativeDirection:
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
            raise ValueError("Current node and next node are at the same position")
        
        print(f"目標方向：{target_direction.value}")

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

    def assign_directions(self, path: List[Node]) -> List[Tuple[str, RelativeDirection]]:
        """沿路徑分配導航指令"""
        directions = []
        for i in range(len(path) - 1):
            current = path[i]
            next_node = path[i + 1]
            direction = self._calculate_direction(current, next_node)
            directions.append((current.node_id, direction))
        return directions