from crewai import Agent, Task, Crew, LLM

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key="AIzaSyBmMCmbSftjsXKBOIUpdsNfvuuNDzb-JFo"
)

company = input("🏢 Enter company name to analyze: ")

research_agent = Agent(
    role="Company Research Specialist",
    goal="Research detailed information about any company",
    backstory="You are an expert business analyst who researches companies deeply",
    llm=llm, verbose=True
)

competitor_agent = Agent(
    role="Competitive Intelligence Specialist",
    goal="Find and analyze top competitors of any company",
    backstory="You are an expert market researcher who identifies competitors and analyzes their strengths",
    llm=llm, verbose=True
)

analysis_agent = Agent(
    role="Market Analysis Expert",
    goal="Analyze market trends and find opportunities and threats",
    backstory="You are a senior market strategist who identifies market gaps and opportunities",
    llm=llm, verbose=True
)

report_agent = Agent(
    role="Business Intelligence Report Writer",
    goal="Create professional executive reports from research data",
    backstory="You are an expert business writer who creates reports for CEOs and executives",
    llm=llm, verbose=True
)

task1 = Task(
    description=f"Research the company '{company}'. Find: founding year, CEO, revenue, main products, market position",
    expected_output="Detailed bullet point report about the company",
    agent=research_agent
)

task2 = Task(
    description=f"Find top 3 competitors of '{company}'. For each: name, revenue, key products, main strength",
    expected_output="Structured competitor analysis report",
    agent=competitor_agent
)

task3 = Task(
    description=f"Analyze '{company}' market position. Find 3 opportunities, 3 threats, overall market trends",
    expected_output="Strategic market analysis with opportunities and threats",
    agent=analysis_agent
)

task4 = Task(
    description=f"""Create Executive Intelligence Report for '{company}' using all research above:
    1. Executive Summary
    2. Company Overview  
    3. Top 3 Competitors
    4. Market Opportunities
    5. Key Threats
    6. Strategic Recommendations""",
    expected_output="Complete professional Executive Intelligence Report",
    agent=report_agent,
    context=[task1, task2, task3]
)

crew = Crew(
    agents=[research_agent, competitor_agent, analysis_agent, report_agent],
    tasks=[task1, task2, task3, task4],
    verbose=True
)

print(f"\n🚀 Starting Multi-Agent Analysis for {company}...\n")
result = crew.kickoff()

filename = f"output/{company.lower().replace(' ', '_')}_report.txt"
with open(filename, "w") as f:
    f.write(str(result))

print(f"\n✅ COMPLETE! Report saved to {filename}")