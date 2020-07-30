import pyblaise

protocol = os.getenv("PROTOCOL", "https")
hostname = os.environ["HOSTNAME"]
username = os.environ["USERNAME"]
password = os.environ["PASSWORD"]
port = int(os.environ["PORT"])

_, x = pyblaise.get_auth_token(protocol, hostname, port, username, password)
z = pyblaise.get_server_park_definitions(protocol, hostname, port, x)

print (z)
