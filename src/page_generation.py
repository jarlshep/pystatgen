import os
from block_markdown import markdown_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.strip("# ")
    raise Exception("No h1 for title")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    f = open(from_path)
    markdown = f.read()
    f.close()

    t = open(template_path)
    template = t.read()
    t.close()

    title = extract_title(markdown)
    html_string = markdown_to_html_node(markdown).to_html()

    formatted_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)

    """ if not os.path.exists(dest_path):
        os.mkdir(dest_path) """

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    """ file_name_full = os.path.basename(from_path)
    file_name = file_name_full.split(".", 1)
    new_file_name = f"{file_name[0]}.html"
    write_to_path = os.path.join(dest_path, new_file_name) """
    
    new_file = open(dest_path, "w")    
    new_file.write(formatted_html)
    new_file.close()
    print(f"File {dest_path} create successfully")





