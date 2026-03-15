import os, shutil

def recursive_copy(src_path, dst_path):
    if not os.path.exists(dst_path):
        print(f'Creating directory "{dst_path}"')
        os.mkdir(dst_path)

    for item in os.listdir(src_path):
        curr_src_path = os.path.join(src_path, item)
        curr_dst_path = os.path.join(dst_path, item)
        if os.path.isfile(curr_src_path):
            print(f'Copying "{curr_dst_path}" to "{curr_src_path}"')
            shutil.copy(curr_src_path, curr_dst_path)
        if os.path.isdir(curr_src_path):
            recursive_copy(curr_src_path, curr_dst_path)