// --- Die Class ---
class Die {
    /** Represents a single, standard six-sided die. */
    roll() {
        // Returns a random integer between 1 and 6, inclusive.
        return Math.floor(Math.random() * 6) + 1;
    }
}

// --- Player Class ---
class Player {
    /** Represents a player with a name and a roll value. */
    constructor(name) {
        this.name = name;
        this.rollValue = 0;
    }

    /** Rolls the provided Die object and saves the result. */
    rollDie(die) {
        this.rollValue = die.roll();
        console.log(`${this.name} rolled a ${this.rollValue}.`);
    }
}

// --- DiceBattle Class ---
class DiceBattle {
    /** Manages the two players and the single die for the game. */
    constructor(p1Name, p2Name) {
        this.die = new Die();               // Composition: Game has a Die
        this.player1 = new Player(p1Name); // Composition: Game has Player 1
        this.player2 = new Player(p2Name); // Composition: Game has Player 2
    }

    /** Executes the game logic. */
    play() {
        console.log("\n--- Dice Battle Start (Node.js) ---");
        
        // Players take turns rolling the same die object
        this.player1.rollDie(this.die);
        this.player2.rollDie(this.die);

        // Determine the winner
        if (this.player1.rollValue > this.player2.rollValue) {
            console.log(`\n${this.player1.name} wins! (High Roll)`);
        } else if (this.player2.rollValue > this.player1.rollValue) {
            console.log(`\n${this.player2.name} wins! (High Roll)`);
        } else {
            console.log("\nIt's a draw!");
        }
        console.log("-----------------------------------");
    }
}

// --- Main Execution ---
// Initialize and play the game
const game = new DiceBattle("PlayerA", "PlayerB");
game.play();
