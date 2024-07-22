import csv
import random
import pandas as pd
import regex
from API.FileProcessor import select_random_texts, map_sid_to_unique_texts, select_all_negative_texts
import regex

def positive_evaluation(generated_pattern, sid, sid_to_unique_texts_dict, file, positive_sid_to_success_rate_dict, error_regex_dict, threshold, mode):
    """
    Evaluates the generated pattern against positive samples.

    Args:
        generated_pattern (str): The regex pattern to evaluate.
        sid (str): The sample ID.
        sid_to_unique_texts_dict (dict): Dictionary mapping sids to their unique texts.
        file (file object): File to write the results.
        positive_sid_to_success_rate_dict (dict): Dictionary to store success rates for positive samples.
        error_regex_dict (dict): Dictionary to store regex patterns that failed to match.
        threshold (float/int): Threshold for determining a match.
        mode (str): Mode of threshold ('fraction' or 'integer').

    Returns:
        tuple: (correct matches, total samples)
    """
    correct, total, error_list = perform_evaluation(
        generated_pattern, 
        sid, 
        sid_to_unique_texts_dict, 
        error_regex_dict, 
        threshold, 
        mode, 
        is_positive=True
    )
    
    positive_sid_to_success_rate_dict[sid] = correct / total
    write_results(file, 'positive', correct, total, error_list, error_regex_dict)
    
    return correct, total

def negative_evaluation(generated_pattern_list, sid, sid_to_unique_texts_dict, file, negative_sid_to_success_rate_dict, error_regex_dict, threshold, mode):
    """
    Evaluates the generated pattern against negative samples.

    Args:
        generated_pattern_list (list): The list of regex patterns to evaluate.
        sid (str): The sample ID.
        sid_to_unique_texts_dict (dict): Dictionary mapping sids to their unique texts.
        negative_sample_number (int): Number of negative samples to select.
        file (file object): File to write the results.
        negative_sid_to_success_rate_dict (dict): Dictionary to store success rates for negative samples.
        error_regex_dict (dict): Dictionary to store regex patterns that failed to match.
        threshold (float/int): Threshold for determining a match.
        mode (str): Mode of threshold ('fraction' or 'integer').

    Returns:
        None
    """
    correct, total, error_list = perform_evaluation(
        generated_pattern_list, 
        sid, 
        sid_to_unique_texts_dict, 
        error_regex_dict, 
        threshold, 
        mode, 
        is_positive=False,
    )
    
    negative_sid_to_success_rate_dict[sid] = correct / total
    write_results(file, 'negative', correct, total, error_list, error_regex_dict)
    
def perform_evaluation(generated_pattern, sid, sid_to_unique_texts_dict, error_regex_dict, threshold, mode, is_positive=True):
    """
    Performs the evaluation of the generated pattern.

    Args:
        generated_pattern (str/list): The regex pattern(s) to evaluate.
        sid (str): The sample ID.
        sid_to_unique_texts_dict (dict): Dictionary mapping sids to their unique texts.
        error_regex_dict (dict): Dictionary to store regex patterns that failed to match.
        threshold (float/int): Threshold for determining a match.
        mode (str): Mode of threshold ('fraction' or 'integer').
        is_positive (bool): Indicates whether the evaluation is for positive or negative samples.
        negative_sample_number (int): Number of negative samples to select (if applicable).

    Returns:
        tuple: (correct matches, total samples, error list)
    """
    correct = 0
    total = 0
    error_list = []
    
    texts = (select_all_negative_texts(sid_to_unique_texts_dict, sid)
             if not is_positive 
             else sid_to_unique_texts_dict[sid])
    
    for text in texts:
        if not isinstance(text, str):
            raise TypeError(f"text is not a string: {text} (type {type(text)})")
        total += 1
        is_match = match_patterns(text, generated_pattern, error_regex_dict, threshold, is_positive, mode)
        correct += is_match
        if not is_match:
            error_list.append(text)
    
    return correct, total, error_list

def write_results(file, test_type, correct, total, error_list, error_regex_dict):
    """
    Writes the evaluation results to the file.

    Args:
        file (file object): File to write the results.
        test_type (str): Type of test ('positive' or 'negative').
        correct (int): Number of correct matches.
        total (int): Total number of samples.
        error_list (list): List of texts that failed to match.
        error_regex_dict (dict): Dictionary to store regex patterns that failed to match.
    """
    file.write(f'{test_type} test\n')
    file.write(f"correct: {correct}, total: {total}, correct rate: {100 * (correct / total):.2f}%\n")
    for not_matched_payload_text in error_list:
        file.write(f"----------------------------------not matched text----------------------------------\n")
        file.write(f"errorList:\n {not_matched_payload_text}\n")
        file.write(f"----------------------------------not matched regex----------------------------------\n")
        for not_matched_regex in error_regex_dict[not_matched_payload_text]:
            file.write(f"error regex: {not_matched_regex}\n")

