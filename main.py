import os
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool # This is the custom tool that we created in the tools.py file. We are importing it here for use in the agent
from tools import wiki_tool # Importing the wiki_tool that we created in the tools.py file
from tools import save_tool # Importing the save_tool that we created in the tools.py file

load_dotenv() # This line loads the .env file

#This below was included as I was running into issues with the .env file not being loaded properly. It still didn't load properly.
#so I had to run the folling command in the terminal to export the api key directly: export ANTHROPIC_API_KEY="YOUR_API_KEY"
# print("ANTHROPIC_API_KEY:", os.getenv("ANTHROPIC_API_KEY"))

# Here is where I have specified all the fields that I want as output from the LLM call.
# It is important that all of the classes inherit from the BaseModel class from Pydantic to ensure that the output is in the correct format/data type
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
parser = PydanticOutputParser(pydantic_object=ResearchResponse)


"""
The prompt below is the prompt that will be sent to the LLM model.
The prompt is a ChatPromptTemplate object that takes in a list of tuples.
Each tuple is a message that will be sent to the LLM model.
The first element of the tuple is the speaker of the message (human or system).
The second element of the tuple is the message itself.
The placeholders in the message are replaced by the values passed to the partial method of the ChatPromptTemplate object.
The placeholders are enclosed in curly braces.

The parser is used to format the output of the LLM model to the desired format so that no errors are encountered due to types.
The format_instructions are added to the prompt to ensure that the output is in the correct format.
The format_instructions are added to the prompt in the partial method of the ChatPromptTemplate object.
The format_instructions are obtained from the parser object by calling the get_format_instructions method.
"""
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that will help generate a research paper.
            Answer the user query and use neccessary tools to generate the research paper.
            Wrap the output in this format and provide no other text\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions()) # This line is where the format instructions are preloaded into the prompt

tools = [search_tool, wiki_tool, save_tool] # This is a list of tools that the agent can use to find information.
agent = create_tool_calling_agent(
    llm=llm, # passing the LLM model to the agent
    prompt=prompt, # passing the prompt to the agent
    tools=tools, # passing the list fo tools to the agent
)

# Verbose is set to True to show us the thought process of the agent
# the {chat_history} and {agent_scratchpad} placeholders from within the prompt are taken care of by the agent_executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True) # list of tools is passed to the agent_executor also
query = input("What can I help you research?\n") # The user is prompted to enter a query
raw_response = agent_executor.invoke({"query": query}) # The query is passed to the agent_executor to be sent to the LLM model
# print(raw_response) # This line is used to print the raw response of the LLM model. I used this for testing purposes.

"""
The below line structures the reponse of the output. If you look at the raw response, it has an "output" 
key that contains the output of the LLM model. This is structued in a list[] format. So we take the first
element of the list (that being the text output) and pass it to the parser to get the structured response.
It structures this response according to the ResearchResponse class that we defined above. Look at the class,
and see how we have defined the fields that we want in the output. The parser will then structure the output
because we gave it the format instructions in the prompt.

The try catch block is simply there to catch any errors that may occur during the parsing of the response.
If an error occurs, it will print the error and the raw response so that we can see what went wrong.
"""
try:
    structured_response = parser.parse(raw_response.get("output")[0]["text"])
    print(structured_response)
except Exception as e:
    print("Error parsing response:", e, "\nRaw Response - ",raw_response)

# The below lines are examples how you can now access individual attributes of the AI's response, which
# are structured according to the attributes of the ResearchResponse class that we defined above:
# print(structured_response.topic)
# print(structured_response.summary)
# print(structured_response.sources)
# print(structured_response.tools_used)
