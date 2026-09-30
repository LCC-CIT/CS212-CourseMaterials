// Group A, Problem 1 Solution (C#): Shipping Cost Calculator - Procedural Version
// This solution places all calculation logic directly within the Main method.

using System;

public class Program
{
    public static void Main(string[] args)
    {
        // --- INPUTS FOR DEMONSTRATION ---
        double weightKg = 7.5;
        string zone = "A";
        
        // Ensure zone is uppercase for robust comparison
        string z = zone.ToUpper(); 
        double cost = 0.0;
        bool isValid = true;

        Console.WriteLine("\n--- Shipping Cost Check (Procedural) ---");
        Console.WriteLine($"Package Details: {weightKg:F2} kg to Zone {z}");

        // Start of the multi-branching procedural logic
        
        // Outer branch: Check the Destination Zone
        if (z == "A")
        {
            // Inner branch: Check the Weight Tiers
            if (weightKg <= 5)
            {
                cost = 10.00;
            }
            else if (weightKg <= 10) 
            {
                cost = 15.00;
            }
            else // weightKg > 10
            {
                cost = 20.00;
            }
        }
        else if (z == "B")
        {
            if (weightKg <= 5)
            {
                cost = 15.00;
            }
            else if (weightKg <= 10)
            {
                cost = 20.00;
            }
            else
            {
                cost = 25.00;
            }
        }
        else if (z == "C")
        {
            if (weightKg <= 5)
            {
                cost = 20.00;
            }
            else if (weightKg <= 10)
            {
                cost = 25.00;
            }
            else
            {
                cost = 30.00;
            }
        }
        else
        {
            Console.WriteLine("Error: Invalid shipping zone specified.");
            isValid = false;
        }

        // Output the result procedurally
        if (isValid)
        {
            Console.WriteLine($"Calculated Shipping Cost: ${cost:F2}");
        }
        
        Console.WriteLine("----------------------------");

        // --- SECOND EXAMPLE RUN ---
        weightKg = 12.0;
        zone = "C";
        z = zone.ToUpper();
        cost = 0.0;
        isValid = true;

        Console.WriteLine("\n--- Shipping Cost Check (Second Run) ---");
        Console.WriteLine($"Package Details: {weightKg:F2} kg to Zone {z}");
        
        // REPEAT of the procedural logic for a second scenario
        if (z == "A")
        {
            if (weightKg <= 5) { cost = 10.00; }
            else if (weightKg <= 10) { cost = 15.00; }
            else { cost = 20.00; }
        }
        else if (z == "B")
        {
            if (weightKg <= 5) { cost = 15.00; }
            else if (weightKg <= 10) { cost = 20.00; }
            else { cost = 25.00; }
        }
        else if (z == "C")
        {
            if (weightKg <= 5) { cost = 20.00; }
            else if (weightKg <= 10) { cost = 25.00; }
            else { cost = 30.00; }
        }
        else
        {
            Console.WriteLine("Error: Invalid shipping zone specified.");
            isValid = false;
        }

        if (isValid)
        {
            Console.WriteLine($"Calculated Shipping Cost: ${cost:F2}");
        }
        
        Console.WriteLine("----------------------------");
    }
}
