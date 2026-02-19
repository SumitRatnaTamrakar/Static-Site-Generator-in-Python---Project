from markdown_blocks import markdown_to_html_node
import os
from pathlib import Path

def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith('# '):
            heading = line.split('# ', 1)[1].strip()
            return heading
        
    raise Exception("There is no h1 header")
        
def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    """ 
    from_path_file = open(from_path, mode='r')
    markdown_file_content = from_path_file.read()
    from_path_file.close()
    """

    # Alternatively
    with open(from_path, "r") as from_path_file:
        markdown_file_content = from_path_file.read()

    """ 
    template_path_file = open(template_path, mode='r')
    template_file_content = template_path_file.read()
    template_path_file.close()
 """
    with open(template_path, "r") as template_path_file:
        template_file_content = template_path_file.read()

    html_node = markdown_to_html_node(markdown_file_content)

    final_html_string = html_node.to_html()

    page_title = extract_title(markdown_file_content)

    template_file_content = template_file_content.replace('{{ Title }}', page_title)
    template_file_content = template_file_content.replace('{{ Content }}', final_html_string)

    template_file_content = template_file_content.replace('href="/', f'href="{basepath}')
    template_file_content = template_file_content.replace('src="/', f'src="{basepath}')

    destination_directory = os.path.dirname(dest_path)
    if destination_directory != "":
        os.makedirs(destination_directory, exist_ok=True)

    """ 
    destination_file = open(dest_path, "w")
    destination_file.write(template_file_content)
    destination_file.close()
 """
    
    with open(dest_path, "w") as destination_file:
        destination_file.write(template_file_content)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    dir_path_dirs = os.listdir(dir_path_content)
    for item in dir_path_dirs:
        dir_full_path = os.path.join(dir_path_content, item)
        dest_full_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(dir_full_path):
            if Path(dir_full_path).suffix == ".md":
                dest_path_ending_in_html = Path(dest_full_path).with_suffix(".html")
                generate_page(dir_full_path, template_path, str(dest_path_ending_in_html), basepath)

        else:
            generate_pages_recursive(dir_full_path, template_path, dest_full_path, basepath)
