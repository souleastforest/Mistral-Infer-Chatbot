import textwrap
import json

class QAPairs:
    def __init__(self):
        pass

    def formatter(self, system_str, intent_message):
        tools = {}

        test_prompt = textwrap.dedent(f"""
            <s>[INST] system: {system_str} \n\n
            [tools]{json.dumps(tools)}[/tools]</s>
            <s>[INST] user: {intent_message} [/INST]</s>
        """)

        prompt_template = {
            "system": textwrap.dedent(f"""
                 system: {system_str} \n\n
                 user: {intent_message} 
            """),
        }

        return prompt_template["system"]