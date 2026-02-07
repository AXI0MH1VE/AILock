# AILock: Sovereign AI Security Gateway

AILock is a comprehensive, network-level security system designed to prevent data siphoning and ensure compliance with data privacy standards (GDPR, CCPA) when using AI services.

## Architecture

The system consists of several layers of defense:

1.  **Network Layer (pfSense)**: Enforces a strict domain allowlist to prevent "Shadow AI" usage and unauthorized data egress.
2.  **Proxy Layer (Squid + PII Redactor)**: Performs deep packet inspection and automatically redacts PII (Personally Identifiable Information) before it leaves the network.
3.  **Inbound Defense (Anubis)**: A Go-based bot blocker that challenges incoming connections to prevent AI scrapers from extracting organizational data.
4.  **Audit Layer**: Maintains a cryptographically verifiable ledger of all redacted data and approved transactions.

## Components

### 1. PII Redaction Proxy (`proxy/`)
A Python-based proxy that intercepts outgoing requests to AI services and redacts sensitive information like emails, phone numbers, and credit card details.

### 2. Anubis Bot Blocker (`bot_blocker/`)
A Go-based service that implements a cryptographic challenge-response mechanism to verify human users and block automated AI crawlers.

### 3. Firewall Configuration (`firewall/`)
Sample pfSense XML configuration for domain allowlisting and traffic control.

### 4. Audit Logger (`audit/`)
A ledger-based logging system that ensures accountability and provides a verifiable audit trail.

## Deployment

1.  **Firewall**: Import `firewall/pfsense_config.xml` into your pfSense instance.
2.  **Proxy**: Run the PII redactor:
    ```bash
    python3 proxy/pii_redactor.py
    ```
3.  **Bot Blocker**: Build and run Anubis:
    ```bash
    go run bot_blocker/anubis.go
    ```

## Compliance

AILock addresses key GDPR requirements:
- **Article 22**: Human Intervention via HITL workflows.
- **Article 25**: Privacy by Design through mandatory redaction.
- **Article 32**: Security of Processing via stateful firewalling.
- **Article 33**: Breach Notification through real-time alerting.

## License
MIT
