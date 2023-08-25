import random

# Define constants and variables
R = 3
C = 2
T = 20
E_per_unit_dis = 2
q1 = 1
q2 = 1

Total_no_of_time_slots = 20
No_of_orders = [3, 3, 3, 1, 5, 3, 4, 3, 4, 2, 2, 3, 1, 1, 4, 5, 6, 6, 4, 1]
#No_of_orders = [2, 1,2]###to check with small number of order 
Times = range(0, len(No_of_orders))


# Other constants and variables...

# Define initial battery degradation for robots
initial_deg = {i: 0.00001 for i in range(R)} #{0 : 0.0001, 1: 0.00001, ...R: 0.0001}

# Define initial energy balance for robots
E_Balance_Zero = {i: 111 for i in range(R)}

# Define initial degradation if you want different values for each robot
# Initial_deg = {0: 0.00001, 1: 0.00012, 2: 0.00005}

# Define available tasks as a dictionary
avail_tasks = []

# Define the task generation function
def task_generation(k):
    tasks = []
    for i in range(No_of_orders[k]):
        # Generate task attributes
        name = f'T{k}_{i}'
        start_loc = (random.randint(0, 9), random.randint(0, 9))  # Adjust bounds as needed
        end_loc = (random.randint(0, 9), random.randint(0, 9))  # Adjust bounds as needed
        arrival_time = k
        deadline = arrival_time + random.randint(5, 15)
        value = random.randint(5, 30)
        # Ensure start_loc and end_loc are not the same
        while start_loc == end_loc:
            end_loc = (random.randint(0, 9), random.randint(0, 9))
        
        # Create task dictionary
        task = {
            'name': name,
            'start_loc': start_loc,
            'end_loc': end_loc,
            'arrival_time': arrival_time,
            'deadline': deadline,
            'value': value
        }
        tasks.append(task)
    return tasks

# Define the Check_for_tasks function
def Check_for_tasks(k):
    tasks_generated = task_generation(k)
    avail_tasks[k] = tasks_generated #{1:[], 2:[], 3:[], ....} # Updating available tasks
    return avail_tasks # returning updated available tasks

# Define the Check_for_robots function (placeholder)
def Check_for_robots():
    # Add your implementation here
    pass

# just to check the avilable tasks are appendng or not
for k in Times:
   new_tasks = task_generation(k)
   avail_tasks=*avail_tasks, *new_tasks   ##adding new tasks in the existing avail_tasks list
print(f'updated available task list: {avail_tasks}') 



#####some operations on the avail_tasks list
print("Element at index 0:", avail_tasks[0]) ##to see the tasks with their attributes in index 0 means the first task
print("start loc of task in index 0:", avail_tasks[0]["start_loc"]) ## to see a particular attribute value of a particular task
del avail_tasks[0] ## to delete a task in a particular index e.g index 0



# Simulate the process over time units
# for k in range(T):
#     avail_tasks = Check_for_tasks(k)
#     print(f"Time Unit {k} - Available Tasks: {avail_tasks[k]}")
#     Check_for_robots()
    # Add more simulation steps or logic as needed

