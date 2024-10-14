from typing import List, Optional


class WTDLNode:
    def __init__(self, key: int, h: int) -> None:
        self.key: int = key
        self.next_nodes: List[Optional[WTDLNode]] = [None] * (h + 1)  # For levels 0 to h
        self.prev: Optional['WTDLNode'] = None  # Pointer for the doubly-linked list


class WorkingToDoList:
    def __init__(self, h: int, epsilon: float, verbose: bool = False) -> None:
        self.h: int = h  # Maximum level
        self.epsilon: float = epsilon  # Arbitrary value
        self.verbose: bool = verbose  # Verbose mode
        self.sentinel: WTDLNode = WTDLNode(float('-inf'), self.h)  # Sentinel node for lists
        self.working_set: dict[int, int] = {}  # Store working set numbers
        self.Q: Optional[WTDLNode] = None  # Head of the doubly linked list for working set ordering

    def __find_predecessors(self, key: int) -> List[Optional[WTDLNode]]:
        predecessors: List[Optional[WTDLNode]] = [None] * (self.h + 1)
        current: WTDLNode = self.sentinel
        for lvl in range(self.h + 1):
            while current.next_nodes[lvl] is not None and current.next_nodes[lvl].key < key:
                current = current.next_nodes[lvl]
            predecessors[lvl] = current
        return predecessors

    def __get_working_set_number(self, key: int) -> int:
        # Calculate working set number for key
        if key not in self.working_set:
            return len(set(self.__collect_last_occurrences(key)))
        return self.working_set[key]

    def __collect_last_occurrences(self, key: int) -> List[int]:
        occurrences = []
        current = self.sentinel.next_nodes[0]
        while current is not None:
            occurrences.append(current.key)
            current = current.next_nodes[0]
        return occurrences

    def __check_rebuilding(self) -> None:
        if self.sentinel.next_nodes[0] is not None and self.sentinel.next_nodes[0].next_nodes[0] is not None:
            self.__partial_rebuilding()

    def __partial_rebuilding(self) -> None:
        """Rebuilds the lists L0, L1, ..., Li to maintain properties."""
        # Find the first index i such that |Li| ≤ (2 - ε/2)^i
        i = 0
        while i in self.L and len(self.L[i]) <= (2 - self.epsilon / 2) ** i:
            i += 1

        # Now i is the first index where the property may be violated
        if i in self.L:
            # Traverse the first (2 - ε)^(i-1) nodes of Q
            current = self.Q
            count = 0

            while current and count < (2 - self.epsilon) ** (i - 1):
                # Get the value of the current node
                z = current.value

                # Check if the working set number of z is defined and is at most (2 - ε)^j
                if z in self.w and self.w[z] <= (2 - self.epsilon) ** (i - 1):
                    # Insert z into the appropriate list Lj
                    if i - 1 not in self.L:
                        self.L[i - 1] = []
                    self.L[i - 1].append(z)

                # Move to the next node in the linked list
                current = current.next
                count += 1

        # Rebuild all lists L0, ..., Li-1
        for j in range(i):
            if j in self.L:
                # Rebuild L_j
                new_list = []
                for value in self.L[j]:
                    # Check if value is in the working set
                    if self.w[value] <= (2 - self.epsilon) ** j:
                        new_list.append(value)
                self.L[j] = new_list

        # Clear the labels in the first (2 - ε)^(i-1) nodes of Q
        current = self.Q
        count = 0
        while current and count < (2 - self.epsilon) ** (i - 1):
            # Clear the label (if applicable, this could be a reference)
            # Here we assume 'label' is handled through w or another structure
            count += 1
            current = current.next


    def insert(self, key: int) -> None:
        # Find predecessors
        predecessors = self.__find_predecessors(key)

        # Create new node
        new_node = WTDLNode(key, self.h)

        # Insert into L0
        new_node.next_nodes[0] = predecessors[0].next_nodes[0]
        predecessors[0].next_nodes[0] = new_node
        new_node.prev = predecessors[0]  # Link back in the doubly-linked list

        # Update working set number
        self.working_set[key] = self.__get_working_set_number(key)

        # Rebuild lists if necessary
        self.__check_rebuilding()

        if self.verbose:
            print(f"Inserted key {key}")

    def delete(self, key: int) -> None:
        predecessors = self.__find_predecessors(key)
        for lvl in range(self.h + 1):
            if predecessors[lvl].next_nodes[lvl] is not None and predecessors[lvl].next_nodes[lvl].key == key:
                # Adjust the links
                successors = predecessors[lvl].next_nodes[lvl].next_nodes[lvl]
                predecessors[lvl].next_nodes[lvl] = successors
                if successors is not None:
                    successors.prev = predecessors[lvl]

        # Remove from working set
        if key in self.working_set:
            del self.working_set[key]

        self.__check_rebuilding()

        if self.verbose:
            print(f"Deleted key {key}")

    def search(self, key: int) -> bool:
        predecessors = self.__find_predecessors(key)

        for i in range(self.h + 1):
            current = predecessors[i].next_nodes[i]
            if current is not None and current.key == key:
                # Move to front of Q
                self.__move_to_front(current)
                if self.verbose:
                    print(f"Found key {key}")
                return True
        
        if self.verbose:
            print(f"Key {key} not found")
        return False

    def __move_to_front(self, node: WTDLNode) -> None:
        # Move the node in Q to the front
        if self.Q is None or self.Q.key == node.key:
            return  # Already at front

        # Unlink node from Q
        if node.prev is not None:
            node.prev.next_nodes[0] = node.next_nodes[0]
        if node.next_nodes[0] is not None:
            node.next_nodes[0].prev = node.prev

        # Link to front
        node.prev = None
        node.next_nodes[0] = self.Q
        if self.Q is not None:
            self.Q.prev = node
        self.Q = node

    def __str__(self) -> str:
        output = "\nWorking ToDo List:\n"
        for lvl in range(self.h + 1):
            current = self.sentinel.next_nodes[lvl]
            level_str = f"Level {lvl}: "
            while current is not None:
                level_str += f"{current.key} -> "
                current = current.next_nodes[lvl]
            level_str += "None"
            output += level_str + "\n"
        return output
    


'''
working_todolist = WorkingToDoList(5,0.2)
x = working_todolist.insert(5)
print(x)
y = working_todolist.search(5)
print(y)
z = working_todolist.delete(5)
print(z)
'''