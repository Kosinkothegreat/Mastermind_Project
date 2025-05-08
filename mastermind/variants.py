# variants.py

import numpy as np
from .mastermind_game import MastermindGame

# Standard Mastermind game: allows repetition, standard feedback
class StandardGame(MastermindGame):
    def generate_guess(self, previous_guesses):
        """
        Generate a random guess with possible repetitions (standard mode).
        """
        return np.random.randint(0, self.m, self.n)

# No Repetition variant: colors in code must be unique
class NoRepetitionGame(MastermindGame):
    def generate_guess(self, previous_guesses):
        """
        Generate a random guess without repeated colors.
        """
        return np.random.choice(self.m, self.n, replace=False)

# Beginner Mode variant: uses ordered feedback (black/white per position)
class BeginnerGame(MastermindGame):
    def __init__(self, n, m):
        """
        Initialize beginner mode game:
        - Allows repetition
        - Uses ordered feedback
        """
        super().__init__(n, m, no_repetition=False, beginner_mode=True)

    def generate_guess(self, previous_guesses):
        """
        Generate a random guess with repetitions, suitable for beginner feedback.
        """
        return np.random.randint(0, self.m, self.n)

# Combined variant: Beginner feedback + No repetition
class CombinedGame(MastermindGame):
    def __init__(self, n, m):
        """
        Initialize combined game:
        - No repeated colors
        - Uses ordered feedback (beginner mode)
        """
        super().__init__(n, m, no_repetition=True, beginner_mode=True)

    def generate_guess(self, previous_guesses):
        """
        Generate a random guess without repetition, with beginner feedback.
        """
        return np.random.choice(self.m, self.n, replace=False)
