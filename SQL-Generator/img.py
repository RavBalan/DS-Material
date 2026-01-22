import os
import time
import sys

def print_colored(text, color):
    """Helper function to print text in specified color using ANSI codes."""
    colors = {
        "blue": "\033[94m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "gray": "\033[90m",
        "reset": "\033[0m"
    }
    return f"{colors.get(color, '')}{text}{colors['reset']}"

def draw_vector_robot(expression):
    """Draw Vector robot with a given facial expression."""
    # Base structure of Vector robot
    vector_art = [
        ( "    ____    ", "blue" ),   # Top of body
        ( "   /    \\   ", "blue" ),  # Body with screen
        ( f"  | {expression} |  ", "yellow" ),  # Dynamic face
        ( "   \\    /   ", "blue" ),  # Bottom of body
        ( "    |  |    ", "gray" ),  # Lift arm
        ( "  [==||==]  ", "gray" )   # Treads
    ]
    # Clear terminal (works on Unix-like systems and Windows)
    os.system('cls' if os.name == 'nt' else 'clear')
    # Print title and art
    print(print_colored("Vector Robot (Animated):", "green"))
    for line, color in vector_art:
        print(print_colored(line, color))

def animate_vector():
    """Animate Vector's face with different expressions using a loop."""
    expressions = [
        "*  * ",  # Happy eyes
        "^  ^ ",  # Curious eyes
        "-  - "   # Blinking eyes
    ]
    print("Press Ctrl+C to stop the animation.")
    try:
        while True:
            for expression in expressions:
                draw_vector_robot(expression)
                time.sleep(0.5)  # Delay between frames for smooth animation
    except KeyboardInterrupt:
        print("\nAnimation stopped.")
        sys.exit(0)

def main():
    print("Type 'start' to display the animated Vector robot ASCII art:")
    while True:
        command = input().strip().lower()
        if command == 'start':
            animate_vector()
            break
        else:
            print("Please type 'start' to proceed.")

if __name__ == "__main__":
    main()