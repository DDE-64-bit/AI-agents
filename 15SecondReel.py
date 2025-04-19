from agent.Agent import Agent
from agent.Chain import Chain
from agent.Config import ModelConfig

ModelConfig.setDefaultModel("gpt-4o", True)

reelConceptAgent = Agent(
    name="reelConceptAgent",
    instruction="You generate 3 creative reel ideas for the city. Focus on visual punch and vibe. Keep it under 10 words per idea."
)

captionAgent = Agent(
    name="captionAgent",
    instruction="You write 3 short, catchy captions that match each reel idea. Keep each under 10 words."
)

shotListAgent = Agent(
    name="shotListAgent",
    instruction="You give 3 quick bullet points per reel idea with shots to film. Be concise and specific (e.g. skyline, coffee shop, street artist)."
)

travelReelChain = Chain([
    reelConceptAgent,
    captionAgent,
    shotListAgent
])

if __name__ == "__main__":
    #city = "Lisbon"
    city = input("City: ")
    results = travelReelChain.execute(prompt=city, debug=False)

    for name, output in results.items():
        print(f"\n=== {name} ===\n{output.strip()}")
