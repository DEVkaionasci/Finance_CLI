from hashlib import pbkdf2_hmac
import hmac
import os

def gerar_senha(senha):
    salt = os.urandom(16)
    iteracoes = 600000

    hash_senha = pbkdf2_hmac(
        'sha256', 
        senha.encode('utf-8'), 
        salt, 
        iteracoes
    )

    return salt, hash_senha

def verificar_senha(senha_digitada, salt_salvo, hash_salvo):
    iteracoes = 600000

    hash_digitado = pbkdf2_hmac(
        'sha256',
        senha_digitada.encode('utf-8'),
        salt_salvo,
        iteracoes
    )

    return hmac.compare_digest(hash_digitado, hash_salvo)