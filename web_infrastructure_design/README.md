# Web Infrastructure Design

Note: The task files in this directory (0-simple_web_stack, 1-distributed_web_infrastructure, etc.)
should contain ONLY the URL to your uploaded diagram screenshot. All explanations are documented here.

Acronyms:
- LAMP: Linux + (Apache/Nginx) + MySQL + PHP/Python
- SPOF: Single Point of Failure
- QPS: Queries/Requests Per Second


## 0. Simple web stack (1 server)
### Components (required)
- Domain: foobar.com with `www` record pointing to 8.8.8.8 (A record)
- 1 server (8.8.8.8) running:
  - Nginx (web server)
  - Application server
  - Application files (code base)
  - MySQL (database)

### Request flow
User -> DNS lookup (www.foobar.com -> 8.8.8.8) -> TCP/IP -> HTTP/HTTPS -> Nginx -> App server -> MySQL -> response.

### What each part does
- Server: machine providing services over a network
- Domain name: human-friendly name mapped to an IP via DNS
- DNS record type for www: A record (IPv4 -> 8.8.8.8)
- Web server (Nginx): handles HTTP, serves static content, reverse-proxies to app server
- App server: runs the backend logic / dynamic content
- Database (MySQL): persistent data storage
- Communication: TCP/IP + HTTP (80) / HTTPS (443)

### Issues
- SPOF: one server failure = total outage
- Downtime on deploy/maintenance: restarting services causes outage
- Cannot scale horizontally: limited by single machine resources


## 1. Distributed web infrastructure (3 servers)
### Added components (and why)
- 1 Load balancer (HAProxy): distributes traffic, improves availability, helps scale
- 1 extra backend server: redundancy + capacity
- DB Primary–Replica: read scalability + redundancy for data copy

### Typical design
User -> DNS -> HAProxy -> (Server1 OR Server2)
Each backend server has: Nginx + App server + App files + MySQL (Primary on one, Replica on the other)

### Load balancing algorithm
- Round Robin: sends requests to servers in rotation (S1, S2, S1, S2...)

### Active-Active vs Active-Passive
- This setup is Active-Active for web/app: both backends serve traffic at the same time.
- Active-Passive would keep one backend idle until failover.

### MySQL Primary–Replica (Master–Slave)
- Primary accepts writes and logs changes (binlog)
- Replica replays changes to stay in sync (often async)
- App writes to Primary; reads can optionally go to Replica (but replica may lag)

### Issues
- SPOF: load balancer (only one), and DB Primary for writes
- Security: no firewall, no HTTPS
- No monitoring: failures/performance issues may go unnoticed


## 2. Secured and monitored web infrastructure (3 servers, secured)
### Added components (and why)
- 3 firewalls: restrict traffic per server, reduce attack surface
- 1 SSL certificate (HTTPS): encrypt + integrity + server authentication for users
- 3 monitoring agents/clients: collect logs/metrics from each server

### Firewalls (what they do)
Filter traffic by rules (IP/port/protocol). Example intent:
- Allow 443 to LB from the internet
- Allow backend traffic only from LB to app/web servers
- Allow DB traffic only from app servers (not public internet)

### Why HTTPS
Encrypts data in transit, prevents sniffing/tampering, protects credentials/cookies.

### Monitoring (what it’s used for)
Availability, latency, errors, CPU/RAM/disk, traffic anomalies, alerting.

### How monitoring collects data
Agents on each server collect system metrics + service logs/metrics and ship them to a monitoring platform (e.g., Sumologic/Datadog/Prometheus).

### Monitoring web server QPS
- Enable Nginx metrics (stub_status) or parse access logs
- Export to monitoring system and graph requests/sec
- Set alerts for unusual spikes/drops

### Issues
- SSL termination at LB: LB->backend traffic may be unencrypted (sniffing risk on internal network)
- Only one MySQL server accepting writes: Primary is still a write SPOF; failover needed
- Same components on each server: resource contention, harder scaling, larger blast radius if compromised


## 3. Scale up (higher availability + split roles)
(Usually adds: one extra server, a second load balancer clustered with the first, and splits web/app/db onto dedicated servers.)

### Why add a 2nd load balancer (cluster)
Removes LB as a SPOF. A common pattern is a floating VIP with failover (Active-Passive for the LB layer).

### Why split components onto separate servers
- Scale web, app, and DB independently
- Reduce resource contention
- Improve security boundaries (DB is more protected)
- Easier maintenance and tuning
