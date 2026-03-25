# DataGrip Setup

## Install

```bash
brew install --cask datagrip
```

## Migrate Connections from DBeaver

A script is provided to automatically import all DBeaver connections into DataGrip, preserving folder structure.

### What the script does

- Reads DBeaver configs from `~/Library/DBeaverData/workspace6/*/`
- Merges into existing DataGrip project at `~/DataGripProjects/Ridango/.idea/dataSources.xml`
- Skips duplicate connections (matched by JDBC URL)
- Creates a backup of the existing config before writing

### Grouping

- **AWS PROD** and **VeloDB** stay at the root level (no folder)
- DBeaver `General` workspace connections go into the `Random/` group
- DBeaver `Ridango` workspace connections preserve their folder hierarchy under `Ridango/<folder>/`

### Auto-sync (introspection)

- **AWS PROD** and **VeloDB** have auto-sync **enabled** — schema changes appear immediately in the sidebar
- All other connections have auto-sync **disabled** — use `Cmd+Shift+R` to manually refresh when needed

To change which connections auto-sync, edit `AUTOSYNC_NAMES` in the script.

### Run

```bash
# make sure DataGrip is CLOSED first
python3 scripts/dbeaver_to_datagrip.py
# then open DataGrip — all connections + folders should appear
```

Passwords do not transfer from DBeaver (they're encrypted separately). Re-enter credentials as you connect to each database.

### Rollback

```bash
cp ~/DataGripProjects/Ridango/.idea/dataSources.xml.bak \
   ~/DataGripProjects/Ridango/.idea/dataSources.xml
```

## Tips

- **Query console**: `Cmd+Shift+F10` — each console tracks its own connection/schema
- **Auto-complete**: `Ctrl+Space` — context-aware SQL completion
- **Explain plan**: `Cmd+Shift+E` — visualize query execution
- **Refresh schema**: `Cmd+Shift+R` on any connection
- **Export results**: right-click query results -> Export to CSV, JSON, SQL
- **Query history**: `Cmd+E`
- **Schema filter**: click the "1 of N" schemas badge on a connection to show/hide schemas
- **SSH tunnel**: connection Properties -> SSH/SSL tab
