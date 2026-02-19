from textnode import TextNode, TextType
import os, shutil
from gencontent import generate_page, generate_pages_recursive
import sys

def main():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    
    content_dir = os.path.join(base_dir, "content")
    template_path = os.path.join(base_dir, "template.html")
    static_dir = os.path.join(base_dir, "static")
    public_dir = os.path.join(base_dir, "docs")

    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    # print("hello world")
    # TextNode_obj = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    # print(TextNode_obj)

    copy_static(static_dir, public_dir)

    # generate_page("content/index.md", "template.html", "public/index.html")
    
    generate_pages_recursive(content_dir, template_path, public_dir, basepath)

def clean_public_directory(public_directory_path):
    if os.path.exists(public_directory_path):
        shutil.rmtree(public_directory_path)
    os.mkdir(public_directory_path)

def recursive_copy(source_path, destination_path):
    if not os.path.exists(destination_path):
        os.mkdir(destination_path)

    contents = os.listdir(source_path)
    for content in contents:
        full_source_path = os.path.join(source_path, content)
        full_destination_path = os.path.join(destination_path, content)
        
        # Logging steps
        print(f"Copying {full_source_path} to {full_destination_path}")

        if os.path.isfile(full_source_path):
            shutil.copy(full_source_path, full_destination_path)
        else:
            if not os.path.exists(full_destination_path):
                os.mkdir(full_destination_path)
            recursive_copy(full_source_path, full_destination_path)

def copy_static(static_dir, public_dir):

    clean_public_directory(public_dir)
    recursive_copy(static_dir, public_dir)

"""      
    # Alternatively using relative paths

    clean_public_directory("public")
    recursive_copy("static", "public")
"""

if __name__ == "__main__":
    main()