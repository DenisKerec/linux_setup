#!/usr/bin/env python3
"""Convert DBeaver data-sources.json to DataGrip dataSources.xml."""

import json
import uuid
import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path

DBEAVER_FILES = [
    Path.home() / "Library/DBeaverData/workspace6/General/.dbeaver/data-sources.json",
    Path.home() / "Library/DBeaverData/workspace6/Ridango/.dbeaver/data-sources.json",
]

# Map DBeaver driver/provider to DataGrip driver refs
DRIVER_MAP = {
    "postgresql": ("postgresql", "org.postgresql.Driver", "jdbc:postgresql://"),
    "postgres-jdbc": ("postgresql", "org.postgresql.Driver", "jdbc:postgresql://"),
    "mysql": ("mysql.8", "com.mysql.cj.jdbc.Driver", "jdbc:mysql://"),
    "mariadb": ("mariadb", "org.mariadb.jdbc.Driver", "jdbc:mariadb://"),
    "clickhouse": ("clickhouse", "com.clickhouse.jdbc.ClickHouseDriver", "jdbc:clickhouse://"),
    "com_clickhouse": ("clickhouse", "com.clickhouse.jdbc.ClickHouseDriver", "jdbc:clickhouse://"),
    "oracle": ("oracle", "oracle.jdbc.OracleDriver", "jdbc:oracle:thin:@"),
    "sqlserver": ("sqlserver.ms", "com.microsoft.sqlserver.jdbc.SQLServerDriver", "jdbc:sqlserver://"),
    "sqlite": ("sqlite.xerial", "org.sqlite.JDBC", "jdbc:sqlite:"),
    "h2": ("h2", "org.h2.Driver", "jdbc:h2:"),
    "mongo": ("mongo", "", ""),
    "bigquery": ("bigquery", "com.simba.googlebigquery.jdbc.Driver", "jdbc:bigquery://"),
}

# Connections that should have auto-sync enabled (all others get sync disabled)
# These also stay ungrouped (no folder) at the root level
AUTOSYNC_NAMES = {"AWS PROD", "VeloDB"}


def parse_dbeaver_sources():
    connections = []
    for path in DBEAVER_FILES:
        if not path.exists():
            print(f"Skipping {path} (not found)")
            continue
        with open(path) as f:
            data = json.load(f)
        workspace = path.parent.parent.name  # "General" or "Ridango"
        for conn_id, conn in data.get("connections", {}).items():
            config = conn.get("configuration", {})
            connections.append({
                "name": conn.get("name", "unnamed"),
                "provider": conn.get("provider", ""),
                "driver": conn.get("driver", ""),
                "host": config.get("host", "localhost"),
                "port": config.get("port", ""),
                "database": config.get("database", ""),
                "url": config.get("url", ""),
                "workspace": workspace,
                "ssh": config.get("handler-properties", {}),
                "folder": conn.get("folder", ""),
            })
    return connections


