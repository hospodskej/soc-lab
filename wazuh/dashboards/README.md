# Wazuh Dashboards for SOC Lab

The following dashboards were created in Wazuh 4.14.5 to support triage and
visualisation of Suricata alerts. Screenshots are not available because the
lab environment is currently offline, but the layouts and correlation logic
are described below.

---

## 1. Suricata Alerts Overview
- **Pie chart:** Alert severity distribution (High/Medium/Low)
- **Bar chart:** Top alert signatures (brute‑force, port scan, exploitation)
- **Data table:** Recent 50 events with timestamp, source IP, destination, alert
- **Filters:** `rule.groups: suricata`, time range = last 24 hours

This dashboard gives the SOC analyst an immediate situational awareness of
active threats across the segmented network.

## 2. Brute‑Force Triage
- **Correlation alert highlight:** Custom Wazuh rule 100002 (level 10) fires
  when ≥3 SSH brute‑force alerts (Suricata SID 1000001) from the same source
  are seen within 60 seconds.
- **Top offenders table:** Source IP, number of attempts, first/last seen,
  automatic response status (manual block via firewall API).
- **Timeline:** Events colour‑coded by source IP, showing the burst pattern.

---

+-------------------+  +---------------------+
| Severity Pie       |  | Alerts by Signature |
|  H: 3 (25%)  red   |  | Exploit   : 3      |
|  M: 5 (42%)  orange|  | Brute-force: 5     |
|  L: 4 (33%)  blue  |  | Port scan : 4      |
+-------------------+  +---------------------+
| Recent Events Table                         |
| Time     | Src IP          | Dest      | Sig|
| 08:20:25 | 10.99.99.100   | 10.0.2.10 | CMD|
| ...                                        |
+----------------------------------------------+

*The configurations that feed these dashboards are in `../local_rules.xml`
and `../ossec.conf`. Sample log data that generated the views is available in
`../../suricata/logs/sample-eve.json`.*
