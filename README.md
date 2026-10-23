# StudentSmart AI — Hackathon Prototype

A student-first personal finance demo with a distinctive dark-navy + lime visual system, clear navigation, and five focused workspaces:

- **Overview:** habit indicator, income/expense summary, cash-flow chart, spending mix, weekly nudge.
- **Spend Simulator:** interactive “what if I spend this?” calculator showing the impact on essentials and a savings goal.
- **Scam Shield:** checks text for common scam warning patterns and explains safe next steps.
- **Money Mentor:** topic-based student finance guidance in English, Kannada, and Hindi (curated rule-based prototype).
- **Transactions:** add transactions, import CSV, inspect ledger, export CSV, reset sample data.

## Run locally (Windows)
1. Install Python 3.10 or newer from https://www.python.org/downloads/ and enable **Add Python to PATH**.
2. Extract the ZIP.
3. Open the extracted `studentsmart_ai` folder, click the address bar, type `cmd`, and press Enter.
4. Run:
   ```bat
   py -m venv .venv
   .venv\Scripts\activate.bat
   python -m pip install -r requirements.txt
   python -m streamlit run app.py
   ```
5. Open the local URL shown in Command Prompt (usually http://localhost:8501). Keep the terminal open while demoing.

## CSV format
Required columns: `Date`, `Merchant`, `Amount`. Positive Amount = income; negative Amount = expense. `Category` is optional and will be inferred using simple keywords.

## Important prototype boundaries
- No live bank, UPI, SMS, payment-blocking, or credit-bureau integration.
- Scam Shield uses keyword/rule checks and cannot establish that a message is safe or fraudulent.
- The Student Smart Score is an illustrative habit indicator, **not** a credit score or lending decision.
- Forecast/simulation outputs depend on the inputs and are not financial guarantees.
- The dashboard uses local demo/sample data. Do not upload sensitive account information.

## Suggested live judging flow (2–3 minutes)
1. Open Overview and explain the student-specific money snapshot.
2. Open Spend Simulator; change purchase amount/frequency and show the savings-goal warning change.
3. Open Scam Shield and paste the example scholarship/OTP message to show explainable red flags.
4. Open Money Mentor and switch languages.
5. Add one transaction or import the sample CSV to demonstrate the data workflow.
