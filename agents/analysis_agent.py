from crewai import Agent, Task, Crew, LLM
from dotenv import load_dotenv
import os

load_dotenv()

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

analysis_agent = Agent(
    role="Market Analysis Expert",
    goal="Analyze market trends and find opportunities and threats for any company",
    backstory="You are a senior market strategist who identifies market gaps, threats, and growth opportunities",
    llm=llm,
    verbose=True
)

analysis_task = Task(
    description="Analyze Tesla's market position. Find: 3 market opportunities Tesla can exploit, 3 threats Tesla faces, and overall market trend in EV industry",
    expected_output="A strategic market analysis report with opportunities, threats and trends in bullet points",
    agent=analysis_agent
)

crew = Crew(
    agents=[analysis_agent],
    tasks=[analysis_task],
    verbose=True
)

result = crew.kickoff()
print("\n✅ MARKET ANALYSIS COMPLETE!")
print(result)