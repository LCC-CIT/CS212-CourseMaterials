# Problem 3 Solution: Coffee Order Configuration & Pricing (Python)
# Uses sequential if-elif-else statements to determine base price and apply surcharges.

def calculate_coffee_price(size, milk_type):
    """Calculates the total coffee price based on size and milk type."""
    base_price = 0.0
    milk_charge = 0.0

    print(f"Order: {size.capitalize()} with {milk_type.capitalize()} Milk")

    # Step 1: Determine Base Price (Multi-branching)
    if size.lower() == "small":
        base_price = 3.00
    elif size.lower() == "medium":
        base_price = 4.00
    elif size.lower() == "large":
        base_price = 5.50
    else:
        print("Error: Invalid size specified.")
        return

    # Step 2: Determine Milk Surcharge (Multi-branching on top of base logic)
    if milk_type.lower() == "oat":
        milk_charge = 0.75
    elif milk_type.lower() == "almond":
        milk_charge = 0.50
    elif milk_type.lower() == "dairy":
        milk_charge = 0.00
    else:
        print("Error: Invalid milk type specified.")
        return

    # Final Calculation
    total_price = base_price + milk_charge
    print(f"Base Price: ${base_price:.2f}")
    print(f"Milk Surcharge: ${milk_charge:.2f}")
    print(f"Total Price: ${total_price:.2f}")

# Example 1: Large with Oat Milk
calculate_coffee_price("Large", "Oat")
print("-" * 30)
# Example 2: Small with Dairy Milk
calculate_coffee_price("Small", "Dairy")
