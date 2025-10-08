# Deployment Information

## Server Details
- **Public IP**: 172.206.32.165
- **Port**: 8080
- **Protocol**: HTTP

## Access URLs

### All Pages Available:
1. **Homepage**: http://172.206.32.165:8080/rail-100-localized.html
2. **Banking Partners**: http://172.206.32.165:8080/rail-banking-partners-100-localized.html
3. **Blog**: http://172.206.32.165:8080/rail-blog-100-localized.html
4. **Company**: http://172.206.32.165:8080/rail-company-100-localized.html
5. **Contact**: http://172.206.32.165:8080/rail-contact-100-localized.html
6. **How It Works**: http://172.206.32.165:8080/rail-how-it-works-100-localized.html
7. **Payment Clients**: http://172.206.32.165:8080/rail-payment-clients-100-localized.html

## Directory Listing
http://172.206.32.165:8080/

## Server Status
- Status: ✓ Running
- Process ID: 50930
- Server Type: Python http.server
- Directory: /home/azureuser/replica

## Notes
- All files are 100% localized (critical dependencies embedded)
- Server is running in background via nohup
- Logs available at: /home/azureuser/replica/server.log

## Stop Server
To stop the server:
```bash
kill 50930
```

## Restart Server
```bash
cd /home/azureuser/replica
nohup python3 -m http.server 8080 > server.log 2>&1 &
```

## Firewall Note
If URLs are not accessible externally, ensure port 8080 is open:
```bash
sudo ufw allow 8080/tcp
# OR for Azure Network Security Group
# Add inbound rule for port 8080
```
