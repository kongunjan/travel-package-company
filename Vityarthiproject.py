import math
import random
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import mean_absolute_error, accuracy_score

# ==============================
# CONFIGURATION
# ==============================
gst_rate = 12

price_tiers = {
    (1, 3): 700,
    (4, 7): 600,
    (8, 10): 550
}

language_fees = {
    "english": 1200,
    "hindi": 800,
    "spanish": 1350,
    "french": 1500
}

experience_fees = {
    "beginner": 800,
    "intermediate": 1000,
    "expert": 1200
}

# ==============================
# HELPER FUNCTIONS
# ==============================
def get_price_per_place(num_places):
    for (first_num, last_num), price in price_tiers.items():
        if first_num <= num_places <= last_num:
            return price
    raise ValueError("Enter a valid number of places from 1 to 10.")

def calculate_total_cost(num_places, language, experience):
    per_place_price = get_price_per_place(num_places)
    base_cost = per_place_price * num_places
    language_cost = language_fees[language]
    experience_cost = experience_fees[experience]

    subtotal = base_cost + language_cost + experience_cost
    gst_amount = math.ceil((subtotal * gst_rate) / 100)
    total = subtotal + gst_amount

    return {
        "base_cost": base_cost,
        "language_cost": language_cost,
        "experience_cost": experience_cost,
        "subtotal": subtotal,
        "gst_amount": gst_amount,
        "total": total
    }

def classify_package(total):
    if total < 5000:
        return "Budget"
    elif total < 8000:
        return "Standard"
    else:
        return "Premium"

# ==============================
# DATASET GENERATION
# ==============================
def generate_dataset(num_samples=500):
    data = []

    languages = list(language_fees.keys())
    experiences = list(experience_fees.keys())

    for _ in range(num_samples):
        num_places = random.randint(1, 10)
        language = random.choice(languages)
        experience = random.choice(experiences)

        costs = calculate_total_cost(num_places, language, experience)
        total = costs["total"]
        category = classify_package(total)

        data.append({
            "num_places": num_places,
            "language": language,
            "experience": experience,
            "base_cost": costs["base_cost"],
            "language_cost": costs["language_cost"],
            "experience_cost": costs["experience_cost"],
            "subtotal": costs["subtotal"],
            "gst_amount": costs["gst_amount"],
            "total": total,
            "category": category
        })

    return pd.DataFrame(data)

# ==============================
# PREPROCESSING
# ==============================
def preprocess_data(df):
    df_encoded = pd.get_dummies(df, columns=["language", "experience"])
    return df_encoded

# ==============================
# TRAIN MODELS
# ==============================
def train_models(df):
    df_encoded = preprocess_data(df)

    # Features for regression
    X_reg = df_encoded.drop(columns=["total", "category", "base_cost", "language_cost", "experience_cost", "subtotal", "gst_amount"])
    y_reg = df_encoded["total"]

    X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
        X_reg, y_reg, test_size=0.2, random_state=42
    )

    reg_model = LinearRegression()
    reg_model.fit(X_train_reg, y_train_reg)
    reg_predictions = reg_model.predict(X_test_reg)
    reg_mae = mean_absolute_error(y_test_reg, reg_predictions)

    # Features for classification
    X_clf = X_reg.copy()
    y_clf = df["category"]

    X_train_clf, X_test_clf, y_train_clf, y_test_clf = train_test_split(
        X_clf, y_clf, test_size=0.2, random_state=42
    )

    clf_model = DecisionTreeClassifier(random_state=42)
    clf_model.fit(X_train_clf, y_train_clf)
    clf_predictions = clf_model.predict(X_test_clf)
    clf_accuracy = accuracy_score(y_test_clf, clf_predictions)

    return reg_model, clf_model, X_reg.columns, reg_mae, clf_accuracy

# ==============================
# USER INPUT FUNCTIONS
# ==============================
def choose_from(criteria, options):
    options_display = "/".join(options)
    while True:
        choice = input(f"{criteria} ({options_display}): ").strip().lower()
        if choice in options:
            return choice
        print(f"Please enter one of: {options_display}")

