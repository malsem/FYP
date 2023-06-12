import os
import pandas as pd
from durian_plant_analysis import analyze_durian_plant

# Define the directory containing the images
image_dir = "D:\Desktop\FYP\duriantrees1"

# Define the output file path
output_file = "D:\Desktop\FYP\Datasets_Durian.xlsx"

# Define the column names for the output file
column_names = ['image_name', 'canopy_size_cm', 'stem_size_cm', 'plant_height_cm', 'canopy_size', 'stem_size', 'plant_height', 'greenness_index', 'growth_rate', 'health', 'deficiencies', 'counteractions']

# Create an empty DataFrame to store the results
results_df = pd.DataFrame(columns=column_names)

# Loop over all the images in the directory
for image_name in os.listdir(image_dir):
    # Load the image
    image_path = os.path.join(image_dir, image_name)

    # Analyze the durian plant in the image
    result = analyze_durian_plant(image_path)

    # Add the result to the DataFrame
    result['image_name'] = image_name
    results_df = results_df._append(result, ignore_index=True)

# Save the results to the output file
results_df.to_excel(output_file, index=False)
