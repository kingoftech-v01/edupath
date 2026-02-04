# Edupath Desktop Security Guidelines

**Version**: 1.0
**Last Updated**: 2026-01-28
**Status**: MANDATORY

---

## Table of Contents

1. [Security Principles](#1-security-principles)
2. [Credential Storage](#2-credential-storage)
3. [Network Security](#3-network-security)
4. [Data Protection](#4-data-protection)
5. [Code Signing](#5-code-signing)
6. [Auto-Update Security](#6-auto-update-security)
7. [Security Checklist](#7-security-checklist)

---

## 1. Security Principles

### 1.1 Defense in Depth

```
┌──────────────────────────────────────┐
│        Code Signing                   │  Verify app integrity
├──────────────────────────────────────┤
│        Secure Updates                 │  Signed update packages
├──────────────────────────────────────┤
│        Network Security               │  TLS 1.3, cert pinning
├──────────────────────────────────────┤
│        Credential Storage             │  OS keychain/credential manager
├──────────────────────────────────────┤
│        Data Encryption                │  Encrypt local data
└──────────────────────────────────────┘
```

### 1.2 Key Principles

1. **Never store secrets in code**
2. **Use OS credential storage**
3. **Encrypt sensitive local data**
4. **Sign all releases**
5. **Verify update signatures**

---

## 2. Credential Storage

### 2.1 Windows Credential Manager (Tauri/Rust)

```rust
// src-tauri/src/storage/secure.rs
use keyring::Entry;

const SERVICE_NAME: &str = "com.edupath.desktop";

pub fn save_token(token: &str) -> Result<(), String> {
    let entry = Entry::new(SERVICE_NAME, "auth_token")
        .map_err(|e| e.to_string())?;
    entry.set_password(token)
        .map_err(|e| e.to_string())
}

pub fn get_token() -> Result<Option<String>, String> {
    let entry = Entry::new(SERVICE_NAME, "auth_token")
        .map_err(|e| e.to_string())?;
    match entry.get_password() {
        Ok(password) => Ok(Some(password)),
        Err(keyring::Error::NoEntry) => Ok(None),
        Err(e) => Err(e.to_string()),
    }
}

pub fn delete_token() -> Result<(), String> {
    let entry = Entry::new(SERVICE_NAME, "auth_token")
        .map_err(|e| e.to_string())?;
    entry.delete_password()
        .map_err(|e| e.to_string())
}

// Expose as Tauri commands
#[tauri::command]
pub fn save_auth_token(token: String) -> Result<(), String> {
    save_token(&token)
}

#[tauri::command]
pub fn get_auth_token() -> Result<Option<String>, String> {
    get_token()
}

#[tauri::command]
pub fn clear_auth_token() -> Result<(), String> {
    delete_token()
}
```

### 2.2 .NET Credential Manager

```csharp
// Services/CredentialService.cs
using System.Security;
using CredentialManagement;

public class CredentialService : ICredentialService
{
    private const string TargetName = "Edupath.Desktop.AuthToken";

    public void SaveToken(string token)
    {
        using var credential = new Credential
        {
            Target = TargetName,
            Username = "oauth_token",
            Password = token,
            PersistanceType = PersistanceType.LocalComputer
        };
        credential.Save();
    }

    public string? GetToken()
    {
        using var credential = new Credential { Target = TargetName };
        if (credential.Load())
        {
            return credential.Password;
        }
        return null;
    }

    public void DeleteToken()
    {
        using var credential = new Credential { Target = TargetName };
        credential.Delete();
    }
}
```

### 2.3 What to Store Securely

| Data | Storage | Never Store |
|------|---------|-------------|
| Auth tokens | OS Keychain | In files |
| Refresh tokens | OS Keychain | In localStorage |
| API keys | Environment/Config | In code |
| User passwords | NEVER locally | Anywhere |

---

## 3. Network Security

### 3.1 TLS Configuration

```rust
// Force TLS 1.2+
use reqwest::Client;

fn create_client() -> Client {
    Client::builder()
        .min_tls_version(reqwest::tls::Version::TLS_1_2)
        .build()
        .expect("Failed to create client")
}
```

### 3.2 Certificate Pinning

```rust
// src-tauri/src/network/pinning.rs
use reqwest::Certificate;

const PINNED_CERT: &[u8] = include_bytes!("../certs/api.edupath.com.pem");

fn create_pinned_client() -> Result<Client, reqwest::Error> {
    let cert = Certificate::from_pem(PINNED_CERT)?;

    Client::builder()
        .add_root_certificate(cert)
        .build()
}
```

### 3.3 API Security Headers

```typescript
// api/client.ts
const securityHeaders = {
  'X-Content-Type-Options': 'nosniff',
  'X-Frame-Options': 'DENY',
  'X-App-Version': APP_VERSION,
  'X-Platform': 'desktop',
};

apiClient.interceptors.request.use((config) => {
  config.headers = { ...config.headers, ...securityHeaders };
  return config;
});
```

---

## 4. Data Protection

### 4.1 Local Data Encryption

```rust
// src-tauri/src/storage/encrypted.rs
use aes_gcm::{
    aead::{Aead, KeyInit},
    Aes256Gcm, Nonce,
};
use rand::Rng;

pub struct EncryptedStorage {
    cipher: Aes256Gcm,
}

impl EncryptedStorage {
    pub fn new(key: &[u8; 32]) -> Self {
        let cipher = Aes256Gcm::new_from_slice(key)
            .expect("Invalid key length");
        Self { cipher }
    }

    pub fn encrypt(&self, data: &[u8]) -> Result<Vec<u8>, String> {
        let mut rng = rand::thread_rng();
        let nonce_bytes: [u8; 12] = rng.gen();
        let nonce = Nonce::from_slice(&nonce_bytes);

        let ciphertext = self.cipher
            .encrypt(nonce, data)
            .map_err(|e| e.to_string())?;

        // Prepend nonce to ciphertext
        let mut result = nonce_bytes.to_vec();
        result.extend(ciphertext);
        Ok(result)
    }

    pub fn decrypt(&self, data: &[u8]) -> Result<Vec<u8>, String> {
        if data.len() < 12 {
            return Err("Data too short".to_string());
        }

        let nonce = Nonce::from_slice(&data[..12]);
        let ciphertext = &data[12..];

        self.cipher
            .decrypt(nonce, ciphertext)
            .map_err(|e| e.to_string())
    }
}
```

### 4.2 Secure Deletion

```rust
// Securely clear sensitive data from memory
fn secure_clear(data: &mut [u8]) {
    for byte in data.iter_mut() {
        *byte = 0;
    }
    // Prevent compiler optimization
    std::sync::atomic::fence(std::sync::atomic::Ordering::SeqCst);
}
```

### 4.3 Prevent Memory Dumps

```rust
// Disable core dumps on crash
#[cfg(unix)]
fn disable_core_dumps() {
    use libc::{rlimit, setrlimit, RLIMIT_CORE};
    let limit = rlimit { rlim_cur: 0, rlim_max: 0 };
    unsafe { setrlimit(RLIMIT_CORE, &limit) };
}
```

---

## 5. Code Signing

### 5.1 Windows Code Signing

```powershell
# Sign with certificate
signtool sign /f certificate.pfx /p password /tr http://timestamp.digicert.com /td sha256 /fd sha256 Edupath.exe

# Verify signature
signtool verify /pa Edupath.exe
```

### 5.2 Tauri Code Signing Configuration

```json
// tauri.conf.json
{
  "tauri": {
    "bundle": {
      "windows": {
        "certificateThumbprint": "YOUR_CERT_THUMBPRINT",
        "digestAlgorithm": "sha256",
        "timestampUrl": "http://timestamp.digicert.com"
      }
    }
  }
}
```

### 5.3 CI/CD Signing

```yaml
# GitHub Actions
- name: Sign Windows Binary
  env:
    WINDOWS_CERTIFICATE: ${{ secrets.WINDOWS_CERTIFICATE }}
    WINDOWS_CERTIFICATE_PASSWORD: ${{ secrets.WINDOWS_CERTIFICATE_PASSWORD }}
  run: |
    echo $WINDOWS_CERTIFICATE | base64 --decode > certificate.pfx
    signtool sign /f certificate.pfx /p $WINDOWS_CERTIFICATE_PASSWORD /tr http://timestamp.digicert.com /td sha256 /fd sha256 target/release/edupath.exe
```

---

## 6. Auto-Update Security

### 6.1 Signed Updates

```rust
// tauri.conf.json
{
  "tauri": {
    "updater": {
      "active": true,
      "endpoints": [
        "https://releases.edupath.com/{{target}}/{{current_version}}"
      ],
      "dialog": true,
      "pubkey": "dW50cnVzdGVkIGNvbW1lbnQ6IG1pbmlzaWduIHB1YmxpYyBrZXk6..."
    }
  }
}
```

### 6.2 Update Verification

Tauri automatically verifies signatures. The update JSON must include:

```json
{
  "version": "1.0.1",
  "notes": "Bug fixes",
  "pub_date": "2024-01-20T00:00:00Z",
  "platforms": {
    "windows-x86_64": {
      "signature": "dW50cnVzdGVkIGNvbW1lbnQ6...",
      "url": "https://releases.edupath.com/Edupath_1.0.1_x64.msi.zip"
    }
  }
}
```

### 6.3 Update Server Security

- Serve over HTTPS only
- Use CDN with DDoS protection
- Implement rate limiting
- Log all download requests

---

## 7. Security Checklist

### Pre-Release

- [ ] Code is signed with valid certificate
- [ ] Updates are signed
- [ ] No hardcoded secrets
- [ ] Credentials use OS keychain
- [ ] Network uses TLS 1.2+
- [ ] Certificate pinning enabled
- [ ] Debug logging disabled
- [ ] Core dumps disabled

### Code Review

- [ ] No secrets in code
- [ ] Input validation on all user input
- [ ] Secure credential storage
- [ ] Error messages don't leak info
- [ ] No sensitive data in logs

### Deployment

- [ ] Certificate not expired
- [ ] Update server HTTPS
- [ ] Monitoring enabled
- [ ] Incident response plan ready

---

**Security is mandatory for all Edupath desktop development.**

*Last updated: 2026-01-28*
