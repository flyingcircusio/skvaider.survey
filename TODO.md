# Preparation

* devenv
* [ ] uv / pre-commit / ruff, basedpyright
* pytest
* pyramid, pydantic for lightweight API, config, ... baseline layout
* htmx, hyperscript

* aramaki server code

* [x] github repo

* [ ] milestones
* [ ] github tickets

# Tasks


* [ ] documentation for users and developers


# Design

XXX Overview
* slides inhalte rausziehen
*
## Skvaider

* accept a second (multiple) aramaki server connections
* mode to manage exclusive access temporarily for running isolated loads
* revive ollama integration for local models

## Arena

* generate temporary
* be an aramaki server to the skvaider
* create runs with given parameters to make clear what the identifying:
	* GPU, drivers, model and version, inference engine parameters, skvaider version, ... (likely a nested structure)
* get statistics from skvaider in exclusive mode: how many requests have we seen, parallelism, tokens, ...

* matching model for "this task requires these kinds of models" so we know which models and which combinations to test

* support runs with multiple model slots

## Runner

* dashboard
* locally triggered runs and recorded results
* integration with local runner (github actions style, see codeberg runners?)
* define local runs - integration with some repo, see runner integration
* connecting to a leaderboard
* accepting runs
