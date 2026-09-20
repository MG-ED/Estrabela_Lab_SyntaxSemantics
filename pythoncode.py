# Custom error for grammar problems, includes where the error happened
class GrammarError(Exception):
    def __init__(self, message, position):
        self.message = message
        self.position = position
        super().__init__(f"{message} at position {position}")

# Parser that reads the expression from left to right
class Parser:
    def __init__(self, text):
        self.text = text  # the input string
        self.pos = 0      # current position in the string

    # Look at current character without moving
    def peek(self):
        if self.pos < len(self.text):
            return self.text[self.pos]
        return None

    # Move one step forward and return the character we passed
    def advance(self):
        ch = self.peek()
        self.pos += 1
        return ch

    # Raise a grammar error with a message and position
    def fail(self, message):
        raise GrammarError(message, self.pos)

    # Handle + and - (lowest precedence)
    def expr(self):
        value = self.term()
        while self.peek() in ('+', '-'):
            operator = self.advance()
            right = self.term()
            if operator == '+':
                value = value + right
            else:
                value = value - right
        return value

    # Handle * and / (higher precedence than + and -)
    def term(self):
        value = self.factor()
        while self.peek() in ('*', '/'):
            operator = self.advance()
            right = self.factor()
            if operator == '*':
                value = value * right
            else:
                # Check for division by zero
                if right == 0:
                    self.fail("Division by zero")
                value = value / right
        return value

    # Handle numbers and parentheses
    def factor(self):
        ch = self.peek()
        if ch == '(':
            self.advance()                  # skip '('
            value = self.expr()             # evaluate inside parentheses
            if self.peek() != ')':
                self.fail("Expected ')'")
            self.advance()                  # skip ')'
            return value
        elif ch is not None and ch.isdigit():
            return self.digit()
        else:
            self.fail("Expected a digit or '('")

    # Read a single digit and convert to int
    def digit(self):
        ch = self.peek()
        if ch is not None and ch.isdigit() and len(ch) == 1:
            self.advance()
            return int(ch)
        self.fail("Expected a digit")

# Try to parse and evaluate the expression; return (valid, error, result)
def check_and_evaluate(text):
    parser = Parser(text)
    try:
        result = parser.expr()
    except GrammarError as e:
        # Parsing failed (syntax or semantic error)
        return False, str(e), None

    # Make sure there are no extra characters left
    if parser.pos != len(parser.text):
        leftover = parser.text[parser.pos]
        return False, f"Unexpected token '{leftover}' at position {parser.pos}", None

    return True, None, result

# Show integer results without .0 if possible
def format_result(value):
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value

def main():
    print("=== Arithmetic Grammar Checker and Evaluator ===\n")

    print("=== Try Your Own Expression ===")
    print("(Press Enter with no input to skip / quit)\n")

    # Keep asking for expressions until the user presses Enter on an empty line
    while True:
        text = input("Enter expression: ").strip()
        if text == "":
            print("Goodbye!")
            break

        valid, error, result = check_and_evaluate(text)
        print("\nSyntax Check:")
        if valid:
            print("Valid syntax")
            print("\nSemantic Evaluation:")
            print(f"Result: {format_result(result)}")
        else:
            print("Invalid syntax")
            print(f"Error: {error}")
        print()


if __name__ == "__main__":
    main()