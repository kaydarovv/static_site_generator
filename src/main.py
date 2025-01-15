from textnode import TextNode, TextType

def main():
    node1 = TextNode("bananza", TextType.CODE, 'https://www.boot.dev/lessons/cdae7fca-a7dc-4706-b2c5-7a03d66db1c9')
    print(node1.__repr__())

main()