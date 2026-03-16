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

    generate_page("content/index.md", "template.html", "./public/index.html")
    generate_page("content/blog/glorfindel/index.md", "template.html", "./public/blog/glorfindel/index.html")
    generate_page("content/blog/tom/index.md", "template.html", "./public/blog/tom/index.html")
    generate_page("content/blog/majesty/index.md", "template.html", "./public/blog/majesty/index.html")
    generate_page("content/contact/index.md", "template.html", "./public/contact/index.html")

main()