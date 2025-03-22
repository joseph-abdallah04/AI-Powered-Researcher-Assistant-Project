This project is the serve as a basic AI researcher assistant that researches topics that you give it.

For this probject, Anthropic's LLM, Claude 3.5 Sonnet, was used. A prompt was configured telling the LLM that it is required to write a short snippet/summary of research that it performs 
using tools provided to it (DuckDuckGo search engine and Wikipedia), and that it must return a formatted response including a summary of information, a list of sources, and a list of the 
tools it has used. One of these tools is designed to allow it to save its response into a the research_output.txt file.
