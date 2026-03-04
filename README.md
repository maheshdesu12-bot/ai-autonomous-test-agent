# AI Autonomous Test Agent

An agent-based, data-driven autonomous test framework built with **Python 3.11**, **Playwright**, and **MongoDB**.  
It executes end-to-end flows (Register/Login), validates outcomes using UI + backend state changes, captures evidence (screenshots + DOM snapshots), and generates an HTML report.

---

## Key Features

- **Autonomous agent workflow**
  - Orchestrator → Planner → Task Agents (Register/Login) → Executors
- **Data-driven execution**
  - Reads users from `test_data/users.json`
- **Robust validation**
  - Supports UI-based validation and backend state-change validation
- **Evidence collection**
  - Screenshots stored under `reports/screenshots/`
  - DOM snapshots saved for debugging/self-healing foundation
- **HTML reporting**
  - Generates `reports/report.html`
- **Extensible design**
  - Easy to add agents (e.g., SecurityAgent, APIAgent, SelfHealingAgent)

---

## Project Structure
