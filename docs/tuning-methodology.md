# Tuning Methodology

## Objective

Reduce false positives while maintaining detection coverage for brute-force,
port scanning, and exploitation attacks. Tuning was applied at two layers:
Suricata (network detection) and Wazuh (correlation thresholds).

---

## Suricata Tuning

### Layer 1: Inline Rule Thresholds

The custom rule for SSH brute-force (SID 1000001) uses an inline threshold:

 `
threshold:type both,track by_src,count 5,seconds 30
 `

 **Why add a second threshold?**
- The inline threshold controls *when Suricata evaluates the rule*.
- The post-detection threshold controls *when Suricata outputs the alert*.
- This two-stage approach allows the rule to remain sensitive (catching
  early attack indicators) while the output threshold reduces dashboard noise.

  **Use case:** During lab testing, a backup script triggered SSH connections
6–8 times in 60 seconds from a legitimate host. The rule matched (5/30)
internally, but the threshold (10/60) suppressed the output. When real
brute-force reached 10 attempts, the alert fired. This avoided a false
positive while preserving detection.

### Port Scan Rule (SID 1000002) — No Additional Threshold

The port scan rule uses only an inline threshold (`count 20, seconds 5`)
with no post-detection threshold. Reasoning:
- 20 SYNs in 5 seconds is aggressive — normal services don't produce
  this pattern.
- `nmap` default scans (`-T3`) trigger this threshold reliably.
- False positives were zero during baseline monitoring.

- ---

## Wazuh Correlation Tuning

### Threshold Selection Per Attack Type

| Attack Type       | Wazuh Window | Threshold | Reasoning |
|-------------------|--------------|-----------|-----------|
| SSH brute-force   | 60 seconds   | 3 events  | 3 Suricata alerts = 15+ SSH attempts (each alert represents 5 attempts). Confident it's not accidental. |
| Port scan         | 30 seconds   | 5 events  | 5 Suricata alerts = 100+ SYN packets. Indicates sustained reconnaissance, not a burst of legitimate connections. |
| Exploit attempt   | 30 seconds   | 2 events  | Any exploitation attempt is critical. Two in 30 seconds indicates either retry or multi-vector attack. Low threshold by design. |

### Severity Escalation Design

Wazuh correlation rules escalate severity significantly from single events:

- **Port scan:** Level 3 (single) → Level 8 (correlated) - Reconnaissance
  becomes more concerning when sustained.
- **SSH brute-force:** Level 3 (single) → Level 10 (correlated) - Active
  credential attacks deserve immediate attention.
- **Exploit attempt:** Level 5 (single) → Level 12 (correlated) - Two exploit
  attempts = likely compromise in progress. Highest escalation.

  ---

  **Principle:** Single events may be probes or mistakes. Repeated events
from the same source in a short window indicate intent.

### False Positive Testing Process

1. **Baseline monitoring** - Collected 2 hours of normal lab traffic
   (admin SSH, web browsing from Kali, Windows updates).
2. **Rule activation** - Enabled custom Suricata rules and Wazuh correlation
   rules.
3. **Observation window** - Monitored for 1 hour with no attack traffic.
   Recorded any false positives.
4. **Iteration** - Adjusted thresholds until zero false positives during
   baseline, while simulated attacks (hydra, nmap, curl injection) still
   triggered within expected timeframes.
5. **Documentation** - Final thresholds recorded in `threshold.config` and
   `local_rules.xml`.

---

## Tuning Decisions Not Made

The following were consciously excluded from this lab tuning:

| Decision | Why Not Applied |
|----------|-----------------|
| Whitelist internal IP ranges | Lab is small (3–4 hosts). In production, whitelist backup servers, monitoring tools, and CI/CD pipelines. |
| DNS-based false positive suppression | Not relevant - no DNS rules in custom ruleset. Would apply if using Emerging Threats DNS rules. |
| GeoIP filtering | Single-lab environment. In production, restrict `$EXTERNAL_NET` to non-business countries to reduce attack surface. |

Mentioning these in an interview demonstrates awareness of enterprise tuning
practices beyond the lab scope.

---

## Tuning Summary

| Component        | What Was Tuned                               | Result |
|------------------|----------------------------------------------|--------|
| Suricata rule    | SSH brute-force inline threshold (5/30s)     | Caught hydra attacks, zero false positives on admin SSH |
| threshold.config | SSH brute-force output threshold (10/60s)    | Suppressed backup script noise without losing detection |
| Wazuh rule       | Correlation windows and frequencies          | Single events logged, bursts escalated, analyst notified only on confident incidents |
| Port scan rule   | Deliberately left sensitive (20/5s, no post-threshold) | Reliable nmap detection, no legitimate traffic triggers |

The result: a detection pipeline that fires accurately on real attacks
while remaining quiet during normal operations.
