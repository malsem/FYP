import cv2
import os
import numpy as np
from growth_rate_analysis import analyze_growth_rate

def read_image(file_path):
    image = cv2.imread(file_path)
    return image

def preprocess_image(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image

def detect_edges(gray_image):
    edges = cv2.Canny(gray_image, 100, 200)
    return edges

def segment_image(gray_image):
    ret, thresholded = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def process_durian_plant_images(image_paths):
    measurements = []
    previous_measurements = []
    current_measurement = None

    for image_path in image_paths:
        result = analyze_durian_plant(image_path, previous_measurements, current_measurement)
        measurements.append(result)
        previous_measurements.append(result)
        current_measurement = result

    return measurements

# Specify the folder locations for the current and previous sets of durian tree images
current_images_folder = 'D:\Desktop\FYP\duriantrees1'
previous_images_folder = 'D:\Desktop\FYP\duriantrees2'

# Automatically obtain the image paths from the folders
current_image_paths = [os.path.join(current_images_folder, img) for img in os.listdir(current_images_folder) if img.endswith('.jpg')]
previous_image_paths = [os.path.join(previous_images_folder, img) for img in os.listdir(previous_images_folder) if img.endswith('.jpg')]

# Process the images and obtain measurements
current_measurements = process_durian_plant_images(current_image_paths)
previous_measurements = process_durian_plant_images(previous_image_paths)

def extract_canopy_size(image):
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a Gaussian blur to reduce noise
    blurred_gray_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Apply the Canny edge detection algorithm
    edges = cv2.Canny(blurred_gray_image, 50, 150)

    # Find contours in the edges
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour (assuming it's the durian tree canopy)
    largest_contour = max(contours, key=cv2.contourArea)

    # Calculate the canopy size
    x, y, w, h = cv2.boundingRect(largest_contour)
    canopy_size = w * h

    return canopy_size

def analyze_nutrient_content(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_green = (30, 40, 40)
    upper_green = (90, 255, 255)
    mask = cv2.inRange(hsv_image, lower_green, upper_green)
    return mask

def calculate_greenness_index(mask, canopy_size):
    green_pixels = cv2.countNonZero(mask)
    greenness_index = green_pixels / canopy_size
    return greenness_index

    # Custom function to measure stem size
def measure_stem_size(image, contours):
    # You may need to adjust the following parameters based on your specific images
    stem_width_range = (5, 50)
    stem_height_range = (50, 300)

    stem_contours = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if stem_width_range[0] <= w <= stem_width_range[1] and stem_height_range[0] <= h <= stem_height_range[1]:
            stem_contours.append(contour)

    # Assuming there's only one stem in the image
    if len(stem_contours) == 1:
        x, y, w, h = cv2.boundingRect(stem_contours[0])
        stem_size = (w, h)
        return stem_size
    else:
        return None

# Custom function to measure plant height
def measure_height(contours):
    topmost = None
    bottommost = None

    for contour in contours:
        for point in contour:
            if topmost is None or point[0][1] < topmost[1]:
                topmost = point[0]
            if bottommost is None or point[0][1] > bottommost[1]:
                bottommost = point[0]

    if topmost is not None and bottommost is not None:
        plant_height = bottommost[1] - topmost[1]
        return plant_height
    else:
        return None

# Custom function to detect deficiencies
def detect_deficiencies(canopy_size, stem_size, plant_height, greenness_index):
    deficiencies = []

    if greenness_index < 0.7:
        deficiencies.append("low_greenness_index")

    # Add more deficiency detection conditions here
    if canopy_size < 1000:  # Adjust the threshold based on your domain knowledge
        deficiencies.append("small_canopy_size")

    if stem_size is not None and stem_size[0] < 10:  # Adjust the threshold based on your domain knowledge
        deficiencies.append("thin_stem")

    if plant_height < 100:  # Adjust the threshold based on your domain knowledge
        deficiencies.append("short_plant_height")

    return deficiencies

# Custom function to analyze health
def analyze_health(greenness_index):
    # You can use the greenness index to determine the health of the plant
    # For example, you can use predefined thresholds
    if greenness_index >= 0.7:
        health = "healthy"
    elif greenness_index >= 0.4:
        health = "moderately healthy"
    else:
        health = "unhealthy"

    return health

# Custom function to suggest counteractions
def suggest_counteractions(deficiencies):
    counteractions = []

    for deficiency in deficiencies:
        if deficiency == "low_greenness_index":
            counteractions.append("apply_nitrogen_fertilizer")

        # Add more counteractions for other deficiencies here
        if deficiency == "small_canopy_size":
            counteractions.append("increase_sunlight_exposure")

        if deficiency == "thin_stem":
            counteractions.append("apply_phosphorus_fertilizer")

        if deficiency == "short_plant_height":
            counteractions.append("apply_growth_stimulant")

    return counteractions


def analyze_durian_plant(image_path, previous_measurements, current_measurement=None):
    image = read_image(file_path)
    gray_image = preprocess_image(image)
    edges = detect_edges(gray_image)
    contours = segment_image(gray_image)
    canopy_size = extract_canopy_size(image)
    mask = analyze_nutrient_content(image)
    greenness_index = calculate_greenness_index(mask, canopy_size)

    # Measure stem size and height
    stem_size = measure_stem_size(image, contours)
    plant_height = measure_height(contours)

    # Detect deficiencies and suggest counteractions
    deficiencies = detect_deficiencies(canopy_size, stem_size, plant_height, greenness_index)

    # Analyze growth rate and health
    growth_rate = analyze_growth_rate(current_measurement, previous_measurements)
    health = analyze_health(greenness_index)

    # Detect deficiencies and suggest counteractions
    deficiencies = detect_deficiencies(canopy_size, stem_size, plant_height, greenness_index)
    counteractions = suggest_counteractions(deficiencies)

    reference_object_length_cm = 30  # Length of the reference object in centimeters (e.g., a 30 cm ruler)
    reference_object_length_pixels = 300  # Length of the reference object in pixels (measure this in the image)

    # Calculate the conversion factor (pixels to centimeters)
    pixels_to_cm = reference_object_length_cm / reference_object_length_pixels

    # Convert the canopy_size, stem_size, and plant_height values to centimeters using the conversion factor
    canopy_size_cm = canopy_size * pixels_to_cm

    if stem_size is not None:
        stem_size_cm = (stem_size[0] * pixels_to_cm, stem_size[1] * pixels_to_cm)
    else:
        stem_size_cm = None

    plant_height_cm = plant_height * pixels_to_cm

    # Return the results as a dictionary
    return {
        'canopy_size_cm': canopy_size_cm,
        'stem_size_cm': stem_size_cm,
        'plant_height_cm': plant_height_cm,
        'canopy_size': canopy_size,
        'stem_size': stem_size,
        'plant_height': plant_height,
        'greenness_index': greenness_index,
        'growth_rate': growth_rate,
        'health': health,
        'deficiencies': deficiencies,
        'counteractions': counteractions
    }

if __name__ == "__main__":
    file_path = 'D:\Desktop\FYP\duriantrees1\durian_tree1.JPG'
    result = analyze_durian_plant(file_path, previous_measurements, current_measurement=None)
    print(result)