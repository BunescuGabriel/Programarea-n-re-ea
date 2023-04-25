import socket
import dns.resolver
import dns.reversename
from ipwhois import IPWhois

flag=0
print(f'Bun venit la aplicația DNS! \npentru început, aici sunt disponibile comenzi:\n'
      f'* /commands - arată lista de comenzi\n'
      f'* /resolve_domain / resolve_ip> - arată o listă de adrese IP atribuite domeniului sau o listă de domenii atribuite adresei IP\n'
      f'* /use_dns<ip> comutați serverul DNS pentru a răsfoi comenzile precedente')
resolver = dns.resolver.Resolver(configure=False)
while True:

    try:
        message=input('tastați comanda:\n')

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
                        print(f"Serverul DNS nu a fost găsit sau inaccesibil")
                except :
                    print(f"Nu a fost găsită nicio înregistrare DNS pentru acest domeniu")
        elif '/resolve_ip' in message:
            ip_addr = input("tastați adresa ip:\n")
            if flag==0:
                hostname = socket.gethostbyaddr(ip_addr)[0]
                print(f'numele de domeniu este:{hostname}')
            elif flag==1:
                try:
                    domain_name = dns.reversename.from_address(ip_addr)
                    result = resolver.resolve(domain_name, 'PTR')
                    # Extrageți numele de gazdă din rezultat
                    hostname = result[0].to_text().rstrip('.')
                    # Tipăriți numele de gazdă returnat de serverul DNS
                    print(hostname)
                except dns.resolver.NoNameservers:
                    print(f"Serverul DNS nu a fost găsit sau inaccesibil")
                except dns.resolver.NXDOMAIN:
                    print(f"Nu a fost găsită nicio înregistrare DNS pentru adresa IP {ip_addr}")
        elif '/use_dns' in message and flag==0:
            flag=1
            dns_addr=input("introduceți adresa dns")
            resolver.nameservers = [dns_addr]
            print(f'trecut la {dns_addr} dns')
        elif '/use_dns' in message and flag == 1:
            dns_addr = input("introduceți adresa dns")
            if 'default' in dns_addr:
                flag=0
                print(f'a trecut la dns implicit')
    except:
      print('error')