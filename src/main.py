from copy_static import copy_contents_to_other_dir
from generate_page import generate_page

def main():
    copy_contents_to_other_dir()
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()