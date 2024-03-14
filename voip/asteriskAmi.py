import asterisk.manager


address = '192.168.23.10'
port = 5038
username = 'amiuser'
password = 'ami@user'

def connect_to_ami():
    ami = asterisk.manager.Manager()
    try:
        ami.connect(address, port)
        ami.login(username, password)
        return ami
    except Exception as e:
        print(f"Error connecting to AMI: {e}")
        return None