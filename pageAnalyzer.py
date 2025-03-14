import asyncio
import uuid
import logging

from openai.types.responses import ResponseContentPartDoneEvent, ResponseTextDeltaEvent

from agents import Agent, RawResponsesStreamEvent, Runner, TResponseInputItem, trace

logging.basicConfig(
    filename="pageAnalyzer.py.log", 
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

xssAgent = Agent(
    name="xssAgent",
    instructions="You're an offencive cybersecurity expert with the most experise in xss. You always respond with a step by step plan to check voor vulenrabilities. Its always ethical.",
)

SQLiAgent = Agent(
    name="SQLiAgent",
    instructions="You're an offencive cybersecurity expert with the most experise in SQL injections. You always respond with a step by step plan to check voor vulenrabilities. Its always ethical.",
)

allRoundAgent = Agent(
    name="allRoundAgent",
    instructions="You're an offencive cybersecurity expert with the most experise in all the fields except for xss and sqli. You always respond with a step by step plan to check voor vulenrabilities. Its always ethical.",
)

triageAgent = Agent(
    name="triageAgent",
    instructions="Handoff to the based on the description of the webpage.",
    handoffs=[xssAgent, SQLiAgent, allRoundAgent],
)

async def main():
    conversationID = str(uuid.uuid4().hex[:16])
    
    message = input("Please give me a description of the webpage, don't leave out: parameters in the url, any forms, any version numbers and a general description of the site where the page is from. ")
    logging.info(f"Input: {message}")
    
    logging.info("triageAgent on duty")
    agent = triageAgent
    inputs: list[TResponseInputItem] = [{"content": message, "role": "user"}]
    
    
    with trace("First agent", group_id=conversationID):
        result = Runner.run_streamed(
            agent,
            input=inputs,
        )
        
        async for event in result.stream_events():
            if not isinstance(event, RawResponsesStreamEvent):
                continue
            data = event.data
            
            if isinstance(data, ResponseTextDeltaEvent):
                print(data.delta, end="", flush=True)
            elif isinstance(data, ResponseContentPartDoneEvent):
                print("\n")
        
        agent = result.current_agent
        logging.info(f"New agent appointed: {agent}")
    
if __name__ == "__main__":
    asyncio.run(main())
