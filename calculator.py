import math
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("=" * 50)
    print("           ADVANCED COMMAND LINE CALCULATOR")
    print("=" * 50)
    print("\nAvailable Operations:")
    print("1. Basic Operations (+, -, *, /)")
    print("2. Power (^)")
    print("3. Square Root (√)")
    print("4. Trigonometric Functions (sin, cos, tan)")
    print("5. Logarithmic Functions (log, ln)")
    print("6. Constants (π, e)")
    print("7. Clear Screen")
    print("8. Exit")
    print("=" * 50)

def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input! Please enter a valid number.")

def calculate():
    while True:
        print_header()
        choice = input("\nEnter your choice (1-8): ")

        if choice == '1':
            num1 = get_number("Enter first number: ")
            operator = input("Enter operator (+, -, *, /): ")
            num2 = get_number("Enter second number: ")

            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                if num2 == 0:
                    print("Error: Division by zero!")
                    continue
                result = num1 / num2
            else:
                print("Invalid operator!")
                continue

            print(f"\nResult: {num1} {operator} {num2} = {result}")

        elif choice == '2':
            base = get_number("Enter base: ")
            exponent = get_number("Enter exponent: ")
            result = math.pow(base, exponent)
            print(f"\nResult: {base} ^ {exponent} = {result}")

        elif choice == '3':
            number = get_number("Enter number: ")
            if number < 0:
                print("Error: Cannot calculate square root of negative number!")
                continue
            result = math.sqrt(number)
            print(f"\nResult: √{number} = {result}")

        elif choice == '4':
            angle = get_number("Enter angle in degrees: ")
            print("\nSelect trigonometric function:")
            print("1. Sine")
            print("2. Cosine")
            print("3. Tangent")
            trig_choice = input("Enter choice (1-3): ")
            
            angle_rad = math.radians(angle)
            if trig_choice == '1':
                result = math.sin(angle_rad)
                print(f"\nResult: sin({angle}°) = {result}")
            elif trig_choice == '2':
                result = math.cos(angle_rad)
                print(f"\nResult: cos({angle}°) = {result}")
            elif trig_choice == '3':
                result = math.tan(angle_rad)
                print(f"\nResult: tan({angle}°) = {result}")
            else:
                print("Invalid choice!")

        elif choice == '5':
            print("\nSelect logarithmic function:")
            print("1. Natural Logarithm (ln)")
            print("2. Base-10 Logarithm (log)")
            log_choice = input("Enter choice (1-2): ")
            number = get_number("Enter number: ")
            
            if number <= 0:
                print("Error: Number must be positive!")
                continue
                
            if log_choice == '1':
                result = math.log(number)
                print(f"\nResult: ln({number}) = {result}")
            elif log_choice == '2':
                result = math.log10(number)
                print(f"\nResult: log({number}) = {result}")
            else:
                print("Invalid choice!")

        elif choice == '6':
            print("\nSelect constant:")
            print("1. π (pi)")
            print("2. e")
            const_choice = input("Enter choice (1-2): ")
            
            if const_choice == '1':
                print(f"\nπ = {math.pi}")
            elif const_choice == '2':
                print(f"\ne = {math.e}")
            else:
                print("Invalid choice!")

        elif choice == '7':
            clear_screen()
            continue

        elif choice == '8':
            print("\nThank you for using the Advanced Calculator!")
            break

        else:
            print("Invalid choice! Please try again.")

        input("\nPress Enter to continue...")
        clear_screen()

if __name__ == "__main__":
    clear_screen()
    calculate() 