import matplotlib.pyplot as plt
from IPython import display

plt.ion()

def format_value(value):
    # Check if the value is an integer by comparing it to an int of itself
    if value == int(value):
        return f"{int(value)}"
    else:
        return f"{value:.3f}"

def plot(scores, mean_scores, avg_moves_to_apple, mean_avg_moves_to_apple, model):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()

    # Create a figure and a set of subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 8))  # 2 rows, 1 column
    fig.suptitle(f"{model}", fontsize=16, fontweight='bold')


    # First subplot for scores and mean scores
    ax1.set_title('Score Development Over Games')
    ax1.set_xlabel('Number of Games')
    ax1.set_ylabel('Score')
    ax1.plot(scores, label='Scores')
    ax1.plot(mean_scores, label='Mean Scores', linestyle='--')
    ax1.legend(loc='upper left')
    ax1.set_ylim(ymin=0)
    ax1.text(len(scores) - 1, scores[-1], format_value(scores[-1]))  # Conditional formatting
    ax1.text(len(mean_scores) - 1, mean_scores[-1], format_value(mean_scores[-1]))  # Conditional formatting

    # Second subplot for average moves to apple and mean average moves
    ax2.set_title('Average Moves to Apple Over Games')
    ax2.set_xlabel('Number of Games')
    ax2.set_ylabel('Average Moves')
    ax2.plot(avg_moves_to_apple, label='Average Moves to Apple', color = 'green')
    ax2.plot(mean_avg_moves_to_apple, label='Mean Average Moves to Apple', linestyle='--', color = 'red')
    ax2.legend(loc='upper right')
    ax2.set_ylim(ymin=0)
    ax2.text(len(avg_moves_to_apple) - 1, avg_moves_to_apple[-1], format_value(avg_moves_to_apple[-1]))  # Conditional formatting
    ax2.text(len(mean_avg_moves_to_apple) - 1, mean_avg_moves_to_apple[-1], format_value(mean_avg_moves_to_apple[-1]))  # Conditional formatting


    # Adjust layout
    plt.tight_layout()
    plt.show()
