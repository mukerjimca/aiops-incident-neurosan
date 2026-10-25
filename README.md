# 🛠️ AIOps Incident Copilot – Neuro SAN Multi-Agent Network

> **Agentic AI Hackathon – Build with Neuro® AI Multi-Agent Accelerator | Track 2: Vibe Coding + Grounding**

A **multi-agent AIOps copilot** built on [Neuro SAN Studio](https://github.com/cognizant-ai-lab/neuro-san-studio).
You describe an IT incident or alert in plain English. A team of AI agents then:

1. **Triages** it (severity P1–P4, category, impacted server from the CMDB)
2. Finds the **probable root cause** by matching past incidents
3. Recommends **fix steps from an approved runbook library**
4. **Validates** the plan for safety, with **human-in-the-loop** approval for risky production changes

All answers are **grounded** on a local knowledge base through Python coded tools, so the agents do **not** make up servers, commands or fixes.

> ⚠️ Uses **synthetic sample data only**. No client data and no API keys are included in this repo.

---

## 🎯 Problem Statement

When an alert fires (often at night), L1/L2 engineers spend a lot of time:
- working out how critical the affected server is
- searching old tickets for similar issues
- finding the correct runbook
- deciding whether a change needs approval

This slows down **MTTR (Mean Time To Resolve)**. Plain LLM chatbots can also **hallucinate** unsafe commands.

## 💡 Solution

A team of 5 specialised agents that work together like a real incident response team.
The agents use only company-approved data (CMDB, incident history, runbooks), and a validation agent checks every plan before it reaches the engineer.

---

## 🧩 Agent Network Architecture

```
                    ┌──────────────────────────┐
     User  ───────► │   incident_commander     │  (front-man / orchestrator)
                    └────────────┬─────────────┘
         ┌───────────────┬───────┴───────┬──────────────────┐
         ▼               ▼               ▼                  ▼
   triage_agent      rca_agent    remediation_agent   validation_agent
         │               │               │            (APPROVE / NEEDS HUMAN
         ▼               ▼               ▼             APPROVAL / REJECT)
   cmdb_lookup   incident_history   runbook_lookup
  (coded tool)   _search (tool)     (coded tool)
         │               │               │
         ▼               ▼               ▼
     cmdb.json   incident_history.json  runbooks.json
```

| Agent | Role |
|---|---|
| **incident_commander** | Orchestrator. Delegates to the specialist agents and returns the final structured report |
| **triage_agent** | Sets severity (P1–P4) and category, and looks up the server in the CMDB |
| **rca_agent** | Finds the probable root cause from similar past incidents, with a confidence level |
| **remediation_agent** | Returns step-by-step fix actions from an approved runbook only |
| **validation_agent** | Safety and change-control check: APPROVE / NEEDS HUMAN APPROVAL / REJECT |

| Coded Tool (Python) | Grounding data |
|---|---|
| `cmdb_lookup` | `cmdb.json`: servers, environment, criticality, owner |
| `incident_history_search` | `incident_history.json`: past incidents and root causes |
| `runbook_lookup` | `runbooks.json`: approved fix steps, risk, change-request flag |

---

## ✨ Key Features

- **Multi-agent orchestration** using Neuro SAN's data-driven HOCON configuration
- **Grounding / RAG-style lookup** through Python Coded Tools, with no hallucinated fixes
- **Human-in-the-loop safety**: production and high-risk changes always need approval
- **Explainable output**: shows the CI details, matching past incident IDs and runbook ID
- **Safe fallback**: if no runbook matches, it says *"escalate to L3"* instead of guessing

---

## 📁 Repository Structure

```
registries/
  └── aiops_incident_copilot.hocon        # Agent network definition
coded_tools/
  └── aiops_incident_copilot/
        ├── kb_tools.py                   # Coded tools (CMDB, history, runbook lookup)
        └── data/
              ├── cmdb.json
              ├── incident_history.json
              └── runbooks.json
README.md
```

---

## 🚀 How to Run

**Prerequisites:** Python 3.12+, [uv](https://docs.astral.sh/uv/), and a Google Gemini API key (free from Google AI Studio).

```powershell
# 1. Create project and install Neuro SAN Studio
uv venv --python 3.12
.venv\Scripts\activate          # Linux/Mac: source .venv/bin/activate
uv init
uv add neuro-san-studio
ns init                          # choose Google Gemini

# 2. Copy this repo's 'registries' and 'coded_tools' folders into the project

# 3. Register the network in registries/manifest.hocon
#    "aiops_incident_copilot.hocon": true,

# 4. Add your own key in a .env file (never commit it)
#    GOOGLE_API_KEY=your_key_here

# 5. Run
ns run
```

Open **http://localhost:4173** and select **aiops_incident_copilot**.

---

## 🧪 Demo Prompts & Expected Results

| # | Prompt | Expected result |
|---|---|---|
| 1 | `Alert: vm-web-01 CPU at 97% for the last 20 minutes after this morning's deployment.` | Runbook **RB-CPU-01**, verdict **APPROVE** |
| 2 | `Customer Portal is down with 502 Bad Gateway on appgw-prod.` | Runbook **RB-CERT-01**, **NEEDS HUMAN APPROVAL** |
| 3 | `sql-prod-01 is very slow, users report order timeouts.` | Runbook **RB-SQL-01**, **NEEDS HUMAN APPROVAL** |
| 4 | `vm-test-05 shows strange network packet loss.` | No runbook, **escalate to L3** (grounding test) |

### Sample output format
```
Incident Summary      : High CPU on vm-web-01 after deployment
Severity & Category   : P2 – Compute
Impacted CI           : vm-web-01 | Azure VM | Production | Criticality High
Probable Root Cause   : Runaway IIS worker process (match INC-1001) – Confidence: High
Recommended Runbook   : RB-CPU-01 – High CPU on Azure VM (steps 1–5)
Validation Verdict    : APPROVE (low-risk, approved runbook, no change request)
Next Action           : Recycle app pool and monitor CPU for 15 min
```

---

## 📈 Business Value

| Benefit | Impact |
|---|---|
| ⏱️ Faster MTTR | Triage, RCA and fix plan in seconds instead of manual searching |
| ✅ Trustworthy AI | Every recommendation is traced to an approved runbook and past incident |
| 🔒 Governance | Built-in change control and human approval for production risk |
| 🔁 Reusable | Swap the JSON files for a real CMDB/ITSM (e.g. ServiceNow) or MCP server |

## 🔮 Future Enhancements
- Connect to live ServiceNow / Azure Monitor through MCP servers
- Vector database search over large runbook libraries
- Auto-create change requests after human approval
- Teams notification to the on-call engineer

---

## 🛡️ Compliance
- Synthetic data only. **No client data.**
- **No LLM API keys** in this repository (`.env` is git-ignored).

## 👤 Author
**Subhajit Mukherjee**, Cognizant
Built for the *Agentic AI Hackathon – Neuro® AI Multi-Agent Accelerator (Track 2)*

## 🙏 Acknowledgements
Built with [Neuro SAN](https://github.com/cognizant-ai-lab/neuro-san) and [Neuro SAN Studio](https://github.com/cognizant-ai-lab/neuro-san-studio) by Cognizant AI Lab.
