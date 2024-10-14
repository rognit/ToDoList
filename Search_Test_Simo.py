from SkipList import SkipList
from ToDoList import ToDoList
from Working_Todo import WorkingToDoList
import time
import os
import matplotlib.pyplot as plt
#import matplotlib.pyplot as searching_test_Plot
import random  # Import random for generating priorities


number_insertions  = 9000

# Create a new skip list
skiplist = SkipList(max_level=5, p=0.5, verbose=True)
# Create a skip list with height 3 and epsilon value of 0.1
todolist = ToDoList(h=5, epsilon=0.2, verbose=True)
#Create Working to do list 
working_todolist = WorkingToDoList(h=5, epsilon=0.5, verbose=True)


start_skiplist = time.time()
for element in range(number_insertions):

    skiplist.insert(random.randint(1,10000000))  # Call the insert method from SkipList
finsh_skiplist = time.time()
time_tot_skip_ins = finsh_skiplist - start_skiplist




start_todo = time.time()
for element in range(number_insertions):
    todolist.insert(random.randint(1,10000000))  # Call the insert method from ToDoList
finsh_todo = time.time()
time_tot_todo_ins = finsh_todo - start_todo




start_working_todo = time.time()
for element in range(number_insertions):
    working_todolist.insert(random.randint(1,10000000))  # Call the insert method from Working_ToDoList
finsh_working_todo = time.time()
time_working_todo_ins = finsh_working_todo - start_working_todo











searching_number = number_insertions * 20

# Lists to store time data
time_skiplist = []
time_todolist = []
time_working_todo = []

# Measure time for SkipList
start_skiplist = time.time()
for element in range(searching_number):
    skiplist.search(random.randint(1, 10000000))
    current_time = time.time() - start_skiplist
    time_skiplist.append(current_time)

# Measure time for ToDoList
start_todo = time.time()
for element in range(searching_number):
    todolist.search(random.randint(1, 10000000))
    current_time = time.time() - start_todo
    time_todolist.append(current_time)

# Measure time for Working_ToDoList
start_working_todo = time.time()
for element in range(searching_number):
    working_todolist.search(random.randint(1, 10000000))
    current_time = time.time() - start_working_todo
    time_working_todo.append(current_time)

# Plot the results
plt.figure(figsize=(10, 6))

# X-axis is the search number, Y-axis is time (cumulative)
x_axis = list(range(1, searching_number + 1))

plt.plot(x_axis, time_skiplist, label="SkipList", color='blue')
plt.plot(x_axis, time_todolist, label="ToDoList", color='green')
plt.plot(x_axis, time_working_todo, label="Working_ToDoList", color='red')

plt.xlabel('Number of Searches')
plt.ylabel('Time (seconds)')
plt.title('Search Time vs Number of Searches')
plt.legend()
plt.grid(True)

plt.show()


print(f"I tre metodi ci hanno messo per inserire: {time_tot_skip_ins},{time_tot_todo_ins},{time_working_todo_ins}")
#print(f"I tre metodi ci hanno messo per cercare: {time_tot_skip},{time_tot_todo},{time_working_todo}")








'''
# Testing the SkipList and ToDoList
def Testing_Searching(number_searches):
    
    # Initialize data structures
    # Create a new skip list
    skiplist = SkipList(max_level=3, p=0.5, verbose=True)
    # Create a skip list with height 3 and epsilon value of 0.1
    todolist = ToDoList(h=5, epsilon=0.2, verbose=True)
    #Create Working to do list 
    working_todolist = WorkingToDoList(h=3, epsilon=0.5, verbose=True)
    

    # Measure SkipList searching time
    time_VS_element_inserted_skiplist = []
    
    # Start measuring time for SkipList
    start_time = time.time()
    for n_element_inserted in range(1, number_searches + 1):
        skiplist.search(random.randint(1, 10000))  # Search for numbers between (1 and 10000)
        elapsed_time = time.time() - start_time
        time_VS_element_inserted_skiplist.append((n_element_inserted, elapsed_time))

    # Compute and print execution time for SkipList
    execution_time_skiplist = time.time() - start_time
    print(f"Execution time for SkipList: {execution_time_skiplist} seconds, for searching {number_searches} elements.")

    # Extract data for plotting SkipList
    elements_inserted_skiplist, time_instant_skiplist = zip(*time_VS_element_inserted_skiplist)

    # Plotting SkipList results
    searching_test_Plot.figure(figsize=(10, 6))
    searching_test_Plot.plot(elements_inserted_skiplist, time_instant_skiplist, color='red', label='SkipList Searching')








    value_priority_couple = [(element, random.randint(1, 10)) for element in range(number_searches)]

    # Measure ToDoList searching time
    time_VS_element_inserted_todolist = []

    # Start measuring time for ToDoList
    start_time = time.time()
    for n_element_inserted in range(1, number_searches + 1):
        todolist.search(random.randint(1, 10000))  # Search for numbers between (1 and 10000)
        elapsed_time = time.time() - start_time
        time_VS_element_inserted_todolist.append((n_element_inserted, elapsed_time))

    # Compute and print execution time for ToDoList
    execution_time_todolist = time.time() - start_time
    print(f"Execution time for ToDoList: {execution_time_todolist} seconds, for searching {number_searches} elements.")

    # Extract data for plotting ToDoList
    elements_inserted_todolist, time_instant_todolist = zip(*time_VS_element_inserted_todolist)

    # Plotting ToDoList results
    searching_test_Plot.plot(elements_inserted_todolist, time_instant_todolist, color='blue', label='ToDoList Searching')









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
    print(f"Execution time for ToDoList: {execution_time_working_todo} seconds, for inserting {number_searches} elements.")

    # Extract data for plotting ToDoList
    elements_inserted_working_todolist, time_instant__working_todolist = zip(*time_VS_element_inserted_todolist)

    # Plotting ToDoList results
    searching_test_Plot.plot(elements_inserted_working_todolist, time_instant__working_todolist,color='green', label='Working_ToDoList Insertion')





    # Finalize the plot
    searching_test_Plot.title('Execution Time of Searching vs. Elements Inserted')
    searching_test_Plot.xlabel('Number of Elements Searched')
    searching_test_Plot.ylabel('Execution Time (seconds)')
    searching_test_Plot.ylim(0, max(max(time_instant_skiplist), max(time_instant_todolist)) * 1.1)  # Adjust y-limits
    searching_test_Plot.grid()
    searching_test_Plot.legend(title='Legend', fontsize='medium', frameon=True, edgecolor='black', facecolor='lightgray')
    
    # Display the plot
    searching_test_Plot.show(block=False)

    # Crea la cartella dove salvare i grafici se non esiste
    save_folder = 'd:\Desktop\Plots'
    os.makedirs(save_folder, exist_ok=True)

    # Salva il grafico nella cartella specificata come immagine (es. PNG)
    save_path = os.path.join(save_folder, 'Plot_Searches.png')
    searching_test_Plot.savefig(save_path)

#Search_Test = Testing_Searching()
number_searches = 5000
Testing_Searching(number_searches)

'''