// Group A, Problem 1 Solution (JavaScript): Shipping Cost Calculator
// This system uses nested if-else if statements to determine cost based on Zone and Weight tiers.

function calculateShippingCost(weightKg, zone) {
    let cost = 0.0;
    // Convert zone to uppercase for robust comparison
    const z = zone.toUpperCase();

    console.log(`\n--- Shipping Cost Check ---`);
    console.log(`Package Details: ${weightKg} kg to Zone ${z}`);

    // Outer branch: Check the Destination Zone
    if (z === "A") {
        // Inner branch: Check the Weight Tiers
        if (weightKg <= 5) {
            cost = 10.00;
        } else if (weightKg <= 10) { // Implies > 5 kg
            cost = 15.00;
        } else { // Implies > 10 kg
            cost = 20.00;
        }
    } else if (z === "B") {
        if (weightKg <= 5) {
            cost = 15.00;
        } else if (weightKg <= 10) {
            cost = 20.00;
        } else {
            cost = 25.00;
        }
    } else if (z === "C") {
        if (weightKg <= 5) {
            cost = 20.00;
        } else if (weightKg <= 10) {
            cost = 25.00;
        } else {
            cost = 30.00;
        }
    } else {
        console.log("Error: Invalid shipping zone specified.");
        return;
    }

    console.log(`Calculated Shipping Cost: $${cost.toFixed(2)}`);
    console.log("----------------------------");
}

// Example 1: Zone A, 7.5 kg
calculateShippingCost(7.5, "A");
// Example 2: Zone C, 12.0 kg
calculateShippingCost(12.0, "C");
