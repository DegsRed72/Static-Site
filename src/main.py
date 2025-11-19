from copy_static import copy_contents_to_other_dir
from generate_page import generate_page_recursive
import sys

def main():
    print(sys.argv)
    if sys.argv:
        basepath = sys.argv
    else:
        basepath = "/"
    copy_contents_to_other_dir()
    generate_page_recursive("content/", "template.html", "docs/", basepath[0])


if __name__ == "__main__":
    main()