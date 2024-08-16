import requests
import uuid

from etc import AUTH_NAMESPACE

def auth(username, password):
	mac = get_mac_address()
	res = requests.post('https://tellurium.ejae8319.workers.dev/api/users/auth', json={
		"project": AUTH_NAMESPACE,
		"username": username,
		"password": password,
		"code": mac,
	})
	return res.ok

def get_mac_address():
	id = uuid.getnode()
	mac = ':'.join(("%012X" % id)[i:i + 2] for i in range(0, 12, 2))
	return mac