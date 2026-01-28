# Concert Booking Agent 🎵

An intelligent concert booking assistant built with **LangChain**, **AWS Bedrock (Claude 3 Sonnet)**, featuring semantic guardrails and trajectory evaluation for enhanced safety and performance.

## ✨ Features

### Core Functionality
- **Concert Search**: Find concerts by artist, city, or date
- **Venue Management**: Check venue availability and details
- **Ticket Pricing**: Get detailed pricing information for different ticket tiers
- **Booking System**: Book concert tickets with seat selection
- **Artist Information**: Access comprehensive artist bios, genres, and discographies
- **Date Availability**: Check concerts on specific dates

### Advanced Features
- **🛡️ Semantic Guardrails**: Uses SentenceTransformers to block off-topic queries
- **📊 Trajectory Evaluation**: LLM-as-judge evaluation with AgentEvals
- **📈 Langfuse Integration**: Full observability and tracing
- **⚡ AWS Bedrock**: Powered by Claude 3 Sonnet for intelligent responses

## 🏗️ Architecture

```
┌─────────────┐
│    User     │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│   Guardrails Layer              │
│   (Sentence Transformers)       │
│   - Semantic similarity check   │
│   - Blocks off-topic queries    │
└──────┬──────────────────────────┘
       │ (passes guardrails)
       ▼
┌─────────────────────────────────┐
│   Concert Booking Agent         │
│   (LangChain + AWS Bedrock)     │
│   - Claude 3 Sonnet             │
│   - Tool calling                │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│   Concert Tools                 │
│   - search_concerts             │
│   - book_concert_tickets        │
│   - get_ticket_prices           │
│   - check_venue_availability    │
│   - get_artist_info             │
│   - check_date_availability     │
└─────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│   Observability                 │
│   - Langfuse (tracing)          │
│   - Trajectory Evaluation       │
└─────────────────────────────────┘
```

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- AWS Account with Bedrock access
- Langfuse account (optional, for observability)

### Setup

1. **Clone the repository**
```bash
cd "Week 6/Task 1"
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
Create a `.env` file:
```env
# AWS Configuration
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0

# Langfuse Configuration (Optional)
LANGFUSE_PUBLIC_KEY=your_public_key
LANGFUSE_SECRET_KEY=your_secret_key
LANGFUSE_HOST=https://cloud.langfuse.com
```

## ⚙️ Configuration

### Guardrails Settings

The guardrails system uses semantic similarity to determine if queries are in-scope.

**Adjust threshold in code:**
```python
agent = create_bedrock_agent(
    use_guardrails=True,
    guardrail_threshold=0.60  # Lower = stricter, Higher = more lenient
)
```

**Threshold guidelines:**
- `0.70+`: Very lenient (may allow some off-topic queries)
- `0.60`: Balanced (recommended)
- `0.50-`: Very strict (may block some valid queries)

### Trajectory Evaluation

Enable trajectory evaluation to assess agent reasoning quality:
```python
agent = create_bedrock_agent(
    use_guardrails=True,
    use_trajectory_eval=True  # Enable LLM-as-judge evaluation
)
```

## 🚀 Usage

### Interactive Mode

Run the agent in interactive mode:
```bash
python concert_booking_agent.py
```

### Example Queries

**✅ In-Scope Queries (Allowed):**
```
"Show me concerts by Taylor Swift"
"What are ticket prices in New York?"
"Tell me about Coldplay"
"Book 2 tickets for Ed Sheeran concert on 2026-05-10"
"Check venue availability at Madison Square Garden"
"What concerts are available on 2026-03-15?"
```

**❌ Out-of-Scope Queries (Blocked):**
```
"What are today's news headlines?"
"Write Python code for me"
"Tell me a joke"
"What's the weather?"
"Solve this math problem"
```

### Programmatic Usage

```python
from concert_booking_agent import create_bedrock_agent

# Create agent
agent = create_bedrock_agent(
    use_guardrails=True,
    use_trajectory_eval=True
)

# Process query
response = agent.process_query("Show me concerts by Taylor Swift")
print(response)
```

## 🛡️ Guardrails

### How It Works

The guardrails system uses **SentenceTransformers** (`all-mpnet-base-v2` model) to compute semantic similarity between user queries and allowed intents.

**Allowed Intents:**
- book concert ticket
- find concert details
- venue info for a concert
- search for concerts
- check venue availability
- get ticket prices
- artist information
- upcoming concerts
- concert dates
- live music events
- concert booking
- ticket availability
- greetings (Hi, Hello, Hey)

### Guardrails Flow

```
User Query → Encode with SentenceTransformer
              ↓
         Compare with allowed intents (cosine similarity)
              ↓
         Score >= threshold?
         ├─ Yes → Process with agent
         └─ No  → Block with message
```

### Customizing Allowed Intents

Edit `guardrails_integration.py`:
```python
self.allowed_intents = [
    "book concert ticket",
    "find concert details",
    # Add your custom intents here
]
```

## 📊 Evaluation

### Trajectory Evaluation with AgentEvals

The agent supports **LLM-as-judge** evaluation using the `agentevals` library:

```python
from agentevals.trajectory.llm import create_trajectory_llm_as_judge, TRAJECTORY_ACCURACY_PROMPT

