

<h1>Python Crash Course for Programmers</h1>

[TOC]

## Overview of Python

Here’s a high‑altitude, programmer‑to‑programmer overview of Python that focuses on its “big picture” differences from C#, C++, and JavaScript — without drowning you in operator minutiae.  

---

### Syntax Philosophy: Readability First
Python’s core design principle, *“There should be one—and preferably only one—obvious way to do it”*[^1], drives its uncluttered, whitespace‑driven style.

- **Indentation as syntax**: Code blocks are defined by consistent indentation, not curly braces or semicolons. This forces a uniform visual structure and eliminates whole categories of style debates.
- **Minimal ceremony**: Variable declarations, type annotations, and scope markers are optional or lightweight. You often get more done with less text on screen.
- **Significant whitespace** means you can’t “hide” logic inside messy formatting — the visual layout *is* the structure.

---

### Paradigm Emphasis
- **Multi‑paradigm, but not in equal balance**  
  While Python supports OOP, functional programming, and procedural code, its sweet spot blends object orientation with functional elements — without the ceremony of C++ or Java’s class scaffolding.
- **Dynamic typing and duck typing**: Python favors type flexibility at runtime over compile‑time enforcement. Class types are implicit — *if it quacks and walks like a duck, it’s treated like a duck*.
- **First‑class functions**: You can pass, return, and store functions just like data, which supports a more functional style than many C‑family languages.

---

### Typing & Execution Model
- **Interpreted, dynamic runtime**: Execution happens line‑by‑line via an interpreter, which encourages rapid prototyping but requires different performance tuning instincts.
- **No explicit variable typing by default**: Type hints exist, but they’re optional and not enforced at runtime.
- **Memory management**: Handled automatically via reference counting and garbage collection — no explicit free/delete.

---

### Standard Library & Ecosystem
- Python’s *batteries‑included* philosophy means the standard library ships with tools for everything from JSON parsing to HTTP servers to regular expressions — more comparable to Java’s extensive core than JavaScript’s minimalism.
- The package ecosystem (PyPI) is a vast landscape, especially for data science, AI, automation, and scripting.

---

### Control Flow & Structure
- Fewer “ceremonial” constructs: For example, no `switch` statement, and many iteration patterns use high‑level abstractions like `for item in iterable` instead of manual index counters.
- Exceptions are the primary error‑handling mechanism — no checked exceptions like in Java, and idiomatic Python often uses *EAFP* (*Easier to Ask Forgiveness than Permission*) rather than *LBYL* (*Look Before You Leap*).

---

### Cultural Norms
- The community is heavily style‑guided by **PEP 8** (naming conventions, spacing, docstring formats), which makes Python codebases unusually consistent across projects.
- “Pythonic” is shorthand for idioms that balance clarity, brevity, and explicitness.

---

If you think of C#/C++/JS as languages that often make you *declare your intent to the compiler in detail before acting*, Python leans toward *just act, and let the runtime sort it out* — with readability as the social contract between developers.

---



## Comparison of C#, C++, JavaScript and Python

---

