import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import os

def draw_outcome_bar(outcome_dict, experiment_name, title='Success Rate by SID'):
    """
    Draws a bar plot of success rates by SID.

    Args:
        outcome_dict (dict): Dictionary with SIDs as keys and success rates as values.
        experiment_name (str): Name of the experiment for saving the plot.
        title (str): Title of the plot.
    """
    # Convert dictionary to lists for plotting
    sids = list(outcome_dict.keys())
    success_rates = list(outcome_dict.values())
    
    # Function to format y-axis as percentage
    def to_percentage(x, _):
        return f'{100 * x:.0f}%'
    
    # Bar Plot
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x=sids, y=success_rates, palette="viridis")
    plt.xlabel('SID')
    plt.ylabel('Success Rate')
    ax.yaxis.set_major_formatter(FuncFormatter(to_percentage))  # Apply percentage formatting
    plt.title(title)
    plt.xticks(rotation=45)  # Rotate labels to avoid overlap
    
    # Display the value on top of each bar
    for p in ax.patches:
        ax.annotate(to_percentage(p.get_height(), None), 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', 
                    xytext=(0, 9), 
                    textcoords='offset points')
    
    # Ensure the directory exists
    directory = os.path.join('./experiment', experiment_name, 'graph')
    os.makedirs(directory, exist_ok=True)
    
    # Save the plot to a file
    plt.savefig(os.path.join(directory, f'{title.replace(" ", "_")}_bar.png'), bbox_inches='tight')
    plt.show()

def draw_outcome_histogram(outcome_dict, experiment_name, title='Distribution of Success Rates'):
    """
    Draws a histogram of the distribution of success rates.

    Args:
        outcome_dict (dict): Dictionary with SIDs as keys and success rates as values.
        experiment_name (str): Name of the experiment for saving the plot.
        title (str): Title of the plot.
    """
    success_rates = [rate * 100 for rate in outcome_dict.values()]  # Convert to percentages
    
    plt.figure(figsize=(8, 6))
    # Dynamic bins: more detailed bins in the range where most data points lie
    if all(rate >= 90 for rate in success_rates):
        bins = list(range(90, 101))  # 1% intervals from 90 to 100
    else:
        bins = range(0, 101, 10)  # 10% intervals from 0 to 100
    
    ax = sns.histplot(success_rates, bins=bins, kde=False, color='skyblue')
    plt.xlabel('Success Rate (%)')
    plt.ylabel('Frequency')
    plt.title(title)
    
    plt.xticks(bins)
    
    # Add numbers on top of each bar
    for p in ax.patches:
        ax.text(p.get_x() + p.get_width() / 2., p.get_height(), '%d' % int(p.get_height()), 
                fontsize=12, ha='center', va='bottom')
    
    # Ensure the directory exists
    directory = os.path.join('./experiment', experiment_name, 'graph')
    os.makedirs(directory, exist_ok=True)
    
    plt.savefig(os.path.join(directory, f'{title.replace(" ", "_")}_histogram.png'), bbox_inches='tight')
    plt.show()

def draw_outcome_scatter(outcome_dict, experiment_name, title='Success Rate Trend by SID'):
    """
    Draws a scatter plot of success rates by SID.

    Args:
        outcome_dict (dict): Dictionary with SIDs as keys and success rates as values.
        experiment_name (str): Name of the experiment for saving the plot.
        title (str): Title of the plot.
    """
    sids = list(outcome_dict.keys())
    success_rates = list(outcome_dict.values())
    
    # Scatter Plot
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=sids, y=success_rates, color='red')
    plt.xlabel('SID')
    plt.ylabel('Success Rate')
    plt.title(title)
    plt.xticks(rotation=45)  # Rotate labels to avoid overlap
    
    # Ensure the directory exists
    directory = os.path.join('./experiment', experiment_name, 'graph')
    os.makedirs(directory, exist_ok=True)
    
    # Save the plot to a file
    plt.savefig(os.path.join(directory, f'{title.replace(" ", "_")}_scatter.png'), bbox_inches='tight')
    plt.show()

# Example usage:
# outcome_dict = {'sid1': 0.8, 'sid2': 0.9, 'sid3': 0.85}
# experiment_name = 'experiment_1'
# draw_outcome_bar(outcome_dict, experiment_name)
# draw_outcome_histogram(outcome_dict, experiment_name)
# draw_outcome_scatter(outcome_dict, experiment_name)

def calculate_contribution(grouped_sid_to_regex_dict, sid_to_unique_texts_dict, text_to_error_regex_dict):
    regex_fault_count_dict = {}
    for payload, regex_list in text_to_error_regex_dict.items():
        for regexText in regex_list:
            if regexText in regex_fault_count_dict:
                regex_fault_count_dict[regexText] += 1
            else:
                regex_fault_count_dict[regexText] = 1

    regex_to_sid_dict = {}
    for sid, regex_list in grouped_sid_to_regex_dict.items():
        for regexText in regex_list:
            if regexText not in regex_to_sid_dict:
                regex_to_sid_dict[regexText] = sid

    expanded_dict = {}
    for sid, texts in grouped_sid_to_regex_dict.items():
        total_texts = len(sid_to_unique_texts_dict[sid])
        text_scores = {}
        for text in texts:
            fault_count = regex_fault_count_dict.get(text, 0)
            score = (total_texts - fault_count) / total_texts
            if 0 <= score <= 1:
                text_scores[text] = score
        expanded_dict[sid] = {'text list': text_scores}

    return expanded_dict

def save_plot(expanded_dict, base_path, title_prefix):
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    for sid, data in expanded_dict.items():
        texts = list(data['text list'].keys())
        scores = list(data['text list'].values())
        codes = [f'regex{i+1}' for i in range(len(texts))]

        plt.figure(figsize=(10, 5))
        plt.bar(codes, scores, color='skyblue')
        plt.xlabel('Text Code')
        plt.ylabel('Score')
        
        plt.title(f'{title_prefix} Scores for {sid}')
        plt.ylim(0, 1)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

        file_path = os.path.join(base_path, f'{sid}.png')
        plt.savefig(file_path)
        plt.close()
        
def draw_positive_contribution_of_generated_regex(grouped_sid_to_regex_dict, sid_to_unique_texts_dict, text_to_error_regex_dict, experiment_name):
    expanded_dict = calculate_contribution(grouped_sid_to_regex_dict, sid_to_unique_texts_dict, text_to_error_regex_dict)
    base_path = os.path.join('./experiment', experiment_name, 'graph/contribution/positive')
    os.makedirs(base_path, exist_ok=True)
    save_plot(expanded_dict, base_path, 'Positive')
    return expanded_dict


def draw_negative_contribution_of_generated_regex(grouped_sid_to_regex_dict, sid_to_unique_texts_dict, text_to_error_regex_dict, experiment_name):
    expanded_dict = calculate_contribution(grouped_sid_to_regex_dict, sid_to_unique_texts_dict, text_to_error_regex_dict)
    base_path = os.path.join('./experiment', experiment_name, 'graph/contribution/negative')
    os.makedirs(base_path, exist_ok=True)
    save_plot(expanded_dict, base_path, 'Negative')
