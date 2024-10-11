from random import random
from typing import List, Optional

class SLNode:
    def __init__(self, key: int, level: int) -> None:
        self.key: int = key
        self.next_nodes: List[Optional[SLNode]] = [None] * (level + 1)

class SkipList:
    def __init__(self, max_level: int, p: float = 0.5, verbose: bool = False) -> None:
        self.max_level_limit: int = max_level  # Maximum level of the SkipList
        self.p: float = p  # Promotion probability
        self.verbose: bool = verbose  # Verbose mode
        self.sentinel: SLNode = SLNode(-1, self.max_level_limit)  # Header node (dummy node)
        self.current_level_number: int = 0  # Current level number in the SkipList

    def __random_promotion(self) -> int:
        for lvl in range(self.max_level_limit):
            if random() >= self.p:
                return lvl
        return self.max_level_limit

    def __find_predecessors(self, key: int) -> List[Optional[SLNode]]:
        """Search for all the predecessors of the key to be inserted"""
        previous_nodes: List[Optional[SLNode]] = [None] * (self.max_level_limit + 1)
        current: SLNode = self.sentinel

        # Move forward to find the correct insertion position
        for i in range(self.current_level_number, -1, -1):
            while current.next_nodes[i] and current.next_nodes[i].key < key:
                current = current.next_nodes[i]
            previous_nodes[i] = current

        return previous_nodes

    def insert(self, key: int) -> None:
        # Promotion of the new node
        new_level: int = self.__random_promotion()

        # Find the correct positions to insert the new node
        predecessors: List[Optional[SLNode]] = self.__find_predecessors(key)

        # If new level is higher than the current list level, update header links
        if new_level > self.current_level_number:
            for i in range(self.current_level_number + 1, new_level + 1):
                predecessors[i] = self.sentinel
            self.current_level_number = new_level

        # Create the new node and adjust the next node references
        new_node: SLNode = SLNode(key, new_level)
        for i in range(new_level + 1):
            new_node.next_nodes[i] = predecessors[i].next_nodes[i]
            predecessors[i].next_nodes[i] = new_node

        if self.verbose:
            print(f"Inserted key {key} at level {new_level}")



    def delete(self, key: int) -> None:
        # Find the correct positions where the key should be located
        predecessors: List[Optional[SLNode]] = self.__find_predecessors(key)

        # Retrieve the candidate node to be deleted
        candidate_node: Optional[SLNode] = predecessors[0].next_nodes[0] if predecessors and predecessors[0].next_nodes else None

        if candidate_node and candidate_node.key == key:  # If the candidate node has the right key
            # Update 'next nodes' pointers
            for i in range(self.current_level_number + 1):
                if predecessors[i].next_nodes[i].key != candidate_node.key:
                    break
                predecessors[i].next_nodes[i] = candidate_node.next_nodes[i]

            # Adjust the level of the skip list if needed
            while self.current_level_number > 0 and self.sentinel.next_nodes[self.current_level_number] is None:
                self.current_level_number -= 1

            if self.verbose:
                print(f"Deleted key {key}")
        else:
            if self.verbose:
                print(f"key {key} not found")

    def search(self, key: int) -> bool:
        current: SLNode = self.sentinel
        for lvl in range(self.current_level_number, -1, -1):
            while True:
                next_node: Optional[SLNode] = current.next_nodes[lvl]
                if next_node is None or next_node.key >= key:
                    break
                current = next_node
            if next_node is not None and next_node.key == key:
                if self.verbose:
                    print(f"Found key {key} at level {lvl}")
                return True

        if self.verbose:
            print(f"Key {key} not found")
        return False

    def __str__(self) -> str:
        output = "\nSkip List:"
        for i in range(self.current_level_number, -1, -1):
            current: Optional[SLNode] = self.sentinel.next_nodes[i]
            level_str = f"Level {i}: "
            while current is not None:
                level_str += f"{current.key} -> "
                current = current.next_nodes[i]
            level_str += "None"
            output += level_str + "\n"
        return output
