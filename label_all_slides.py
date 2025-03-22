import pandas as pd

# exp_dir = '/data/temporary/salma/Experiments/CLAM_Hypertrophy/'
exp_dir = "/Volumes/temporary/salma/Experiments/TG-GATES_OOD/"
image_dir = "/data/pa_cpgarchive/archives/toxicology/open-tg-gates/images"
# archive_dir = "/data/pa_cpgarchive/"
archive_dir = "/Volumes/RBS_PA_CPGARCHIVE/"


# Read the CSV files into DataFrames
overall_df = pd.read_csv(archive_dir + "/archives/toxicology/open-tg-gates/pathology/open_tggates_pathological_image SD.csv", 
    encoding='ISO-8859-1')
abnormality_df = pd.read_csv(archive_dir + "/archives/toxicology/open-tg-gates/pathology/open_tggates_pathology_SD.csv",
    encoding='ISO-8859-1')

# Merge the DataFrames on the unique identifier columns
merged_df = pd.merge(overall_df, abnormality_df, on=['EXP_ID', 'GROUP_ID', 'INDIVIDUAL_ID'], how='left')

# Fill the rows with no abnormalities with "no abnormalities"
merged_df['FINDING_TYPE'].fillna('no abnormalities', inplace=True)

# Function to replace the base path
def replace_base_path(file_location):
    return file_location.replace("ftp://ftp.biosciencedbc.jp/archive/open-tggates-pathological-images/LATEST/images", image_dir)

# Apply the function to the "FILE_LOCATION" column and create a new column "LOCAL_FILE_LOCATION"
merged_df['LOCAL_FILE_LOCATION'] = merged_df['FILE_LOCATION'].apply(replace_base_path)

# Step 4: Save the merged DataFrame to a new CSV file
merged_df.to_csv(exp_dir + 'merged_output_2.csv', index=False)
