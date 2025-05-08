# app.py

from flask import Flask, render_template, request
from mastermind.variants import StandardGame, NoRepetitionGame, BeginnerGame, CombinedGame
import numpy as np

# Initialize Flask application
app = Flask(__name__)

# Home route to render the simulation configuration form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle simulation submission and display results
@app.route('/results', methods=['POST'])
def results():
    # Extract user inputs from the form
    n = int(request.form['n'])              # Code length
    m = int(request.form['m'])              # Number of colors
    mode = request.form['mode']             # Game mode selected
    num_runs = int(request.form['runs'])    # Number of simulations to run

    # Select the appropriate game class based on mode
    if mode == 'standard':
        GameClass = StandardGame
    elif mode == 'norep':
        GameClass = NoRepetitionGame
    elif mode == 'beginner':
        GameClass = BeginnerGame
    elif mode == 'combo':
        GameClass = CombinedGame
    else:
        return "Invalid mode selected", 400  # Handle invalid input

    # Run simulations and collect number of attempts for each
    attempts_list = []
    for _ in range(num_runs):
        game = GameClass(n, m)
        attempts = game.play()              # Run the game simulation
        attempts_list.append(attempts)      # Track how many attempts it took

    # Compute statistics from the collected attempts
    attempts_array = np.array(attempts_list)
    stats = {
        'mean': round(np.mean(attempts_array), 2),
        'std': round(np.std(attempts_array), 2),
        'max': int(np.max(attempts_array))
    }

    # Render the results page with statistics and attempts list
    return render_template('results.html', stats=stats, attempts=attempts_list, mode=mode)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
