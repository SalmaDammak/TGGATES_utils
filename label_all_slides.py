import pandas as pd

base_dir = '/data/temporary/salma/Experiments/CLAM_Hypertrophy/'
# Step 1: Read the CSV files into DataFrames
overall_df = pd.read_csv('/data/pa_cpgarchive/archives/toxicology/open-tg-gates/pathology/open_tggates_pathological_image SD.csv', 
    encoding='ISO-8859-1')
abnormality_df = pd.read_csv('/data/pa_cpgarchive/archives/toxicology/open-tg-gates/pathology/open_tggates_pathology_SD.csv',
    encoding='ISO-8859-1')

# Step 2: Merge the DataFrames on the unique identifier columns
merged_df = pd.merge(overall_df, abnormality_df, on=['EXP_ID', 'GROUP_ID', 'INDIVIDUAL_ID'], how='left')

# Step 3: Fill the rows with no abnormalities with "no abnormalities"
merged_df['FINDING_TYPE'].fillna('no abnormalities', inplace=True)

# Step 4: Save the merged DataFrame to a new CSV file
merged_df.to_csv(base_dir + 'merged_output.csv', index=False)
