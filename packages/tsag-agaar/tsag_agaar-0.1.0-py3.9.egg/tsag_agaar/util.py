import json


def validate_json(data):
    """
    Incredibly rudimentary function that checks if a dictionary is valid JSON using the built-in `json`
    module.
    """
    try:
        json.dumps(data)
        return True
    except:
        return False


def recursive_dict(node):
    """
    Fairly simple functiion that recursively converts a class to a dictionary while convert it's properties as well.

    There are a few caveats to my approach, including the inability to convert classes that have circular dependencies
    as it will cause the function to be stuck calling itself over and over again until it reaches a stack overflow and exits.

    Here's a little code snippet that replicates this issue.

    ```py
    @dataclasses.dataclass
    class Node:
        parent: typing.Optional[Node] = None
        child: typing.Optional[Node] = None
        index: int = 0

        def create_child(self):
            node = Node(parent=self, index=self.index + 1)
            self.child = node
            return node


    initial_node = Node()

    new_node = None

    for _ in range(2):
        if new_node is None:
            new_node = initial_node.create_child()
            continue

        new_node = new_node.create_child()

    print(recursive_dict(new_node))
    ```
    """
    if validate_json(node):
        return node

    if isinstance(node, (bool, int, str)):
        return node

    if isinstance(node, dict):
        for key, value in node.items():
            if isinstance(value, (bool, int, str)):
                continue

            if isinstance(value, list) or hasattr(value, "__iter__"):
                node[key] = [recursive_dict(item) for item in value]
            else:
                node[key] = recursive_dict(value)
        return recursive_dict(node)
    elif hasattr(node, "__dict__"):
        return recursive_dict(node.__dict__)
