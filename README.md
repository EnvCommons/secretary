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

[MIT](https://github.com/LeonGuertler/TextArena/blob/main/LICENSE).

## Tasks

There are two splits: train (300 tasks) and test (300 tasks). Each split contains 50 tasks across each of 6 variants:

- **Secretary-v0**
- **Secretary-v0-long**
- **Secretary-v0-long-raw**
- **Secretary-v0-long-train**
- **Secretary-v0-raw**
- **Secretary-v0-train**

Each task is seeded for reproducibility.

## Reward Structure

This is a sparse reward environment. The reward is determined by whether the agent successfully selects the best candidate from the pool. Rewards are returned directly from TextArena without mapping.

We do not use LLM graders for this environment; reward is determined programmatically.

## Data

Game state is generated procedurally by the TextArena engine using seeded randomness. No external data files are required.

## Tools

Agents are given two tools:

- `accept()`: Accept and hire the current candidate
- `skip()`: Skip the current candidate and continue to the next one

## Time Horizon

Secretary is a multi-turn environment.

## Environment Difficulty

This environment presents moderate to challenging difficulty, requiring agents to develop threshold-based strategies that balance gathering information with committing to decisions.

## Other Environment Requirements

There are no further environment requirements; Secretary works out of the box without any secrets or API keys.

## Safety

Agents in Secretary interact only with a sequential decision-making game and have no access to external systems, the internet, or sensitive data. The environment does not present safety risks.

## Citations

```bibtex
@software{textarena2024,
  author    = {Guertler, Leon and Banting, Wilfried and Pignatelli, Eduardo},
  title     = {TextArena},
  year      = {2024},
  publisher = {GitHub},
  url       = {https://github.com/LeonGuertler/TextArena}
}
```
