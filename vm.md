# Virtual Machines (GNOME Boxes)

For running Windows-only tools like Tableau Desktop and Power BI on Linux.

---

## 1. Install GNOME Boxes
```bash
sudo apt install gnome-boxes
```

## 2. Create a Windows 11 VM

1. Open **Boxes** (from Activities or `Alt+Space` Ulauncher)
2. Click **+** -> **Create a Virtual Machine**
3. Select **Windows 11** (Boxes can auto-download it) or provide your own ISO
4. Recommended resources:
   - **RAM**: 8GB+ (minimum 4GB)
   - **Disk**: 60GB+
   - **CPUs**: 4+
5. Follow Windows installer, then install your apps

## 3. Apps to Install Inside the VM

- **Tableau Desktop** — download from tableau.com
- **Power BI Desktop** — download from Microsoft Store or powerbi.microsoft.com

## 4. Tips

- **Shared clipboard**: Boxes supports copy/paste between host and VM — install SPICE guest tools inside Windows for best experience
- **Shared folders**: Use Boxes preferences to share a folder between Linux and the VM
- **Performance**: Close other heavy apps on the host when running the VM
- **Snapshots**: Take a snapshot before big changes (right-click VM -> Properties -> Snapshots)

## 5. Install SPICE Guest Tools (inside Windows VM)
For better performance, shared clipboard, and auto screen resize:
1. Inside the Windows VM, open browser
2. Download from https://www.spice-space.org/download.html (Windows guest tools)
3. Install and reboot the VM
