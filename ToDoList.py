from typing import List, Optional
from math import inf


class TDLNode:
    def __init__(self, key: float, h: int) -> None:
        self.key: float = key
        self.next_nodes: List[Optional[TDLNode]] = [None] * (h + 1)


class ToDoList:
    def __init__(self, h: int, epsilon: float, verbose: bool = False) -> None:
        self.h: int = h  # Height of the ToDoList (Maximum level)
        self.epsilon: float = epsilon  # Arbitrary value
        self.verbose: bool = verbose  # Verbose mode
        self.sentinel: TDLNode = TDLNode(-inf, self.h)  # Header node (dummy node)

    def __find_predecessors(self, key: int) -> List[Optional[TDLNode]]:
        predecessors: List[Optional[TDLNode]] = [None] * (self.h + 1)
        current: TDLNode = self.sentinel
        for lvl in range(self.h + 1):
            # Since at most only one node in two is not promoted to the next level,
            # a single comparison is sufficient to determine the predecessor at each level.
            predecessors[lvl] = current if current.next_nodes[lvl] is None or current.next_nodes[lvl].key >= key \
                else current.next_nodes[lvl]
            current = predecessors[lvl]

        return predecessors

    def __check_rebuilding(self) -> None:
        # If there is more than one node in the top level, we partially rebuild the list
        if self.sentinel.next_nodes[0] is not None and self.sentinel.next_nodes[0].next_nodes[0] is not None:
            self.__partial_rebuilding()

    def __partial_rebuilding(self) -> None:
        def __compute_length(lvl: int) -> int:
            length: int = 0
            node: Optional[TDLNode] = self.sentinel.next_nodes[lvl]
            while node is not None:
                length += 1
                node = node.next_nodes[lvl]
            return length

        def __compute_special_index() -> int:
            for lvl in range(self.h + 1):
                if __compute_length(lvl) <= (2 - self.epsilon) ** lvl:
                    return lvl
            return self.h

        # We find the smallest index i such that |Lindex| < (2 - epsilon) ** index
        index: int = __compute_special_index()

        # We then rebuild the lists L0, ..., Lindex-1 in a bottom up fashion;
        # Lindex-1 gets every second element from Lindex (starting with the second),
        # Lindex-2 gets every second element from Lindex-1, and so on down to L0
        for lvl in range(index, 0, -1):
            current: TDLNode = self.sentinel
            while (nxt := current.next_nodes[lvl]) is not None and (nxt_nxt := nxt.next_nodes[lvl]) is not None:
                current.next_nodes[lvl - 1] = nxt_nxt
                current = nxt_nxt
            current.next_nodes[lvl - 1] = None

    def insert(self, key: int) -> None:

        # Find the correct positions to insert the new node
        predecessors: List[Optional[TDLNode]] = self.__find_predecessors(key)

        # Create the new node
        new_node: TDLNode = TDLNode(key, self.h)

        # We add the new node after each predecessor
        for lvl in range(self.h + 1):
            new_node.next_nodes[lvl] = predecessors[lvl].next_nodes[lvl]
            predecessors[lvl].next_nodes[lvl] = new_node

        self.__check_rebuilding()

        if self.verbose:
            print(f"Inserted key {key}")

    def delete(self, key: int) -> None:
        predecessors: List[Optional[TDLNode]] = self.__find_predecessors(key)

        # The one to be promoted in place of the element to be deleted
        substitute = predecessors[self.h].next_nodes[self.h].next_nodes[self.h] \
            if predecessors[self.h].next_nodes[self.h] is not None \
            else None

        for lvl in range(self.h + 1):
            if (target := predecessors[lvl].next_nodes[lvl]) is not None and target.key == key:
                predecessors[lvl].next_nodes[lvl] = substitute
                successor = target.next_nodes[lvl]
                if successor is not None and successor.key != substitute.key:
                    substitute.next_nodes[lvl] = successor

        self.__check_rebuilding()

        if self.verbose:
            print(f"Deleted key {key}")

    def search(self, key: int) -> bool:
        predecessors: List[Optional[TDLNode]] = self.__find_predecessors(key)
        if predecessors[self.h].next_nodes[self.h] is not None and predecessors[self.h].next_nodes[self.h].key == key:
            if self.verbose:
                print(f"Found key {key}")
            return True
        else:
            if self.verbose:
                print(f"Key {key} not found")
            return False

    def __str__(self) -> str:
        output: str = "\nSkip List:\n"
        for lvl in range(self.h + 1):
            current: Optional[TDLNode] = self.sentinel.next_nodes[lvl]
            level_str: str = f"Level {lvl}: "
            while current is not None:
                level_str += f"{current.key} -> "
                current = current.next_nodes[lvl]
            level_str += "None"
            output += level_str + "\n"
        return output
