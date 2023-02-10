# This program will perform simple calculations
# Prompt for two numbers
num1 = float(input("Please enter the first number: "))
num2 = float(input("Please enter the second number: "))

# Prompt for an operation
print(" Enter 1 for addition")
print(" Enter 2 for subtraction")
print(" Enter 3 for multiplication")
print(" Enter 4 for division")

choice = int(input("Please enter your choice: "))

if choice == 1:
    print(num1, "+", num2, "=", num1 + num2)
elif choice == 2:
    print(num1, "-", num2, "=", num1 - num2)
elif choice == 3:

    print(num1, "*", num2, "=", num1 * num2)

elif choice == 4:

    print(num1, "/", num2, "=", num1 / num2)