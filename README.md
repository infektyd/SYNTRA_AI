# SYNTRA — Symbolic Cognition Engine

This is SYNTRA. A general-purpose symbolic AI system I’ve built from the ground up.

It’s not an LLM. It’s not a chatbot.  
It’s a modular cognition framework that compresses thought into symbolic logic — built using Python, real-time reasoning modules, and a symbolic language I designed called **VLD**.

---

## The idea behind SYNTRA is simple:
**Let a system observe. Let it think symbolically. Let it reason over time.**

---

## What It Does

- Interprets real-world signals or inputs (sensor values, telemetry, etc.)
- Converts those inputs into symbolic memory — not just raw data
- Detects patterns and symbolic drift over time
- Compresses logic using VLD — a symbolic language meant to reduce runtime and increase clarity
- Runs independently (can be hosted on a Raspberry Pi or local machine)
- Doesn’t require a full LLM — though it can bridge to one if needed

---

## Key Components

| Module      | Purpose                                                   |
|-------------|-----------------------------------------------------------|
| `modi`      | Diagnostic reasoning logic — fault detection, drift logic |
| `valon`     | Symbol interpreter and symbolic glossary/translation      |
| `field`     | Runtime feedback, symbolic logging                        |
| `io`        | Signal decoding, input symbol generation                  |
| `vld`       | Symbolic language core (VLD engine)                       |
| `prime`     | Core synchronizer and module router                       |
| `relay`     | Proposal/document manager                                 |
| `benchmark` | Python vs VLD comparison and clarity testing              |
| `runtime`   | Full execution loop (`Deep_Cognition_Run.py`, etc.)       |

---

## Symbolic Logic Example (VLD)

```vld
⊕engineWarm ⊕TPSsteady ⊖crank.signal.missing ↯faultCode_17 → ⚠crank.sensor.suspect
```

That’s one symbolic line.  
It represents around 40 lines of equivalent Python fault logic.

---

## How to Run

To test VLD logic:
```bash
cd vld_demo
python3 vld_runner.py
```

To compare with procedural logic:
```bash
python3 benchmark.py
```

To run the full cognition loop:
```bash
python3 runtime/Deep_Cognition_Run.py
```

---

## Security

This repo uses a `.env` file for API keys.  
If you’re forking or expanding, do not hardcode keys.  
Check `.gitignore` — sensitive files are blocked by default.

---

## License

MIT License — authored by **Hans Axelsson**  
This work includes original symbolic structures, diagnostic chains, and cognitive memory handling logic.

---

## Why This Exists

I built SYNTRA because I wanted a diagnostic assistant that could actually think.  
It started with mechanical diagnostics — but it grew into something general.

This repo represents that growth.  
Symbolic memory. Recursive loops. Logic compression. Field-ready thinking.

No fluff. Just function.
