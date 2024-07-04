# Programmer: Abe Mefleh
# Program Description: This program analyzes fish weight statistics collected from various lakes in Maine.

# Define the fish data list
fish_data_list = [
    "1000 3.5",
    "1010 2.0",
    "1050 1.5",
    "1000 2.0",
    "1100 2.2",
    "1010 1.9",
    "1050 2.8",
    "1010 4.0"
]

# Initialize an empty dictionary to store fish data
fish_data = {}

# Process input data and populate the fish_data dictionary
for data in fish_data_list:
    try:
        lake_id, weight = map(float, data.split())
        if lake_id in fish_data:
            fish_data[lake_id].append(weight)
        else:
            fish_data[lake_id] = [weight]
    except ValueError:
        print("Invalid input format. Please enter in 'LakeID Weight' format.")

# Convert the dictionary to the required formatted list for further processing
formatted_fish_data = [(lake_id, "Lake" + str(lake_id), weights) for lake_id, weights in fish_data.items()]

# Processing and Statistics:

# Initialize variables for statistics
total_fish = sum(len(weights) for _, _, weights in formatted_fish_data) if formatted_fish_data else 0
total_weight = sum(sum(weights) for _, _, weights in formatted_fish_data)
heaviest_fish = max(weight for _, _, weights in formatted_fish_data for weight in weights) if formatted_fish_data else 0
lightest_fish = min(weight for _, _, weights in formatted_fish_data for weight in weights) if formatted_fish_data else 0

# Output: Displaying statistics and a histogram

# Displaying fish data in a table
print("\nLake ID    Lake Name    Fish Weight (lbs)")
print("-----------------------------------------")
for lake_id, lake_name, weights in formatted_fish_data:
    for weight in weights:
        print(f"{lake_id:<10} {lake_name:<12} {weight:.1f}")

# Displaying statistics
if total_fish > 0:
    average_weight = total_weight / total_fish
    print("\nStatistics:")
    print(f"Overall number of fish collected: {total_fish}")
    print(f"Average fish weight over all sites: {average_weight:.1f}")
    print(f"Weight of heaviest fish over all sites: {heaviest_fish:.1f}")
    print(f"Weight of lightest fish over all sites: {lightest_fish:.1f}")

    # Displaying the histogram
    print("\nLake        Fish Count")
    print("---------------------")
    for lake_id, lake_name, weights in formatted_fish_data:
        print(f"{lake_name:<10} {'*' * len(weights)}")
else:
    print("No statistics")
