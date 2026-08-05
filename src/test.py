import random
import pandas as pd
import trafficlib as tl



FILE_PATH = "src/trafficData.xlsx"
CYCLES = 50

TRUE_DISCHARGE_RATE = 0.8


df = pd.read_excel(FILE_PATH)


previous_green = df["Green Duration"].iloc[-1]
previous_estimated_rate = df["Estimated Discharge Rate"].iloc[-1]
next_number = df["number"].iloc[-1] + 1


for cycle in range(CYCLES):

    queue_length = random.randint(5, 40)

    
    previous_crossed = round(previous_green * TRUE_DISCHARGE_RATE)

    green_duration, estimated_rate = tl.calculate_duration(
        queue_length=queue_length,
        previous_green=previous_green,
        vehicle_crossed=previous_crossed,
        previous_estimated_discharge_rate=previous_estimated_rate,
    )

    noise = random.uniform(-0.05, 0.05)

    real_discharge_rate = TRUE_DISCHARGE_RATE + noise

    vehicles_crossed = min(
        queue_length,
        round(real_discharge_rate * green_duration)
    )

    real_discharge_rate = vehicles_crossed / max(green_duration, 1)

    prediction_error = abs(
        estimated_rate - real_discharge_rate
    )

    print("=" * 50)
    print(f"Cycle : {next_number}")
    print(f"Queue : {queue_length}")
    print(f"Estimated Rate : {estimated_rate:.3f}")
    print(f"Real Rate : {real_discharge_rate:.3f}")
    print(f"Prediction Error : {prediction_error:.3f}")
    print(f"Vehicles Crossed : {vehicles_crossed}")
    print(f"Green Duration : {green_duration:.2f}")

    new_row = pd.DataFrame({
        "number": [next_number],
        "Queue": [queue_length],
        "Estimated Discharge Rate": [round(estimated_rate, 3)],
        "Real Discharge Rate": [round(real_discharge_rate, 3)],
        "Prediction Error": [round(prediction_error, 3)],
        "Vehicles Crossed": [vehicles_crossed],
        "Green Duration": [round(green_duration, 2)],
    })

    df = pd.concat([df, new_row], ignore_index=True)

    previous_green = green_duration
    previous_estimated_rate = estimated_rate
    next_number += 1

df.to_excel(FILE_PATH, index=False)
print("\nSimulation completed successfully!")