# Correlation Logic

## Overview

This lab implements a **three-tier detection and correlation pipeline**:

1. **Suricata** - Network-level signature detection (IDS/IPS)
2. **Wazuh** - Host-level correlation and alert enrichment (SIEM)
3. **Python Prioritizer** - Analyst-facing triage automation

Each tier reduces noise and adds context, following the SOC analyst workflow
from raw events to actionable incidents

---

## Tier 1: Suricata Signature Detection

Suricata inspects traffic inline on pfSense between LAN and DMZ segments.
Three custom rules catch specific attack patterns:

| SID      | Attack Type        | Detection Logic                          | Severity |
|----------|--------------------|------------------------------------------|----------|
| 1000001  | SSH brute-force    | 5+ TCP SYN to port 22 in 30s per source  | 2 (Med)  |
| 1000002  | TCP port scan      | 20+ TCP SYN to any port in 5s per source | 3 (Low)  |
| 1000003  | Command injection  | HTTP URI contains `;wget http`           | 1 (High) |

**Tuning layer:** `threshold.config` post-processes alerts before output.
The brute-force rule fires at 5 attempts/30s, but the threshold delays
output until 10 attempts/60s - reducing false positives from legitimate
admin SSH sessions

**Output:** All alerts written to `/var/log/suricata/eve.json` as
newline-delimited JSON. Each event contains timestamp, source/destination
IPs, signature ID, and severity.

---

## Tier 2: Wazuh Correlation Rules

The Wazuh agent on pfSense reads `eve.json` and forwards events to the
Wazuh manager. Custom rules in `local_rules.xml` then **correlate repeated
events from the same source** into higher-severity incidents.

---

## Tier 3: Python Alert Prioritizer

The analyst opens their terminal and runs:

```bash
python alert_prioritizer.py /var/log/suricata/eve.json
