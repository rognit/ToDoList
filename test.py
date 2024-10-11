from SkipList import SkipList
from ToDoList import ToDoList

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
    todolist = ToDoList(h=3, epsilon=0.1, verbose=True)

    todolist.insert(3)
    todolist.insert(6)
    todolist.insert(7)
    todolist.insert(9)
    todolist.insert(12)
    todolist.insert(19)
    todolist.insert(17)

    print(todolist)

    todolist.search(6)
    todolist.search(9)
    todolist.search(15)

    todolist.delete(3)
    todolist.delete(7)
    print(todolist)


if __name__ == "__main__":
    #test_skiplist()
    test_todolist()