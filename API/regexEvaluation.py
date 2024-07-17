import csv
import random
import pandas as pd
import re
from API.FileProcessor import select_random_texts, map_sid_to_unique_texts

def get_pcre_by_sid(sid):
    with open('sid_table(packet).csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['SID'] == str(sid):
                # Remove leading and trailing slashes from the pcre value
                return row['pcre']
    return None

def match_patterns(targetText, GeneratedPatternList,isPositive=True):
    non_matching_patterns = []  # Step 1: Initialize list for non-matching patterns
    # Check each pattern and add non-matching ones to the list
    for i, pattern in enumerate(GeneratedPatternList):
        if not re.search(pattern, targetText, re.DOTALL):
            non_matching_patterns.append(f"Pattern {i+1}: {pattern}")
    ourResult = True if (9-len(non_matching_patterns)) >= 7 else False
    with open('evaluation_result.txt', 'w') as file:
        for pattern in non_matching_patterns:
            file.write(pattern)
    #ansMatch = bool(re.search(ansPattern, targetText))
    return ourResult == isPositive

def positive_answer_evaluation(threeAnsPattern,sid,df):
    correct = 0
    total = 0
    errorList = []
    ansPattern = get_pcre_by_sid(str(sid))
    print(f"ansPattern: {ansPattern}")
    sid_to_unique_texts = map_sid_to_unique_texts(df)
    texts = sid_to_unique_texts[sid]
    for text in texts:
        total = total + 1
        correct = correct + bool(re.search(ansPattern, text, re.DOTALL))
        if not match_patterns(text, threeAnsPattern, True):
            errorList.append(text)

    print("positive test")
    print(f"correct: {correct}, total: {total}")
    print(f"errorList: {errorList}")
    return correct, total
def negative_answer_evaluation(GeneratedPatternList,sid,sid_to_unique_texts_dict):
    correct = 0
    total = 0
    errorList = []
    ansPattern = get_pcre_by_sid(str(sid))
    texts = select_random_texts(sid_to_unique_texts_dict, sid)
    for text in texts:
        total = total + 1
        if(not re.search(ansPattern, text, re.DOTALL)):
            correct = correct + 1
        if  not match_patterns(text, GeneratedPatternList, False):
            errorList.append(text)
    print("negative test")
    print(f"correct: {correct}, total: {total}")
    for error_text in errorList:
        print(error_text)
    print(f"errorList: {errorList}")
    
def positive_evaluation(generatedPattern,sid,sid_to_unique_texts_dict):
    correct = 0
    total = 0
    errorList = []
    ansPattern = get_pcre_by_sid(str(sid))
    print(f"ansPattern: {ansPattern}")
    texts = sid_to_unique_texts_dict[sid]
    for text in texts:
        total = total + 1
        correct = correct + match_patterns(text, generatedPattern, True)
        if not match_patterns(text, generatedPattern, True):
            errorList.append(text)

    print("positive test")
    print(f"correct: {correct}, total: {total}")
    print(f"errorList: {errorList}")
    return correct, total

def negative_evaluation(GeneratedPatternList,sid,sid_to_unique_texts_dict):
    correct = 0
    total = 0
    errorList = []
    ansPattern = get_pcre_by_sid(str(sid))
    texts = select_random_texts(sid_to_unique_texts_dict, sid)
    for text in texts:
        total = total + 1
        correct = correct + match_patterns(text, GeneratedPatternList, False)
        if  not match_patterns(text, GeneratedPatternList, False):
            errorList.append(text)
    print("negative test")
    print(f"correct: {correct}, total: {total}")
    for error_text in errorList:
        print(error_text)
    print(f"errorList: {errorList}")
    


