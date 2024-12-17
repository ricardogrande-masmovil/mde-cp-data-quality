from .tool import Tool

class Inventory:
    """Inventory stores tools and provides methods to add, get, and list tools.
    It also provides any methods that are useful for agents to interact with the inventory,
    adding any logic that might be needed to manage the tools.
    """

    def __init__(self):
        self._tools= {}

        self.add_tool(
            tool=Tool(
                name="inventory",
                description="list of all available tools and their descriptions",
                action=self.list_inventory,
            )
        )

    def add_tool(self, tool):
        self._tools[tool.name] = tool

    def get_tool(self, name: str) -> Tool:
        return self._tools.get(name)
    
    @property
    def tools(self):
        return self._tools.keys()
    
    def list_inventory(self, *args, **kwargs):
        """ 
        Returns a string with the list of tools in the inventory and their descriptions. 
        Useful for agents needing to know what tools are available.
        Example: 
            tool1: description1
            tool2: description2
        """
        return 'The inventory has the tools:\n' + '\n'.join([str(tool) for tool in self._tools.values()])
