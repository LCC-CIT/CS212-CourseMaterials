import random

# --- Occupant Classes ---

class Occupant:
    """
    Base class representing a person who can be in the car.
    """
    def __init__(self, name, role="passenger"):
        self.name = name
        self.role = role

    def get_info(self):
        """Returns the occupant's name and role."""
        return f"{self.name} ({self.role.capitalize()})"

class Driver(Occupant):
    """
    Subclass for the person responsible for operating the car.
    """
    def __init__(self, name):
        # Driver's role is fixed as 'driver'
        super().__init__(name, role="driver")

    def operate(self):
        """A driver-specific action."""
        return f"{self.name} is focusing on the road."

class Passenger(Occupant):
    """
    Subclass for non-driving occupants.
    """
    def __init__(self, name):
        # Passenger's role is fixed as 'passenger'
        super().__init__(name, role="passenger")

    def relax(self):
        """A passenger-specific action."""
        return f"{self.name} is enjoying the ride."

# --- Engine Class ---

class Engine:
    """
    Represents the car's engine component.
    """
    def __init__(self, model="V6 Turbo", max_power_hp=300):
        self.model = model
        self.max_power_hp = max_power_hp
        self.is_running = False
        self.fuel_level = 100 # Percentage

    def start(self):
        """Starts the engine."""
        if self.fuel_level > 0:
            self.is_running = True
            return f"The {self.model} engine rumbles to life!"
        else:
            return "Cannot start engine, fuel tank is empty."

    def stop(self):
        """Stops the engine."""
        self.is_running = False
        return f"The {self.model} engine shuts down."

    def consume_fuel(self, distance_km):
        """Simulates fuel consumption based on distance."""
        # Simple consumption model: 0.1% fuel loss per km
        consumption = distance_km * 0.1
        self.fuel_level = max(0, self.fuel_level - consumption)
        return consumption

# --- Car Class ---

class Car:
    """
    The main class representing the car, aggregating an Engine and Occupants.
    """
    def __init__(self, make, model, engine_model, engine_power):
        self.make = make
        self.model = model
        self.engine = Engine(engine_model, engine_power) # Composition: Car has an Engine
        self.occupants = []

    def add_occupant(self, occupant):
        """Adds an Occupant (Driver or Passenger) to the car."""
        # Ensure there is only one driver
        if occupant.role == "driver" and any(o.role == "driver" for o in self.occupants):
            return f"Error: {self.make} {self.model} already has a driver."
        
        self.occupants.append(occupant)
        return f"{occupant.name} ({occupant.role.capitalize()}) has boarded the car."

    def list_occupants(self):
        """Prints a list of all current occupants."""
        if not self.occupants:
            return "The car is empty."

        occupant_list = [o.get_info() for o in self.occupants]
        return f"Current occupants in the {self.make} {self.model}: {', '.join(occupant_list)}"

    def drive(self, distance_km):
        """Simulates driving the car a certain distance."""
        if not self.engine.is_running:
            return "Cannot drive. The engine is off."
        
        if not any(o.role == "driver" for o in self.occupants):
            return "Cannot drive. There is no driver in the car."
            
        if self.engine.fuel_level <= 0:
            return "Cannot drive. The fuel tank is empty."
        
        # Simulate driving and fuel consumption
        consumption = self.engine.consume_fuel(distance_km)
        
        # Check if we ran out of fuel mid-trip
        if self.engine.fuel_level <= 0:
            self.engine.is_running = False
            return f"Drove {distance_km:.1f} km, but ran out of fuel! Total fuel consumed: {consumption:.2f}%."
        
        return (f"The {self.make} {self.model} is driving {distance_km:.1f} km. "
                f"Fuel consumed: {consumption:.2f}%. Remaining fuel: {self.engine.fuel_level:.2f}%.")

# --- Simulation ---

if __name__ == "__main__":
    
    print("--- Car Simulation Start ---")
    
    # 1. Create components
    my_car = Car("Ford", "Mustang GT", "Coyote V8", 450)
    
    # 2. Create occupants
    driver = Driver("Alex")
    passenger1 = Passenger("Sarah")
    passenger2 = Passenger("Mike")
    
    print("\n--- Boarding the Car ---")
    print(my_car.add_occupant(driver))
    print(my_car.add_occupant(passenger1))
    print(my_car.add_occupant(passenger2))
    
    # Try adding a second driver (should fail)
    print(my_car.add_occupant(Driver("Bob"))) 
    
    print(my_car.list_occupants())
    
    print("\n--- Engine Operations ---")
    # Try driving before starting (should fail)
    print(my_car.drive(10)) 
    
    # Start the engine
    print(my_car.engine.start())
    
    print("\n--- Driving Simulation ---")
    
    # Driver performs an action
    print(driver.operate())
    # Passenger performs an action
    print(passenger1.relax())

    # Take a short drive
    print(my_car.drive(20))
    
    # Take a long drive to show fuel depletion
    long_distance = 500
    print(my_car.drive(long_distance))

    print(f"\nCurrent fuel level: {my_car.engine.fuel_level:.2f}%")
    print(my_car.engine.stop())
    print("\n--- Simulation End ---")
