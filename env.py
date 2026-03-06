from openreward.environments import Environment, JSONObject, ToolOutput, TextBlock, tool
from pydantic import BaseModel
from typing import List
import textarena as ta


class TaskSpec(BaseModel):
    id: str
    env_id: str
    seed: int
    variant: str


class AcceptParams(BaseModel, extra="forbid"):
    pass


class SkipParams(BaseModel, extra="forbid"):
    pass


class SecretaryEnvironment(Environment):
    VARIANTS = [
        "Secretary-v0",
        "Secretary-v0-long",
        "Secretary-v0-long-raw",
        "Secretary-v0-long-train",
        "Secretary-v0-raw",
        "Secretary-v0-train"
    ]

    def __init__(self, task_spec: JSONObject, secrets: dict[str, str] = {}) -> None:
        super().__init__(task_spec)
        self.config = TaskSpec.model_validate(task_spec)

        # Initialize TextArena environment
        self.ta_env = ta.make(env_id=self.config.env_id)
        self.game_done = False

    NUM_TASKS_PER_VARIANT = 50

    @classmethod
    def list_splits(cls) -> list[str]:
        return ["train", "test"]

    @classmethod
    def list_tasks(cls, split: str) -> list[JSONObject]:
        tasks = []
        for variant_id in cls.VARIANTS:
            for seed_idx in range(cls.NUM_TASKS_PER_VARIANT):
                seed = seed_idx if split == "train" else seed_idx + 10000
                tasks.append({
                    "id": f"{variant_id}_seed{seed}",
                    "env_id": variant_id,
                    "seed": seed,
                    "variant": variant_id,
                })
        return tasks

    async def get_prompt(self) -> List[TextBlock]:
        self.ta_env.reset(num_players=1, seed=self.config.seed)
        _, observation = self.ta_env.get_observation()
        obs_text = observation if isinstance(observation, str) else str(observation)
        prompt = (
            "You are playing the Secretary Problem game.\n\n"
            "You are interviewing candidates one at a time. After seeing each candidate, "
            "you must decide whether to hire them (accept) or pass on them (skip) and continue "
            "to the next candidate. Once you skip a candidate, you cannot return to them.\n\n"
            "Your goal is to hire the best candidate from the pool.\n\n"
            f"{obs_text}\n\n"
            "Use the 'accept' tool to hire the current candidate, or the 'skip' tool to pass "
            "and see the next candidate."
        )
        return [TextBlock(text=prompt)]

    def _execute_action(self, action_str: str) -> ToolOutput:
        """Execute action and return ToolOutput"""
        if self.game_done:
            return ToolOutput(
                blocks=[TextBlock(text="Game is already over.")],
                metadata={"error": "game_finished"},
                reward=0.0,
                finished=True,
            )

        done, info = self.ta_env.step(action=action_str)

        if done:
            self.game_done = True
            rewards, game_info = self.ta_env.close()
            raw_reward = rewards.get(0, 0.0) if isinstance(rewards, dict) else float(rewards)
            reward = float(raw_reward)

            _, observation = self.ta_env.get_observation()
            obs_text = observation if isinstance(observation, str) else str(observation)

            summary = f"Game Over! Reward: {reward:.2f}\n\n{obs_text}"
            return ToolOutput(
                blocks=[TextBlock(text=summary)],
                metadata={"reward": reward},
                reward=reward,
                finished=True,
            )

        _, observation = self.ta_env.get_observation()
        obs_text = observation if isinstance(observation, str) else str(observation)
        return ToolOutput(
            blocks=[TextBlock(text=obs_text)],
            metadata={},
            reward=0.0,
            finished=False,
        )

    @tool
    async def accept(self, params: AcceptParams) -> ToolOutput:
        """Accept and hire the current candidate"""
        return self._execute_action("[accept]")

    @tool
    async def skip(self, params: SkipParams) -> ToolOutput:
        """Skip the current candidate and continue to the next one"""
        return self._execute_action("[continue]")
