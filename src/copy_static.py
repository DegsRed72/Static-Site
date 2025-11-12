import os, shutil
def copy_contents_to_other_dir(current_source_directory="static", current_destination_directory="public"):
    if os.path.exists("public") and current_destination_directory == "public":
        shutil.rmtree("public")
    if not os.path.exists("public"):
        os.mkdir("public")
    if os.path.exists("static"):
        entries = os.listdir(current_source_directory)
        for entry in entries:
            file_path = os.path.join(current_source_directory, entry)
            if os.path.isfile(file_path):
                shutil.copy(file_path, current_destination_directory)
            elif os.path.isdir(file_path):
                os.mkdir(f"{current_destination_directory}/{entry}")
                copy_contents_to_other_dir(f"{current_source_directory}/{entry}", f"{current_destination_directory}/{entry}")