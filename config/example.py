"""
Override this file in production to define to use different LLMs,
with specific connectors & chain of thoughts
"""
from src.models.connectors import DumbCameLLMConnector, DumbLLaMAConnector
from src.models.chain_of_thoughts import BasicChainOfThoughts
from src.models.llms import LLaMA, CameLLM


def get_llama2():
    return LLaMA(DumbLLaMAConnector(), BasicChainOfThoughts())


def get_camellm():
    return CameLLM(DumbCameLLMConnector(), BasicChainOfThoughts())
