from textnode import TextNode, TextType

def main():
    new_node = TextNode("oogabooga", TextType.PLAIN_TEXT, None)
    print(new_node)

if __name__ == "__main__":
    main()