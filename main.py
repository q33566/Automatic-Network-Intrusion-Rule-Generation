from API.FileReader import readPkl, readCsv
from API.FileProcessor import merge_dataframes_to_dict,  filter_sids_by_text_length, select_random_texts
from API.regexEvaluation import positive_evaluation, negative_evaluation

pop_df = readPkl("pop_report_with_tknscore_new.pkl")
imap_df = readPkl("imap_report_with_tknscore_new.pkl")
smtp_df = readPkl("smtp_report_with_tknscore_new.pkl")
sip_df = readPkl("sip_report_with_tknscore_new.pkl")
label_df = readCsv("sid_table(packet).csv")

dfs = [pop_df, imap_df, smtp_df, sip_df]
sid_to_unique_texts_dict = merge_dataframes_to_dict(dfs)
filted_sid = filter_sids_by_text_length(sid_to_unique_texts_dict)




GeneratedPatternList = [
r"^DELE \d+\r\n$", 
r"^DELE [0-9]+\r\n$", 
r"^DELE [1-9][0-9]*\r\n$", 
r"^(DELE \d+\r\n)$", 
r"^(DELE [1-9]\d*\r\n)$", 
r"^(DELE (?:[1-9]\d{0,2}|1[0-2]\d{2})\r\n)$", 
r"^DELE [0-9]{1,3}\r\n$", 
r"^DELE \d{1,3}\r\n$", 
r"^DELE [1-9][0-9]{0,2}\r\n$"
]

SID = '1161912'
positive_evaluation(GeneratedPatternList, SID, sid_to_unique_texts_dict)
negative_evaluation(GeneratedPatternList, SID, sid_to_unique_texts_dict)