def ask_number_of_places_to_visit():
    while True:
        spots_to_see = input("Enter number of places to visit (1-10): ").strip()
        if not spots_to_see.isdigit():
            print("Please enter a whole number.")
            continue
        p = int(spots_to_see)
        if 1 <= p <= 10:
            return p
        print("ERROR: Enter a number between 1 and 10!")

def ask_budget():
    while True:
        budget = input("Enter your budget (₹): ").strip()
        if budget.isdigit():
            return int(budget)
        print("Please enter a valid budget amount.")

# ==============================
# PREPARE SINGLE USER INPUT FOR MODEL
# ==============================
def prepare_user_input(num_places, language, experience, feature_columns):
    user_data = {
        "num_places": num_places
    }

    # initialize all dummy columns as 0
    for col in feature_columns:
        if col != "num_places":
            user_data[col] = 0

    lang_col = f"language_{language}"
    exp_col = f"experience_{experience}"

    if lang_col in user_data:
        user_data[lang_col] = 1
    if exp_col in user_data:
        user_data[exp_col] = 1

    user_df = pd.DataFrame([user_data])
    user_df = user_df[feature_columns]
    return user_df

# ==============================
# RECOMMENDATION ENGINE
# ==============================
def recommend_best_package(user_budget):
    best_option = None
    min_diff = float("inf")

    for num_places in range(1, 11):
        for language in language_fees.keys():
            for experience in experience_fees.keys():
                costs = calculate_total_cost(num_places, language, experience)
                total = costs["total"]

                if total <= user_budget:
                    diff = user_budget - total
                    if diff < min_diff:
                        min_diff = diff
                        best_option = {
                            "num_places": num_places,
                            "language": language,
                            "experience": experience,
                            "total": total
                        }

    return best_option

# ==============================
# MAIN PROGRAM
# ==============================
def main():
    print("========== AI-Powered Smart Travel Package System ==========\n")

    # Step 1: Generate and train models
    print("Generating dataset and training AI/ML models...")
    df = generate_dataset(500)

    reg_model, clf_model, feature_columns, reg_mae, clf_accuracy = train_models(df)

    print(f"Model training complete!")
    print(f"Price Prediction Model MAE: ₹{reg_mae:.2f}")
    print(f"Package Classification Accuracy: {clf_accuracy * 100:.2f}%\n")

    # Step 2: User input
    num_places = ask_number_of_places_to_visit()
    language = choose_from("Choose language for your tourist guide", list(language_fees.keys()))
    experience = choose_from("Choose your guide experience", list(experience_fees.keys()))
    budget = ask_budget()

    # Step 3: Actual calculation
    actual_costs = calculate_total_cost(num_places, language, experience)

    # Step 4: ML prediction
    user_input_df = prepare_user_input(num_places, language, experience, feature_columns)

    predicted_price = reg_model.predict(user_input_df)[0]
    predicted_category = clf_model.predict(user_input_df)[0]

    # Step 5: Recommendation
    recommendation = recommend_best_package(budget)

    # Step 6: Display results
    print("\n================ PRICE BREAKDOWN ================")
    print(f"Base cost (places):                 ₹{actual_costs['base_cost']}")
    print(f"Language extra cost:               ₹{actual_costs['language_cost']}")
    print(f"Guide experience extra cost:       ₹{actual_costs['experience_cost']}")
    print(f"Subtotal:                          ₹{actual_costs['subtotal']}")
    print(f"GST ({gst_rate}%):                         ₹{actual_costs['gst_amount']}")
    print(f"Final total cost:                  ₹{actual_costs['total']}")

    print("\n================ AI/ML PREDICTIONS ================")
    print(f"Predicted Package Price (ML):      ₹{predicted_price:.2f}")
    print(f"Predicted Traveler Category:       {predicted_category}")

    print("\n================ SMART RECOMMENDATION ================")
    if recommendation:
        print(f"Best package within your budget (₹{budget}):")
        print(f"  Places to visit: {recommendation['num_places']}")
        print(f"  Guide language: {recommendation['language'].title()}")
        print(f"  Guide experience: {recommendation['experience'].title()}")
        print(f"  Estimated total: ₹{recommendation['total']}")
    else:
        print("Sorry! No package fits within your budget.")

    print("\nThank you for using the AI Travel Package System!")

# Run program
if __name__ == "__main__":
    main()
