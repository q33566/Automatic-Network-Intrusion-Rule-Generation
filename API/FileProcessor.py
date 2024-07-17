import pandas as pd
import csv
import random

def get_unique_sids_list(df):
    unique_sids = df[df['text'].notnull()]['sid'].unique()
    return unique_sids

def map_sid_to_unique_texts(df):
    sid_to_texts = {}
    for _, row in df.iterrows():
        sid = row['sid']
        text = row['text']
        if pd.notnull(text):  # 確保 text 不是 NaN
            if sid in sid_to_texts:
                sid_to_texts[sid].add(text)
            else:
                sid_to_texts[sid] = {text}
    return sid_to_texts


def merge_dataframes_to_dict(dfs):
    """
    Merge multiple dataframes into a dictionary where each sid maps to a list of unique texts.

    :param dfs: List of pandas DataFrames, each with columns 'sid' and 'text'
    :return: Dictionary with sid as keys and list of unique texts as values
    """
    merged_dict = {}

    for df in dfs:
        for _, row in df.iterrows():
            sid = row['sid']
            text = row['text']
            if sid not in merged_dict:
                merged_dict[sid] = set()  # Use a set to avoid duplicates
            merged_dict[sid].add(text)

    # Convert sets to lists
    merged_dict = {sid: list(texts) for sid, texts in merged_dict.items()}
    
    return merged_dict

def filter_sids_by_text_length(sid_to_texts_dict):
    filtered_sid_to_texts_dict = set()
    for key, value in sid_to_texts_dict.items():
        if len(value) > 5:  # 確保字串長度超過 5
            filtered_sid_to_texts_dict.add(key)
    return filtered_sid_to_texts_dict

def select_random_texts(sid_to_texts_dict, exclude_sid, num_texts=100):
    # 過濾掉給定的 SID
    filtered_texts = [texts for sid, texts in sid_to_texts_dict.items() if sid != exclude_sid]
    
    # 將多個列表平坦化為單一列表
    all_texts = [text for sublist in filtered_texts for text in sublist]
    
    # 隨機選擇 100 個文本，若總數少於 100 則選擇所有文本
    selected_texts = random.sample(all_texts, min(len(all_texts), num_texts))
    
    return selected_texts

def prompt_generator(pop_df, imap_df, smtp_df, sip_df):
    protocols = [
    {'name': 'pop_df', 'data': pop_df},
    {'name': 'imap_df', 'data': imap_df},
    {'name': 'smtp_df', 'data': smtp_df},
    {'name': 'sip_df', 'data': sip_df}
    ]

    with open('prompt.txt', 'w') as file:
        pass

    with open('prompt.txt', 'a') as file:
        for protocol in protocols:
            protocol_name = protocol['name']
            protocol_data = protocol['data']
            
            sid_to_unique_texts = map_sid_to_unique_texts(protocol_data)
            filtered_sids = filter_sids_by_text_length(sid_to_unique_texts)
            
            # Sort the filtered_sids to ensure the output is ordered by SID
            sorted_filtered_sids = sorted(filtered_sids)
            
            file.write(f"Protocol: {protocol_name}\n")
            
            for sid in sorted_filtered_sids:
                texts = list(sid_to_unique_texts[sid])
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
            file.write("\n")