import cv2
import numpy as np

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

def find_red_object(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return None
    
    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)
    return x, y, w, h

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

    # Return the width, height, and size as a dictionary
    return {'width': w, 'height': h, 'size': canopy_size}

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

# Custom function to analyze growth rate
def analyze_growth_rate(canopy_size, stem_size, plant_height):
    # You'll need to store previous measurements to calculate the growth rate
    # For this example, let's assume you have a list of previous measurements
    previous_measurements = [
        {'canopy_size': 1000, 'stem_size': (10, 100), 'plant_height': 120},
        {'canopy_size': 1100, 'stem_size': (12, 110), 'plant_height': 130},
        # Add more previous measurements here
    ]

    # Calculate the average growth rate for each feature
    canopy_growth_rate = (canopy_size - previous_measurements[-1]['canopy_size']) / len(previous_measurements)
    
    if stem_size is not None:
        stem_width_growth_rate = (stem_size[0] - previous_measurements[-1]['stem_size'][0]) / len(previous_measurements)
        stem_height_growth_rate = (stem_size[1] - previous_measurements[-1]['stem_size'][1]) / len(previous_measurements)
    else:
        stem_width_growth_rate = None
        stem_height_growth_rate = None

    plant_height_growth_rate = (plant_height - previous_measurements[-1]['plant_height']) / len(previous_measurements)

    growth_rate = {
        'canopy_growth_rate': canopy_growth_rate,
        'stem_width_growth_rate': stem_width_growth_rate,
        'stem_height_growth_rate': stem_height_growth_rate,
        'plant_height_growth_rate': plant_height_growth_rate
    }

    return growth_rate

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

def analyze_durian_plant(file_path):
    image = read_image(file_path)
    gray_image = preprocess_image(image)
    edges = detect_edges(gray_image)
    contours = segment_image(gray_image)
    canopy_data = extract_canopy_size(image)
    mask = analyze_nutrient_content(image)
    greenness_index = calculate_greenness_index(mask, canopy_data['size'])

    # Measure stem size and height
    stem_size = measure_stem_size(image, contours)
    plant_height = measure_height(contours)

    # Detect deficiencies and suggest counteractions
    deficiencies = detect_deficiencies(canopy_data['size'], stem_size, plant_height, greenness_index)

    # Analyze growth rate and health
    growth_rate = analyze_growth_rate(canopy_data['size'], stem_size, plant_height)
    health = analyze_health(greenness_index)

    # Detect deficiencies and suggest counteractions
    deficiencies = detect_deficiencies(canopy_data['size'], stem_size, plant_height, greenness_index)
    counteractions = suggest_counteractions(deficiencies)

    red_object = find_red_object(image)
    if red_object is not None:
        x, y, w, h = red_object
        pixel_to_cm_width = 30 / w
        pixel_to_cm_height = 30 / h
    else:
        # Set default pixel to cm conversion factors if the red reference object is not found
        pixel_to_cm_width = 0.1
        pixel_to_cm_height = 0.1

    # Convert the canopy_size, stem_size, and plant_height values to centimeters using the conversion factor
    canopy_size_cm = canopy_data['size'] * pixel_to_cm_width

    if stem_size is not None:
        stem_size_cm = (stem_size[0] * pixel_to_cm_width, stem_size[1] * pixel_to_cm_height)
    else:
        stem_size_cm = None

    plant_height_cm = plant_height * pixel_to_cm_height

    # Return the results as a dictionary
    return {
        'canopy_size_cm': canopy_size_cm,
        'stem_size_cm': stem_size_cm,
        'plant_height_cm': plant_height_cm,
        'canopy_size': canopy_data['size'],
        'stem_size': stem_size,
        'plant_height': plant_height,
        'canopy_width': canopy_data['width'],
        'canopy_height': canopy_data['height'],
        'greenness_index': greenness_index,
        'growth_rate': growth_rate,
        'health': health,
        'deficiencies': deficiencies,
        'counteractions': counteractions
    }

if __name__ == "__main__":
    file_path = 'D:\Desktop\FYP\duriantrees\durian_tree1.JPG'
    result = analyze_durian_plant(file_path)
    print(result)
