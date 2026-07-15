


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
    
