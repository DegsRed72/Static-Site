from copy_static import copy_contents_to_other_dir
from generate_page import generate_page_recursive

def main():
    copy_contents_to_other_dir()
    generate_page_recursive("content/", "template.html", "public/")


if __name__ == "__main__":
    main()