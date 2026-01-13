# AI Model Comparison Sheet

### Models Evaluated

* **GPT-4o (OpenAI)**
* **Claude Sonnet (Anthropic)**
* **Gemini Flash (Google)**
* **DeepSeek-R1:7B (Local model via Ollama)**

### Evaluation Criteria

Each model was evaluated using the same prompts across the following use cases:

* Code Generation (Application Development)
* SQL Generation
* Infrastructure Automation (Scripts)
* Ease of Use

Ratings are expressed using qualitative indicators:

* **Excellent**
* **Good**
* **Basic**
* **Not Supported**

Response time indicates the approximate time taken to generate the first usable response.

---

## Prompt 1: Code Generation (Application Development)

**Prompt Used**

> Create a REST API in Python (FastAPI) with JWT authentication and PostgreSQL integration.
> Include folder structure and error handling.
> Also provide time taken to generate this response at the end.

| Model                   | Code Quality | Response Time | Comments                                                                                                                                 |
| ----------------------- | ------------ | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| GPT-4o                  | Good         | ~15 sec       | Provided code for a simple login and register application with basic logic. Useful for learning purposes but not fully production-ready. |
| Claude Sonnet           | Excellent    | ~45 sec       | Generated a complete project with folder structure and production-ready patterns. Covered all major HTTP methods.                        |
| Gemini Flash            | Basic        | ~5 sec        | Output was very minimal and required significant rework. Included a reference YouTube video for further learning.                        |
| DeepSeek-R1:7B (Ollama) | Basic        | ~10 sec       | Provided very basic code with excessive explanation. Did not fully understand or implement all prompt requirements.                      |

---

## Prompt 2: SQL Generation (Data Analysis)

**Prompt Used**

> Write an optimized PostgreSQL query to find the top 3 customers by total purchase amount in the last 6 months.
> Tables: customers, orders, order_items.
> Also provide time taken to generate this response at the end.

| Model                   | Code Quality | Response Time | Comments                                                                                             |
| ----------------------- | ------------ | ------------- | ---------------------------------------------------------------------------------------------------- |
| GPT-4o                  | Excellent    | ~4 sec        | Generated an optimized SQL query and explicitly addressed edge cases and performance considerations. |
| Claude Sonnet           | Excellent    | ~8 sec        | Provided a clean and optimized query with proper joins and aggregation logic.                        |
| Gemini Flash            | Good         | ~3 sec        | Suggested optimization strategies but did not provide a fully optimized final SQL query.             |
| DeepSeek-R1:7B (Ollama) | Good         | ~13 sec       | Correct query logic but included excessive explanations and exposed internal reasoning steps.        |

---

## Prompt 3: Infrastructure Automation (DevOps Scripts)

**Prompt Used**

> Create a GitHub Actions workflow to:
>
> * Build a Docker image
> * Run unit tests
> * Push image to Docker Hub
> * Trigger on push to main branch
>   Also provide time taken to generate this response at the end.

| Model                   | Code Quality  | Response Time | Comments                                                                                             |
| ----------------------- | ------------- | ------------- | ---------------------------------------------------------------------------------------------------- |
| GPT-4o                  | Excellent     | ~30 sec       | Provided a complete workflow with enhancement suggestions and best practices.                        |
| Claude Sonnet           | Excellent     | ~8 sec        | Delivered a clean and production-ready YAML file with clear placeholders for environment variables.  |
| Gemini Flash            | Excellent     | ~2 sec        | Generated working workflow quickly with helpful explanations of key components, useful for learning. |
| DeepSeek-R1:7B (Ollama) | Not Supported | ~8 sec        | Output included excessive reasoning text and incomplete YAML. Required significant manual rework.    |

---

## Use Case 4: Ease of Use

This category evaluates clarity of responses, structure, verbosity, and developer experience.

| Model                   | Ease of Use | Comments                                                                                                |
| ----------------------- | ----------- | ------------------------------------------------------------------------------------------------------- |
| GPT-4o                  | Excellent   | Provides clear explanations along with optimization techniques, balancing depth and clarity.            |
| Claude Sonnet           | Excellent   | Organizes output into well-structured files with detailed explanations, ideal for production workflows. |
| Gemini Flash            | Good        | Very fast and concise responses, suitable for quick references but sometimes lacks depth.               |
| DeepSeek-R1:7B (Ollama) | Basic       | Excessive explanations and reasoning output reduce usability for day-to-day development.                |


