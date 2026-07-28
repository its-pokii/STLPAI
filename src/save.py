import pandas as pd

file_path = "src\\trafficData.xlsx"  # path to your actual file

# Read existing file (in case it already has some data/headers)
df = pd.read_excel(file_path)

new_row = pd.DataFrame(
    { "Estimated Discharge Rate" : [5],
      "Vehicles Crossed" : [10],
      "Green Duration" : [15]
     })

df = pd.concat([df, new_row], ignore_index=True)
df.to_excel(file_path, index=False)
