from openai import OpenAI
from job_assistant.agent import JobPositionTipificationAgent
from provider import LlmProvider
import configparser
import os

def main():

    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), '.config'))
    api_key = config.get('DEFAULT', 'api_key')
    client = OpenAI(api_key=api_key)

    llmProvider = LlmProvider(model="gpt-4o", client=client)

    agent = JobPositionTipificationAgent(provider=llmProvider)

    agent.process("""
                  {
                    'job_responsibilities': 'We are looking for a Hands-On QA Leader for our talented R&amp;D team, located in the Center of Tel Aviv.In this role you'll be responsible for leading and building our QA process. You will work closely with people across engineering, product, and community to help develop an amazing experience for our customers.'
                  }
                  """
                  )


if __name__ == "__main__":
    main()