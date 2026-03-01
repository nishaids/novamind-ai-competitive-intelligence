from dotenv import load_dotenv
import os
load_dotenv()
from crewai import Agent, Task, Crew
import os

api_key=os.getenv("GROQ_API_KEY")


research_agent = Agent(
    role="Company Research Specialist",
    goal="Research detailed information about any company",
    backstory="You are an expert business analyst who researches companies deeply and finds key insights",
    verbose=True
)

research_task = Task(
    description="Research the company 'Tesla' and find: founding year, CEO, revenue, main products, and market position",
    expected_output="A detailed report with Tesla's key business information in bullet points",
    agent=research_agent
)

crew = Crew(
    agents=[research_agent],
    tasks=[research_task],
    verbose=True
)

result = crew.kickoff()

print("\n✅ RESEARCH COMPLETE!")
print(result)