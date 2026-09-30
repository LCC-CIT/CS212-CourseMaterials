import random

class Die:
    """Represents a single, standard six-sided die."""
    def roll(self):
        # Returns a random integer between 1 and 6, inclusive.
        return random.randint(1, 6)

class Player:
    """Represents a player with a name and a roll value."""
    def __init__(self, name):
        self.name = name
        self.roll_value = 0

    def roll_die(self, die):
        """Rolls the provided Die object and saves the result."""
        self.roll_value = die.roll()
        print(f"{self.name} rolled a {self.roll_value}.")

class DiceBattle:
    """Manages the two players and the single die for the game."""
    def __init__(self, p1_name, p2_name):
        self.die = Die() # Composition: Game has a Die
        self.player1 = Player(p1_name) # Composition: Game has Player 1
        self.player2 = Player(p2_name) # Composition: Game has Player 2

    def play(self):
        """Executes the game logic."""
        print("\n--- Dice Battle Start ---")
        
        # Players take turns rolling the same die object
        self.player1.roll_die(self.die)
        self.player2.roll_die(self.die)

        # Determine the winner
        if self.player1.roll_value > self.player2.roll_value:
            winner = self.player1.name
            print(f"\n{winner} wins! (High Roll)")
        elif self.player2.roll_value > self.player1.roll_value:
            winner = self.player2.name
            print(f"\n{winner} wins! (High Roll)")
        else:
            print("\nIt's a draw!")

if __name__ == "__main__":
    # Initialize and play the game
    game = DiceBattle("Alice", "Bob")
    game.play()
