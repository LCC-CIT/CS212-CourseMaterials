// Group B, Problem 1 Solution (JavaScript): Meeting Room Reservation System
// This system uses multi-branching (attendees) with nested checks (projector).

function recommendRoom(attendees, projectorNeeded) {
    let room = "N/A";
    
    console.log("\n--- Meeting Room Reservation ---");
    console.log(`Request: Attendees=${attendees}, Projector Needed=${projectorNeeded}`);

    // Check the number of attendees (outer branch)
    if (attendees >= 1 && attendees <= 5) {
        // Small Room (1-5 attendees)
        room = "Room Alpha (Small, No Projector)";
        
    } else if (attendees >= 6 && attendees <= 15) {
        // Medium Room (6-15 attendees) - Refine based on projector (inner branch)
        if (projectorNeeded) {
            room = "Room Beta (Medium, Has Projector)";
        } else {
            room = "Room Gamma (Medium, No Projector)";
        }
        
    } else if (attendees >= 16) {
        // Large Room (16+ attendees)
        room = "Reservation Denied (No large rooms available)";
        
    } else {
        // Invalid attendee count
        room = "Error: Invalid number of attendees.";
    }

    console.log(`Recommended Room: ${room}`);
    console.log("---------------------------------");
}

// Example 1: Small group, projector not needed
recommendRoom(4, false);

// Example 2: Medium group, projector needed
recommendRoom(12, true);

// Example 3: Medium group, projector not needed
recommendRoom(10, false);
