import sys
from dataclasses import dataclass
from fractions import Fraction
import numpy as np
import matplotlib.pyplot as plt


# Utility function
def format_value(x: float) -> str:
  """
  Convert a float to a human-readable string.

  - Integers are returned without decimal places.
  - Non-integers are returned as a simplified fraction if the denominator ≤ 20.
  - Otherwise, they are rounded to 2 decimal places.
  """
  if x.is_integer():
    return str(int(x))

  else:
    frac = Fraction(x).limit_denominator(100)
    return f'({frac})' if abs(frac.denominator) <= 20 else f'{x:.2f}'


# Dataclass to store quadratic results
@dataclass
class QuadraticResult:
    a: float              # Coefficient a
    b: float              # Coefficient b
    c: float              # Coefficient c
    equation: str         # Formatted equation string
    root1: float          # First root
    root2: float          # Second root
    discriminant: float   # Discriminant value
    vertex_x: float       # x-coordinate of vertex
    vertex_y: float       # y-coordinate of vertex


# Compute quadratic results
def compute_quadratic(a: float, b: float, c: float) -> QuadraticResult:
    """
    Compute key properties of a quadratic equation: roots, discriminant, vertex,
    and a nicely formatted equation string.

    Raises ValueError if equation is not quadratic or has no real roots.
    """
    if a == 0:
        raise ValueError("Coefficient 'a' cannot be zero. not a quadratic equation.")

    # Build formatted equation string
    equation = f"{format_value(a) if a != 1 else ''}x²"

    if b != 0:
        sign_b = ' + ' if b > 0 else ' - '
        equation += f"{sign_b}{'' if abs(b) == 1 else format_value(abs(b))}x"

    if c != 0:
        sign_c = ' + ' if c > 0 else ' - '
        equation += f"{sign_c}{format_value(abs(c))}"

    # Discriminant
    discriminant = b**2 - 4 * a * c
    if discriminant < 0:
        raise ValueError("Quadratic has no real solutions.")

    # Roots
    root1 = (-b + np.sqrt(discriminant)) / (2 * a)
    root2 = (-b - np.sqrt(discriminant)) / (2 * a)

    # Vertex
    vertex_x = -b / (2 * a)
    vertex_y = a*vertex_x**2 + b*vertex_x + c

    return QuadraticResult(a, b, c, equation, root1, root2, discriminant, vertex_x, vertex_y)


# Display results
def display_quadratic(result: QuadraticResult) -> None:
    """
    Print the expanded equation, factored form, and roots.
    """
    r1, r2 = result.root1, result.root2
    eq = result.equation

    print(f"\n{eq} = 0")

    # Determine signs for factoring
    sign1 = ' + ' if r1 < 0 else ' - '
    sign2 = ' + ' if r2 < 0 else ' - '

    # Factored form
    if r1 == r2:
        if r1 != 0:
            print(f"(x{sign1}{format_value(abs(r1))})² = 0")

        print(f"\nThe only solution is: x = {format_value(r1)}\n")

    else:
        if r1 == 0:
            print(f"x(x{sign2}{format_value(abs(r2))}) = 0")
        else:
            print(f"(x{sign1}{format_value(abs(r1))})(x{sign2}{format_value(abs(r2))}) = 0")

        print(f"\nSolution 1: x = {format_value(r1)}")
        print(f"Solution 2: x = {format_value(r2)}\n")


# Graph the quadratic
def graph_quadratic(result: QuadraticResult) -> None:
    """
    Plot the quadratic equation using the original coefficients, marking vertex and roots.
    """
    a, b, c = result.a, result.b, result.c

    # Creating x and y-values
    x = np.linspace(-20, 20, 500)
    y = a * x**2 + b * x + c

    # Plot the quadratic
    plt.plot(x, y, label = 'f(x)')

    # Axes
    plt.axhline(0, color = 'black', linewidth = 1)
    plt.axvline(0, color = 'black', linewidth = 1)

    # Vertex
    vertex_label = f"Vertex: ({format_value(result.vertex_x)}, {format_value(result.vertex_y)})"
    plt.scatter(result.vertex_x, result.vertex_y, color = 'red', label = vertex_label)

    # Roots
    root_label = f"Root(s): x = {format_value(result.root1)}, {'' if result.root1 == result.root2 else format_value(result.root2)}"
    plt.scatter([result.root1, result.root2], [0, 0], color = 'green', label = root_label)

    # Labels and title
    plt.title(f'f(x) = {result.equation}')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    plt.show()


# Main program
def main():
    """
    Retrieve command-line arguments, compute quadratic, display and graph it.
    """
    if len(sys.argv) != 4:
        print("\nUsage: python factor.py 'a' 'b' 'c'\nOnly enter three args\n")
        return

    try:
        a = float(sys.argv[1])
        b = float(sys.argv[2])
        c = float(sys.argv[3])

        # Compute all results
        result = compute_quadratic(a, b, c)

        # Display equation and roots
        display_quadratic(result)

        # Plot graph
        graph_quadratic(result)

    except ValueError as error:
        print(f"\nError: {error}\n")

main()
