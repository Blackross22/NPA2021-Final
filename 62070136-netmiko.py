from netmiko import ConnectHandler

if __name__ == '__main__':
    device_ip = "10.0.15.106"
    username = "cisco"
    password = "cisco"
    device_params = {'device_type': 'cisco_ios',
                    'ip': device_ip,
                    'username': username,
                    'password': password,
    }

def get_info(device_params):
    with ConnectHandler(**device_params) as ssh:
        info = ssh.send_command('sh ip int br')
        return info
def checkLoopback(device_params, name, ip):
    status = 0
    result = get_info(device_params)
    line = result.strip().split('\n')
    for word in line[1:]:
        descri = word.split()
        if descri[0][0] == "L":
            if descri[0] == name and descri[1] == ip:
                status += 1
            elif descri[0] == name and descri[1] != ip:
                status == 0
            else:
                with ConnectHandler(**device_params) as ssh:
                    print(ssh.send_config_set(delete_loopback + descri[0]))
    if status == 0:
        with ConnectHandler(**device_params) as ssh:
            print(ssh.send_config_set(create_loopback))
            return ssh.send_command('sh ip int br')
    else:
        return "loopback62070136 already configured"
            
def save_config():
    with ConnectHandler(**device_params) as ssh:
        print(ssh.send_command("wr"))

create_loopback = ["int lo62070136", "ip add 192.168.1.1 255.255.255.0", "no sh"]
delete_loopback = "no int "

print(checkLoopback(device_params, "Loopback62070136", "192.168.1.1"))
save_config()