### Structure & Scaffolding
| Concept (C#/C++/JS)     | Python Equivalent         | Key Difference                                               |
| ----------------------- | ------------------------- | ------------------------------------------------------------ |
| `{ }` braces for blocks | Indentation (spaces/tabs) | Whitespace defines scope — no `{}` or `end`.                 |
| `;` terminators         | Newline                   | Statements end at line breaks unless explicitly continued.   |
| `main()` entry point    | Top‑level execution       | Any code at file root runs on import/execute; scripts often have `if __name__ == "__main__":`. |

---

### Typing & Variables
| In C#/C++                           | In Python                            | Mental Shift                                           |
| ----------------------------------- | ------------------------------------ | ------------------------------------------------------ |
| Static typing, explicit declaration | Dynamic typing, implicit declaration | No type keyword; variables appear on first assignment. |
| Overloads by signature              | Single definition, dynamic behavior  | Duck typing replaces compile‑time overload resolution. |
| `const`/`readonly`                  | No built‑in immutability enforcement | Convention and immutable types (tuple, str) instead.   |

---

### Functions & Methods
| In C#/C++/JS          | In Python                  | Mental Shift                                       |
| --------------------- | -------------------------- | -------------------------------------------------- |
| Explicit return types | No declared return type    | You can return any type at runtime.                |
| Overloading           | No traditional overloading | Default args and `*args/**kwargs` for flexibility. |
| Lambda expressions    | Lambda expressions         | Limited to a single expression (no statements).    |

---

### OOP Model
| In C#/C++/JS                                 | In Python                      | Mental Shift                                                 |
| -------------------------------------------- | ------------------------------ | ------------------------------------------------------------ |
| Class members with explicit access modifiers | All members public by default  | `_single_underscore` signals “internal use” by convention.   |
| Method overloading                           | No overloads, but default args | Same method name re‑assignment overrides.                    |
| Interfaces                                   | Informal via duck typing       | Use `abc` module for formal abstract base classes if needed. |

---

### Control Flow
| In C#/C++/JS              | In Python               | Mental Shift                                                 |
| ------------------------- | ----------------------- | ------------------------------------------------------------ |
| `for (int i=0; i<n; i++)` | `for item in iterable:` | Iterates over sequences/iterables directly.                  |
| `switch`                  | No direct equivalent    | Use `if/elif/else` chains or mapping dicts.                  |
| `try/catch`               | `try/except`            | Exceptions are common and preferred over manual checks (EAFP). |

---

### Ecosystem & Build Mentality
- **C#/C++**: Compiler step, explicit build artifacts.  
  **Python**: Direct execution; `.pyc` bytecode caching is transparent.  
- **JavaScript**: Minimal stdlib; ecosystem is npm‑driven.  
  **Python**: Massive stdlib + PyPI; scripting, tooling, data science, web, automation all use same base runtime.

---

#### Mindset Shift in Practice
If you’re coming from C#/C++/JS, think of Python as:
- **Less “declare before doing”** — jump in, test, refactor.
- **More emphasis on readability as a shared contract** rather than compiler guarantees.
- **Interfaces by behavior, not declaration**.

---



## Example: “FizzBuzz with a Twist”

This example wil help you *see* the “mental shift” from C#/C++/JavaScript to Python at a glance. This tiny but complete program touches on variables, control flow, functions, and basic I/O.

### C# Version

 ```csharp 
using System;   
class Program { 
    static void Main() {
        for (int i = 1; i <= 15; i++) {
            if (i % 15 == 0) Console.WriteLine("FizzBuzz");
            else if (i % 3 == 0) Console.WriteLine("Fizz");
            else if (i % 5 == 0) Console.WriteLine("Buzz");
            else Console.WriteLine(i);
        }
    }
}
 ```

### C++ Version
```cpp
#include <iostream>
using namespace std;
int main() {
    for (int i = 1; i <= 15; i++) {
        if (i % 15 == 0) cout << "FizzBuzz\n";
        else if (i % 3 == 0) cout << "Fizz\n";
        else if (i % 5 == 0) cout << "Buzz\n";
        else cout << i << "\n";
    }
    return 0;
}
```

### JavaScript Version
```javascript
for (let i = 1; i <= 15; i++) {
    if (i % 15 === 0) console.log("FizzBuzz");
    else if (i % 3 === 0) console.log("Fizz");
    else if (i % 5 === 0) console.log("Buzz");
    else console.log(i);
}
```

### Python Version
```python
for i in range(1, 16):
    if i % 15 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)
```

---

### Takeaways from the Examples

In Python there is/are:

- **No ceremony**: No `main()` scaffolding, `using`/`#include`, or type declarations — just logic.
- **Range semantics**: `range(1, 16)` produces integers 1–15, end‑exclusive like many iterator APIs.
- **Whitespace = blocks**: Indentation replaces `{ }`.
- **`print` is built‑in**: No namespace prefix (`System.Console`, `std::cout`, etc.).
- **Equality/operator differences**: `==` in Python compares values (like `===` in JS for most types).

---

### Why This Matters
When moving from a C‑style language, the hardest shift isn’t *what* you can do — Python covers that — but *how much less you have to declare before doing it*. You’ll find that encourages:
- Rapid prototyping
- More readable “top‑to‑bottom” scripts
- Fewer mental hops between boilerplate and logic

---

## Python “Gotcha” Field Guide

Dodge the common traps when coming from C#/C++/JavaScript.  

### 1. Mutability Surprises
- **Lists & dicts are mutable** — changes inside a function *persist* outside if you pass them as arguments.
- **Tuples** are immutable, but can hold mutable objects.
- **Default arguments trap**:  
  ```python
  def foo(items=[]):  # BAD: same list reused
      ...
  ```
  Use `None` and assign inside to avoid state bleed.

---

### 2. Truthiness Rules
- `0`, `0.0`, `''`, `[]`, `{}`, `None`, and `False` all evaluate to false in conditionals.
- Non‑empty containers are *truthy*, even if they contain falsy elements.

---

### 3. Integer & Float Behavior
- Integers are **arbitrary precision** — no 32/64‑bit overflow.
- Division `/` always returns a float. Use `//` for integer division.

---

### 4. Equality & Identity
- `==` checks *value equality*, `is` checks *object identity*.  
- In CPython, small integers and short strings may be cached, so `a is b` *might* be `True` in some cases — but don’t rely on it.

---

### 5. Imports & Execution
- Importing a module runs its top‑level code once and caches it.
- Circular imports can break in surprising ways — reorganize shared code into a common module.

---

### 6. Variable Scope & Closures
- Python’s closure variables are **late‑bound**:  
  ```python
  funcs = [lambda: i for i in range(3)]
  funcs[0]()  # returns 2, not 0
  ```
  Fix with default arg capture: `lambda i=i: i`.

---

### 7. Looping Nuances
- `for` loops iterate directly over iterables — modifying the sequence while iterating can cause skipped items.
- `range` objects are lazy; convert to list if you need materialized values.

---

### 8. Concurrency Expectations
- Threads are limited by the GIL for CPU‑bound work — use multiprocessing or native extensions for heavy CPU tasks.
- Async/await is cooperative — tasks only switch at `await` points.

---

### 9. String Encoding
- All `str` are Unicode. Explicitly `.encode()` to bytes for file/network I/O when needed.
- Mixing bytes and strings without conversion raises `TypeError`.

---

### 10. Philosophy Shift
- **EAFP** (“Easier to Ask Forgiveness than Permission”) beats heavy upfront type/feature checks.
- Embrace idioms like unpacking (`a, b = b, a`) and comprehension syntax for clarity and concision.

---



## Anti‑Pitfall Translation Table

This maps the *instincts* you might carry from C#/C++/JavaScript to their Python‑safe equivalents. It’s meant to be a cognitive bridge so your habits rewire smoothly.

---

### Common Instincts vs. Pythonic Practice

| If You’re Used To… (C#/C++/JS)                        | In Python, Do This Instead                              | Why / Mindset Shift                                          |
| ----------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------------ |
| Declaring types (`int x = 0;`)                        | Just assign: `x = 0`                                    | Type is inferred dynamically; optional hints don’t affect runtime. |
| Using `{}` for blocks                                 | Indent consistently                                     | Whitespace defines scope — visual structure *is* syntax.     |
| For‑loops with counters (`for (i=0; i<n; i++)`)       | `for item in iterable:`                                 | Direct iteration over elements is idiomatic; counters via `enumerate()`. |
| Overloading by signature                              | Use default args, `*args`, `**kwargs`                   | Behavior adapts at runtime; no compile‑time signature resolution. |
| `const` or `readonly`                                 | Trust convention, use immutables (`tuple`, `frozenset`) | No enforced const; naming (`UPPER_CASE`) signals constants.  |
| Manual memory management                              | Let GC handle it                                        | Reference counting + garbage collection remove `malloc`/`free` concerns. |
| Compiling before running                              | Just run `.py` file                                     | Interpreter executes source directly; `.pyc` bytecode caching is automatic. |
| `switch` statements                                   | `if/elif/else` or dict mapping                          | Control flow favors simplicity and data‑driven dispatch.     |
| Guarding with type/feature checks                     | Wrap in `try/except`                                    | EAFP: attempt action, handle exceptions.                     |
| Small int/short string identity quirks (`==` vs `is`) | Use `==` for value equality                             | `is` only for object identity (e.g., `x is None`).           |
| Modifying a list while looping                        | Iterate over copy or build new list                     | Prevents skipped elements due to mutation during iteration.  |
| Threading for CPU‑bound speed‑ups                     | Use multiprocessing or native extensions                | GIL limits Python threads for pure Python CPU work.          |

---

### Quick Memory Hooks
- **Whitespace is law** → your formatter *is* the compiler.
- **No type fences** → runtime duck typing means more flexibility, less ceremony.
- **Ask forgiveness** → exceptions > pre‑checks for many idioms.
- **Mutable ≠ safe default** → beware of shared state.
- **Iterables over indexes** → think data streams, not counter loops.

---



## Tic‑Tac‑Toe in C++, C#, JS, and Python

The game of tic-tac-toe written in four languages so you can compare architecture and idioms side‑by‑side.  

The *overall structure* is the same in each:  
- Board as a 1D array/list of 9 cells  
- Simple console UI  
- Loop for alternating turns  
- Win/draw detection in a helper function  
- Minimal but clear procedural style  

---

### C++  

```cpp
#include <iostream>
#include <vector>
using namespace std;

void printBoard(const vector<char>& b) {
    for (int i = 0; i < 9; i++) {
        cout << (b[i] ? b[i] : ' ');
        if (i % 3 != 2) cout << "|";
        if (i % 3 == 2 && i != 8) cout << "\n-+-+-\n";
    }
    cout << "\n";
}

bool checkWin(const vector<char>& b, char p) {
    int wins[8][3] = {{0,1,2},{3,4,5},{6,7,8},
                      {0,3,6},{1,4,7},{2,5,8},
                      {0,4,8},{2,4,6}};
    for (auto& w : wins)
        if (b[w[0]] == p && b[w[1]] == p && b[w[2]] == p)
            return true;
    return false;
}

int main() {
    vector<char> board(9, 0);
    char player = 'X';
    for (int turn = 0; turn < 9; ++turn) {
        printBoard(board);
        int move;
        cout << "Player " << player << " move (0-8): ";
        cin >> move;
        if (board[move]) { cout << "Invalid.\n"; --turn; continue; }
        board[move] = player;
        if (checkWin(board, player)) {
            printBoard(board);
            cout << player << " wins!\n";
            return 0;
        }
        player = (player == 'X') ? 'O' : 'X';
    }
    printBoard(board);
    cout << "Draw!\n";
}
```

---

### C#  
```csharp
using System;

class TicTacToe {
    static void PrintBoard(char[] b) {
        for (int i = 0; i < 9; i++) {
            Console.Write(b[i] == '\0' ? ' ' : b[i]);
            if (i % 3 != 2) Console.Write("|");
            if (i % 3 == 2 && i != 8) Console.Write("\n-+-+-\n");
        }
        Console.WriteLine();
    }

    static bool CheckWin(char[] b, char p) {
        int[,] wins = { {0,1,2},{3,4,5},{6,7,8},
                        {0,3,6},{1,4,7},{2,5,8},
                        {0,4,8},{2,4,6} };
        for (int i = 0; i < wins.GetLength(0); i++)
            if (b[wins[i,0]] == p && b[wins[i,1]] == p && b[wins[i,2]] == p)
                return true;
        return false;
    }

    static void Main() {
        char[] board = new char[9];
        char player = 'X';
        for (int turn = 0; turn < 9; turn++) {
            PrintBoard(board);
            Console.Write($"Player {player} move (0-8): ");
            int move = int.Parse(Console.ReadLine());
            if (board[move] != '\0') { Console.WriteLine("Invalid."); turn--; continue; }
            board[move] = player;
            if (CheckWin(board, player)) {
                PrintBoard(board);
                Console.WriteLine($"{player} wins!");
                return;
            }
            player = (player == 'X') ? 'O' : 'X';
        }
        PrintBoard(board);
        Console.WriteLine("Draw!");
    }
}
```

---

### JavaScript (Node.js Console)  
```javascript
const readline = require('readline').createInterface({
  input: process.stdin, output: process.stdout
});

let board = Array(9).fill(null);
let player = 'X';

function printBoard(b) {
  for (let i = 0; i < 9; i++) {
    process.stdout.write(b[i] || ' ');
    if (i % 3 !== 2) process.stdout.write('|');
    if (i % 3 === 2 && i !== 8) process.stdout.write('\n-+-+-\n');
  }
  console.log();
}

function checkWin(b, p) {
  const wins = [[0,1,2],[3,4,5],[6,7,8],
                [0,3,6],[1,4,7],[2,5,8],
                [0,4,8],[2,4,6]];
  return wins.some(w => w.every(i => b[i] === p));
}

function nextTurn(turn = 0) {
  if (turn >= 9) { printBoard(board); console.log("Draw!"); return readline.close(); }
  printBoard(board);
  readline.question(`Player ${player} move (0-8): `, ans => {
    const move = parseInt(ans);
    if (board[move]) { console.log("Invalid."); return nextTurn(turn); }
    board[move] = player;
    if (checkWin(board, player)) {
      printBoard(board);
      console.log(`${player} wins!`);
      return readline.close();
    }
    player = (player === 'X') ? 'O' : 'X';
    nextTurn(turn + 1);
  });
}

nextTurn();
```

---

### Python  
```python
def print_board(b):
    for i in range(9):
        print(b[i] if b[i] else ' ', end='')
        if i % 3 != 2:
            print('|', end='')
        if i % 3 == 2 and i != 8:
            print('\n-+-+-')
    print()

def check_win(b, p):
    wins = [(0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)]
    return any(b[a] == b[b_] == b[c] == p for a,b_,c in wins)

board = [None]*9
player = 'X'

for turn in range(9):
    print_board(board)
    move = int(input(f"Player {player} move (0-8): "))
    if board[move]:
        print("Invalid.")
        continue
    board[move] = player
    if check_win(board, player):
        print_board(board)
        print(f"{player} wins!")
        break
    player = 'O' if player == 'X' else 'X'
else:
    print_board(board)
    print("Draw!")
```

---

### Cross‑Language Observations
- **Scaffolding overhead**: C++/C# need explicit entry points and library imports; Python/JS jump straight to logic.
- **Type verbosity**: C++/C# declare arrays with types; Python/JS just make a list/array.
- **Loop structure**: In Python/JS, loops often iterate directly; in C++/C#, classic `for` constructs are common.
- **Console I/O**: In Python, `print`/`input` are built‑ins; in JS, Node’s `console.log`/`readline` stand in; C++ uses streams; C# uses `Console` class.

---



## OO Version of Tic-Tac-Toe in Four Languages

This has the same **overall architecture and flow** we used before, but has a deliberately **parallel object‑oriented design** across C++, C#, JavaScript, and Python.  

The goal:  
- Same **class name** (`TicTacToe`)  
- Same **method names** (`printBoard`, `checkWin`, `play`)  
- Each language uses idioms natural to it, but the *program structure* is preserved so your mental mapping is trivial.

---

### C++

```cpp
#include <iostream>
#include <vector>
using namespace std;

class TicTacToe {
    vector<char> board;
    char player;
public:
    TicTacToe() : board(9, ' '), player('X') {}

    void printBoard() {
        for (int i = 0; i < 9; i++) {
            cout << board[i];
            if (i % 3 != 2) cout << "|";
            if (i % 3 == 2 && i != 8) cout << "\n-+-+-\n";
        }
        cout << "\n";
    }

    bool checkWin(char p) {
        int wins[8][3] = {{0,1,2},{3,4,5},{6,7,8},
                          {0,3,6},{1,4,7},{2,5,8},
                          {0,4,8},{2,4,6}};
        for (auto &w : wins)
            if (board[w[0]] == p && board[w[1]] == p && board[w[2]] == p)
                return true;
        return false;
    }

    void play() {
        for (int turn = 0; turn < 9; ++turn) {
            printBoard();
            cout << "Player " << player << " move (0-8): ";
            int move; cin >> move;
            if (board[move] != ' ') { cout << "Invalid.\n"; --turn; continue; }
            board[move] = player;
            if (checkWin(player)) { printBoard(); cout << player << " wins!\n"; return; }
            player = (player == 'X') ? 'O' : 'X';
        }
        printBoard();
        cout << "Draw!\n";
    }
};

int main() {
    TicTacToe game;
    game.play();
}
```

---

### C#

```csharp
using System;

class TicTacToe {
    char[] board = new char[9];
    char player = 'X';

    public TicTacToe() {
        for (int i = 0; i < 9; i++) board[i] = ' ';
    }

    void PrintBoard() {
        for (int i = 0; i < 9; i++) {
            Console.Write(board[i]);
            if (i % 3 != 2) Console.Write("|");
            if (i % 3 == 2 && i != 8) Console.Write("\n-+-+-\n");
        }
        Console.WriteLine();
    }

    bool CheckWin(char p) {
        int[,] wins = { {0,1,2},{3,4,5},{6,7,8},
                        {0,3,6},{1,4,7},{2,5,8},
                        {0,4,8},{2,4,6} };
        for (int i = 0; i < wins.GetLength(0); i++)
            if (board[wins[i,0]] == p && board[wins[i,1]] == p && board[wins[i,2]] == p)
                return true;
        return false;
    }

    public void Play() {
        for (int turn = 0; turn < 9; turn++) {
            PrintBoard();
            Console.Write($"Player {player} move (0-8): ");
            int move = int.Parse(Console.ReadLine());
            if (board[move] != ' ') { Console.WriteLine("Invalid."); turn--; continue; }
            board[move] = player;
            if (CheckWin(player)) { PrintBoard(); Console.WriteLine($"{player} wins!"); return; }
            player = (player == 'X') ? 'O' : 'X';
        }
        PrintBoard();
        Console.WriteLine("Draw!");
    }

    static void Main() {
        new TicTacToe().Play();
    }
}
```

---

### JavaScript (Node.js)

```javascript
const readline = require('readline').createInterface({
  input: process.stdin, output: process.stdout
});

class TicTacToe {
  constructor() {
    this.board = Array(9).fill(' ');
    this.player = 'X';
  }

  printBoard() {
    for (let i = 0; i < 9; i++) {
      process.stdout.write(this.board[i]);
      if (i % 3 !== 2) process.stdout.write('|');
      if (i % 3 === 2 && i !== 8) process.stdout.write('\n-+-+-\n');
    }
    console.log();
  }

  checkWin(p) {
    const wins = [[0,1,2],[3,4,5],[6,7,8],
                  [0,3,6],[1,4,7],[2,5,8],
                  [0,4,8],[2,4,6]];
    return wins.some(w => w.every(i => this.board[i] === p));
  }

  play(turn = 0) {
    if (turn >= 9) { this.printBoard(); console.log("Draw!"); return readline.close(); }
    this.printBoard();
    readline.question(`Player ${this.player} move (0-8): `, ans => {
      const move = parseInt(ans);
      if (this.board[move] !== ' ') { console.log("Invalid."); return this.play(turn); }
      this.board[move] = this.player;
      if (this.checkWin(this.player)) { this.printBoard(); console.log(`${this.player} wins!`); return readline.close(); }
      this.player = this.player === 'X' ? 'O' : 'X';
      this.play(turn + 1);
    });
  }
}

new TicTacToe().play();
```

---

### Python

```python
class TicTacToe:
    def __init__(self):
        self.board = [' '] * 9
        self.player = 'X'

    def printBoard(self):
        for i in range(9):
            print(self.board[i], end='')
            if i % 3 != 2:
                print('|', end='')
            if i % 3 == 2 and i != 8:
                print('\n-+-+-', end='')
        print()

    def checkWin(self, p):
        wins = [(0,1,2),(3,4,5),(6,7,8),
                (0,3,6),(1,4,7),(2,5,8),
                (0,4,8),(2,4,6)]
        return any(all(self.board[i] == p for i in w) for w in wins)

    def play(self):
        for turn in range(9):
            self.printBoard()
            move = int(input(f"Player {self.player} move (0-8): "))
            if self.board[move] != ' ':
                print("Invalid.")
                continue
            self.board[move] = self.player
            if self.checkWin(self.player):
                self.printBoard()
                print(f"{self.player} wins!")
                return
            self.player = 'O' if self.player == 'X' else 'X'
        self.printBoard()
        print("Draw!")

if __name__ == "__main__":
    TicTacToe().play()
```

---

### What to Notice
- **Method mapping is 1:1** — makes it easier to port mental models.
- **OOP ceremony**: C++ and C# need explicit constructors and access modifiers; Python/JS are leaner.
- **Console I/O**: `cin`/`cout`, `Console`, `readline`, and `input/print` all fill the same role, but with idiomatic differences.
- **Collection semantics**: Fixed‑size array vs. `vector` vs. dynamic list/array.

---



## Code Snippets in Four Languages

We’ll group by category and keep a **parallel snippet table** for C++, C#, JavaScript, and Python, followed by a quick **idiomatic Python alternative** when there’s a more “Pythonic” way. This way you get both the 1‑to‑1 mapping *and* the cultural upgrade.

---

### Conditional Control Structures

#### C++

 ```cpp       
 if (x > 0) { 
    cout << "Positive";
} else if (x == 0) {
    cout << "Zero";
} else {
    cout << "Negative";
}
 ```

#### C#
```csharp
if (x > 0) {
    Console.WriteLine("Positive");
} else if (x == 0) {
    Console.WriteLine("Zero");
} else {
    Console.WriteLine("Negative");
}
```

#### JavaScript
```javascript
if (x > 0) {
  console.log("Positive");
} else if (x === 0) {
  console.log("Zero");
} else {
  console.log("Negative");
}
```

#### Python
```python
if x > 0:
    print("Positive")
elif x == 0:
    print("Zero")
else:
    print("Negative")
``` |

**Pythonic tip** 💡: Condition chaining is common, e.g.:
```python
print("Positive" if x > 0 else "Zero" if x == 0 else "Negative")
```

---

### Loops

#### For Loops

##### C++

```cpp
 for (int i = 0; i < 5; i++) { 
    cout << i << "\n";
}
```

##### C#
 ```csharp
for (int i = 0; i < 5; i++) {
    Console.WriteLine(i);
}
 ```

##### JavaScript
```javascript
for (let i = 0; i < 5; i++) {
  console.log(i);
}
```

##### Python
```python
for i in range(5):
    print(i)
``` |
| ```cpp
while (n > 0) {
    n--;
}
```

#### While Loops

##### C#

```csharp
while (n > 0) {
    n--;
}
```

##### JavaScript
```javascript
while (n > 0) {
  n--;
}
```

##### Python
```python
while n > 0:
    n -= 1
```

**Pythonic tip** 💡: Iterating directly over data is more idiomatic than manual index control:
```python
for name in ["Ada", "Linus", "Guido"]:
    print(name)
```

---

### Functions / Methods

#### C++

 ```cpp        
int add(int a, int b) { 
    return a + b;
}
int result = add(2, 3);
 ```

#### C#
```csharp
int Add(int a, int b) {
    return a + b;
}
int result = Add(2, 3);
```

#### JavaScript
```javascript
function add(a, b) {
  return a + b;
}
let result = add(2, 3);
```

#### Python
```python
def add(a, b):
    return a + b

result = add(2, 3)
```

**Pythonic tip** 💡: Inline lambdas for short functions:
```python
square = lambda x: x * x
```

---

### Arrays / Lists

#### C++
```cpp      
int nums[3] = {1, 2, 3}; 
nums[1] = 42;            
```

#### C#
```csharp
int[] nums = {1, 2, 3};
nums[1] = 42;
```

#### JavaScript
```javascript
let nums = [1, 2, 3];
nums[1] = 42;
``` | ```python
nums = [1, 2, 3]
nums[1] = 42
```

**Pythonic tip** 💡: List comprehensions:
```python
squares = [n*n for n in range(5)]
```

---

### Class Declaration & Object Use

#### C++
```cpp     
class Greeter { 
public:      
    void greet() {
        cout << "Hello\n";
    }
};

Greeter g;
g.greet();
```

#### C#
```csharp
class Greeter {
    public void Greet() {
        Console.WriteLine("Hello");
    }
}

Greeter g = new Greeter();
g.Greet();
``` | ```javascript
class Greeter {
  greet() {
    console.log("Hello");
  }
}

let g = new Greeter();
g.greet();
```

#### Python
```python
class Greeter:
    def greet(self):
        print("Hello")

g = Greeter()
g.greet()
```

**Pythonic tip** 💡: You can add attributes on the fly:
```python
g.new_attr = "Dynamic!"
```

---

### Method Calls & Chaining

#### C++
```cpp      
obj.setX(5);  
obj.setY(10); 
```

#### C#
```csharp
obj.SetX(5).SetY(10);
```

#### JavaScript
```javascript
obj.setX(5).setY(10);
```

#### Python
```python
obj.set_x(5).set_y(10)
```

**Pythonic tip** 💡: Chainable methods are created by returning `self`:
```python
def set_x(self, value):
    self.x = value
    return self
```

---



## More Programming Examples in Four Languages

Here’s a set of **“micro‑recipes”** that glue together the constructs we’ve been mapping, so you can see them *in motion*.  
Each is small enough to digest in one glance but complete enough to run, with **C++ / C# / JavaScript / Python** side‑by‑side.

---

### Temperature Converter (Celsius ↔ Fahrenheit)

#### C++
 ```cpp                                      
#include <iostream>                          
using namespace std;                      
double toF(double c) { return c * 9/5 + 32; }       
 int main() {                                
    double c; cin >> c;
    cout << toF(c) << "\n";
}
 ```

#### C#
```csharp
using System;
class Program {
    static double ToF(double c) => c * 9/5 + 32;
    static void Main() {
        double c = double.Parse(Console.ReadLine());
        Console.WriteLine(ToF(c));
    }
}
```

#### JavaScript
```javascript
function toF(c) { return c * 9/5 + 32; }
process.stdin.on('data', d => {
  console.log(toF(parseFloat(d)));
});
```

#### Python
```python
def to_f(c): return c * 9/5 + 32
c = float(input())
print(to_f(c))
```

---



### Word Counter

#### C++
```cpp
#include <iostream>
#include <sstream>
using namespace std;
int main() {
    string line; getline(cin, line);
    stringstream ss(line);
    string word; int count = 0;
    while (ss >> word) count++;
    cout << count << "\n";
}
```

#### C#
```csharp
using System;
class Program {
    static void Main() {
        var line = Console.ReadLine();
        var count = line.Split(' ',
                     StringSplitOptions.RemoveEmptyEntries).Length;
        Console.WriteLine(count);
    }
}
```

#### JavaScript
```javascript
process.stdin.on('data', d => {
  const count = d.toString().trim().split(/\s+/).length;
  console.log(count);
});
```

#### Python
```python
line = input()
count = len(line.split())
print(count)
```

---



### Simple Guessing Game

#### C++
```cpp
#include <iostream>
#include <cstdlib>
#include <ctime>
using namespace std;
int main() {
    srand(time(0));
    int target = rand() % 10 + 1;
    int guess;
    do {
        cin >> guess;
        if (guess < target) cout << "Higher\n";
        else if (guess > target) cout << "Lower\n";
    } while (guess != target);
    cout << "Correct!\n";
}
```

#### C#
```csharp
using System;
class Program {
    static void Main() {
        var rnd = new Random();
        int target = rnd.Next(1, 11), guess;
        do {
            guess = int.Parse(Console.ReadLine());
            if (guess < target) Console.WriteLine("Higher");
            else if (guess > target) Console.WriteLine("Lower");
        } while (guess != target);
        Console.WriteLine("Correct!");
    }
}
```

#### JavaScript
```javascript
const target = Math.floor(Math.random()*10) + 1;
process.stdin.on('data', d => {
  const guess = parseInt(d);
  if (guess < target) console.log("Higher");
  else if (guess > target) console.log("Lower");
  else { console.log("Correct!"); process.exit(); }
});
```

#### Python
```python
import random
target = random.randint(1, 10)
while True:
    guess = int(input())
    if guess < target:
        print("Higher")
    elif guess > target:
        print("Lower")
    else:
        print("Correct!")
        break
```

---

### OO Example: Bank Account

#### C++
```cpp
#include <iostream>
using namespace std;
class Account {
    double balance;
public:
    Account(double b): balance(b) {}
    void deposit(double amt) { balance += amt; }
    double get() { return balance; }
};
int main() {
    Account acc(100);
    acc.deposit(50);
    cout << acc.get() << "\n";
}
````

#### C#
```csharp
using System;
class Account {
    double balance;
    public Account(double b) { balance = b; }
    public void Deposit(double amt) => balance += amt;
    public double Get() => balance;
}
class Program {
    static void Main() {
        var acc = new Account(100);
        acc.Deposit(50);
        Console.WriteLine(acc.Get());
    }
}
```

#### JavaScript
```javascript
class Account {
  constructor(b) { this.balance = b; }
  deposit(amt) { this.balance += amt; }
  get() { return this.balance; }
}
let acc = new Account(100);
acc.deposit(50);
console.log(acc.get());
```

#### Python
```python
class Account:
    def __init__(self, b): self.balance = b
    def deposit(self, amt): self.balance += amt
    def get(self): return self.balance

acc = Account(100)
acc.deposit(50)
print(acc.get())
```

---

These are intentionally **bite‑sized but runnable** in each language, showing:
- Control flow  
- Function calls  
- I/O handling  
- Object usage  






[^1]: From "[The Zen of Python](https://peps.python.org/pep-0020/)" by Tim Peters
