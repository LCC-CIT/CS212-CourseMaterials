// Problem 2 Solution: Simple Medical Diagnostic System (JavaScript)
// Uses combined boolean conditions (&& / !) within multi-branching to diagnose.

function diagnoseSymptoms(hasFever, hasCough) {
    // Convert booleans to strings for display
    const feverStr = hasFever ? "Yes" : "No";
    const coughStr = hasCough ? "Yes" : "No";
    console.log("------------------------------");
    console.log(`Patient Symptoms: Fever (${feverStr}), Persistent Cough (${coughStr})`);

    let diagnosis = "";

    // Check for the combination of symptoms (Highest concern first)
    if (hasFever && hasCough) {
        diagnosis = "Flu - Recommend rest and hydration.";
    } else if (hasFever && !hasCough) {
        diagnosis = "Possible Infection - Recommend primary care physician visit.";
    } else if (!hasFever && hasCough) {
        diagnosis = "Cold/Allergies - Recommend over-the-counter medication.";
    } else { // !hasFever and !hasCough
        diagnosis = "General Check-up - Patient appears healthy.";
    }

    console.log(`Diagnosis: ${diagnosis}`);
}

// Example 1: True Fever, True Cough (Flu)
diagnoseSymptoms(true, true);
// Example 2: False Fever, True Cough (Cold)
diagnoseSymptoms(false, true);
