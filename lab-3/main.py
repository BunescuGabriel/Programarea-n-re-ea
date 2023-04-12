import socket
import dns.resolver
import dns.reversename
from ipwhois import IPWhois

flag=0
print(f'Welcome to DNS application! \nfor begining here are disponible commands:\n'
      f'* /commands - arată lista de comenzi\n'
      f'* /resolve_domain / resolve_ip> - arată o listă de adrese IP atribuite domeniului sau o listă de domenii atribuite adresei IP\n'
      f'* /use_dns<ip> comutați serverul DNS pentru a răsfoi comenzile precedente')
resolver = dns.resolver.Resolver(configure=False)
while True:

    try:
        message=input('type the command:\n')

        if '/commands' in message:
            print(f'* /resolve<domain/ip> - afișează o listă de adrese IP atribuite domeniului sau o listă de domenii atribuite adresei IP\n'
                  f'* /use_dns<ip> comutați serverul DNS pentru a răsfoi comenzile precedente')
        elif '/resolve_domain' in message:
            domain=input('type the domain:\n')
            if flag==0:
                ip_address = socket.gethostbyname_ex(domain)[2]
                for i in range(len(ip_address)):
                    print(f'the ip adress:{ip_address[i]}')
            if flag ==1:
                try:
                    result = resolver.resolve(domain)
                    for rdata in result:
                        print(f'{domain} has IP address {rdata.address}.')
                except dns.resolver.NoNameservers:
                        print(f"DNS server not found or unreachable")
                except :
                    print(f"No DNS record found for this  domain")
        elif '/resolve_ip' in message:
            ip_addr = input("type the ip adress:\n")
            if flag==0:
                hostname = socket.gethostbyaddr(ip_addr)[0]
                print(f'the domain name is:{hostname}')
            elif flag==1:
                try:
                    domain_name = dns.reversename.from_address(ip_addr)
                    result = resolver.resolve(domain_name, 'PTR')
                    # Extract the hostname from the result
                    hostname = result[0].to_text().rstrip('.')
                    # Print the hostname returned by the DNS server
                    print(hostname)
                except dns.resolver.NoNameservers:
                    print(f"DNS server not found or unreachable")
                except dns.resolver.NXDOMAIN:
                    print(f"No DNS record found for IP address {ip_addr}")
        elif '/use_dns' in message and flag==0:
            flag=1
            dns_addr=input("type the dns adress")
            resolver.nameservers = [dns_addr]
            print(f'switched to {dns_addr} dns')
        elif '/use_dns' in message and flag == 1:
            dns_addr = input("type the dns adress")
            if 'default' in dns_addr:
                flag=0
                print(f'switched to default dns')
        #ip_adress = socket.gethostbyname(domain_name)

        #print(f'the ip of {domain_name} is {ip_adress}')
    except:
      print('error')