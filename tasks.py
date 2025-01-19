from crewai import Task
from tools import tool, anilist_tool, myanilist_tool
from agents import anime_researcher, anime_writer, anime_recommender


research_task = Task(
    description=(
        """
        1. Analyze query: '{topic}'
        2. Check for summary keywords: 'describe', 'summarize', 'tell me about', 'what is'
        3. If summary keywords present:
            - Research using anilist_tool and tool
            - Create structured summary
            - Delegate theme analysis to recommender agent if needed
            - Compile complete summary with delegated insights
            - Return: 'SUMMARY_REQUESTED: <content>'
        4. If no summary keywords:
            - Return: 'NO_SUMMARY_REQUESTED'
        5. Always consider opportunities for collaboration with other agents
        """
    ),
    expected_output=(
        "Detailed analysis or summary based on the query requirements.\n"
        "Must include processed information, not raw search results."
    ),
    tools=[anilist_tool, myanilist_tool],
    agent=anime_researcher
)

recommendation_task = Task(
    description=(
        """
            1. Analyze query: '{topic}'
            2. Check for recommendation keywords: 'recommend', 'suggest', 'similar', 'like'
            3. If recommendation keywords present:
                - Research using myanilist_tool and tool
                - Consult with researcher agent for detailed context if needed
                - Generate 3-5 relevant recommendations with explanations
                - Return: 'RECOMMENDATIONS_REQUESTED: <content>'
            4. If no recommendation keywords:
                - Return: 'NO_RECOMMENDATIONS_REQUESTED'
            5. Provide theme analysis support to other agents when requested
        """
    ),
    expected_output=(
        "- If recommendations requested: 3-5 recommendations + delegation to writer\n"
        "- If not requested: Notification to writer only\n"
        "Never return raw search results"
    ),
    tools=[anilist_tool, myanilist_tool],
    agent=anime_recommender
)

write_task = Task(
    description=(
        """
            1. Coordinate with specialist agents for '{topic}'
            2. Request additional information or clarification when needed
            3. Structure response:
                - If received 'SUMMARY_REQUESTED': Integrate summary and relevant analysis
                - If received 'RECOMMENDATIONS_REQUESTED': Include recommendations with context
                - Ensure smooth integration of all agent contributions
            4. Format final output with clear organization and natural flow
        """
    ),
    expected_output=(  
        "Well-structured, comprehensive response that directly addresses the query.\n"
        "Must include processed information from all relevant agents."
    ),
    tools=[tool],
    agent=anime_writer,
    async_execution=False
)