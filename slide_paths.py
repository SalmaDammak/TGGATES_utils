import os

def get_slide_full_paths(path_to_parent_dir, output_dir, organ=None):
    if organ is None:
        # do both liver and kidney
        organs = ['liver', 'kidney']  
    else:
        organs = [organ]      

    for organ in organs:

        # Get folders in the parent directory
        drug_folder_names = [f for f in os.listdir(path_to_parent_dir) if os.path.isdir(os.path.join(path_to_parent_dir, f))]

        # for every folder in folders, append "organ" as a folder name to the path
        slide_folder_paths = []
        for drug_folder_name in drug_folder_names:
            slide_folder_paths.append(os.path.join(path_to_parent_dir, drug_folder_name, organ))

        # for each folder in slidefolder_fullpaths, get the slides in the directory
        slide_full_paths = []
        all_slide_names = []
        num_folders = len(slide_folder_paths)
        folder_counter = 1
        for slide_folder_path in slide_folder_paths:
            
            try:
                slide_names = [f for f in os.listdir(slide_folder_path) 
                            if os.path.isfile(os.path.join(slide_folder_path, f)) 
                            and f.endswith('.svs')]
                
                for slide_name in slide_names:
                    slide_full_paths.append(os.path.join(slide_folder_path, slide_name))
                    all_slide_names.append(slide_name)

            except FileNotFoundError as e:
                print(f'WARNING! Error in {slide_folder_path}: {e}')
                            
            # print how many folders are complete
            percentage_complete = (folder_counter / num_folders) * 100
            print(f'{folder_counter}/{num_folders} folders complete ({percentage_complete:.2f}%)')
            folder_counter += 1
            

    # write slide_fullpaths to csv
    output_file_path = os.path.join(output_dir, f'{organ}_slide_full_paths.csv')
    with open(output_file_path, 'w') as f:
        for slide_fullpath in slide_full_paths:
            f.write(slide_fullpath + '\n')

    # write all slide names to csv
    output_file_path = os.path.join(output_dir, f'{organ}_all_slide_names.csv')
    with open(output_file_path, 'w') as f:
        for slide_name in all_slide_names:
            f.write(slide_name + '\n')

    return slide_full_paths

# Example usage
path_to_parent_dir = '/Volumes/RBS_PA_CPGARCHIVE/archives/toxicology/open-tg-gates/images'
output_dir = '/Volumes/temporary/toxicology/TG-GATES/liver'
organ = 'liver'
get_slide_full_paths(path_to_parent_dir, output_dir, organ=organ)


# output_dir = '/Volumes/temporary/toxicology/TG-GATES/kidney'
# organ = 'kidney'
# get_slide_full_paths(path_to_parent_dir, output_dir, organ=organ)