# SYNTRA Security Exclusions Log

**Established:** 2025-04-25

---

## Permanent Exclusions and Clean-Up List

### 1. API Keys and Tokens
- `OPENAI_API_KEY`
- `ELEVENLABS_API_KEY`
- `MISTRAL_KEY`
- Any token starting with `sk-`
- Any generic `"api_key"` or `"token"` references

### 2. Configuration Files
- `config.json` must be removed if containing keys
- `.env` only with placeholder keys

### 3. Runtime Artifacts
- No cached `.log` or trace files if containing sensitive interactions

---

This log evolves as SYNTRA's architecture expands.
