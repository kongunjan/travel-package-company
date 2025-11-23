# Travel Package Price Calculator

import math

gst_rate = 12


price_tiers = {
    (1, 3): 700,   
    (4, 7): 600,   
    (8, 10): 550}   





language_fees = {
    "english": 1200,
    "hindi": 800,
    "spanish": 1350,
    "french": 1500}



experinece_fees = {
    "beginner": 800,
    "intermediate": 1000,
    "expert": 1200}




def get_price_per_place(num_places):

    for (first_num, last_num), price in price_tiers.items():
        if first_num <= num_places <= last_num:
            return price
    raise ValueError("enter a valid number of places 1 thoygh 10.")

def choose_from(criteria, options):
    options_display = "/".join(options)
    while True:
        choice = input(f"{criteria} ({options_display}): ").strip().lower()
        if choice in options:
            return choice
        print(f"Please enter one of: {options_display}")
def ask__number_of_places_to_visit():
    while True:
        spots_to_see= input("Enter number of places to visit (1-10): ").strip()
        if not spots_to_see.isdigit():
         
            print("Please enter a whole number.")
            continue
        p = int(spots_to_see)
        if 1 <= p <= 10:
            return p
        print("ERROR: ENETER A number between 1 and 10!!")


def main():
    print("=== Travel Packagge Price Calculator ===\n")
    num_places = ask__number_of_places_to_visit()
    per_place_price = get_price_per_place(num_places)
    base_cost = per_place_price * num_places

    print(f"\nSelecteed places: {num_places} -> ₹{per_place_price} per place, each = ₹{base_cost}")
    language = choose_from("Choose language for your tourist guide", list (language_fees.keys()))
    language_extraprice_per_guide =   language_fees[language]
    print(f"Language: {language.title()} -> extra ₹{language_extraprice_per_guide}")
  


    
    experinece_ = choose_from("choose youwr guide experience", list(experinece_fees.keys()))
    experinece_extra_for_the_guide = experinece_fees[experinece_]
    print(f"guide experience: {experinece_.title()} -> extra ₹{experinece_extra_for_the_guide}")


    
    subtotal = base_cost + language_extraprice_per_guide + experinece_extra_for_the_guide
    gst_amount = math.ceil((subtotal * gst_rate) / 100)
    total = round(subtotal + gst_amount, 2)



    
    print("\n--- Price breakdown ---")
    print(f"Base cost (places) you visited during our service: ₹{base_cost}")
    print(f"Language extra price ooe has to pay :       ₹{language_extraprice_per_guide}")
    print(f"Experience extra price you have to pay:     ₹{experinece_extra_for_the_guide}")
    print(f"Subtotal of your amazing expreince:             ₹{subtotal}")
    print(f"GST (as goverment implimented) {gst_rate}%:        ₹{gst_amount}")
    print(f"Total payable price to us:        ₹{total}")
    print("--- END OF BILLL ---")
    print("\nThank you! \nSave this quote and contact the travel agent to confirm booking.")
main()

