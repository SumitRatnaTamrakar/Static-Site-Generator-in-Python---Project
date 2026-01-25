class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Subclasses must implement to_html method")

    def props_to_html(self):
        if not self.props:
            return ""
        props_str = " ".join(f'{key}="{value}"' for key, value in self.props.items())
        return f" {props_str}"
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict = None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        props_html = self.props_to_html()
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        elif not self.tag:
            return self.value
        elif self.tag in ["img", "br", "hr", "input", "meta", "link"]:
            return f"<{self.tag}{props_html}/>"
        else:
            return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict = None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have children")
        
        opening_tag = f"<{self.tag}{self.props_to_html()}>"
        children_html = "".join(child.to_html() for child in self.children)
        closing_tag = f"</{self.tag}>"
        return f"{opening_tag}{children_html}{closing_tag}"

    def __repr__(self):
        return f"ParentNode(tag={self.tag}, children={self.children}, props={self.props})"
    