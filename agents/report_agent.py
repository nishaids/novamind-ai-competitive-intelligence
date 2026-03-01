from crewai import Agent, Task, Crew, LLM

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key="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"
)

report_agent = Agent(
    role="Business Intelligence Report Writer",
    goal="Create professional executive reports from research and analysis data",
    backstory="You are an expert business writer who creates clear, professional intelligence reports for CEOs and executives",
    llm=llm,
    verbose=True
)

report_task = Task(
    description="""Create a professional Executive Intelligence Report for Tesla with these sections:
    1. Executive Summary
    2. Company Overview
    3. Top 3 Competitors
    4. Market Opportunities
    5. Key Threats
    6. Strategic Recommendations
    Keep it concise and professional like a real business report""",
    expected_output="A complete professional Executive Intelligence Report with all 6 sections clearly formatted",
    agent=report_agent
)

crew = Crew(
    agents=[report_agent],
    tasks=[report_task],
    verbose=True
)

result = crew.kickoff()

print("\n✅ REPORT GENERATION COMPLETE!")
print(result)

with open("output/tesla_intelligence_report.txt", "w") as f:
    f.write(str(result))

print("\n📁 Report saved to output/tesla_intelligence_report.txt")