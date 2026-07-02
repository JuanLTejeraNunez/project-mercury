from cryptography.hazmat.primitives import serialization

pkcs1_path = r'C:\Users\jltej\.secrets\kalshi_pkcs1.pem'
pkcs8_path = r'C:\Users\jltej\.secrets\kalshi_private.pem'

with open(pkcs1_path, 'rb') as f:
    pkcs1_data = f.read()

private_key = serialization.load_pem_private_key(
    pkcs1_data,
    password=None,
)

pkcs8_data = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption(),
)

with open(pkcs8_path, 'wb') as f:
    f.write(pkcs8_data)

print('Clave convertida correctamente a PKCS8.')


