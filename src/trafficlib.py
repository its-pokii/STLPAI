


def check_car_zoneBox(carPosition,hUpperLine: int, hLowerLine: int, rVerticalLine: int, lVerticalLine: int):
    in_vertical_range = hUpperLine < carPosition[1] < hLowerLine
    in_horizontal_range = lVerticalLine < carPosition[0] < rVerticalLine
    return in_vertical_range and in_horizontal_range
    
def check_car_zone(carPosition,hUpperLine: int, hLowerLine: int):
    # Check if the car is between the lines
    if int(carPosition) > hUpperLine and int(carPosition) < hLowerLine:
        return True
    else:
        return False

def lineCrossedDown(carPosition,the_line):
    # Check if the car has crossed the line
    if carPosition[1] > the_line:
        return True
    else:
        return False
    
def lineCrossedUp(carPosition,the_line):
    # Check if the car has crossed the line
    if carPosition[1] < the_line:
        return True
    else:
        return False
    


def calculate_duration(traffic_density, queue_length, traffic_flow, min_time, max_time):
    #traffic flow = number of vehicles passing in the other green light direction
    #traffic density and queue length = number of vehicles in the waiting zone
    
    alpha = 0.5
    beta = 0.3 
    gamma = 0.2

    score = alpha * traffic_density + beta * queue_length + gamma * traffic_flow
    duration = min_time + (max_time - min_time) * score
    return duration