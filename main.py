from src.static_to_public import source_to_destination
from src.generate_page import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
template = "./template.html"
dir_path_content = "./content"

def main():
    source_to_destination(dir_path_static, dir_path_public)
    generate_pages_recursive(dir_path_content, template, dir_path_public)
if __name__ == "__main__":
    main()