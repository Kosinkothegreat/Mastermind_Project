# mastermind_game.py

import numpy as np
from abc import ABC, abstractmethod

# Abstract base class for all Mastermind game variants
class MastermindGame(ABC):
    def __init__(self, n: int, m: int, no_repetition=False, beginner_mode=False):
        """
        Initialize the Mastermind game configuration.

        Parameters:
        - n: length of the code (number of positions)
        - m: number of available colors (0 to m-1)
        - no_repetition: if True, code has no repeated colors
        - beginner_mode: if True, use beginner-style ordered feedback
        """
        self.n = n
        self.m = m
        self.no_repetition = no_repetition
        self.beginner_mode = beginner_mode
        self.secret_code = self.generate_code()  # generate secret code on creation

    def generate_code(self):
        """
        Generate the secret code either with or without repetition.
        """
        if self.no_repetition:
            return np.random.choice(self.m, self.n, replace=False)
        return np.random.randint(0, self.m, self.n)

    def give_feedback(self, guess):
        """
        Compare a guess against the secret code and return feedback.

        Feedback is a NumPy array of 1s (black pegs) and 0s (white pegs).

        - Black peg (1): correct color in correct position.
        - White peg (0): correct color in wrong position.
        """
        secret = self.secret_code.copy()
        guess = np.array(guess)

        # Count black pegs (correct value and position)
        black = np.sum(secret == guess)

        # Mask out black matches to calculate white pegs
        secret_masked = secret[secret != guess]
        guess_masked = guess[secret != guess]

        white = 0
        for g in guess_masked:
            if g in secret_masked:
                white += 1
                # Remove first occurrence of matched color to avoid duplicate credit
                secret_masked = secret_masked[secret_masked != g]

        if self.beginner_mode:
            # In beginner mode, return ordered feedback without shuffling
            return np.array([1]*black + [0]*white)
        else:
            # Standard mode: total pegs limited to n positions
            return np.array([1]*black + [0]*white)[:self.n]

    def play(self, max_attempts=1000):
        """
        Simulate playing the game until the correct code is guessed or max attempts reached.

        Returns:
        - Number of attempts it took to crack the code.
        """
        attempts = 0
        previous_guesses = []

        while attempts < max_attempts:
            guess = self.generate_guess(previous_guesses)  # generate next guess
            feedback = self.give_feedback(guess)           # evaluate guess
            previous_guesses.append((guess, feedback))     # store guess-feedback pair
            attempts += 1

            # Success condition: all positions are black pegs
            if np.sum(feedback == 1) == self.n:
                break

        return attempts

    @abstractmethod
    def generate_guess(self, previous_guesses):
        """
        Abstract method to be implemented in subclasses for guessing strategy.
        """
        pass
