import random

# Define constants and variables
R = 3
C = 5  # Total number of charging stations
T = 20
E_per_unit_dis = 2
q1 = 1
q2 = 1
cs_loc = 3  # Total number of CS locations
robot_speed = 1  # 1 meter/sec
total_area = 20  # Meter square, assuming each small cell is 1m² in area
highest_profit = 30
lowest_profit = 10

# Total_no_of_time_slots = 20
# No_of_orders = [3, 3, 3, 1, 5, 3, 4, 3, 4, 2, 2, 3, 1, 1, 4, 5, 6, 6, 4, 1]
No_of_orders = [3]  # To check with a small number of orders
Times = range(0, len(No_of_orders))
# Other constants and variables...

# Define initial battery degradation for robots
initial_deg = {i: 0.00001 for i in range(R)}  # {0 : 0.0001, 1: 0.00001, ...R: 0.0001}

# Define initial energy balance for robots
E_Balance_Zero = {i: 111 for i in range(R)}
Ebat = 111.0  # Battery capacity (Wh)
# Define initial degradation if you want different values for each robot
# Initial_deg = {0: 0.00001, 1: 0.00012, 2: 0.00005}

# Create robot, charging station, and task objects
class Robot:
    def __init__(self):
        self.cur_loc = (random.randint(0, total_area), random.randint(0, total_area))
        self.state_of_charge = round(random.uniform(Ebat, Ebat), 2)  # To have values up to two decimal points
        self.status = "idle"
        self.task_end_time = None
        self.charge_end_time = None
        self.allocated_task = None

    def __str__(self):
        return f"Robot(cur_loc={self.cur_loc}, state_of_charge={self.state_of_charge}, status={self.status}, task_end_time={self.task_end_time}, charge_end_time={self.charge_end_time}, allocated_task={self.allocated_task})"

class ChargingStation:
    def __init__(self, location):
        self.CS_location = location
        self.CS_status = "free"
        self.robot_charging = None

    def __str__(self):
        return f"ChargingStation(CS_location={self.CS_location}, CS_status={self.CS_status}, robot_charging={self.robot_charging})"

class Task:
    def __init__(self, k):
        random.seed(a=None, version=2)
        self.start_loc = (random.randint(0, total_area), random.randint(0, total_area))
        self.end_loc = (random.randint(0, total_area), random.randint(0, total_area))
        while self.start_loc == self.end_loc:
            self.end_loc = (random.randint(0, total_area), random.randint(0, total_area))
        self.value = random.randint(lowest_profit, highest_profit)
        self.arrival_time = k
        self.deadline = self.arrival_time + random.randint(10, 20)
        self.total_distance_to_cover = abs(self.start_loc[0] - self.end_loc[0]) + abs(self.start_loc[1] - self.end_loc[1])

    def __str__(self):
        return f"Task(start_loc={self.start_loc}, end_loc={self.end_loc}, value={self.value}, arrival_time={self.arrival_time}, deadline={self.deadline}, total_distance_to_cover={self.total_distance_to_cover})"

# Create initial lists
all_robots = [Robot() for _ in range(R)]
avail_robots = all_robots.copy()
charging_locations = [(random.randint(0, total_area), random.randint(0, total_area)) for _ in range(cs_loc)]
all_CS = [ChargingStation(charging_locations[i % 2]) for i in range(C)]
avail_CS = all_CS.copy()
all_tasks = []

for k in Times:
    if k == 0:
        all_tasks = [Task(k) for _ in range(No_of_orders[k])]
        avail_tasks = all_tasks.copy()

# Calculate the energy required for each task based on distance
for task in avail_tasks:
    task.energy_required = task.total_distance_to_cover * E_per_unit_dis

# Define a function to calculate energy consumption per time unit
def calculate_energy_consumption(task, robot):
    if task.total_distance_to_cover > 0:
        return task.energy_required / (task.total_distance_to_cover / robot_speed)
    else:
        return 0

