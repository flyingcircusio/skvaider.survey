# Why and what

While developing our AI platform and helping customers and their developers to
implement AI features in their applications we found two interesting
challenges that complement each other:

1. **Model progression**

   Running AI models requires careful management of GPU resources (mostly
   VRAM) and although there are many approaches to optimize the use of VRAM,
   running anything at whatever scale (in our case a small number of GPUs,
   typically around 10) will quickly run in to limits on the number of models
   that can be provided.

   At the same time, new models (or derivations thereof) appear regularly on the market
   and developers want to make use of the newest abilities. We also want to benefit from
   models becoming more capable over time while utilizing GPU compute and memory
   resources more efficiently.

   This requires inference providers to strike a balance between keeping old models available
   and making new models available.

   Predictably, this will lead to sufficient pressure so that old models will need to
   be retired on a regular basis.

   This is further complicated by different flexibilities: embedding models
   likely need a long term commitment as generally the exactly same model
   needs to be used for indexing as for querying. Developers should implement
   model progression when relying models on this way, but at the same time,
   re-indexing millions of documents takes time and is costly, too.

2. **Prompt validation vs. the business value of validation sets**

	Similarly, when evolving an application that uses AI, due to the nature of the
	non-deterministic results developers need to keep an eye on the quality of their
	results while interacting with the the actual models and APIs.

	However, the validation is valuable to businesses and even though
	established AI providers have standardized APIs to upload validation
	sets, this is seen as a substantial business risk of having customers'
	data inadvertently used for training or other purposes that may
	undermine their business in the medium to long term.

Looking at those two challenges, we want to add a suite of two new utilities
to our AI platform, the new suite being called `skvaider.survey` with the
`arena` and `runner` utilities.

The `arena` is intended to be a server that provides a dashboard aggregating the provider
perspective. The `runner` is intended to be installed easily by customers and allows

The `arena` server is shall be connected to runners to:

* register known evaluations (runs) from the runners
* trigger runs by providing temporary end
* collect results from runs (triggered or sent freely)
* keep statistics about results from triggers about parameters as well as quality and speed of the results
* provide public and private dashboards

The `runner` shall be a daemon for developers, that:

* is easy to install and configure
* allows developers to register arbitrary code running their evaluations
* connects to one or more arena servers
* provides a local dashboard of the known evaluations and the history of runs
* allows manually triggering runs with known credentials
* accepts triggers from the `arena` with temporary credentials

# Challenges

## Define evaluation parameters and results

Evaluations run as a provider need to track a number of input variables to be
able to later make sense of the results, this includes: model identity (name,
source, version/hash, derivation parameters, ...), inference environment (GPU
hardware, drivers, engine, engine version), model configuration/engine
parameters (cache size, data types, kernels, OS version, ...), skvaider
version, ...

Similarly the output need to be defined but simple, we initially think that
for every evaluation from a single runner we record: number of individual
tests, successes, failures (unexpected result), errors (technical issues) and
response times (per test?)

In addition, we'd like to track the experiment on the skvaider proxy side so
we can later fuse this with the report from the runner: tokens in/out, number
of requests seen, models used, parallel requests, timings (histograms?)

## Trust in results

We need to ensure the trustworthiness of the results. Compared to the
architectures from vendors that provide a standardized API and see all the
expected/actual results we only retrieve summarized data that could easily be
forged.

Considering that we can track the experiment partially on the skvaider side,
we may be able to detect outliers and flag issues.

This also means we may need to be able to redact statistics retroactively if
we notice that a certain client may have been malicious.

## Multi-model tasks

Customers are expected to go beyond simple A/B input/output tasks and validate
more complex flows that may involve tasks from different models at once.

This means we need to a) define sufficient metadata for each task which kinds
of models it accepts and b) consider running "matrix style" evaluations for
different combinations of models on the same task.

## Model progression tasks

Embedding models may want to compare numerical stability of the outputs of one
model to that of another model. This could integrate with the multi-model /
matrix concept or warrant investigating an additional approach.

# Implementation details

Generally our stack uses:

* modern Python (3.14+)
* asyncio instead of threads for application code (webservers running threads are fine)
* SQLAlchemy+Alembic (we'll start with sqlite and can move to PostgreSQL as needed)
* Pydantic to parse models on IO boundaries into properly typed structures from toml or json
* Pyramid as a webserver with bootstrap, HTMX, and Hyperscript for the UI.
* Aramaki as a way to implement this as a federated system.

## Skvaider

Our inference serving platform `skvaider` will need to grow two new abilities:

* accept a second aramaki connection to manage temporary credentials
* allow to quiesce competing access so that evaluations can run without noisy neighbours
* ability to track experiment metadata: number of requests, which endpoints, timings, errors, tokens, model, ...
* revive llama-cpp integration for local models during development

## Arena

* be an aramaki server that passes out information about temporary credentials and experiments to skvaider
* a public dashboard that anonymizes the statistics and status
* a private operations backend to manage runners, manage evaluations

## Runner

* Use a GitHub-Action-style approach, letting customers register a number of repositories that contain action definitions.
* We likely want to build on top of something like Forgejo Actions.
* interlink the local dashboard with the relevant public dashboard where applicable
