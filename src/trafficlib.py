




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

def calculate_duration(queue_length, previous_green, vehicle_crossed, previous_estimated_discharge_rate):
    max_green = 45
    min_green = 10
    alpha = 0.8 
    messured_discharge_rate = vehicle_crossed / max(previous_green, 1)

    if previous_estimated_discharge_rate is None or previous_estimated_discharge_rate == 0:
        previous_estimated_discharge_rate = messured_discharge_rate
    
    estimated_discharge_rate = (alpha * previous_estimated_discharge_rate) + ((1 - alpha) * messured_discharge_rate)

    green_time = min(max_green, max(min_green, (queue_length / estimated_discharge_rate)))

    # return green_time, estimated_discharge_rate

    return green_time, estimated_discharge_rate