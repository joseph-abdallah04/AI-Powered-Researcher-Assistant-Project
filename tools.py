from langchain_community.tools import WikipediaQueryRun # These tools are free but you will get rate limited if you use them too much
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool # allows you to wrap or create your own custom tool
from datetime import datetime

search = DuckDuckGoSearchRun()
search_tool = Tool( # This is a custom tool that we can pass to our agent that uses the search tool (in the line above) that uses DuckDuckGo as a search engine to find information
    name="search", # The name of the tool
    func=search.run, # The function that the tool will run
    description="Search the web for information." # The description of the tool so the AI knows when to use it
)

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100) # This is a wrapper for the Wikipedia API that allows us to get information from Wikipedia
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper) # This is a custom tool that we can pass to our agent that uses the Wikipedia API to find information

# This is a custom function that we use as a tool to save the output of the agent to a text file
def save_to_txt(data:str, filename: str = "research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    formatted_text = f"- - - Research Output - - -\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as file:
        file.write(formatted_text)

    return f"Data successfully saved to {filename}."

# This is a custom tool that we can pass to our agent that uses the save_to_txt function to save the output of the agent to a text file
# It uses the save_to_txt() function that we created above to do so
save_tool = Tool(
    name="save_text_to_file",
    func=save_to_txt,
    description="Save the generated research paper or output to a text file. Use this tool after completing the research."
)