# Define a function to allocate robots to tasks
def allocate_robot_to_task(robot, task):
    # Update the robot's status and allocated task
    robot.status = "busy"
    robot.allocated_task = task

    # Calculate energy consumption per time unit
    robot.energy_consumption_rate = calculate_energy_consumption(task, robot)

# Define a function to perform energy deduction per time unit
def deduct_energy_per_time_unit(robot):
    if robot.status == "busy":
        # Deduct energy based on energy consumption rate    
        robot.state_of_charge -= robot.energy_consumption_rate
    elif robot.status == "charging":
        # Charging logic here, if needed
        pass
    elif robot.status == "idle":
        # Idle logic here, if needed
        pass

# Define a function to allocate robots to tasks using your allocation logic
def random_allocation(avail_robots, avail_tasks, num_to_allocate):
    allocated_robots = []
    state_of_charge_history = {robot: [] for robot in avail_robots}

    while num_to_allocate > 0 and avail_robots and avail_tasks:
        # Randomly select a robot and a task
        selected_robot = random.choice(avail_robots)
        selected_task = random.choice(avail_tasks)

        # Allocate the robot to the task
        allocate_robot_to_task(selected_robot, selected_task)

        # Remove the selected robot and task from their respective lists
        avail_robots.remove(selected_robot)
        avail_tasks.remove(selected_task)

        # Add the selected robot to the list of allocated robots
        allocated_robots.append(selected_robot)
        num_to_allocate -= 1

    return allocated_robots, state_of_charge_history

# Create 2D matrix

matrix = [[0 for _ in range(len(avail_tasks) + len(avail_CS) + len(avail_robots))] for _ in range(len(avail_robots))]

# Calculate element values: 
# - First condition checks if it's a robot to task node.
# - Second condition checks if it's a robot to charging station.
# - Third condition checks if it's a robot to idle node.
for row_index, robot in enumerate(avail_robots):
    for col_index in range(len(matrix[0])):
        if col_index < len(avail_tasks):
            task = avail_tasks[col_index]
            # Calculate distance between robot and task
            matrix[row_index][col_index] = (
                abs(robot.cur_loc[0] - task.start_loc[0]) + 
                abs(robot.cur_loc[1] - task.start_loc[1]) + 
                task.total_distance_to_cover
            )
        elif col_index < len(avail_tasks) + len(avail_CS):
            cs = avail_CS[col_index - len(avail_tasks)]
            # Calculate distance between robot and charging station
            matrix[row_index][col_index] = (
                abs(robot.cur_loc[0] - cs.CS_location[0]) + 
                abs(robot.cur_loc[1] - cs.CS_location[1])
            )
        else:
            # Assign a large negative value for robot to idle node
            matrix[row_index][col_index] = -100

# Print the matrix
print("\nMatrix:")
for row in matrix:
    print(row)

# Call the modified random_allocation function
allocated_robots, state_of_charge_history = random_allocation(avail_robots, avail_tasks, len(avail_robots))

# Time loop to simulate each time unit
for time_unit in range(T):
    # Deduct energy for each robot
    for robot in allocated_robots:
        deduct_energy_per_time_unit(robot)

    # Print the state of charge history for each robot at this time unit
    for robot, soc_history in state_of_charge_history.items():
        soc_history.append(robot.state_of_charge)
        print(f"Time Unit {time_unit}: Robot {robot} State of Charge = {robot.state_of_charge}")

if allocated_robots:
    print("Allocated Robots:")
    for robot in allocated_robots:
        print(robot)
else:
    print("No available robots.")

# Print the state of charge history for each robot
for robot, soc_history in state_of_charge_history.items():
    print(f"Robot {robot} State of Charge History:")
    for time_unit, soc in enumerate(soc_history):
        print(f"Time Unit {time_unit}: State of Charge = {soc}")
