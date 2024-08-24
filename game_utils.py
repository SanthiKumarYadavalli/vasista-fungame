import random

NUM_OPERATORS = 4
MAX_NUM = 9
NUM_QUESTIONS = 5
DELAY = 1  # seconds to wait for next question


class Expressions:
    def __init__(self):
        self.left, self.left_val = self.generate()
        self.right, self.right_val = self.generate()
        # makes sure both expressions are not equal value
        self.check_for_equal()
        self.answer = "left" if self.left_val > self.right_val else "right"
            
    def generate(self):
        exp = f"{random.randint(1, MAX_NUM)}"
        for _ in range(NUM_OPERATORS):
            exp += random.choice([' + ', ' - ', ' × ', ' ÷ '])
            exp += str(random.randint(1, MAX_NUM))
        return exp, eval(exp.replace('×', '*').replace('÷', '/'))

    def check_for_equal(self):
        while self.left_val == self.right_val:
            self.left, self.left_val = self.generate()


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.expressions = [Expressions() for _  in range(NUM_QUESTIONS)]
    