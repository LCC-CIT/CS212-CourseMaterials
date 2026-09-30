// Group B, Problem 1 Solution (C#): Meeting Room Reservation System
// This system uses multi-branching (attendees) with nested checks (projector).

using System;

public class RoomReservation
{
    public static void RecommendRoom(int attendees, bool projectorNeeded)
    {
        string room = "N/A";
        
        Console.WriteLine("\n--- Meeting Room Reservation ---");
        Console.WriteLine($"Request: Attendees={attendees}, Projector Needed={projectorNeeded}");

        // Check the number of attendees (outer branch)
        if (attendees >= 1 && attendees <= 5)
        {
            // Small Room (1-5 attendees)
            room = "Room Alpha (Small, No Projector)";
            
        }
        else if (attendees >= 6 && attendees <= 15)
        {
            // Medium Room (6-15 attendees) - Refine based on projector (inner branch)
            if (projectorNeeded)
            {
                room = "Room Beta (Medium, Has Projector)";
            }
            else
            {
                room = "Room Gamma (Medium, No Projector)";
            }
            
        }
        else if (attendees >= 16)
        {
            // Large Room (16+ attendees)
            room = "Reservation Denied (No large rooms available)";
            
        }
        else
        {
            // Invalid attendee count
            room = "Error: Invalid number of attendees.";
        }

        Console.WriteLine($"Recommended Room: {room}");
        Console.WriteLine("---------------------------------");
    }

    public static void Main(string[] args)
    {
        // Example 1: Small group, projector not needed
        RecommendRoom(4, false);

        // Example 2: Medium group, projector needed
        RecommendRoom(12, true);

        // Example 3: Too large
        RecommendRoom(20, true);
    }
}
