import asyncio
from openreward import AsyncOpenReward


async def test_locally():
    print("=== Starting Secretary Environment Smoke Test ===\n")

    client = AsyncOpenReward()

    # Connect to local server
    env = client.environments.get(
        name="secretary",
        base_url="http://localhost:8080"
    )

    # Get tasks
    print("Fetching tasks...")
    tasks = await env.list_tasks(split="train")
    print(f"Found {len(tasks)} tasks\n")

    example_task = tasks[0]
    print(f"Testing with task: {example_task}\n")

    # Test with session
    async with env.session(task=example_task) as session:
        # Test prompt generation
        print("Getting prompt...")
        prompt = await session.get_prompt()
        print(f"Prompt:\n{prompt[0].text}\n")
        print("-" * 80)

        # Test skip tool
        print("\nCalling skip()...")
        result = await session.call_tool("skip", {})
        print(f"Output: {result.blocks[0].text}")
        print(f"Reward: {result.reward}")
        print(f"Finished: {result.finished}")
        print("-" * 80)

        # Test accept tool
        print("\nCalling accept()...")
        result = await session.call_tool("accept", {})
        print(f"Output: {result.blocks[0].text}")
        print(f"Reward: {result.reward}")
        print(f"Finished: {result.finished}")
        print("-" * 80)

    print("\n=== Smoke test PASSED ===")


if __name__ == "__main__":
    asyncio.run(test_locally())
