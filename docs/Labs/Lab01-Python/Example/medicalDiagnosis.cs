// Problem 2 Solution: Simple Medical Diagnostic System (C#)
// Uses combined boolean conditions (&& / !) within multi-branching to diagnose.

using System;

public class MedicalDiagnoser
{
    public static void DiagnoseSymptoms(bool hasFever, bool hasCough)
    {
        // Convert booleans to strings for display
        string feverStr = hasFever ? "Yes" : "No";
        string coughStr = hasCough ? "Yes" : "No";
        Console.WriteLine("------------------------------");
        Console.WriteLine($"Patient Symptoms: Fever ({feverStr}), Persistent Cough ({coughStr})");

        string diagnosis = "";

        // Check for the combination of symptoms (Highest concern first)
        if (hasFever && hasCough)
        {
            diagnosis = "Flu - Recommend rest and hydration.";
        }
        else if (hasFever && !hasCough)
        {
            diagnosis = "Possible Infection - Recommend primary care physician visit.";
        }
        else if (!hasFever && hasCough)
        {
            diagnosis = "Cold/Allergies - Recommend over-the-counter medication.";
        }
        else // !hasFever and !hasCough
        {
            diagnosis = "General Check-up - Patient appears healthy.";
        }

        Console.WriteLine($"Diagnosis: {diagnosis}");
    }

    public static void Main(string[] args)
    {
        // Example 1: True Fever, True Cough (Flu)
        DiagnoseSymptoms(true, true);
        // Example 2: False Fever, True Cough (Cold)
        DiagnoseSymptoms(false, true);
    }
}
