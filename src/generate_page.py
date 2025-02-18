from .markdown_to_html import markdown_to_html_node
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_title(markdown: str) -> str:
    if not markdown:
        raise Exception("Please provide valid markdown text")
    lines = markdown.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith("# "):
            header_text = line.lstrip("#").strip()
            return header_text
    raise Exception("No header h1(# ) was found")

def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    logger.info(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    title = extract_title(markdown)
    html = markdown_to_html_node(markdown).to_html()
    template = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    
    directory = os.path.dirname(dest_path)
    if directory:
        logger.info(f"Creating directory structure: {directory}")
        os.makedirs(directory, exist_ok=True)
    
    with open(dest_path, "w+") as f:
        f.write(template)
    
    logger.info(f"Successfully wrote file to {dest_path}")
    logger.debug(f"Generated content:\n{template}")

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str) -> None:
    logger.info(f"Generating pages recursively from {dir_path_content} to {dest_dir_path} using {template_path}")
    entries = os.listdir(path=dir_path_content)
    logger.info(f"The contents are: \n {entries}")
    
    for entry in entries:
        entry_path = os.path.join(dir_path_content, entry)
        dest_entry_path = os.path.join(dest_dir_path, entry)
        if os.path.isfile(entry_path):
            dest_html_path = dest_entry_path.replace(".md", ".html")
            generate_page(entry_path, template_path, dest_html_path)
        if os.path.isdir(entry_path):
            generate_pages_recursive(entry_path, template_path, dest_entry_path)