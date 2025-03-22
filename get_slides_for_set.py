import pandas as pd

def get_slides_for_set(all_slides_csv, set_csv_path, output_dir,organ):
    
    slides_df = pd.read_csv(all_slides_csv)

    compound_names_df =pd.read_csv(set_csv_path, header=None,sep=';')
    compound_names_list = compound_names_df[0].tolist()
    filtered_slides_df = slides_df[slides_df['COMPOUND_NAME_x'].isin(compound_names_list) & 
                                   (slides_df['ORGAN_x'].isin([organ]))]
    
    # Write the filtered file (for human inspection) and the slides file (for experimentation)
    set_name = set_csv_path.split('/')[-1].split('.')[0]
    filtered_slides_df.to_csv(output_dir + "/" + set_name + "_all_cols.csv", index=False)
    filtered_slides_df['LOCAL_FILE_LOCATION'].to_csv(output_dir + "/" +  set_name + "_slides.csv", index=False, header=False)

    # Check if all the compounds in the set are present in the filtered slides
    filtered_compounds = filtered_slides_df['COMPOUND_NAME_x'].unique()
    missing_compounds = set(compound_names_list) - set(filtered_compounds)
    if len(missing_compounds) > 0:
        print("The following compounds are missing from the filtered slides: ", missing_compounds)
    else:
        print("All compounds are present in the filtered slides")

    return filtered_slides_df


base_dir = "/Volumes/temporary/salma/Experiments/TG-GATES_OOD"
organ = "Kidney"
get_slides_for_set(base_dir + "/merged_output_2.csv", base_dir + "/S_drugs.csv", base_dir,organ)
get_slides_for_set(base_dir + "/merged_output_2.csv",base_dir + "/T_drugs.csv", base_dir,organ)