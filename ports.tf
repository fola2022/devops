variable "rules" {
  description = "Map of known security group rules (define as 'name' = ['from port', 'to port', 'protocol', 'description'])"
  type        = map(list(any))
  default = {
    # DNS
    dns-udp = [53, 53, "udp", "DNS"]
    dns-tcp = [53, 53, "tcp", "DNS"]
   
    # HTTP
    http-tcp   = [80, 80, "tcp", "HTTP"]
    
    # HTTPS
    https-tcp  = [443, 443, "tcp", "HTTPS"]
    
    # Kerberos
    kdc-tcp	= [88, 88, "tcp", "Kerberos"]
    kdcs-tcp = [464, 464, "tcp", "Kerberos"]

    # Kubernetes
    kubernetes-api-tcp = [6443, 6443, "tcp", "Kubernetes API Server"]
   
    # LDAP
    ldap-tcp = [389, 389, "tcp", "LDAP"]
    ldap-udp = [389, 389, "udp", "LDAP"]
    # LDAPS
    ldaps-tcp = [636, 636, "tcp", "LDAPS"]
    
    # MySQL
    mysql-tcp = [3306, 3306, "tcp", "MySQL/Aurora"]

    # NFS/EFS
    nfs-tcp = [2049, 2049, "tcp", "NFS/EFS"]

    # NTP
    ntp-udp	= [123, 123, "udp", "NTP"]

    # PostgreSQL
    postgresql-tcp = [5432, 5432, "tcp", "PostgreSQL"]

    # RDP
    rdp-tcp = [3389, 3389, "tcp", "Remote Desktop"]
    rdp-udp = [3389, 3389, "udp", "Remote Desktop"]

    # SMB
    smb-tcp = [445, 445, "tcp", "Server Message Block"]
    smb-udp = [445, 445, "udp", "Server Message Block"]

    # SSH
    ssh-tcp = [22, 22, "tcp", "SSH"]

    # Open all ports & protocols
    all-all       = [-1, -1, "-1", "All protocols"]
    all-tcp       = [0, 65535, "tcp", "All TCP ports"]
    all-udp       = [0, 65535, "udp", "All UDP ports"]
    all-icmp      = [-1, -1, "icmp", "All IPV4 ICMP"]
    all-ipv6-icmp = [-1, -1, 58, "All IPV6 ICMP"]

    ad-tcp  = [3268, 3269, "tcp", "AD Global catalog"]
    rpc-tcp = [135, 135, "tcp", "RPC"]

  }

}

# variable "ad_rules" {
#   description = "Map of known security group rules (define as 'name' = ['from port', 'to port', 'protocol', 'description'])"
#   type        = map(list(any))
#   default = {
#     # AD Global catalog
#     ad-tcp  = [3268, 3269, "tcp", "AD Global catalog"]
#     # DNS
#     dns-udp = [53, 53, "udp", "DNS"]
#     dns-tcp = [53, 53, "tcp", "DNS"]

#     # LDAP
#     ldap-tcp = [389, 389, "tcp", "LDAP"]
#     ldap-udp = [389, 389, "udp", "LDAP"]
#     # LDAPS
#     ldaps-tcp = [636, 636, "tcp", "LDAPS"]

#     # Kerberos
#     kdc-tcp	= [88, 88, "tcp", "Kerberos"]
#     kdcs-tcp = [464, 464, "tcp", "Kerberos"]

#     # NTP
#     ntp-udp	= [123, 123, "udp", "NTP"]

#     rpc-tcp = [135, 135, "tcp", "RPC"]


#     # SMB
#     smb-tcp = [445, 445, "tcp", "Server Message Block"]
#     smb-udp = [445, 445, "udp", "Server Message Block"]






