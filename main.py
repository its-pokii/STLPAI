import trafficLogic as tf


number = 0

while number != 3:

    colors = ['red','green']
    number = input("chose a traffic light color")

    if number == 1:
        tf.redlight()
    elif number == 2:
        tf.greenlight()
    else:
        break


