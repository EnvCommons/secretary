# Secretary

[![OpenReward Environment](https://img.shields.io/badge/%E2%AD%90%20OpenReward-Environment-f7e6cc)](https://openreward.ai/GeneralReasoning/Secretary)

## Description

**Secretary** is an environment for evaluating agents on optimal stopping and sequential decision-making under uncertainty. This environment wraps the Secretary implementation from [TextArena](https://github.com/LeonGuertler/TextArena), a framework for text-based game environments.

## Capabilities

- Optimal stopping problem solving
- Sequential decision-making under uncertainty
- Threshold-based strategy development
- Balancing exploration and exploitation

## Compute Requirements

Secretary does not require a sandbox. It has minimal compute requirements.

## License

[MIT](https://opensource.org/licenses/MIT). TextArena itself is also released under MIT.

## Tasks

There are 300 tasks in the `train` split and 300 in `test`. Each split contains 50 tasks for each of 6 TextArena variants (Secretary-v0 variants have 5 candidates, Secretary-v0-long variants have 10):

- **Secretary-v0**
- **Secretary-v0-long**
- **Secretary-v0-long-raw**
- **Secretary-v0-long-train**
- **Secretary-v0-raw**
- **Secretary-v0-train**

Each task is seeded for reproducibility: train uses seeds 0 to 49 and test uses seeds 10000 to 10049.

## Reward Structure

This is a sparse reward environment with a single reward at the end of the game: 1.0 if the accepted candidate is the best in the pool and 0.0 otherwise. If the agent skips every candidate, the last one is accepted automatically. Rewards are returned directly from TextArena without mapping. All intermediate steps have reward 0.

We do not use LLM graders for this environment; reward is determined programmatically.

## Data

Game state is generated procedurally by the TextArena engine using seeded randomness. No external data files are required.

## Tools

Agents are given two tools:

- `accept()`: Accept and hire the current candidate
- `skip()`: Skip the current candidate and continue to the next one

## Time Horizon

Secretary is a multi-turn environment. Each tool call reveals at most one new candidate, so an episode lasts at most 5 or 10 tool calls depending on the variant.

## Other Environment Requirements

There are no further environment requirements; Secretary works out of the box without any secrets or API keys.

## Safety

Agents in Secretary interact only with a sequential decision-making game and have no access to external systems, the internet, or sensitive data. The environment does not present safety risks.

## Citations

```bibtex
@misc{guertler2025textarena,
    title={TextArena},
    author={Leon Guertler and Bobby Cheng and Simon Yu and Bo Liu and Leshem Choshen and Cheston Tan},
    year={2025},
    eprint={2504.11442},
    archivePrefix={arXiv},
    primaryClass={cs.CL},
    url={https://arxiv.org/abs/2504.11442},
}
```
