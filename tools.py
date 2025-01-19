from dotenv import load_dotenv
import os
from crewai_tools import SerperDevTool, WebsiteSearchTool
load_dotenv()

os.environ['SERPER_API_KEY'] = os.getenv("SERPER_API_KEY")

anilist_tool = WebsiteSearchTool(website='https://anilist.co/')

myanilist_tool = WebsiteSearchTool(website='https://myanimelist.net/anime.php')

# Initialize the tool for internet searching capabilities
tool = SerperDevTool()