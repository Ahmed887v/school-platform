from cryptography.fernet import Fernet
import hashlib
import base64
from django.conf import settings

def encrypt_data(data):
    if not data: return data
    cipher = Fernet(settings.ENCRYPTION_KEY)
    encrypted = cipher.encrypt(data.encode())
    return base64.urlsafe_b64encode(encrypted).decode()

def decrypt_data(encrypted_data):
    if not encrypted_data: return encrypted_data
    cipher = Fernet(settings.ENCRYPTION_KEY)
    decrypted = cipher.decrypt(base64.urlsafe_b64decode(encrypted_data.encode()))
    return decrypted.decode()

def secure_hash(data):
    """تشفير الهاش الحساس (National ID, Phone) بـ PBKDF2 بمعدل 650,000 تكرار"""
    salt = b'some-static-salt-value'
    iterations = 650_000
    return hashlib.pbkdf2_hmac('sha256', data.encode(), salt, iterations)
