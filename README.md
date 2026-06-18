# SOC Lab - Suricata IDS/IPS + Wazuh SIEM + Alert Prioritization

A segmented virtualized SOC lab demonstrating network intrusion detection,
SIEM correlation, and automated alert triage. Built on VMware Workstation
with pfSense, Suricata (inline IPS), Wazuh, and custom Python tooling.


## Key Features

### Suricata IDS/IPS Configuration & Tuning
- Inline IPS mode on pfSense monitoring LAN and DMZ interfaces
- Custom detection rules for three attack categories:
  - SSH brute-force (SID 1000001)
  - TCP port scanning (SID 1000002)
  - Command injection exploitation (SID 1000003)
- Two-stage threshold tuning to reduce false positives:
  - Inline rule thresholds for initial detection sensitivity
  - `threshold.config` for post-detection noise filtering
- Documented tuning methodology with baseline testing results

### Wazuh Correlation & Dashboards
- Custom correlation rules in `local_rules.xml`:
  - Repeated SSH brute-force from single source -> Level 10 alert
  - Sustained port scanning from single source -> Level 8 alert
  - Multiple exploit attempts from single source -> Level 12 alert
- Severity escalation based on event frequency and attack type
- Dashboards for alert overview and brute-force triage

### Python Alert Prioritization Script
- Parses Suricata `eve.json` log files
- Groups alerts by source IP
- Ranks by severity (High > Medium > Low) then total count
- Outputs prioritized analyst triage list
- Zero external dependencies

---

## Skills Demonstrated:
- Network segmentation with VMware and pfSense
- Suricata IDS/IPS rule writing and threshold tuning
- Wazuh SIEM correlation rule development
- Python scripting for security automation
- SOC analyst workflow design (detection -> correlation -> triage)
- Technical documentation

## Notes:
- This lab was built for learning and demonstration purposes. Production
deployments would include additional tuning (GeoIP filtering, internal
IP whitelisting, DNS rule suppression) as noted in the tuning methodology.
