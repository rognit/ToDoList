
#FINITO
from Insertion_Test_Simo import *
from Search_Test_Simo import *
from Deletion_Test_Simo import *
from Alternate_Insertion_Deletion_Test_Simo import *
import threading


number_insertions = 5000
number_searches = number_insertions*5
number_deletion = 5000
number_insertions_deletions = 5000

Insertion_Test = Testing_Insertion(number_insertions)
Search_Test = Testing_Searching(number_searches)
Deletion_Test = Testing_Deletion(number_deletion)
Insertion_Deletion_Test = Testing_Insertion_Deletion(number_insertions_deletions)


