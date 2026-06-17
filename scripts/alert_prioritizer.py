import json
import sys
from collections import defaultdict

def load_alerts(filename):
    alerts = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                alerts.append(json.loads(line))
    return alerts

def prioritize(alerts):
    # severity mapping: lower number = higher urgency
    ip_stats = defaultdict(lambda: {'total': 0, 'high': 0, 'medium': 0, 'low': 0})

    for alert in alerts:
        if alert.get('event_type') != 'alert':
            continue
        src_ip = alert.get('src_ip', 'unknown')
        severity = alert.get('alert', {}).get('severity', 3)
        ip_stats[src_ip]['total'] += 1
        if severity == 1:
            ip_stats[src_ip]['high'] += 1
        elif severity == 2:
            ip_stats[src_ip]['medium'] += 1
        else:
            ip_stats[src_ip]['low'] += 1

    return sorted(ip_stats.items(),
                  key=lambda x: (x[1]['high'], x[1]['total']),
                  reverse=True)

def main():
    if len(sys.argv) != 2:
        print("Usage: python alert_prioritizer.py <eve.json>")
        sys.exit(1)

    alerts = load_alerts(sys.argv[1])
    ranked = prioritize(alerts)

    print("Prioritized List of Source IPs (High Sev > Medium Sev > Total Alerts):\n")
    for ip, stats in ranked:
        print(f"{ip:15s}  High:{stats['high']:2d}  Med:{stats['medium']:2d}  "
              f"Low:{stats['low']:2d}  Total:{stats['total']:3d}")

if __name__ == "__main__":
    main()
