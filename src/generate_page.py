import os, shutil, pathlib
from markdown import markdown_to_html_node
def extract_title(markdown):
    if markdown.startswith("# "):
        split_markdown = markdown.splitlines()
        return split_markdown[0].strip("# ")
    else:
        raise Exception("No title present")
    
def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as t:
        template = t.read()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    usable_template = template.replace("{{ Title }}", title)
    usable_template = usable_template.replace("{{ Content }}", html)
    usable_template = usable_template.replace('href="/', basepath)
    usable_template = usable_template.replace('src="/', basepath)
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    with open(dest_path, "w") as d:
        d.write(usable_template)

def generate_page_recursive(dir_path_content, template_path, dest_dir_path , basepath):
    content_files = os.listdir(dir_path_content)
    for file in content_files:
        path = os.path.join(dir_path_content, pathlib.Path(file))
        if os.path.isfile(path):
            generate_page(path, template_path, f"{dest_dir_path}index.html", basepath)
        else:
            if not os.path.exists(f"{dest_dir_path}{file}"):
                os.mkdir(f"{dest_dir_path}{file}")
            generate_page_recursive(dir_path_content + file + "/", template_path, dest_dir_path + file + "/", basepath)
            






