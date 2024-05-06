# The following code can compare two csv files in order to find any mismatches and can write the results
# (including mismatched_column, Mimatched_row id & missing records in both tables) in different sheet of an Excel file.
# In addition, it can illustrate the results in a (streamlit) Dashboard.

import pandas as pd
import streamlit as st
def compare_files(file1, file2, output_file):
    # read the both csv files
    r1 = pd.read_csv(file1)
    r2 = pd.read_csv(file2)
    # join data to ensure that we are comparing apple to apple
    merged = pd.merge(r1, r2, how="inner", on="trade_sk", suffixes=("_r1", "_r2"), indicator=True)
    print(merged.shape)
    # print(merged.iloc[1,1])

    # identify the missing records
    r1_count = len(set(r1['trade_sk']))
    r2_count = len(set(r2['trade_sk']))
    merged_count = len(set(merged['trade_sk']))

    r1_missing_count = r1_count - merged_count
    r2_missing_count = r2_count - merged_count
    print(r1_missing_count)
    print(r2_missing_count)

    data3 = {'table': ['r1', 'r2'],
            'row_count': [r1_missing_count, r2_missing_count]}

    # get the columns as a list
    column_list = merged.columns.to_list()
    # print(column_list)
    r1_column_list = [value for value in column_list if '_r1' in value]
    r2_column_list = [value for value in column_list if '_r2' in value]
    # compare cell by cell
    mismatched_column = []
    key = []
    for i in range(len(merged)):
        for j in range(len(r1_column_list)):
            if (j + 1 < len(merged.columns)) and (j + len(r1_column_list) + 1 < len(merged.columns)):
                if merged.iloc[i, j + 1] != merged.iloc[i, j + len(r1_column_list) + 1]:
                    mismatched_column.append(column_list[j + 1])
                    key.append(merged['trade_sk'][i])

    # identify unique column and other state
    key = list(set(key))
    mismatched_column = list(set(mismatched_column))
    data1 = {'Mismatched_column': mismatched_column}
    df1 = pd.DataFrame(data1)
    data2 = {'Mismatched_row': key}
    df2 = pd.DataFrame(data2)
    df3 = pd.DataFrame(data3)

    print(mismatched_column)
    print(key)

    # write the results in Excel file
    with pd.ExcelWriter(output_file) as writer:
        df1.to_excel(writer, sheet_name='Mismatched_column', index=False, header=['Mismatched_column'])
        df2.to_excel(writer, sheet_name='Mismatched_row', index=False, header=['Mismatched_row(trade_sk)'])
        df3.to_excel(writer, sheet_name='missing_count', index=False, header=['table', 'missing_count'])

    st.title('File Comparison Dashboard')
    # Display result
    st.write('Mismatched Columns:')
    st.dataframe(df1)

    st.write('Mismatched Rows:')
    st.dataframe(df2)

    st.write("Missing Counts:")
    st.dataframe(df3)

compare_files("r1.csv", "r2.csv", "output1.xlsx")
