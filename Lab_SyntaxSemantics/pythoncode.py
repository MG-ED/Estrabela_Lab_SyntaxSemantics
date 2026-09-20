class GrammarError(Exception):
    def __init__(self, message, position):
        self.message = message
        self.position = position
        super().__init__(f"{message} at position {position}")

class Parser:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def peek(self):
        if self.pos < len(self.text):
            return self.text[self.pos]
        return None

    def advance(self):
        ch = self.peek()
        self.pos += 1
        return ch

    def fail(self, message):
        raise GrammarError(message, self.pos)

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

    def term(self):
        value = self.factor()
        while self.peek() in ('*', '/'):
            operator = self.advance()
            right = self.factor()
            if operator == '*':
                value = value * right
            else:
                if right == 0:
                    self.fail("Division by zero")
                value = value / right
        return value

    def factor(self):
        ch = self.peek()
        if ch == '(':
            self.advance()                  
            value = self.expr()             
            if self.peek() != ')':
                self.fail("Expected ')'")
            self.advance()                  
            return value
        elif ch is not None and ch.isdigit():
            return self.digit()
        else:
            self.fail("Expected a digit or '('")

    def digit(self):
        ch = self.peek()
        if ch is not None and ch.isdigit() and len(ch) == 1:
            self.advance()
            return int(ch)
        self.fail("Expected a digit")

def check_and_evaluate(text):
    parser = Parser(text)
    try:
        result = parser.expr()
    except GrammarError as e:
        return False, str(e), None

    if parser.pos != len(parser.text):
        leftover = parser.text[parser.pos]
        return False, f"Unexpected token '{leftover}' at position {parser.pos}", None

    return True, None, result

def format_result(value):
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value

def main():
    print("=== Arithmetic Grammar Checker and Evaluator ===\n")

    print("=== Try Your Own Expression ===")
    print("(Press Enter with no input to skip / quit)\n")

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