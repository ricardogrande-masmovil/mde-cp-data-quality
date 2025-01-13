from openai import OpenAI

class LlmProvider:
    def __init__(self, model, client: OpenAI):
        # TODO: make it a generic provider
        self._model = model
        self._llm = client
        self._temperature=0
        self._top_p=1

    @property
    def model(self) -> str:
        return self._model
    
    @property
    def llm(self) -> OpenAI:
        # TODO: make it a generic provider
        return self._llm
    
    @property
    def temperature(self) -> float:
        return self._temperature
    
    @property
    def top_p(self) -> float:
        return self._top_p