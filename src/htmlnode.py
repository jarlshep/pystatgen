
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        prop_string = ""
        if self.props:
            i = 0
            for item in self.props:
                prop_string = prop_string + f' {item}="{self.props[item]}"'
                i += 1
        return prop_string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
