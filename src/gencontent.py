import os
from block_markdown import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path, basepath):
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
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    
    # 6. Ensure the destination directory exists
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    
    # 7. Write the final HTML to the destination
    with open(dest_path, "w") as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    # 1. Iterate over every entry in the content directory
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)

        # 2. If it's a file, check if it's markdown
        if os.path.isfile(from_path):
            if filename.endswith(".md"):
                dest_html_path = dest_path.replace(".md", ".html")
                generate_page(from_path, template_path, dest_html_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)