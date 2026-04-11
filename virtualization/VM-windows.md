# Windows VM Setup (KVM/QEMU + virt-manager)

## Prerequisites

Already installed by `install.sh`:
- qemu-kvm, libvirt, virt-manager, ovmf (UEFI), swtpm (TPM)
- User added to `libvirt` and `kvm` groups

**Important:** Log out and back in after running `install.sh` so group membership takes effect.

## ISO Location

```
~/Downloads/Win11_Enterprise_25H2_en-us.iso
```

This is a **90-day evaluation** copy of Windows 11 Enterprise (25H2) from Microsoft.
After 90 days you can reset the trial with `slmgr /rearm` (up to 3 times), or activate with a license key.

## Create the VM

1. Open **virt-manager** (Virtual Machine Manager) from your app launcher

2. Click **Create a new virtual machine**

3. **Step 1 — Install media:**
   - Select "Local install media (ISO image)"
   - Browse to `~/Downloads/Win11_Enterprise_25H2_en-us.iso`
   - OS type should auto-detect as "Microsoft Windows 11"

4. **Step 2 — Memory and CPU:**
   - RAM: **8192 MB** (8 GB) minimum, 16384 MB (16 GB) recommended
   - CPUs: **4** minimum, 6+ recommended
   - (Your CPU has 14 threads total — leave some for the host)

5. **Step 3 — Storage:**
   - Create a disk image: **80 GB** minimum, 120+ GB recommended
   - Uses thin provisioning by default (only uses actual space needed)

6. **Step 4 — Name and final settings:**
   - Name: `Windows-11` (or whatever you prefer)
   - **Check "Customize configuration before install"** (important!)
   - Click **Finish**

7. **Customization window (critical for Windows 11):**

   a. **Overview** tab:
      - Firmware: change to **UEFI x86_64: /usr/share/OVMF/OVMF_CODE_4M.ms.fd**
      - (This enables Secure Boot which Windows 11 requires)

   b. **Add Hardware** -> **TPM**:
      - Model: TIS
      - Backend: Emulated (swtpm)
      - Version: 2.0
      - (Windows 11 requires TPM 2.0)

   c. **Video** tab:
      - Model: change to **Virtio** (better performance) or keep QXL

   d. Click **Begin Installation**

8. **Windows installer:**
   - Proceed through the normal Windows setup
   - Select "Windows 11 Enterprise" when prompted
   - Choose "Custom: Install Windows only" for clean install
   - Select the virtual disk and install

## After Installation

### Install virtio drivers (better performance)

1. In virt-manager, go to VM details -> **Add Hardware** -> **Storage**
   - Device type: CDROM
   - Select the virtio-win ISO:
   ```bash
   sudo apt install -y virtio-win
   # ISO will be at: /usr/share/virtio-win/virtio-win.iso
   ```
   If the package isn't available, download from:
   ```bash
   wget -O ~/Downloads/virtio-win.iso https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/stable-virtio/virtio-win.iso
   ```

2. Inside Windows, open the virtio-win CD drive and run `virtio-win-guest-tools.exe`
   - This installs optimized network, disk, and display drivers

### Enable shared clipboard

1. Inside Windows, the virtio-win guest tools installer also includes the SPICE agent
2. Clipboard sharing between host and VM should work automatically after install

### Shared folders

To share a folder between host and VM:

1. In virt-manager VM details -> **Add Hardware** -> **Filesystem**
   - Driver: virtiofs
   - Source path: `/home/denis/shared` (or any host folder)
   - Target path: `shared`

2. Inside Windows, open PowerShell as admin:
   ```powershell
   # Install WinFsp first (required for virtiofs)
   # Download from: https://winfsp.dev/rel/
   # Then mount:
   net use Z: \\viofs\shared
   ```

## Quick Reference

```bash
# List all VMs
virsh list --all

# Start VM
virsh start Windows-11

# Shutdown VM gracefully
virsh shutdown Windows-11

# Force stop
virsh destroy Windows-11

# Open virt-manager GUI
virt-manager
```

## Performance Tips

- **CPU pinning**: For best performance, pin vCPUs to physical cores in the VM XML config
- **Hugepages**: Enable for better memory performance with large VMs
- **Disk I/O**: Use virtio disk bus (default in virt-manager) for best disk performance
- **Networking**: Use virtio NIC (default) for best network performance
