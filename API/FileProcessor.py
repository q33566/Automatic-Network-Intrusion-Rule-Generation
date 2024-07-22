import pandas as pd
import os
import random
import numpy as np

def get_unique_sids_list(df):
    """
    Get a list of unique sids from the dataframe where the 'text' column is not null.

    Args:
        df (pd.DataFrame): DataFrame containing 'sid' and 'text' columns.

    Returns:
        np.ndarray: Array of unique sids.
    """
    unique_sids = df[df['text'].notnull()]['sid'].unique()
    return unique_sids

def map_sid_to_unique_texts(df):
    """
    Map each sid to a set of unique texts from the dataframe.

    Args:
        df (pd.DataFrame): DataFrame containing 'sid' and 'text' columns.

    Returns:
        dict: Dictionary mapping sids to sets of unique texts.
    """
    sid_to_texts = {}
    for _, row in df.iterrows():
        sid = row['sid']
        text = row['text']
        if pd.notnull(text):  # Ensure text is not NaN
            if sid in sid_to_texts:
                sid_to_texts[sid].add(text)
            else:
                sid_to_texts[sid] = {text}
    return sid_to_texts

def merge_dataframes_to_dict(dfs):
    """
    Merge multiple dataframes into a dictionary where each sid maps to a list of unique texts.

    Args:
        dfs (list): List of pandas DataFrames, each with columns 'sid' and 'text'.

    Returns:
        dict: Dictionary with sid as keys and list of unique texts as values.
    """
    merged_dict = {}

    for df in dfs:
        for _, row in df.iterrows():
            sid = row['sid']
            text = row['text']
            if pd.notnull(text):  # Ensure text is not NaN
                if sid not in merged_dict:
                    merged_dict[sid] = set()  # Use a set to avoid duplicates
                merged_dict[sid].add(text)

    # Convert sets to lists
    merged_dict = {sid: list(texts) for sid, texts in merged_dict.items()}
    
    return merged_dict

def filter_sids_by_text_length(sid_to_texts_dict):
    """
    Filter sids whose associated texts have a length greater than 5.

    Args:
        sid_to_texts_dict (dict): Dictionary mapping sids to their unique texts.

    Returns:
        set: Set of filtered sids.
    """
    filtered_sid_to_texts_dict = set()
    for key, value in sid_to_texts_dict.items():
        if len(value) > 5:  # Ensure text length exceeds 5
            filtered_sid_to_texts_dict.add(key)
    return filtered_sid_to_texts_dict

def get_sorted_filtered_sids(sid_to_texts_dict):
    """
    Get sorted and filtered sids based on text length.

    Args:
        sid_to_texts_dict (dict): Dictionary mapping sids to their unique texts.

    Returns:
        list: Sorted list of filtered sids.
    """
    filtered_sids = filter_sids_by_text_length(sid_to_texts_dict)
    sorted_filtered_sids = sorted(filtered_sids)
    return sorted_filtered_sids

def select_random_texts(sid_to_texts_dict, exclude_sid, num_texts=100):
    """
    Select random texts excluding a specific sid.

    Args:
        sid_to_texts_dict (dict): Dictionary mapping sids to their unique texts.
        exclude_sid (str): Sid to be excluded.
        num_texts (int): Number of texts to select.

    Returns:
        list: List of randomly selected texts.
    """
    # Filter out the given SID
    filtered_texts = [texts for sid, texts in sid_to_texts_dict.items() if sid != exclude_sid]
    
    # Flatten multiple lists into a single list
    all_texts = [text for sublist in filtered_texts for text in sublist]
    
    # Filter out NaN values
    all_texts = [text for text in all_texts if not (isinstance(text, float) and np.isnan(text))]
    
    # Randomly select num_texts texts, if total is less than num_texts select all
    selected_texts = random.sample(all_texts, min(len(all_texts), num_texts))
    
    return selected_texts

def select_all_negative_texts(sid_to_texts_dict, exclude_sid, num_texts=100):
    """
    Select all texts excluding a specific sid.

    Args:
        sid_to_texts_dict (dict): Dictionary mapping sids to their unique texts.
        exclude_sid (str): Sid to be excluded.
        num_texts (int): Number of texts to select (not used here).

    Returns:
        list: List of all texts excluding the given sid.
    """
    # Filter out the given SID
    filtered_texts = [texts for sid, texts in sid_to_texts_dict.items() if sid != exclude_sid]
    
    # Flatten multiple lists into a single list
    all_texts = [text for sublist in filtered_texts for text in sublist]
    
    # Filter out NaN values
    all_texts = [text for text in all_texts if not (isinstance(text, float) and np.isnan(text))]
    
    return all_texts

