# Windows 11 VM — Backup & Restore

## Backup location

```
/var/lib/libvirt/images/Windows-11-fresh-install.qcow2
```

This is a clean snapshot taken right after Windows 11 Enterprise was installed with virtio drivers.

## VM disk location

```
/var/lib/libvirt/images/Windows-11.qcow2
```

## Restore from backup

```bash
# 1. Stop the VM
sudo virsh --connect qemu:///system destroy Windows-11

# 2. Replace the disk with the backup
sudo cp /var/lib/libvirt/images/Windows-11-fresh-install.qcow2 /var/lib/libvirt/images/Windows-11.qcow2

# 3. Start the VM
sudo virsh --connect qemu:///system start Windows-11
```

## Create a new backup

```bash
# 1. Shut down the VM first (for a clean backup)
sudo virsh --connect qemu:///system shutdown Windows-11

# 2. Copy the disk image
sudo cp /var/lib/libvirt/images/Windows-11.qcow2 /var/lib/libvirt/images/Windows-11-backup-$(date +%Y%m%d).qcow2
```

## VM details

- **Name:** Windows-11
- **OS:** Windows 11 Enterprise 25H2 (90-day evaluation)
- **CPU:** 6 vCPUs
- **RAM:** 8 GB
- **Disk:** 120 GB (thin provisioned, SATA)
- **Firmware:** UEFI with Secure Boot + TPM 2.0
- **Connection:** qemu:///system
