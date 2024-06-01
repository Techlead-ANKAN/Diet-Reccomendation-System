from flask import Flask, render_template, request
import csv

app = Flask(__name__)

# Function to parse the nutrition distribution dataset
def parse_nutrition_distribution(filename):
    nutrition_data = {}
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            if len(row) >= 12:  # Check if row has enough elements
                food_id = int(row[0])
                nutrition_data[food_id] = {
                    'calories': float(row[1]),
                    'fats': float(row[2]),
                    'proteins': float(row[3]),
                    'iron': float(row[4]),
                    'calcium': float(row[5]),
                    'sodium': float(row[6]),
                    'potassium': float(row[7]),
                    'carbohydrates': float(row[8]),
                    'fiber': float(row[9]),
                    'vitamin_d': float(row[10]),
                    'sugars': float(row[11])
                }
    return nutrition_data


# Function to parse the food dataset
def parse_food(filename):
    food_data = {}
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            food_name = row[0]  # Extract food name
            food_data[food_name] = {
                'category': row[1],
                'servings': float(row[2]),
                'measurement': row[3]
            }
    return food_data

# Function to filter recommended food by meal preference
def filter_food_by_meal(recommended_food, meal_type):
    filtered_food = [food for food in recommended_food if food['meal_type'] == meal_type]
    return filtered_food

# Function to get recommended food items for underweight individuals
def get_underweight_recommendations():
    recommended_food = [
        {'name': 'Whole milk', 'meal_type': 'breakfast'},
        {'name': 'Nuts and seeds', 'meal_type': 'snack'},
        {'name': 'Avocado', 'meal_type': 'snack'},
        {'name': 'Cheese', 'meal_type': 'snack'},
        {'name': 'Dried fruits', 'meal_type': 'snack'}
    ]
    return recommended_food

# Function to get recommended food items for normal weight individuals
def get_normal_weight_recommendations():
    recommended_food = [
        {'name': 'Leafy greens (spinach, kale)', 'meal_type': 'lunch'},
        {'name': 'Lean proteins (chicken, fish, tofu)', 'meal_type': 'lunch'},
        {'name': 'Whole grains (brown rice, quinoa)', 'meal_type': 'dinner'},
        {'name': 'Healthy fats (olive oil, nuts)', 'meal_type': 'snack'},
        {'name': 'Fruits and vegetables', 'meal_type': 'snack'}
    ]
    return recommended_food

# Function to get recommended food items for overweight individuals
def get_overweight_recommendations():
    recommended_food = [
        {'name': 'Broccoli', 'meal_type': 'dinner'},
        {'name': 'Salmon', 'meal_type': 'dinner'},
        {'name': 'Beans and legumes', 'meal_type': 'dinner'},
        {'name': 'Oatmeal', 'meal_type': 'breakfast'},
        {'name': 'Greek yogurt', 'meal_type': 'snack'}
    ]
    return recommended_food

# Function to get recommended food items for obese individuals
def get_obesity_recommendations():
    recommended_food = [
        {'name': 'Green tea', 'meal_type': 'beverage'},
        {'name': 'Lean meats (chicken breast, turkey)', 'meal_type': 'lunch'},
        {'name': 'Non-starchy vegetables (broccoli, cauliflower)', 'meal_type': 'dinner'},
        {'name': 'Whole grains (quinoa, barley)', 'meal_type': 'dinner'},
        {'name': 'Berries (blueberries, strawberries)', 'meal_type': 'snack'}
    ]
    return recommended_food

# Function to calculate total calories based on recommended food items
def calculate_total_calories(recommended_food):
    total_calories = 0
    for food_item in recommended_food:
        food_name = food_item['name']
        if food_name in nutrition_data:
            total_calories += nutrition_data[food_name]['calories']
    return total_calories

# Parse the datasets
nutrition_data = parse_nutrition_distribution('nutrition_distribution.csv')
food_data = parse_food('food.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dietary', methods=['GET', 'POST'])  
def dietary():

    if request.method == 'POST':
        # Extract form data
        age = int(request.form['age'])
        height_cm = int(request.form['height'])
        weight_kg = int(request.form['weight'])
        gender = request.form['gender']
        activity_level = request.form['activity']
        weight_loss_plan = request.form['weight_loss_plan']
        meals_per_day = int(request.form['meals_per_day'])
        meal_preference = request.form['meal_preference']  # New form field for meal preference
        
        # Calculate BMI
        height_m = height_cm / 100
        bmi = weight_kg / (height_m * height_m)
        
        # Determine BMI category
        bmi_category = ''
        if bmi < 18.5:
            bmi_category = 'Underweight'
            recommended_food = get_underweight_recommendations()
        elif bmi < 24.9:
            bmi_category = 'Normal weight'
            recommended_food = get_normal_weight_recommendations()
        elif bmi < 29.9:
            bmi_category = 'Overweight'
            recommended_food = get_overweight_recommendations()
        else:
            bmi_category = 'Obesity'
            recommended_food = get_obesity_recommendations()
        
        # Modify recommendation based on meal preference
        if meal_preference == 'Breakfast':
            recommended_food = filter_food_by_meal(recommended_food, 'breakfast')
        elif meal_preference == 'Lunch':
            recommended_food = filter_food_by_meal(recommended_food, 'lunch')
        elif meal_preference == 'Dinner':
            recommended_food = filter_food_by_meal(recommended_food, 'dinner')

        # Calculate total calories
        total_calories = calculate_total_calories(recommended_food)
        
        return render_template('dietary.html', bmi=bmi, bmi_category=bmi_category, recommended_food=recommended_food, total_calories=total_calories)

    return render_template('dietary.html')

if __name__ == '__main__':
    app.run(debug=True)
