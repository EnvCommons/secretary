import asyncio
import json
import os
from openai import AsyncOpenAI
from openreward import AsyncOpenReward


async def test_with_openai():
    or_client = AsyncOpenReward()
    oai_client = AsyncOpenAI()

    MODEL_NAME = "gpt-5.2"
    ENV_NAME = "secretary"
    SPLIT = "train"
    BASE_URL = "http://localhost:8080"

    environment = or_client.environments.get(name=ENV_NAME, base_url=BASE_URL)
    tasks = await environment.list_tasks(split=SPLIT)
    tools = await environment.list_tools(format="openai")

    print(f"Found {len(tasks)} tasks")
    print(f"Testing with model: {MODEL_NAME}\n")

    for task in tasks[:3]:  # Test first 3 tasks
        print(f"\n{'='*80}")
        print(f"Testing task: {task['id']} (variant: {task['variant']}, seed: {task['seed']})")
        print(f"{'='*80}\n")

        async with environment.session(task=task) as session:
            prompt = await session.get_prompt()
            input_list = [{"role": "user", "content": prompt[0].text}]
            finished = False
            step = 0

            while not finished and step < 20:  # Max 20 steps
                step += 1
                print(f"\n--- Step {step} ---")

                # Use responses.create(), NOT chat.completions.create()
                response = await oai_client.responses.create(
                    model=MODEL_NAME,
                    tools=tools,
                    input=input_list
                )

                # Response has 'output', NOT 'choices'
                input_list += response.output

                for item in response.output:
                    if item.type == "function_call":
                        tool_result = await session.call_tool(
                            item.name,
                            json.loads(str(item.arguments)) if item.arguments else {}
                        )

                        finished = tool_result.finished

                        input_list.append({
                            "type": "function_call_output",
                            "call_id": item.call_id,
                            "output": tool_result.blocks[0].text
                        })

                        print(f"Tool: {item.name}()")
                        print(f"Reward: {tool_result.reward:.3f}")
                        print(f"Finished: {tool_result.finished}")

                        if tool_result.finished:
                            print(f"\n{'='*80}")
                            print(f"TASK FINISHED! Final reward: {tool_result.reward:.3f}")
                            print(f"{'='*80}")
                            break

    print("\n=== Agent test completed ===")


if __name__ == "__main__":
    asyncio.run(test_with_openai())
