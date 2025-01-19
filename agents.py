from crewai import Agent, LLM
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os
from tools import tool, anilist_tool, myanilist_tool
import openai

# Load environment variables
load_dotenv()

# Initialize Ollama LLM
ollama_llm = LLM(
    model='ollama/llama3.2:1b',  # Use your downloaded Ollama model name here
    base_url='http://localhost:11434',  # Default Ollama server URL
    verbose=True,
    temperature=0.5,  # Adjust temperature if needed
)

# Initialize OpenAI LLM
openai.api_key = os.getenv("OPENAI_API_KEY")
openai_llm = LLM(
    model = "gpt-4o-mini",
    verbose=True,
    temperature=0.5,
    api_key=openai.api_key,
)


# Anime Research Analyst Agent
anime_researcher = Agent(
    role="Anime Research & Summary Specialist",
    goal="""
    1. Analyze queries for summary requests using keywords: 'summary', 'describe', 'tell me about', 'what is'
    2. For summary requests:
       - Research the anime thoroughly using provided tools
       - Create a structured summary covering plot, characters, and themes
       - Delegate specific theme analysis to the recommendation agent if needed
       - Format output as: 'SUMMARY_REQUESTED: <content>'
    3. For non-summary requests:
       - Return 'NO_SUMMARY_REQUESTED'
    4. Collaborate with other agents when additional expertise is needed
    """,
    verbose=True,
    memory=False,
    backstory=(
        "Expert anime researcher with deep knowledge of anime series, movies, and industry. "
        "Provides detailed, accurate summaries when explicitly requested. "
        "Always verifies information before sharing."
    ),
    tools=[anilist_tool],
    llm=openai_llm,
    allow_delegation=True,
)

# Anime Recommendation Agent
anime_recommender = Agent(
    role="Anime Recommendation Expert",
    goal="""
    1. Analyze queries for recommendation requests using keywords: 'recommend', 'suggest', 'similar', 'like'
    2. For recommendation requests:
       - Use tools to find relevant recommendations
       - Provide 3-5 recommendations with clear reasoning
       - Consult with researcher agent for detailed anime context if needed
       - Format output as: 'RECOMMENDATIONS_REQUESTED: <content>'
    3. For non-recommendation requests:
       - Return 'NO_RECOMMENDATIONS_REQUESTED'
    4. Support other agents with genre and theme analysis when requested
    """,
    verbose=True,
    memory=False,
    backstory=(
        "Experienced anime curator with deep understanding of various genres and themes. "
        "Specializes in finding connections between different anime and understanding viewer preferences. "
        "Provides detailed, contextualized recommendations with clear explanations for each suggestion."
    ),
    tools=[myanilist_tool],
    llm=openai_llm,
    allow_delegation=True,
)

# Anime Content Writer Agent
anime_writer = Agent(
    role="Anime Content Creator",
    goal="""
    1. Coordinate with researcher and recommender agents to gather comprehensive information
    2. Process inputs and request additional details when needed
    3. Structure final response based on requested content:
       - If summary requested: Incorporate researcher's summary and any relevant theme analysis
       - If recommendations requested: Include recommender's suggestions with context
       - Ensure smooth integration of delegated content
    4. Format final output with clear organization and flow
    """,
    verbose=True,
    memory=False,
    backstory=(
       "You are a skilled content coordinator who works with specialist agents to create "
        "comprehensive content. You only include summaries and recommendations when they "
        "were explicitly requested and provided by the respective specialist agents. "
        "You organize the final content based on what was actually requested and received."
    ),
    tools=[tool],
    llm=openai_llm,
    allow_delegation=True,
)