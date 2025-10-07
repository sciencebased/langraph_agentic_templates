from langchain_core.prompts import PromptTemplate

template = """\
You are a helpful assistant that can extract contact information from a given conversation.
If you are unable to find the information, ask to the user about his name at least.
"""

prompt_template = PromptTemplate.from_template(template)