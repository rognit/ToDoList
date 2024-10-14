import math
from typing import List, Optional
from math import inf
import numpy as np


class WTDLNode:
    def __init__(self, key: float, h: int) -> None:
        self.key: float = key
        self.next_nodes: List[Optional[WTDLNode]] = [None] * (h + 1)
        self.label: Optional[int] = None  # Label of the node (usefully for partial rebuilding)


class DLLNode:
    def __init__(self, node: Optional[WTDLNode]) -> None:
        self.node: Optional[WTDLNode] = node  # WTDLNode ou None
        self.prev: Optional[WTDLNode] = None  # Pointer to the previous node
        self.next: Optional[WTDLNode] = None  # Pointer to the next node


class DoublyLinkedList:
    def __init__(self):
        self.tail = None  # Pointer to the last node

    def append(self, node: WTDLNode) -> None:
        new_node = DLLNode(node)
        if self.tail is not None:  # If the list is not empty
            self.tail.next = new_node
            new_node.prev = self.tail
        self.tail = new_node


class WorkingToDoList:
    def __init__(self, h: int, epsilon: float, verbose: bool = False) -> None:
        self.h: int = h  # Height of the ToDoList (Maximum level)
        self.epsilon: float = epsilon  # Arbitrary value
        self.verbose: bool = verbose  # Verbose mode
        self.sentinel: WTDLNode = WTDLNode(-inf, self.h)  # Header node (dummy node)
        self.Q: DoublyLinkedList = DoublyLinkedList()  # Contains the keys ordered by their current working set numbers

    def __find_predecessors(self, key: int) -> List[Optional[WTDLNode]]:
        predecessors: List[Optional[WTDLNode]] = [None] * (self.h + 1)
        current: WTDLNode = self.sentinel
        for lvl in range(self.h + 1):
            # Since at most only one node in two is not promoted to the next level,
            # a single comparison is sufficient to determine the predecessor at each level.
            predecessors[lvl] = current if (nxt := current.next_nodes[lvl]) is None or nxt.key >= key else nxt
            current = predecessors[lvl]

        return predecessors

    def __compute_length(self, lvl: int) -> int:
        length: int = 0
        node: Optional[WTDLNode] = self.sentinel.next_nodes[lvl]
        while node is not None:
            length += 1
            node = node.next_nodes[lvl]
        return length

    def __check_rebuilding(self) -> None:
        # If the size of the top level is more than epsilon^-1 + 1, we partially rebuild the list
        if self.__compute_length(0) > (1 / self.epsilon) + 1:
            self.__partial_rebuilding()

    def __partial_rebuilding(self) -> None:
        def compute_special_index() -> int:
            for lvl in range(self.h + 1):
                if self.__compute_length(lvl) <= (2 - self.epsilon / 2) ** lvl:
                    return lvl
            return self.h

        index: int = compute_special_index()

        # Labelling_nodes
        dll_node: DLLNode = self.Q.tail
        for i in range(math.floor((2 - self.epsilon / 2) ** (index - 1))):
            if not dll_node:
                break
            if not dll_node.node.label:
                dll_node.node.label = i
            dll_node = dll_node.prev





        for lvl in range(index, 0, -1):
            current: WTDLNode = self.sentinel
            # We walk through Lj and take any value whose label (in Q) is defined and is at most (2 - epsilon)^j
            # as well as every “second value” as needed to ensure that Property 3 holds.
            while nxt := current.next_nodes[lvl]:
                if nxt.label and nxt.label <= (2 - self.epsilon) ** lvl:
                    current.next_nodes[lvl - 1] = nxt
                    current = nxt
                elif nxt_nxt := nxt.next_nodes[lvl]:
                    nxt.label = None
                    current.next_nodes[lvl - 1] = nxt_nxt
                    current = nxt_nxt
            current.next_nodes[lvl - 1] = None

        current: WTDLNode = self.sentinel
        while current.next_nodes[0]:
            current = current.next_nodes[0]
            current.label = None

        # Just to be sure and because it's written in the paper
        dll_node: DLLNode = self.Q.tail
        for i in range(math.floor((2 - self.epsilon / 2) ** (index - 1))):
            if not dll_node:
                break
            dll_node.node.label = None
            dll_node = dll_node.prev


    def insert(self, key: int) -> None:

        # Find the correct positions to insert the new node
        predecessors: List[Optional[WTDLNode]] = self.__find_predecessors(key)

        # Create the new node
        new_node: WTDLNode = WTDLNode(key, self.h)

        # We add the new node after each predecessor
        for lvl in range(self.h + 1):
            new_node.next_nodes[lvl] = predecessors[lvl].next_nodes[lvl]
            predecessors[lvl].next_nodes[lvl] = new_node

        self.__check_rebuilding()

        print(f"Inserted key {key}") if self.verbose else None

    def delete(self, key: int) -> None:
        predecessors: List[Optional[WTDLNode]] = self.__find_predecessors(key)

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
        def is_perfect_square(n: int) -> bool:
            return math.isqrt(n) ** 2 == n

        current: WTDLNode = self.sentinel
        predecessors: List[Optional[WTDLNode]] = [None] * (self.h + 1)

        for lvl in range(self.h + 1):
            if successor := current.next_nodes[lvl] is not None:
                if is_perfect_square(lvl) and successor.key == key:
                    print(f"Found key {key} at level {lvl}") if self.verbose else None
                    key_level: int = lvl
                    break
                predecessors[lvl] = current if (nxt := current.next_nodes[lvl]) is None or nxt.key >= key else nxt
                current = predecessors[lvl]

        if (candidate := current.next_nodes[self.h]) is not None and candidate.key == key:
            print(f"Found key {key}") if self.verbose else None
            key_level : int = self.h
        else:
            print(f"Key {key} not found") if self.verbose else None
            return False

        self.Q.append(candidate)
        new_node: WTDLNode = WTDLNode(key, self.h)

        # We add the key to every level from 0 to key_level - 1
        for lvl in range(key_level):
            new_node.next_nodes[lvl] = predecessors[lvl].next_nodes[lvl]
            predecessors[lvl].next_nodes[lvl] = new_node




    def __str__(self) -> str:
        output: str = "\nSkip List:\n"
        for lvl in range(self.h + 1):
            current: Optional[WTDLNode] = self.sentinel.next_nodes[lvl]
            level_str: str = f"Level {lvl}: "
            while current is not None:
                level_str += f"{current.key} -> "
                current = current.next_nodes[lvl]
            level_str += "None"
            output += level_str + "\n"
        return output
