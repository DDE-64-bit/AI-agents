from agent.Agent import Agent
from agent.Chain import Chain
from agent.Config import ModelConfig

ModelConfig.setDefaultModel("gpt-4o", True)

brandPersonaAgent = Agent(
    name="brandPersonaAgent",
    instruction="You describe the brand's voice and personality based on the product. Be clear and concise. Use 3 bullet points max."
)

visualIdentityAgent = Agent(
    name="visualIdentityAgent",
    instruction="Based on the brand personality, suggest visual identity traits: color palette, logo style, typography vibe. Answer in 3 bullet points."
)

sloganAgent = Agent(
    name="sloganAgent",
    instruction="Create 3 original, catchy slogans that reflect the product and brand voice. Keep each under 8 words."
)

brandLaunchAgent = Agent(
    name="brandLaunchAgent",
    instruction="Create a checklist of 3 key things to prepare before launching this brand. Be practical and high-impact."
)

brandingKitChain = Chain([
    brandPersonaAgent,
    visualIdentityAgent,
    sloganAgent,
    brandLaunchAgent
])

if __name__ == "__main__":
    #product = "a backpack from recycled materials"
    product = input("product: ")
    results = brandingKitChain.execute(prompt=product, debug=False)

    for name, output in results.items():
        print(f"\n=== {name} ===\n{output.strip()}")