def build_datagrip_xml(connections, existing_xml_path=None):
    # Load existing DataGrip config if present, to merge instead of overwrite
    existing_urls = set()
    if existing_xml_path and Path(existing_xml_path).exists():
        existing_tree = ET.parse(existing_xml_path)
        project = existing_tree.getroot()
        component = project.find("component[@name='DataSourceManagerImpl']")
        # Update existing connections: set sync and group
        for ds in component.findall("data-source"):
            url_el = ds.find("jdbc-url")
            if url_el is not None and url_el.text:
                existing_urls.add(url_el.text)
            ds_name = ds.get("name", "")
            is_autosync = ds_name in AUTOSYNC_NAMES
            # Set sync
            sync_el = ds.find("synchronize")
            if sync_el is not None:
                sync_el.text = "true" if is_autosync else "false"
            # Set group: autosync at root, others in "Random"
            if is_autosync:
                if "group" in ds.attrib:
                    del ds.attrib["group"]
            else:
                ds.set("group", "Random")
        print(f"  Found {len(existing_urls)} existing connections (updated sync & groups)\n")
    else:
        project = ET.Element("project", version="4")
        component = ET.SubElement(
            project, "component",
            name="DataSourceManagerImpl",
            format="xml",
            **{"multifile-model": "true"}
        )

    # Collect all unique group paths for the group registry
    all_groups = set()

    for conn in connections:
        driver_key = conn["driver"] or conn["provider"]
        driver_info = DRIVER_MAP.get(driver_key) or DRIVER_MAP.get(conn["provider"])

        if not driver_info:
            print(f"  SKIPPED (unknown driver '{driver_key}'): {conn['name']}")
            continue

        dg_driver, jdbc_class, _ = driver_info

        # Use original JDBC URL if available, build one otherwise
        jdbc_url = conn["url"]
        if not jdbc_url:
            jdbc_url = f"jdbc:postgresql://{conn['host']}:{conn['port']}/{conn['database']}"

        # Skip if this URL already exists in DataGrip
        if jdbc_url in existing_urls:
            print(f"  DUPLICATE (already in DataGrip): {conn['name']}")
            continue

        name = conn["name"]
        is_autosync = name in AUTOSYNC_NAMES

        # Autosync connections stay at root (no group)
        # Everything else goes into Ridango/<folder> or just "Ridango"
        group_path = ""
        if not is_autosync:
            group_parts = []
            if conn["workspace"] != "General":
                group_parts.append(conn["workspace"])
            else:
                group_parts.append("Random")
            if conn["folder"]:
                group_parts.extend(conn["folder"].split("/"))
            group_path = "/".join(group_parts)

        ds = ET.SubElement(
            component, "data-source",
            source="LOCAL",
            name=name,
            uuid=str(uuid.uuid4()),
        )

        # Set the group (folder) for this data source
        if group_path:
            ds.set("group", group_path)
            parts = group_path.split("/")
            for i in range(1, len(parts) + 1):
                all_groups.add("/".join(parts[:i]))

        ET.SubElement(ds, "driver-ref").text = dg_driver
        ET.SubElement(ds, "synchronize").text = "true" if is_autosync else "false"
        if jdbc_class:
            ET.SubElement(ds, "jdbc-driver").text = jdbc_class
        ET.SubElement(ds, "jdbc-url").text = jdbc_url

    # Print group summary
    if all_groups:
        print(f"\n  Created {len(all_groups)} groups:")
        for g in sorted(all_groups):
            print(f"    📁 {g}")

    return project


def main():
    datagrip_xml = Path.home() / "DataGripProjects/Ridango/.idea/dataSources.xml"
    backup_path = Path.home() / "DataGripProjects/Ridango/.idea/dataSources.xml.bak"

    print("Parsing DBeaver connections...")
    connections = parse_dbeaver_sources()
    print(f"Found {len(connections)} connections\n")

    # Backup existing config
    if datagrip_xml.exists():
        import shutil
        shutil.copy2(datagrip_xml, backup_path)
        print(f"Backed up existing config to {backup_path}\n")

    print("Merging into DataGrip format...")
    xml_tree = build_datagrip_xml(connections, existing_xml_path=datagrip_xml)

    # Pretty print
    rough = ET.tostring(xml_tree, encoding="unicode")
    pretty = minidom.parseString(rough).toprettyxml(indent="  ", encoding=None)
    # Remove extra xml declaration
    lines = pretty.split("\n")
    lines = [l for l in lines if not l.startswith("<?xml")]
    output = '<?xml version="1.0" encoding="UTF-8"?>\n' + "\n".join(lines).strip() + "\n"

    datagrip_xml.write_text(output)
    print(f"\nWrote merged config to {datagrip_xml}")
    print(f"Backup at {backup_path}")
    print(f"\nNext steps:")
    print(f"  1. Make sure DataGrip is CLOSED")
    print(f"  2. Open DataGrip — all connections + folders should appear")
    print(f"  3. Re-enter passwords as you connect to each DB")


if __name__ == "__main__":
    main()
