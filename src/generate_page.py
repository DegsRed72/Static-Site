import os, shutil
from markdown import markdown_to_html_node
def extract_title(markdown):
    if markdown.startswith("# "):
        split_markdown = markdown.splitlines()
        return split_markdown[0].strip("# ")
    else:
        raise Exception("No title present")
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as t:
        template = t.read()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    usable_template = template.replace("{{ Title }}", title)
    usable_template = usable_template.replace("{{ Content }}", html)
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    with open(dest_path, "w") as d:
        d.write(usable_template)





