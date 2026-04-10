import os
from block_markdown import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # 1. Read the markdown file
    with open(from_path, "r") as f:
        markdown_content = f.read()
    
    # 2. Read the template file
    with open(template_path, "r") as f:
        template = f.read()
    
    # 3. Convert markdown to HTML string
    node = markdown_to_html_node(markdown_content)
    html_content = node.to_html()
    
    # 4. Extract the title
    title = extract_title(markdown_content)
    
    # 5. Replace placeholders
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_content)
    
    # 6. Ensure the destination directory exists
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    
    # 7. Write the final HTML to the destination
    with open(dest_path, "w") as f:
        f.write(template)