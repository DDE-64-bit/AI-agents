from agent.Agent import Agent
from agent.Chain import Chain
from agent.Config import ModelConfig
from agent.Tool import dynamicTool

ModelConfig.setDefaultModel("gpt-4o", True)

@dynamicTool
def simplifyForStakeholders(summary: str):
    return f"Key Takeaways for Stakeholders:\n{summary}"

bulletSummaryAgent = Agent(
    name="bulletSummaryAgent",
    instruction="Summarize the status update in exactly 3 concise bullet points. Use plain language."
)

stakeholderFormatAgent = Agent(
    name="stakeholderFormatAgent",
    instruction="Use the tool to simplify the summary for stakeholders.",
    tools=[simplifyForStakeholders]
)

statusLineAgent = Agent(
    name="statusLineAgent",
    instruction="Add a short status indicator: ✅ On track, ⚠️ At risk, or ⏳ Delayed — based on the tone of the update."
)

statusUpdateChain = Chain([
    bulletSummaryAgent,
    stakeholderFormatAgent,
    statusLineAgent
])

if __name__ == "__main__":
    rawUpdate = """
    The dev team has completed sprint 4, but the QA cycle took longer than expected due to test environment issues. We're 3 days behind schedule, and client feedback is still pending for module 2.
    """
    results = statusUpdateChain.execute(prompt=rawUpdate, debug=False)

    for name, output in results.items():
        print(f"\n=== {name} ===\n{output.strip()}")
