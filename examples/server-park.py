import pyblaise

_, x = pyblaise.get_auth_token("https", "dev-ed-48-client-tel.social-surveys.gcp.onsdigital.uk", 8031, "Root", "Root")
z = pyblaise.get_server_park_definitions("https", "dev-ed-48-client-tel.social-surveys.gcp.onsdigital.uk", 8031, x)

print (z)
