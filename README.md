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

## License

Apache-2.0
