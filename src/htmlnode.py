class HTMLNode():
    def __init__(self, tag: str=None, value: str=None, children: list=None, props: dict=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError("Not implemented yet...")
    
    def props_to_html(self):
        if not self.props:
            return ""
        
        result = "".join(map(lambda element: f' {element[0]}="{element[1]}"',self.props.items()))
        return result
    
class ParentNode(HTMLNode):
    def __init__(self, tag: str,  children: list, props: dict=None):
        super().__init__(tag=tag, value=None, children=children, props=props)
    

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

    def to_html(self):
        if not self.tag:
            raise ValueError("Missing tag")
            
        if not self.children:
            raise ValueError("WHERE ARE THE CHILDREN, YOU MONSTER")
        
        content = ''.join(child.to_html() for child in self.children)
        result = f"<{self.tag}{self.props_to_html()}>{content}</{self.tag}>" 
        return result

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def to_html(self):
        if self.value is None:  # Changed condition
            raise ValueError("Value cannot be None")
        
        if not self.tag:
            return self.value
    
        result = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return result
    
    
