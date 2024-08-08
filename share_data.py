from API.FileReader import read_file_as_dataframe, read_generated_regex_from_directory
import pandas as pd

class sharedData:
    def __init__(self, generated_regex_directory_path:str):
        self.pop_df: pd.DataFrame = read_file_as_dataframe("dataset/pop_report_with_tknscore_new.pkl")
        #self.imap_df = readPkl("dataset/imap_report_with_tknscore_new.pkl")
        #self.smtp_df = readPkl("dataset/smtp_report_with_tknscore_new.pkl")
        #self.sip_df = readPkl("dataset/sip_report_with_tknscore_new.pkl")
        #self.label_df = readCsv("dataset/sid_table(packet).csv")
        self.sid_to_unique_text: pd.DataFrame = pd.DataFrame({
            'sid': pd.Series([], dtype='str'),
            'texts': pd.Series([], dtype='object')
        })
        self.generated_regex: pd.DataFrame = pd.DataFrame({
            'sid': pd.Series([], dtype='str'),
            'regex': pd.Series([], dtype='object')
        })
        self.generated_regex_directory_path = generated_regex_directory_path
        
    def get_SID_to_unique_texts(self)->pd.DataFrame:
        if self.sid_to_unique_text.empty:
            unfiltered_sids_to_unique_texts: pd.DataFrame = self.pop_df.groupby('sid')['text'].apply(lambda x: list(set(x.dropna()))).reset_index(name='texts')
            filtered_sids_to_unique_texts: pd.DataFrame = unfiltered_sids_to_unique_texts[unfiltered_sids_to_unique_texts['texts'].apply(lambda x: len(x) > 0)]
            self.sid_to_unique_text = filtered_sids_to_unique_texts
            
        return self.sid_to_unique_text
    
    def get_generated_regex(self)->pd.DataFrame:
        if self.generated_regex.empty:
            self.generated_regex = read_generated_regex_from_directory(self.generated_regex_directory_path)
            self.generated_regex = pd.DataFrame(list(self.generated_regex.items()), columns=['sid', 'regex'])
            
        return self.generated_regex
    
    
    