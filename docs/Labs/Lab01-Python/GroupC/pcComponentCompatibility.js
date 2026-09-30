// Group C, Problem 1 Solution (JavaScript): PC Component Compatibility Checker
// This system uses nested if-else if statements to check component compatibility.

function checkCompatibility(socketType, ramType) {
    const socket = socketType.toUpperCase();
    const ram = ramType.toUpperCase();
    
    let result = "INCOMPATIBLE";

    console.log("\n--- PC Component Compatibility Check ---");
    console.log(`Components: Socket=${socket}, RAM=${ram}`);

    // Outer branch: Check the CPU Socket Type
    if (socket === "LGA1700") {
        // Inner branch: Check the required RAM Type
        if (ram === "DDR5") {
            result = "COMPATIBLE";
        } else {
            result = "INCOMPATIBLE (LGA1700 requires DDR5)";
        }
    } else if (socket === "AM4") {
        // Inner branch: Check the required RAM Type
        if (ram === "DDR4") {
            result = "COMPATIBLE";
        } else {
            result = "INCOMPATIBLE (AM4 requires DDR4)";
        }
    } else {
        // Unknown or unsupported socket type
        result = "INCOMPATIBLE (Unknown/Unsupported Socket Type)";
    }

    console.log(`Compatibility Status: ${result}`);
    console.log("--------------------------------------");
}

// Example 1: Compatible components
checkCompatibility("LGA1700", "DDR5");

// Example 2: Incompatible RAM
checkCompatibility("AM4", "DDR5");

// Example 3: Compatible components (lowercase input)
checkCompatibility("am4", "ddr4");
