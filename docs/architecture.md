## Segmentation (VMware Workstation)

Three virtual networks enforce logical separation:

| Segment | VMnet  | Subnet         | Purpose                              | Hosts                             |
|---------|--------|----------------|--------------------------------------|-----------------------------------|
| WAN     | VMnet8 | 192.168.6.0/24 | Internet access via host NAT         | pfSense em0                       |
| LAN     | VMnet2 | 10.0.1.0/24    | Analyst workstations, SIEM, admin    | pfSense em1 (.1), Kali Purple,    |
|         |        |                |                                      | Wazuh-Ubuntu VM                   |
| DMZ     | VMnet3 | 10.0.2.0/24    | Public-facing services, target hosts | pfSense em2 (.1), Windows victim  |

The LAN segment serves double duty as both the analyst network and the
management network — all security tools and the analyst
workstation reside here.
