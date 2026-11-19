# Provider-neutral compliance and security

The same controls apply to every model or coding provider: local models,
NVIDIA, Codex, and Antigravity. No provider is trusted merely because it is
local, hosted, or used for code assistance.

## Required controls

- **Least privilege:** providers receive only the research brief and bounded
  data needed for their role; they receive no broker credentials or order API.
- **Bounded output:** provider responses are parsed into the safe mutation
  vocabulary; malformed responses are rejected or skipped. The current
  proposal parser is defensive custom parsing, while the paper-runtime handoff
  uses a formal Pydantic contract.
- **Deterministic authority:** providers propose hypotheses; local code alone
  calculates returns, drawdown, chronology, and promotion.
- **Prompt-injection resistance:** data, files, model responses, and tool output
  are treated as untrusted content, never as higher-priority instructions.
- **Secret isolation:** keys and OAuth material stay in the OS credential
  store or environment. They never enter prompts, plugin manifests, logs, or
  Git history.
- **Auditability:** record provider, model, prompt/config version, response
  digest, timeout, failure, and resulting evaluation handoff.
- **Fail closed:** provider failure, authentication failure, or policy failure
  must block promotion rather than silently weakening controls.
- **Sandboxing:** the current US.APP plugin is trusted local integration code,
  not an OS-isolated process. New code-capable plugins must be isolated and
  permission-bounded before being enabled. They cannot submit orders.
- **Version pinning:** provider and plugin versions are recorded with every
  candidate and replay.

## Provider roles

Local, NVIDIA, Codex, and Antigravity may have different responsibilities, but
they use the same contract. A coordinator may route and review proposals, but
it still cannot replace the deterministic evaluator or grant itself execution
authority.