def validate_input_types(target_text, generated_pattern_list, error_regex_dict):
    """
    Validates the input types.

    Args:
        target_text (str): The text to search within.
        generated_pattern_list (list): List of regex patterns to match.
        error_regex_dict (dict): Dictionary to store regex patterns that failed to match.

    Raises:
        TypeError: If any input is of an incorrect type.
    """
    if not isinstance(error_regex_dict, dict):
        raise TypeError(f"error_regex_dict is not a dictionary: {error_regex_dict} (type {type(error_regex_dict)})")
    if not isinstance(target_text, str):
        raise TypeError(f"target_text is not a string: {target_text} (type {type(target_text)})")
    for i, pattern in enumerate(generated_pattern_list):
        if not isinstance(pattern, str):
            raise TypeError(f"Pattern at index {i} is not a string: {pattern} (type {type(pattern)})")

def update_error_dict(target_text, pattern, error_regex_dict):
    """
    Updates the error dictionary with the non-matching pattern.

    Args:
        target_text (str): The text that failed to match.
        pattern (str): The regex pattern that failed to match.
        error_regex_dict (dict): Dictionary to update with non-matching patterns.
    """
    if target_text in error_regex_dict:
        if pattern not in error_regex_dict[target_text]:
            error_regex_dict[target_text].append(pattern)
    else:
        error_regex_dict[target_text] = [pattern]

def calculate_result(mode, total_patterns, non_matching_count, threshold):
    """
    Calculates the result based on the mode.

    Args:
        mode (str): Mode of threshold ('fraction' or 'integer').
        total_patterns (int): Total number of patterns.
        non_matching_count (int): Number of non-matching patterns.
        threshold (float/int): Threshold for determining a match.

    Returns:
        bool: True if the result meets the threshold, otherwise False.
    """
    if mode == 'fraction':
        return (total_patterns - non_matching_count) / total_patterns >= threshold
    elif mode == 'integer':
        return total_patterns - non_matching_count >= threshold
    else:
        raise ValueError("Invalid mode specified. Use 'fraction' or 'integer'.")

def match_patterns(target_text, generated_pattern_list, error_regex_dict, threshold, is_positive=True, mode='fraction'):
    """
    Matches patterns in the target text and updates the error dictionary.

    Args:
        target_text (str): The text to search within.
        generated_pattern_list (list): List of regex patterns to match.
        error_regex_dict (dict): Dictionary to update with non-matching patterns.
        threshold (float/int): Threshold for determining a match.
        is_positive (bool): Expected outcome of the match.
        mode (str): Mode of threshold ('fraction' or 'integer').

    Returns:
        bool: True if the match result equals is_positive, otherwise False.
    """
    validate_input_types(target_text, generated_pattern_list, error_regex_dict)
    
    non_matching_patterns = []
    for i, pattern in enumerate(generated_pattern_list):
        if not regex.search(pattern, target_text, regex.DOTALL):
            non_matching_patterns.append(f"Pattern {i + 1}: {pattern}")
            if is_positive:
                update_error_dict(target_text, pattern, error_regex_dict)
            else:
                update_error_dict(target_text, pattern, error_regex_dict)
    
    total_patterns = len(generated_pattern_list)
    non_matching_count = len(non_matching_patterns)
    result = calculate_result(mode, total_patterns, non_matching_count, threshold)
    
    return result == is_positive


# def getPcreAnsBySid(sid):
#     with open('sid_table(packet).csv', newline='') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             if row['SID'] == str(sid):
#                 # Remove leading and trailing slashes from the pcre value
#                 return row['pcre']
#     return None

# def positive_answer_evaluation(threeAnsPattern,sid,df):
#     correct = 0
#     total = 0
#     errorList = []
#     ansPattern = getPcreAnsBySid(str(sid))
#     print(f"ansPattern: {ansPattern}")
#     sid_to_unique_texts = map_sid_to_unique_texts(df)
#     texts = sid_to_unique_texts[sid]
#     for text in texts:
#         total = total + 1
#         correct = correct + bool(regex.search(ansPattern, text, regex.DOTALL))
#         if not match_patterns(text, threeAnsPattern, True):
#             errorList.append(text)

#     print("positive test")
#     print(f"correct: {correct}, total: {total}")
#     print(f"errorList: {errorList}")
#     return correct, total

# def negative_answer_evaluation(GeneratedPatternList,sid,sid_to_unique_texts_dict):
#     correct = 0
#     total = 0
#     errorList = []
#     ansPattern = getPcreAnsBySid(str(sid))
#     texts = select_random_texts(sid_to_unique_texts_dict, sid)
#     for text in texts:
#         # 确保 ansPattern 是字符串类型
#         if not isinstance(ansPattern, str):
#             raise TypeError(f"ansPattern is not a string: {ansPattern} (type {type(ansPattern)})")
#         # 确保 text 是字符串类型
#         if not isinstance(text, str):
#             raise TypeError(f"text is not a string: {text} (type {type(text)})")
#         total = total + 1
#         if(not regex.search(ansPattern, text, regex.DOTALL)):
#             correct = correct + 1
#         if  not match_patterns(text, GeneratedPatternList, False):
#             errorList.append(text)
#     print("negative test")
#     print(f"correct: {correct}, total: {total}")
#     for error_text in errorList:
#         print(error_text)
#     print(f"errorList: {errorList}")