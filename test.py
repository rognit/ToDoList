from SkipList import SkipList

# Testing the SkipList with display method
if __name__ == "__main__":
    skiplist = SkipList(max_level=3, p=0.5, verbose=True)

    # Insert some elements
    skiplist.insert(3)
    skiplist.insert(6)
    skiplist.insert(7)
    skiplist.insert(9)
    skiplist.insert(12)
    skiplist.insert(19)
    skiplist.insert(17)

    # Display the skip list
    print(skiplist)

    # Search for elements
    skiplist.search(6)
    skiplist.search(9)
    skiplist.search(15)

    # Delete elements and display again
    skiplist.delete(3)
    skiplist.delete(7)
    print(skiplist)
