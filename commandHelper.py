import asyncio
import uuid
import subprocess

from openai.types.responses import ResponseContentPartDoneEvent, ResponseTextDeltaEvent

from agents import Agent, function_tool, RawResponsesStreamEvent, Runner, TResponseInputItem, trace, input_guardrail


@function_tool
def runCommands(singleCommand: str) -> str:
    process = subprocess.Popen(
        singleCommand,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    
    outputLines = []
    
    for line in iter(process.stdout.readline, ''):
        print(line, end='')
        outputLines.append(line)
        
    process.stdout.close()
    process.wait()
    
    return ''.join(outputLines)


commandRunnerAgent = Agent(
    name="commandRunnerAgent",
    instructions=(
        "Make commands from the steps given to you. And run them in the right order using your tool"
    ),
    tools=[runCommands],
)


breakDownGoalAgent = Agent(
    name="commandAgent",
    instructions=(
        "Break the goal down into steps which can be completed in one command. You don't generate the commands itself"
        "When breaking down a write a file or create a file with ... content. never let it be a step to open a editor, like nano or vim. just say write to the file or smth"
    ),
)


async def main():
    goal = input("terminal goal: ")
    
    with trace("Command Helper"):
        stepsResult = await Runner.run(
            breakDownGoalAgent,
            goal,
        )
        print("Steps are created")
        
        stepsData = stepsResult.final_output if hasattr(stepsResult, 'final_output') else stepsResult

        print("Gebruik stepsData:", stepsData)

        commandRunResults = await Runner.run(
            commandRunnerAgent,
            stepsData,
        )

        print("Task completed!")

if __name__ == "__main__":
    asyncio.run(main())