def get_grouped_sid_to_regex_dict(generated_regex_list, number_of_regexes, sid_to_unique_texts):
    """
    Group SIDs to a list of regex patterns.

    Args:
        generated_regex_list (list): List of generated regex patterns.
        number_of_regexes (int): Number of regex patterns per SID.
        sid_to_unique_texts (dict): Dictionary mapping SIDs to their unique texts.

    Returns:
        dict: Dictionary mapping SIDs to a list of regex patterns.
    """
    # Validate inputs
    if not isinstance(generated_regex_list, list):
        raise TypeError(f"generated_regex_list should be a list, got {type(generated_regex_list)}")
    if not isinstance(number_of_regexes, int):
        raise TypeError(f"number_of_regexes should be an int, got {type(number_of_regexes)}")
    if not isinstance(sid_to_unique_texts, dict):
        raise TypeError(f"sid_to_unique_texts should be a dict, got {type(sid_to_unique_texts)}")

    sorted_sid_list = get_sorted_filtered_sids(sid_to_unique_texts)
    sid_to_regex_dict = {}  # Dictionary to store SID to regex list mapping
    regex_index = 0  # Index to keep track of the current position in generated_regex_list

    for sid in sorted_sid_list:
        # Extract number_of_regexes elements for each SID, including NaN
        regex_sublist = generated_regex_list[regex_index:regex_index + number_of_regexes]
        # Filter out NaN values from the sublist
        filtered_sublist = [regex_text for regex_text in regex_sublist if pd.notnull(regex_text)]
        sid_to_regex_dict[sid] = filtered_sublist
        regex_index += number_of_regexes  # Move the index

    return sid_to_regex_dict

def prompt_generator(sid_to_unique_texts_dict, experiment_name, number_of_times=0):
    """
    Generate prompt files for the experiment.

    Args:
        sid_to_unique_texts_dict (dict): Dictionary mapping sids to their unique texts.
        experiment_name (str): Name of the experiment.
        number_of_times (int): Number of times to generate prompts.

    Returns:
        None
    """
    directory = f'./experiment/{experiment_name}/prompt/'
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    sorted_filtered_sids = get_sorted_filtered_sids(sid_to_unique_texts_dict)
    for idx in range(number_of_times):
        for sid in sorted_filtered_sids:
            with open(f'{directory}/{sid}_prompt_{idx}.txt', 'w') as file:
                texts = list(sid_to_unique_texts_dict[sid])
                random.shuffle(texts)
                selected_texts = texts[:50]
                file.write(f"sid: {sid}, text: {selected_texts}\n")
                file.write("\n")
                file.write("Please find a regular expression to match all packet payloads.\n" + 
                           "You need to find the similarities in the sentences and generalize the parts where they differ. \n" + 
                           "The regular expression is in PCRE format, please be aware to evaluate the validity of the expression you generated under PCRE regulations. \n" + 
                           "There will be examples to help you find the patterns. \n"  +
                           "[‘DELE 3\\r\\n’, ‘DELE 128\\r\\n’, ‘DELE 74\\r\\n’, ‘DELE 22\\r\\n’, ‘DELE 70\\r\\n’] \n" +
                           "These examples show the attacker is trying to delete someone’s email by POP protocol. \n" +
                           "The index of the desired mail is indicated under the DELE command. \n" +
                           "Thus the best regular expression that matches them will be ‘^(DELE)( )(.*)(\\r\\n)$’ \n" + "\n" +
                           "With the given example payloads: \n" +
                           "[‘EHLO BtuCBHdSb51.com\\r\\n’, ‘EHLO 203.187.87.27\\r\\n’, ‘EHLO slae02Fo9Ep.com\\r\\n’, ‘EHLO 210.64.37.51\\r\\n’, ‘EHLO LLb0RwqdbkikFWo.com\\r\\n’] \n" + 
                           "These examples show the attacker is trying to make sure the SMTP server is up and running. " + 
                           "The command EHLO works in both lower case and uppercase, after that follows the SMTP server address. \n" +
                           "Thus the best regular expression to match them will be ‘^([E|e][H|h][L|l][O|o])(.*)(\\r\\n)$’ \n" + "\n" +
                           "Next, with the given payloads: \n")
                file.write(f"{selected_texts}\n")         
                file.write("Please give 3 possible and different regular expressions to match all of the elements. \n" +
                           "You can give only 1 expression if the 3 expressions you find are too similar. \n" + 
                           "Let’s work this out in a step-by-step way to make sure we have the right answer. \n" + 
                           "To make the expression not too general, make sure the expressions don’t match these negative examples: [‘CAPA\\r\\n’, ‘CAPA\\r\\n’, ‘\\x15\\x03\\x01’, ‘GET / HTTP/1.0\\r\\n\\r\\n’, ‘r\\n\\r\\n’] \n" +
                           "You only need to give me the three regular expressions in code format.\n")
                file.write("\n")
