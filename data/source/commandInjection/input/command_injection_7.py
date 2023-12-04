#
#

def calculate(expression):
    try:
        return eval(expression)
    except Exception as e:
        return str(e)

def main():
    print("Simple Calculator")
    print("Enter 'exit' to quit.")

    while True:
        user_input = input("Enter an expression (e.g., 2 + 2): ")
        
        if user_input.lower() == 'exit':
            break

        result = calculate(user_input)
        print(f"Result: {result}")

if __name__ == "__main__":
    main()