import requests
import uuid

from etc import AUTH_NAMESPACE, AUTH_ID

def auth():
	mac = get_mac_address()
	res = requests.post('https://oxigeno.ejae8319.workers.dev/kv', json = {
		'namespace': AUTH_NAMESPACE,
		'id': AUTH_ID,
		'mac_address': mac
	})
	return res.ok

def get_mac_address():
	id = uuid.getnode()
	mac = ':'.join(("%012X" % id)[i:i + 2] for i in range(0, 12, 2))
	return mac