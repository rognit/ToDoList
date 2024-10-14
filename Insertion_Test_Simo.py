#FINITO
from SkipList import SkipList
from ToDoList import ToDoList
from Working_Todo import WorkingToDoList
import time
import os
import matplotlib.pyplot as insertion_test_Plot
import random  # Import random for generating priorities



# Testing the SkipList and ToDoList
def Testing_Insertion(number_insertions):
    # Create a new skip list
    skiplist = SkipList(max_level=3, p=0.5, verbose=True)
    # Create a skip list with height 3 and epsilon value of 0.1
    todolist = ToDoList(h=5, epsilon=0.2, verbose=True)
    #Create Working to do list 
    working_todolist = WorkingToDoList(h=3, epsilon=0.5, verbose=True)







    # Measure SkipList insertion time
    n_element_inserted = 0
    time_VS_element_inserted_skiplist = []

    # Start measuring time for SkipList
    start_time = time.time()
    for element in range(number_insertions):
        skiplist.insert(element)  # Call the insert method from SkipList
        n_element_inserted += 1
        elapsed_time = time.time() - start_time
        time_VS_element_inserted_skiplist.append((n_element_inserted, elapsed_time))

    # Compute and print execution time for SkipList
    execution_time_skiplist = time.time() - start_time
    print(f"Execution time for SkipList: {execution_time_skiplist} seconds, for inserting {number_insertions} elements.")

    # Extract data for plotting SkipList
    elements_inserted_skiplist, time_instant_skiplist = zip(*time_VS_element_inserted_skiplist)

    # Plotting SkipList results
    insertion_test_Plot.figure(figsize=(10, 6))
    insertion_test_Plot.plot(elements_inserted_skiplist, time_instant_skiplist, color='red', label='SkipList Insertion')










    # Measure ToDoList insertion time
    value_priority_couple = [(element, random.randint(1, 10)) for element in range(number_insertions)]
    
    n_element_inserted = 0
    time_VS_element_inserted_todolist = []

    # Start measuring time for ToDoList
    start_time = time.time()
    for element in value_priority_couple:
        todolist.insert(element)  # Call the insert method from ToDoList
        n_element_inserted += 1
        elapsed_time = time.time() - start_time
        time_VS_element_inserted_todolist.append((n_element_inserted, elapsed_time))

    # Compute and print execution time for ToDoList
    execution_time_todolist = time.time() - start_time
    print(f"Execution time for ToDoList: {execution_time_todolist} seconds, for inserting {number_insertions} elements.")

    # Extract data for plotting ToDoList
    elements_inserted_todolist, time_instant_todolist = zip(*time_VS_element_inserted_todolist)

    # Plotting ToDoList results
    insertion_test_Plot.plot(elements_inserted_todolist, time_instant_todolist, color='blue', label='ToDoList Insertion')


    
    n_element_inserted = 0
    time_VS_element_inserted__Workingtodolist = []

    # Start measuring time for ToDoList
    start_time = time.time()
    for element in value_priority_couple:
        working_todolist.insert(element)  # Call the insert method from Working_ToDoList
        n_element_inserted += 1
        elapsed_time = time.time() - start_time
        time_VS_element_inserted__Workingtodolist.append((n_element_inserted, elapsed_time))

    # Compute and print execution time for ToDoList
    execution_time_working_todo = time.time() - start_time
    print(f"Execution time for ToDoList: {execution_time_working_todo} seconds, for inserting {number_insertions} elements.")

    # Extract data for plotting ToDoList
    elements_inserted_working_todolist, time_instant__working_todolist = zip(*time_VS_element_inserted_todolist)

    # Plotting ToDoList results
    insertion_test_Plot.plot(elements_inserted_working_todolist, time_instant__working_todolist,color='green', label='Working_ToDoList Insertion')

    




    # Finalize the plot
    insertion_test_Plot.title('Execution Time of Insertion vs. Elements Inserted')
    insertion_test_Plot.xlabel('Number of Elements Inserted')
    insertion_test_Plot.ylabel('Execution Time (seconds)')
    insertion_test_Plot.ylim(0, max(max(time_instant_skiplist), max(time_instant_todolist),max(time_instant__working_todolist)) * 1.1)  # Adjust y-limits
    insertion_test_Plot.grid()
    insertion_test_Plot.legend(title='Legend', fontsize='medium', frameon=True, edgecolor='black', facecolor='lightgray')

    # Display the plot
    insertion_test_Plot.show(block=False)

    # Crea la cartella dove salvare i grafici se non esiste
    save_folder = 'd:\Desktop\Plots'
    os.makedirs(save_folder, exist_ok=True)

    # Salva il grafico nella cartella specificata come immagine (es. PNG)
    save_path = os.path.join(save_folder, 'Plot_Insertions.png')
    insertion_test_Plot.savefig(save_path)

    return skiplist, todolist,working_todolist,number_insertions  # Return both data structures


# Run the insertion test
number_insertions = 500
Insertion_Test = Testing_Insertion(number_insertions)


