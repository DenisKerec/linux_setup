# Claude Code — Multiple Account Setup

Two Claude accounts on the same machine. You explicitly pick which one to use per project.

## Commands

| Command | Account |
|---------|---------|
| `claude-work` | Ridango account |
| `claude-private` | Private account |

---

## How it works

Claude Code stores all its data (auth tokens, settings, memory, history) in a config directory. By default this is `~/.claude`.

Claude exposes an environment variable `CLAUDE_CONFIG_DIR` that overrides where it looks for that data. Setting it to a different path makes Claude think it's a completely different installation — different login, different settings, everything.

So the aliases just prepend that env var before calling `claude`:

```zsh
alias claude-work='CLAUDE_CONFIG_DIR=~/.claude claude'
alias claude-private='CLAUDE_CONFIG_DIR=~/.claude-private claude'
```

Each directory holds its own isolated account. They never interfere with each other.

---

## Directory structure

```
~/.claude/          ← Ridango account (auth, settings, memory, history)
~/.claude-private/  ← Private account (auth, settings, memory, history)
```

---

## Setup from scratch

### 1. Create the private config directory

```bash
mkdir -p ~/.claude-private
```

### 2. Add aliases to `~/.zshrc`

```zsh
alias claude-work='CLAUDE_CONFIG_DIR=~/.claude claude'
alias claude-private='CLAUDE_CONFIG_DIR=~/.claude-private claude'
```

### 3. Reload the shell

```bash
source ~/.zshrc
```

### 4. Log in to the private account

The Ridango account is already logged in (its data lives in `~/.claude`).
For the private account, run:

```bash
claude-private
```

Claude will detect an empty config dir and prompt you to log in. After login, credentials are saved to `~/.claude-private` — one time only.

---

## Usage

Just use the right alias for the project you're working on:

```bash
claude-work     # inside a Ridango project
claude-private  # inside a personal project
```

Both accounts have completely separate settings, API keys, memory, and conversation history.
