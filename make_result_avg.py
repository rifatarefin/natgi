import pandas as pd

# Read the CSV file
csv_file_path = "Result_cp.csv"  # Replace with your actual file path
df = pd.read_csv(csv_file_path)

# Group by 'program_name' and compute the average of numeric columns
average_df = df.groupby("program_name").mean(numeric_only=True).reset_index()
average_df.to_csv('TMP.csv')
#print(average_df)
