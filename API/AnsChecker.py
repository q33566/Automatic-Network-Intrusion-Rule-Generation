import csv
def get_pcre_by_sid(sid, filename='sid_table(packet).csv'):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['SID'] == str(sid):
                # 去除 pcre 值的前後斜線
                return row['pcre'].strip('/')
    return None