

def markdown_to_blocks(markdown):
    blocks = []
    split_list = markdown.split("\n\n")
    for string in split_list:
        if string == "":
            continue
        string = string.strip()
        string = string.strip("\n")
        blocks.append(string)
    return blocks

