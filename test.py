from SkipList import SkipList
from ToDoList import ToDoList
from WorkingToDoList import WorkingToDoList

def test_skiplist():
    skiplist = SkipList(max_level=3, p=0.5, verbose=True)

    skiplist.insert(3)
    skiplist.insert(6)
    skiplist.insert(7)
    skiplist.insert(9)
    skiplist.insert(12)
    skiplist.insert(19)
    skiplist.insert(17)

    print(skiplist)

    skiplist.search(6)
    skiplist.search(9)
    skiplist.search(15)

    skiplist.delete(3)
    skiplist.delete(7)
    print(skiplist)


def test_todolist():
    todolist = ToDoList(h=5, epsilon=0.2, verbose=True)

    for i in range(63):
        todolist.insert(i)

    print(todolist)

    todolist.search(6)
    todolist.search(9)
    todolist.search(15)

    todolist.delete(3)
    todolist.delete(7)
    print(todolist)


def test_working_todolist():
    # Create an instance of WorkingToDoList
    working_todolist = WorkingToDoList(h=11, epsilon=0.2, verbose=True)

    # Insert a few keys
    print("Inserting keys:")
    for i in range(10000):  # Inserting 20 keys (0-19)
        working_todolist.insert(i)
    print(working_todolist)

    # Search for some keys
    print("Searching for keys:")
    working_todolist.search(5)
    working_todolist.search(10)
    working_todolist.search(15)
    working_todolist.search(25)  # This should not be found

    # Delete a few keys
    print("Deleting keys:")
    working_todolist.delete(3)
    working_todolist.delete(7)
    working_todolist.delete(15)

    print(working_todolist)


if __name__ == "__main__":
    #test_skiplist()
    #test_todolist()
    test_working_todolist()