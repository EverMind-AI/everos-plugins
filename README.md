# everos-plugins

Official EverOS SDK tools for AI coding assistants: migration, upgrade, and development skills.

## Available Plugins

### everos-sdk-upgrade

Auto-migrate EverOS SDK between versions. Currently supports Python; Go and TypeScript are planned.

- Detects SDK language and current version automatically
- Chains migration rules from current to target version
- Verifies changes with language-specific compile/test tools

## Installation (Claude Code)

```bash
# 1. Add marketplace (one-time)
/plugin marketplace add EverMind-AI/everos-plugins

# 2. Install the plugin
/plugin install everos-sdk-upgrade@everos-plugins

# 3. Use it
/everos-sdk-upgrade

# 4. Update to latest rules
/plugin marketplace update
```

## Repository Structure

```
everos-plugins/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   └── everos-sdk-upgrade/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       └── skills/
│           └── everos-sdk-upgrade/
│               ├── SKILL.md
│               ├── migration/
│               │   └── python/
│               │       └── v0-to-v1.md
│               └── examples/
│                   └── python/
│                       ├── v0.py
│                       └── v1.py
├── .github/
│   └── workflows/
│       └── validate-plugins.yml
├── LICENSE
└── README.md
```

## Other AI Tools (Cursor, GitHub Copilot, Codex, Gemini CLI, Cline, Amp, Warp, Goose, Junie, and 45+ supported)

This skill follows the [Agent Skills](https://agentskills.io) open standard. Install with one command for 45+ supported tools:

```bash
npx skills add https://github.com/EverMind-AI/everos-plugins
```

The CLI will auto-detect your installed tools and copy the skill to the correct directories.

## Adding Migration Rules

When a new SDK version is released:

1. Add `skills/everos-sdk-upgrade/migration/{lang}/vN-to-vN+1.md` with migration rules
2. Add `skills/everos-sdk-upgrade/examples/{lang}/vN+1.{ext}` for major versions
3. Update `plugin.json` version field
4. Push to this repository

Users run `/plugin marketplace update` to get the latest rules.

## EverMind Ecosystem

EverMind connects memory research, production-ready products, and practical
integrations into one open-source ecosystem.

<table>
<tr>
<th colspan="2">Products</th>
</tr>
<tr>
<td><strong><a href="https://github.com/EverMind-AI/EverOS">EverOS</a></strong></td>
<td>A local-first, Markdown-native long-term memory runtime for agents and users.</td>
</tr>
<tr>
<td><strong><a href="https://github.com/EverMind-AI/Raven">Raven</a></strong></td>
<td>A memory-first, self-improving agent harness with proactivity, context control, and skill evolution.</td>
</tr>
<tr>
<td><strong><a href="https://github.com/EverMind-AI/EverMe">EverMe (CLI)</a></strong></td>
<td>A CLI and agent plugin suite for cross-device, cross-agent personal memory.</td>
</tr>
<tr>
<th colspan="2">Research &amp; Evaluation</th>
</tr>
<tr>
<td><strong><a href="https://github.com/EverMind-AI/SkillCorpus">SkillCorpus</a></strong></td>
<td>Curated, retrieval-ready agent skill corpora with retrieval and evaluation tooling.</td>
</tr>
<tr>
<td><strong><a href="https://github.com/EverMind-AI/EverAlgo">EverAlgo</a></strong></td>
<td>Stateless extraction, ranking, parsing, and memory operators that power EverOS.</td>
</tr>
<tr>
<td><strong><a href="https://github.com/EverMind-AI/HyperMem">HyperMem</a></strong></td>
<td>Hypergraph-based hierarchical memory for coarse-to-fine long-term conversation retrieval.</td>
</tr>
<tr>
<td><strong><a href="https://github.com/EverMind-AI/MSA">MSA</a></strong></td>
<td>Memory Sparse Attention for scalable latent memory and 100M-token contexts.</td>
</tr>
<tr>
<td><strong><a href="https://github.com/EverMind-AI/EverMemBench">EverMemBench</a></strong></td>
<td>Evaluation of factual recall, applied reasoning, and personalized generalization in memory systems.</td>
</tr>
<tr>
<td><strong><a href="https://github.com/EverMind-AI/EvoAgentBench">EvoAgentBench</a></strong></td>
<td>Longitudinal evaluation of agent self-evolution, transfer efficiency, error avoidance, and skill use.</td>
</tr>
<tr>
<th colspan="2"><a href="https://github.com/EverMind-AI/plugins">Integrations</a></th>
</tr>
<tr>
<td><strong><a href="https://docs.openclaw.ai">OpenClaw</a></strong></td>
<td><a href="https://github.com/EverMind-AI/plugins/tree/main/openclaw">OpenClaw plugin</a> for automatic recall, capture, and session-memory lifecycle management.</td>
</tr>
<tr>
<td><strong><a href="https://github.com/NousResearch/hermes-agent">Hermes Agent</a></strong></td>
<td><a href="https://github.com/EverMind-AI/plugins/tree/main/hermes">Hermes plugin</a> for persistent memory across Hermes sessions.</td>
</tr>
<tr>
<td><strong><a href="https://github.com/deepseek-ai/DeepSeek-Harness">DeepSeek Harness</a></strong></td>
<td><a href="https://github.com/EverMind-AI/plugins/tree/main/dsh">DSH plugin</a> for memory-aware DeepSeek Harness agents.</td>
</tr>
<tr>
<td><strong><a href="https://dify.ai">Dify</a></strong></td>
<td><a href="https://github.com/EverMind-AI/plugins/tree/main/dify">Self-hosted</a> and <a href="https://github.com/EverMind-AI/plugins/tree/main/dify_cloud">cloud</a> tools for explicit memory search and storage in workflows and agents.</td>
</tr>
</table>

Together, these projects form EverMind's research-to-runtime stack: methods
and benchmarks become reusable memory infrastructure, products, and agent
integrations.

## License

Apache-2.0
