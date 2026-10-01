# Problem 2 Solution: Simple Medical Diagnostic System (Python)
# Uses combined boolean conditions (AND/OR) within multi-branching to diagnose.

def diagnose_symptoms(has_fever, has_cough):
    """Provides a preliminary diagnosis based on binary symptoms."""
    # Convert booleans to strings for display
    fever_str = "Yes" if has_fever else "No"
    cough_str = "Yes" if has_cough else "No"
    print("-" * 30)
    print(f"Patient Symptoms: Fever ({fever_str}), Persistent Cough ({cough_str})")

    diagnosis = ""

    # Check for the combination of symptoms (Highest concern first)
    if has_fever and has_cough:
        diagnosis = "Flu - Recommend rest and hydration."
    elif has_fever and not has_cough:
        diagnosis = "Possible Infection - Recommend primary care physician visit."
    elif not has_fever and has_cough:
        diagnosis = "Cold/Allergies - Recommend over-the-counter medication."
    else: # not has_fever and not has_cough
        diagnosis = "General Check-up - Patient appears healthy."

    print(f"Diagnosis: {diagnosis}")

# Example 1: True Fever, True Cough (Flu)
diagnose_symptoms(True, True)
# Example 2: False Fever, True Cough (Cold)
diagnose_symptoms(False, True)
