import cv2
import numpy as np

def analyze_growth_rate(current_measurement, previous_measurements):
    # Calculate the average growth rate for each feature
    canopy_growth_rate = (current_measurement['canopy_size'] - previous_measurements[-1]['canopy_size']) / len(previous_measurements)
    
    if current_measurement['stem_size'] is not None:
        stem_width_growth_rate = (current_measurement['stem_size'][0] - previous_measurements[-1]['stem_size'][0]) / len(previous_measurements)
        stem_height_growth_rate = (current_measurement['stem_size'][1] - previous_measurements[-1]['stem_size'][1]) / len(previous_measurements)
    else:
        stem_width_growth_rate = None
        stem_height_growth_rate = None

    plant_height_growth_rate = (current_measurement['plant_height'] - previous_measurements[-1]['plant_height']) / len(previous_measurements)

    growth_rate = {
        'canopy_growth_rate': canopy_growth_rate,
        'stem_width_growth_rate': stem_width_growth_rate,
        'stem_height_growth_rate': stem_height_growth_rate,
        'plant_height_growth_rate': plant_height_growth_rate
    }

    return growth_rate
