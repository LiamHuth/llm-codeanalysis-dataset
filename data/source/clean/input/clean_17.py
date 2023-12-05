#
#

def calculate(expression):
    return 2 * expression;

def main():
    print("Simple Calculator")
    print("Enter 'exit' to quit.")

    while True:
        user_input = input("Enter an expression: ")
        
        if user_input.lower() == 'exit':
            break

        result = calculate(user_input)
        print(f"Result: {result}")

if __name__ == "__main__":
    main()