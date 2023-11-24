from src.models.chain_of_thoughts import BasicChainOfThoughts
from src.models.connectors import DumbLLaMAConnector, DumbCameLLMConnector
from src.models.llms import LLaMA, CameLLM


class TestLLaMA:
    """
    Test AbstractLLM operations.
    """

    VERY_LONG_SYSTEM_PROMPT = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed iaculis leo dui. Fusce luctus gravida pulvinar. Maecenas
nec odio ut sapien lobortis volutpat. Fusce pulvinar pellentesque elit, ut scelerisque nisi ullamcorper vitae. Maecenas
molestie quam nec lacus tempor interdum. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras congue posuere
ligula ac mattis. Fusce a iaculis velit. Donec id sapien pharetra, mollis felis tristique, tincidunt orci. Morbi eget
arcu ac elit rutrum porta in quis justo. Maecenas et mattis sapien. Vestibulum ante ipsum primis in faucibus orci luctus
et ultrices posuere cubilia curae; Nullam viverra metus sit amet massa laoreet, eu tincidunt purus fringilla. Aenean eu
leo nec est venenatis vestibulum ac vitae dui. Fusce ut lectus condimentum, volutpat velit ac, dapibus magna. Vestibulum
vel enim a risus porta accumsan a non dolor. Curabitur ultrices pellentesque leo, sed feugiat arcu sollicitudin sit
amet. Aenean enim dui, porttitor ac vulputate id, fermentum in tortor. Curabitur ullamcorper bibendum sollicitudin.
Pellentesque eget sem fermentum, scelerisque sem nec, finibus erat. Duis tristique dictum neque, id auctor nibh maximus
ut. Suspendisse potenti. Maecenas scelerisque urna nec venenatis egestas. Cras dignissim lacinia nisl. Donec vitae
rhoncus sapien. Proin arcu eros, commodo a maximus vitae, malesuada sed ex. Sed lacinia placerat neque, eu sodales purus
porttitor eget. Aliquam nec luctus nisi, sed vulputate sapien. Proin interdum justo vitae erat lobortis fringilla.
Fusce ipsum neque, imperdiet a odio eget, volutpat sodales massa. Pellentesque ac odio vel sapien scelerisque placerat.
Mauris et purus a lectus porta sodales a non tellus. Vivamus dapibus nisl at felis cursus pharetra. Donec nec quam sit
amet leo efficitur lacinia vitae efficitur metus. Nullam congue dolor quis turpis tristique, ac mattis est elementum.
Interdum et malesuada fames ac ante ipsum primis in faucibus. Donec id lacus dolor. Aenean a nulla a nunc rhoncus
porttitor vel in dolor. Donec ultricies venenatis magna, sit amet pulvinar urna accumsan non. Sed luctus urna metus, id
dignissim sapien porttitor ac. Nam efficitur, odio at facilisis imperdiet, enim eros rhoncus nulla, sed lobortis mi
metus quis libero. Sed ultricies, ante ut porta sollicitudin, tortor augue ornare lorem, eget posuere massa ligula a
orci. Etiam mollis sit amet purus porttitor malesuada. Mauris facilisis dolor in lectus pulvinar malesuada. In eget
metus orci. Donec a imperdiet augue, in bibendum orci. In ultrices, libero eu feugiat faucibus, lectus eros pellentesque
urna, eu dictum ex arcu non arcu. Donec malesuada purus eros, laoreet pulvinar orci suscipit id. Ut accumsan libero eu
tortor malesuada pulvinar. Phasellus purus dui, pulvinar congue eleifend at, vulputate a ex. In dignissim in odio eget
aliquam. Cras ornare vel orci nec euismod. Proin auctor lobortis ante sed pretium. Sed leo massa, scelerisque vitae
orci eu, rhoncus semper velit. Integer a leo elementum, pretium felis ac, pharetra nulla. Nunc a erat in urna mollis
interdum eget eget risus. Suspendisse commodo hendrerit molestie. Quisque vulputate euismod erat, eu cursus arcu dictum
imperdiet. Cras eu metus ut lectus consequat placerat at id neque. Suspendisse tempus interdum tortor, et elementum dui
tincidunt at. Pellentesque nisl velit, finibus a varius quis, dignissim id eros. Etiam dapibus dignissim convallis.
Proin scelerisque fermentum elementum. In sed pulvinar sapien. Pellentesque vestibulum mauris vitae vehicula dignissim. 
        """
    LONG_USER_MESSAGE = """
 Mauris dapibus auctor risus, at egestas ligula malesuada vitae. Nunc eu est mi. In luctus faucibus odio, cursus
 molestie tortor tincidunt luctus. Maecenas posuere ligula nec lobortis mattis. Proin blandit nisi condimentum quam
 venenatis, at commodo ligula volutpat. Nullam varius nulla at accumsan pulvinar. Sed lorem arcu, tincidunt vel nibh
 sed, ultrices consectetur nisl. Vivamus fermentum sed nunc ac facilisis. Sed vitae magna imperdiet, vehicula nisl et,
 laoreet sapien. Donec blandit, neque vel dapibus sodales, enim ex laoreet dolor, ut convallis turpis quam in leo. 
"""

    def test_llama_prompt_generation(self):
        llm = LLaMA(DumbLLaMAConnector(), BasicChainOfThoughts())

        query = llm.build_query(
            "You are an expert in household appliances",
            "Can you tell me what is the best laundry machine on the market",
        )

        assert (
            query
            == "[INST] <<SYS>>You are an expert in household appliances<</SYS>> Can you tell me what is the best laundry machine on the market [/INST]"
        )

        assert len(query) <= LLaMA.MAX_LENGTH

        # Test a very long query
        query = llm.build_query(self.VERY_LONG_SYSTEM_PROMPT, self.LONG_USER_MESSAGE)
        assert len(query) <= LLaMA.MAX_LENGTH

    def test_camllm_prompt_generation(self):
        llm = CameLLM(DumbCameLLMConnector(), BasicChainOfThoughts())

        query = llm.build_query(
            "You are an expert in household appliances",
            "Can you tell me what is the best laundry machine on the market",
        )

        assert (
            query
            == """
[INST] <<SYS>>
You are an expert in household appliances
<</SYS>>

Can you tell me what is the best laundry machine on the market [/INST]
"""
        )

        assert len(query) <= CameLLM.MAX_LENGTH

        # Test a very long query
        query = llm.build_query(self.VERY_LONG_SYSTEM_PROMPT, self.LONG_USER_MESSAGE)
        assert len(query) <= CameLLM.MAX_LENGTH
