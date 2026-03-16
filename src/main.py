import os, shutil
from copystatic import recursive_copy
from page_generation import extract_title, generate_page

def copy_files_to_public():
    path_to_static = "./static"
    path_to_public = "./public"

    # delete everything in public first
    print("Deleting public directory...")
    if os.path.exists(path_to_public):
        shutil.rmtree(path_to_public)
    
    #copy everything in static to public
    recursive_copy(path_to_static, path_to_public)
    
def main():
    copy_files_to_public()

    generate_page("content/index.md", "template.html", "./public")

main()