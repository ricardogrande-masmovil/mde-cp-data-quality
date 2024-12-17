from provider import LlmProvider
import time

class BaseAgent:
    """BaseAgent is the base class for all agents in the system. It provides common functionality and an interface for 
    subclasses to implement.
    It is initialized with a provider, which is a generic instance of an LLM Api provider.
    """
    def __init__(self, name, initial_prompt, provider: LlmProvider):
        # TODO: replace OpenAI with a generic provider (make it an interface, or a base class)
        self.name = name
        self.initial_prompt = initial_prompt
        self.provider = provider

        self._messages = [
            {
                "role": "system",
                "content": initial_prompt
            }
        ]

    def add_message(self, role, content):
        self._messages.append({
            "role": role,
            "content": content
        })

    def add_messages(self, messages: list[dict]):
        self._messages.extend(messages)

    def process(self, input):
        """Process a user input and return the response from the agent.
        """
        self.add_message("user", input)

        # TODO: this method is candidate to be refactored to a more abstract method
        is_finished = False
        while not is_finished:
            response = self.provider.llm.chat.completions.create(
                model=self.provider.model,
                messages=self._messages,
                temperature=self.provider.temperature,
                top_p=self.provider.top_p,
            )

            response_text = response.choices[0].message.content
            print(response_text)
            time.sleep(5) # TODO: defensive sleep to avoid rate limiting, should be handled in a better way

            # response_text = get_mock_response(0)

            # run the reasoning implementation (each agent should implement it)
            try :
                reasoning_output = self.reasoning(response_text)
                print(reasoning_output)

                is_finished = self.finished
                self.add_messages([
                    {
                        "role": "system",
                        "content": response_text,
                    },
                    {
                        "role": "user",
                        "content": str(reasoning_output),
                    }
                ])
            except Exception as e:
                self.add_messages([response_text, f"Error: {e}"])
                return

        return
    
    def reasoning(self, response_text):
        """Extract the tool from the response text. 
        This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method")
        
    @property
    def finished(self):
        """Check if the conversation is finished. 
        This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method")
    

def get_mock_response(response_number: int) -> str:
    mock_dict = {
        0: 'Thought: I need to find the modified files for PR 562. This likely requires accessing a tool that can provide information about pull requests and their associated files. I will check the available tools to see if there is one that can help with this request. \nTool: Inventory\nTool input: ',
    }

    return mock_dict.get(response_number)