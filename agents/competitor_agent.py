from crewai import Agent, Task, Crew, LLM

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key="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"
)

competitor_agent = Agent(
    role="Competitive Intelligence Specialist",
    goal="Find and analyze top competitors of any company",
    backstory="You are an expert market researcher who identifies competitors and analyzes their strengths and weaknesses",
    llm=llm,
    verbose=True
)

competitor_task = Task(
    description="Find the top 3 competitors of Tesla. For each competitor provide: company name, revenue, key products, and main strength against Tesla",
    expected_output="A structured report listing 3 Tesla competitors with their details and competitive strengths",
    agent=competitor_agent
)

crew = Crew(
    agents=[competitor_agent],
    tasks=[competitor_task],
    verbose=True
)

result = crew.kickoff()
print("\n✅ COMPETITOR ANALYSIS COMPLETE!")
print(result)