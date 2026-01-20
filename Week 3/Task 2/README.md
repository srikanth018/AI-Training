
# AI-Powered Request Classification & Email Routing (n8n)

This project demonstrates an **AI-powered request classification and email routing system** built using **n8n**, **Groq LLM (LLaMA 3.3-7B-Versatile)**, and an **HTTP Request tool**.
The workflow classifies incoming user queries, determines the appropriate recipient role (**Customer** or **Admin**), fetches users dynamically from an external API, and routes emails accordingly.

---

## Use Case Overview

Organizations receive different types of user queries such as:

* Billing issues
* Product questions
* System outages
* Security incidents

This workflow automates:

1. **Intent classification**
2. **Role-based routing**
3. **Recipient discovery via API**
4. **Email dispatch**

---

## Classification Logic

### Customer Queries → Role: `CUSTOMER`

* Product Inquiry
* General Support
* Sales Question
* Billing Inquiry
* Feature Request

**Example**

> “I was charged twice for this month's subscription. Can someone from billing review my account and process a refund?”

---

### Admin Queries → Role: `ADMIN`

* Technical Escalation
* System Issue
* Security Concern
* Data Issue
* Integration Problem

**Example**

> “URGENT: Our API integration is down and affecting production systems.”

---

## Workflow Architecture

### n8n Nodes Used

1. **When Chat Message Received**

   * Entry point for user queries

2. **AI Agent**

   * Uses Groq LLM for classification
   * Enforces strict system prompt rules
   * Calls HTTP tool mandatorily

3. **HTTP Request (Tool)**

   * Fetches users dynamically
   * Endpoint:

     ```
     GET https://api.escuelajs.co/api/v1/users
     ```

4. **JSON Parser / Function**

   * Parses AI output
   * Filters users by role

5. **Send Message (Gmail)**

   * Sends email to all matched recipients

6. **Edit Fields**

   * Allows manual review or enrichment

---

## Model Configuration

* **Provider:** Groq
* **Model:** `llama-3.3-7b-versatile`
* **Reason:** Fast, cost-effective, and reliable for structured classification tasks

---

## System Prompt (Core Logic)

The AI Agent is strictly guided by a system prompt that enforces:

* Single category & role selection
* Mandatory HTTP tool usage
* No hallucinated users
* JSON-only output

<details>
<summary><strong>Click to view System Prompt</strong></summary>

```
You are an AI-powered request classification and routing assistant.

STEP 1 — Classification
Analyze the user's input query and classify it into exactly ONE category and ONE role.

Customer Queries (Role: CUSTOMER):
- Product Inquiry
- General Support
- Sales Question
- Billing Inquiry
- Feature Request

Admin Queries (Role: ADMIN):
- Technical Escalation
- System Issue
- Security Concern
- Data Issue
- Integration Problem

STEP 2 — Fetch Users (MANDATORY TOOL USAGE)
Use HTTP Request tool:
- Method: GET
- URL: https://api.escuelajs.co/api/v1/users

STEP 3 — Recipient Filtering
Select only users whose "role" matches the classified role.

STEP 4 — Output
Return a single valid JSON object with classification and recipients.
```

</details>

---

## Output Format (Strict JSON)

```json
{
  "role": "CUSTOMER",
  "category": "Billing Inquiry",
  "email_subject": "Duplicate Subscription Charge - Refund Request",
  "email_priority": "HIGH",
  "summary": "User was charged twice for this month's subscription and requests a refund.",
  "recipients": [
    {
      "id": 1,
      "name": "John",
      "email": "john@mail.com",
      "role": "customer"
    }
  ]
}
```