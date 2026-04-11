# Ridango VPN (openfortivpn via terminal)

## Usage

```bash
VPN-Ridango
```

This alias runs:
```bash
sudo openfortivpn vpn.ridango.com:443 --saml-login
```

A browser window opens for SAML authentication. After login, the VPN tunnel starts in the terminal. Keep the terminal open — closing it kills the VPN.

## Install openfortivpn (from source)

The apt version doesn't support `--saml-login`, so it must be built from source.

```bash
# 1. Install build dependencies
sudo apt install -y build-essential pkg-config autoconf automake libssl-dev ppp

# 2. Clone and build
git clone https://github.com/adrienverge/openfortivpn.git /tmp/openfortivpn
cd /tmp/openfortivpn
git checkout v1.23.1
autoreconf -fi
./configure --prefix=/usr/local --sysconfdir=/etc
make
sudo make install

# 3. Verify
openfortivpn --version
```

## Alias (already in zshrc)

```bash
alias VPN-Ridango='sudo openfortivpn vpn.ridango.com:443 --saml-login'
```
