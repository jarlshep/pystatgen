import os
from block_markdown import markdown_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.strip("# ")
    raise Exception("No h1 for title")

def generate_pages_recursive(from_path, template_path, dest_path, basepath="/"):

    dir_list = os.listdir(from_path)

    for item in dir_list:
        into_from = os.path.join(from_path, item)
        into_dest = os.path.join(dest_path, item)
        if os.path.isdir(into_from):
            if not os.path.exists(into_dest):
                os.mkdir(into_dest)
            generate_pages_recursive(into_from, template_path, into_dest)
        else:
            file_name = item.split(".", 1)
            html_file_name = f"{file_name[0]}.html"
            write_to_path = os.path.join(dest_path, html_file_name)

            print(f"Generating page from {from_path} to {dest_path} using {template_path}")

            f = open(into_from)
            markdown = f.read()
            f.close()

            t = open(template_path)
            template = t.read()
            t.close()

            title = extract_title(markdown)
            html_string = markdown_to_html_node(markdown).to_html()

            formatted_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string).replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
            
            new_file = open(write_to_path, "w")    
            new_file.write(formatted_html)
            new_file.close()
            print(f"File {write_to_path} create successfully")





