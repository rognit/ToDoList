

class ToDoList:  # ToDoList = top-down skiplists
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

import random

class Node:
    def __init__(self, value, level):
        self.value = value
        # Forward references (pointers) to the next nodes at each level
        self.forward = [None] * (level + 1)

class SkipList:
    def __init__(self, max_level, p):
        self.max_level = max_level
        self.p = p  # Probability to decide the level for each node
        self.header = self.create_node(self.max_level, -1)  # Header node (dummy node)
        self.level = 0  # Current maximum level in the list

    # Utility function to create a new node
    def create_node(self, level, value):
        return Node(value, level)

    # Random level generator based on the probability
    def random_level(self):
        lvl = 0
        while random.random() < self.p and lvl < self.max_level:
            lvl += 1
        return lvl

    # Insertion of an element into the skip list
    def insert(self, value):
        update = [None] * (self.max_level + 1)
        current = self.header

        # Move forward to find the correct insertion position
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].value < value:
                current = current.forward[i]
            update[i] = current

        # Generate a random level for the new node
        new_level = self.random_level()

        # If new level is higher than the current list level, update header links
        if new_level > self.level:
            for i in range(self.level + 1, new_level + 1):
                update[i] = self.header
            self.level = new_level

        # Create the new node and adjust the forward references
        new_node = self.create_node(new_level, value)
        for i in range(new_level + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

        print(f"Inserted value {value} at level {new_level}")

    # Searching for an element in the skip list
    def search(self, value):
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].value < value:
                current = current.forward[i]
        current = current.forward[0]
        if current and current.value == value:
            print(f"Found value {value}")
            return True
        else:
            print(f"Value {value} not found")
            return False

    # Deletion of an element from the skip list
    def delete(self, value):
        update = [None] * (self.max_level + 1)
        current = self.header

        # Move forward to find the node to delete
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].value < value:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        if current and current.value == value:
            # Update forward pointers
            for i in range(self.level + 1):
                if update[i].forward[i] != current:
                    break
                update[i].forward[i] = current.forward[i]

            # Adjust the level of the skip list if needed
            while self.level > 0 and self.header.forward[self.level] is None:
                self.level -= 1

            print(f"Deleted value {value}")
        else:
            print(f"Value {value} not found")

    # Display the skip list representation
    def display(self):
        print("\nSkip List:")
        for i in range(self.level, -1, -1):
            current = self.header.forward[i]
            level_str = f"Level {i}: "
            while current is not None:
                level_str += f"{current.value} -> "
                current = current.forward[i]
            level_str += "None"
            print(level_str)

# Testing the SkipList with display method
if __name__ == "__main__":
    skiplist = SkipList(max_level=3, p=0.5)

    # Insert some elements
    skiplist.insert(3)
    skiplist.insert(6)
    skiplist.insert(7)
    skiplist.insert(9)
    skiplist.insert(12)
    skiplist.insert(19)
    skiplist.insert(17)

    # Display the skip list
    skiplist.display()

    # Search for elements
    skiplist.search(6)
    skiplist.search(15)

    # Delete elements and display again
    skiplist.delete(3)
    skiplist.delete(7)
    skiplist.display()