# Create evaluator
evaluator = create_trajectory_llm_as_judge(
    model="openai:gpt-4o",  # or "bedrock:claude-3-sonnet"
    prompt=TRAJECTORY_ACCURACY_PROMPT,
)

# Evaluate trajectory
evaluation = evaluator(outputs=result["messages"])
# Returns: {'key': 'trajectory_accuracy', 'score': True/False, 'comment': '...'}
```

**Evaluation Output:**
- `score`: Boolean indicating if trajectory is reasonable
- `comment`: Detailed explanation from the judge
- `key`: Type of evaluation (`trajectory_accuracy`)

## 📁 Project Structure

```
Task 1/
├── concert_booking_agent.py    # Main agent implementation
├── concert_tools.py            # LangChain tools for concert operations
├── guardrails_integration.py   # Semantic guardrails system
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .env                        # Environment variables (not in git)
└── .venv/                      # Virtual environment
```

## 🔧 Available Tools

### 1. search_concerts
Search for concerts by artist, city, or date.
```python
search_concerts(artist="Taylor Swift", city="New York", date="2026-03-15")
```

### 2. check_venue_availability
Check if a venue is available on a specific date.
```python
check_venue_availability(venue_name="Madison Square Garden", date="2026-03-15")
```

### 3. get_ticket_prices
Get ticket prices for an artist's concert.
```python
get_ticket_prices(artist="Coldplay")
```

### 4. book_concert_tickets
Book tickets for a concert.
```python
book_concert_tickets(
    artist="Ed Sheeran",
    date="2026-05-10",
    num_tickets=2,
    ticket_type="standard"
)
```

### 5. get_artist_info
Get artist biography, genre, and albums.
```python
get_artist_info(artist_name="The Weeknd")
```

### 6. check_date_availability
Check concerts on a specific date.
```python
check_date_availability(date="2026-04-20", city="Los Angeles")
```

## 💡 Examples

### Example 1: Search and Book
```
You: Show me Taylor Swift concerts

Agent: Found 1 concert(s):

🎵 Taylor Swift
   📍 Venue: Madison Square Garden, New York
   📅 Date: 2026-03-15
   🎫 Available Tickets: 500
   💰 Price Range: $75 - $500

You: Book 2 standard tickets for that concert

Agent: Booking Confirmed!

Booking ID: BK120260128153045
Artist: Taylor Swift
Venue: Madison Square Garden, New York
Date: 2026-03-15
Tickets: 2 x Standard ($150 each)
Total Amount: $300

Your tickets will be sent to your email. Enjoy the show!
```

### Example 2: Guardrails Block
```
You: What's the weather today?

[GUARDRAILS] Running guardrails check...
[GUARDRAILS] Similarity score: 0.245 (threshold: 0.60)
[GUARDRAILS] Blocked out-of-scope query

Agent: I'm a concert booking assistant and can only help with concert-related queries.
```

## 📈 Observability

### Langfuse Integration

The agent automatically traces all interactions to Langfuse:

1. **View traces**: https://cloud.langfuse.com
2. **Monitor performance**: Response times, token usage
3. **Debug issues**: Full conversation history and tool calls
4. **Track costs**: Token consumption per query

### Trajectory Evaluation Logs

When trajectory evaluation is enabled:
```
[TRAJECTORY EVAL] Score: True
[TRAJECTORY EVAL] The provided agent trajectory is reasonable and demonstrates...
```

## 🐛 Troubleshooting

### Issue: Model download on first run
**Solution**: SentenceTransformers downloads a 438MB model on first use. This is normal and only happens once.

### Issue: Guardrails not blocking off-topic queries
**Solutions:**
- Lower the threshold: `guardrail_threshold=0.50`
- Check similarity scores in console output
- Add more specific intents to allowed list

### Issue: Agent not responding
**Solutions:**
- Verify AWS credentials in `.env`
- Check Bedrock model access in AWS Console
- Ensure Claude 3 Sonnet access is enabled

### Issue: ImportError for agentevals
**Solution**: Trajectory evaluation is optional. If not needed:
```python
agent = create_bedrock_agent(use_trajectory_eval=False)
```

### Issue: Langfuse connection errors
**Solution**: Langfuse is optional. Check credentials or disable by removing from code.

## 🗄️ Mock Database

The current implementation uses a mock database with 5 sample concerts:
- Taylor Swift - Madison Square Garden, New York (2026-03-15)
- Coldplay - Hollywood Bowl, Los Angeles (2026-04-20)
- Ed Sheeran - The O2 Arena, London (2026-05-10)
- The Weeknd - United Center, Chicago (2026-06-05)
- Billie Eilish - Staples Center, Los Angeles (2026-07-12)

To integrate with a real database, replace the `CONCERTS_DB` in `concert_tools.py`.

## 📝 License

MIT License

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with both in-scope and out-of-scope queries
5. Submit a pull request

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review Langfuse traces for debugging
3. Check guardrails similarity scores in logs

---

**Built with:** LangChain • AWS Bedrock • Claude 3 Sonnet • SentenceTransformers • AgentEvals • Langfuse
