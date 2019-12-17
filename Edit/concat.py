import pandas as pd

filename_1 = './resume_final.csv'
resume_table_1 = pd.read_csv(filename_1, encoding='utf-8', index_col=0, header=0, engine='python')

filename_2 = './resume_other.csv'
resume_table_2 = pd.read_csv(filename_2, encoding='utf-8', index_col=0, header=0, engine='python')

resume_table_1 = pd.concat([resume_table_1, resume_table_2])

print(resume_table_1)

# resume_table_end = pd.DataFrame(result_end, columns=('title', 'answer'))
resume_table_1.to_csv("./resume_end.csv", encoding="utf-8", mode='w', index=True)