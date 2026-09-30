using System;
using System.Collections.Generic;

// --- Die Class ---
public class Die
{
    private static readonly Random Rng = new Random();

    /// <summary>
    /// Represents a single, standard six-sided die.
    /// </summary>
    public int Roll()
    {
        // Returns a random integer between 1 and 6, inclusive.
        return Rng.Next(1, 7);
    }
}

// --- Player Class ---
public class Player
{
    public string Name { get; private set; }
    public int RollValue { get; private set; }

    /// <summary>
    /// Represents a player with a name and a roll value.
    /// </summary>
    public Player(string name)
    {
        Name = name;
        RollValue = 0;
    }

    /// <summary>
    /// Rolls the provided Die object and saves the result.
    /// </summary>
    public void RollDie(Die die)
    {
        RollValue = die.Roll();
        Console.WriteLine($"{Name} rolled a {RollValue}.");
    }
}

// --- DiceBattle Class ---
public class DiceBattle
{
    private Die die;
    private Player player1;
    private Player player2;

    /// <summary>
    /// Manages the two players and the single die for the game.
    /// </summary>
    public DiceBattle(string p1Name, string p2Name)
    {
        this.die = new Die();           // Composition: Game has a Die
        this.player1 = new Player(p1Name); // Composition: Game has Player 1
        this.player2 = new Player(p2Name); // Composition: Game has Player 2
    }

    /// <summary>
    /// Executes the game logic and determines the winner.
    /// </summary>
    public void Play()
    {
        Console.WriteLine("\n--- Dice Battle Start (C#) ---");
        
        // Players take turns rolling the same die object
        player1.RollDie(die);
        player2.RollDie(die);

        // Determine the winner
        if (player1.RollValue > player2.RollValue)
        {
            Console.WriteLine($"\n{player1.Name} wins! (High Roll)");
        }
        else if (player2.RollValue > player1.RollValue)
        {
            Console.WriteLine($"\n{player2.Name} wins! (High Roll)");
        }
        else
        {
            Console.WriteLine("\nIt's a draw!");
        }
        Console.WriteLine("------------------------------");
    }
}

// --- Main Program Entry Point ---
public class Program
{
    public static void Main(string[] args)
    {
        // Initialize and play the game
        DiceBattle game = new DiceBattle("Clara", "David");
        game.Play();
        
        // Run a second time for variety
        DiceBattle secondGame = new DiceBattle("Clara", "David");
        secondGame.Play();
    }
}
