from crewai import Crew, Process
from tasks import research_task, write_task, recommendation_task
from agents import anime_researcher, anime_recommender, anime_writer
import streamlit as st
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def clean_header(content):
    # Define the header to remove
    unwanted_start = "Your Anime Personal Assistant"
    unwanted_marker = "The final answer is:"
    
    # Check if the content contains the unwanted header and remove it
    if unwanted_start in content and unwanted_marker in content:
        content = content.split(unwanted_marker, 1)[-1]  # Keep everything after "The final answer is:"

    # Remove Markdown-specific elements
    content = content.replace("```", "")
 
    
    # Strip any leading or trailing whitespace
    return content.strip()


# Streamlit app title
st.title("SENSEI.ai 先生 - AI Anime Assistant")

# Input for topic
topic = st.text_input("How can I help you today danna-sama: ")

# Create Crew instance
crew = Crew(
    agents=[anime_researcher, anime_writer, anime_recommender],
    tasks=[research_task, write_task, recommendation_task],
    process=Process.sequential,
)

# Button to generate the report
if st.button("Press me to search"):
    with st.spinner("Researching and writing... This may take a few minutes."):
        try:
            # Run the Crew process
            result = crew.kickoff(inputs={"topic": topic})
            article_content = ""

            # Parse and extract results
            if result:
                # Extracting relevant fields from JSON
                article_content = clean_header(result.raw)

                # Save the article content to session state
                st.session_state["article_content"] = article_content
            else:
                st.session_state["article_content"] = "No content generated. Please check the input."

            # Display the article content
            st.subheader("Here's your answer:")
            st.text_area("Content", st.session_state["article_content"], height=300)

        except Exception as e:
            st.error(f"An error occurred while generating the report: {e}")
            

def create_pdf_with_wrapping(content, topic):
    # PDF setup
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Add Title
    title = f"Topic: {topic}"
    story.append(Paragraph(title, styles["Title"]))
    story.append(Spacer(1, 12))  # Spacer for better layout

    # Add Content
    paragraphs = content.split("\n")  # Split content into paragraphs
    for para in paragraphs:
        if para.strip():  # Skip empty lines
            story.append(Paragraph(para, styles["BodyText"]))
            story.append(Spacer(1, 12))  # Add spacing between paragraphs

    # Build the PDF
    doc.build(story)
    buffer.seek(0)
    return buffer


# Button to download the article as a PDF
if "article_content" in st.session_state and st.session_state["article_content"]:

    # Generate the PDF when requested
    pdf_buffer = create_pdf_with_wrapping(st.session_state["article_content"], topic)

    # Download button for the PDF file
    st.download_button(
        label="Download Report as PDF",
        data=pdf_buffer,
        file_name=f"{topic.replace(' ', '_')}_anime.pdf",
        mime="application/pdf",
    )



# Create Crew instance
# crew = Crew(
#     agents=[anime_researcher, anime_recommender, anime_writer],
#     tasks=[research_task, write_task, recommendation_task],
#     process=Process.sequential,
# )

# topic="Tell me about Attack on Titan"
# result = crew.kickoff(inputs={"topic": topic})
# print(result)