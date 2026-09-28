// Group C, Problem 1 Solution (C#): PC Component Compatibility Checker
// This system uses nested if-else if statements to check component compatibility.

using System;

public class PCCompatibilityChecker
{
    public static void CheckCompatibility(string socketType, string ramType)
    {
        // Use ToUpperInvariant() for reliable case-insensitive comparison
        string socket = socketType.ToUpperInvariant();
        string ram = ramType.ToUpperInvariant();
        
        string result = "INCOMPATIBLE";

        Console.WriteLine("\n--- PC Component Compatibility Check ---");
        Console.WriteLine($"Components: Socket={socket}, RAM={ram}");

        // Outer branch: Check the CPU Socket Type
        if (socket == "LGA1700")
        {
            // Inner branch: Check the required RAM Type
            if (ram == "DDR5")
            {
                result = "COMPATIBLE";
            }
            else
            {
                result = "INCOMPATIBLE (LGA1700 requires DDR5)";
            }
        }
        else if (socket == "AM4")
        {
            // Inner branch: Check the required RAM Type
            if (ram == "DDR4")
            {
                result = "COMPATIBLE";
            }
            else
            {
                result = "INCOMPATIBLE (AM4 requires DDR4)";
            }
        }
        else
        {
            // Unknown or unsupported socket type
            result = "INCOMPATIBLE (Unknown/Unsupported Socket Type)";
        }

        Console.WriteLine($"Compatibility Status: {result}");
        Console.WriteLine("--------------------------------------");
    }

    public static void Main(string[] args)
    {
        // Example 1: Compatible components
        CheckCompatibility("LGA1700", "DDR5");
        
        // Example 2: Incompatible RAM
        CheckCompatibility("AM4", "DDR5");
        
        // Example 3: Compatible components (lowercase input)
        CheckCompatibility("am4", "ddr4");
    }
}
