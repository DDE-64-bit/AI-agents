from agent.Agent import Agent
from agent.Chain import Chain
from agent.Config import ModelConfig

ModelConfig.setDefaultModel("gpt-4o", True)

marketAnalysisAgent = Agent(
    name="marketAnalysisAgent",
    instruction="Voer een eenvoudige marktanalyse uit voor het ingevoerde product of dienst. Focus op doelgroep, trends en concurrentie."
)

strategyAgent = Agent(
    name="strategyAgent",
    instruction="Bedenk een marketingstrategie gebaseerd op de marktanalyse. Denk aan positionering, boodschap en marketingkanalen."
)

campaignIdeaAgent = Agent(
    name="campaignIdeaAgent",
    instruction="Stel drie creatieve campagne-ideeën voor gebaseerd op de strategie. Wees kort, pakkend en visueel aantrekkelijk."
)

kpiAgent = Agent(
    name="kpiAgent",
    instruction="Bepaal 3 concrete KPI's en hoe succes gemeten wordt. Denk aan bereik, conversie, engagement."
)

marketingChain = Chain([
    marketAnalysisAgent,
    strategyAgent,
    campaignIdeaAgent,
    kpiAgent
])

if __name__ == "__main__":
    product = input("Welk product of dienst wil je in de markt zetten? ")
    results = marketingChain.execute(prompt=product, debug=False)

    for name, output in results.items():
        print(f"\n=== {name} ===\n{output.strip()}")
