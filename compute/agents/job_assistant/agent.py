from agent import BaseAgent
from provider import LlmProvider

from tools.tool import SmartKeyWordConceptRegistry, SmartKeyWordConceptFetcher
from tools.tool_inventory import Inventory
import re
import json

class JobPositionTipificationAgent(BaseAgent):

    prompt = '''
    You are a job assistant agent giving support to HR professionals. You have been assigned the role to 
    identify key concepts in job descriptions. You will receive a text describing a section of a job position. Your goal is to identify the keywords.
    Never repeat the same keyword twice. 
    It is mandatory to first fetch the existing keywords for the given concept, and to use exiting ones if suitable. Never add a new keyword if there is
    an existing one in the registry. You will be asked for a concept section at a time. A text will only contain one concept section. The existing concepts are:
    - Job responsibilities: stored as 'job_responsibilities'
    - Soft skills: stored as 'soft_skills'
    - Hard skills: stored as 'hard_skills'
    You are restricted to only using 3 keywords for every request received. Make sure to use the existing keywords if suitable. Only add new keywords if there are no existing ones that fit the context.
    Ensure to store the new keywords in the registry before responding to the user with the keywords.
      
    You have access to a set of tools that will help you fetch the existing concepts and keywords, and to store new ones. 
    - inventory: a list of all available tools and their descriptions. Make sure to use this tool before using any other tool.

    You will receive a message from a user. You will start a chain of thought and do one of the following:
    
    - Option 1: use a tool to respond to the message. 
    For this, you will use the following JSON format:
    {
        "thought": "[Your thought, think about what to do]",
        "tool": "[Tool name you will use, choose from the inventory. Ask for 'inventory' tool if you need to see the list of tools]",
        "tool_input": "[Input needed for the tool. Inventory needs no input]"
    }
    
    After this, the user will respond with an observation, and you will continue the chain of thought.
    
    - Option 2: You respond to the user. 
    For this, you will use the following JSON format:
    {   
        "tool": "response",
        "tool_input": "[keywords separated by commas]"
    }

    '''

    def __init__(self, provider: LlmProvider):
        super().__init__(name="JobPositionTipificationAgent", initial_prompt=self.prompt, provider=provider)
        self._inventory = Inventory()
        self._inventory.add_tool(SmartKeyWordConceptRegistry())
        self._inventory.add_tool(SmartKeyWordConceptFetcher())
        self.__finished = False

    def reasoning(self, response_text):
        try:
            response_json = json.loads(response_text)
        except json.JSONDecodeError:
            print("Invalid JSON format.")
            return "Invalid JSON format."

        if response_json.get("tool") == "response":
            self.__finished = True
            registry = self._inventory.get_tool("Smart Keyword Concept Registry")
            registry.execute("job_responsibilities", response_json.get("tool_input").split(","))
            return response_json.get("tool_input", "")
        else:
            thought = response_json.get("thought", "")
            tool_name = response_json.get("tool", "")
            tool_input = response_json.get("tool_input", "")
            tool = self._inventory.get_tool(tool_name)
            if tool:
                tool_result = tool.execute(tool_input)
                return json.dumps({
                    "thought": thought,
                    "tool": tool_name,
                    "tool_input": tool_input,
                    "result": tool_result
                })
            else:
                return json.dumps({
                    "thought": thought,
                    "tool": tool_name,
                    "tool_input": tool_input,
                    "error": f"Tool {tool_name} not found in the inventory."
                })

    @property
    def finished(self):
        return self.__finished