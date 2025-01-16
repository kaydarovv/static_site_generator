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
        
        result = " ".join(map(lambda element: f" {element[0]}={element[1]}",self.props.items()))
        return result
    
class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
    
    def to_html(self):
        if not self.value:
            raise ValueError("value can't be empty")
        if not self.tag:
            return self.value
        
        result = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return result
