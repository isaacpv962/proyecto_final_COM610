import paho.mqtt.client as mqtt
import time
import json
import random

# --- Configuración ---
BROKER = "34.201.16.79"
PORT = 1883
TOPIC = "sensores/laboratorio"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Conectado exitosamente al broker en {BROKER}")
    else:
        print(f"Error al conectar. Código: {rc}")

# --- Inicialización ---
client = mqtt.Client(client_id="Simulador_Linux")
client.on_connect = on_connect

# Conectar al servidor de AWS
client.connect(BROKER, PORT, 60)
client.loop_start()

try:
    print("Iniciando envío de datos dummy. Presiona Ctrl+C para detener.")
    while True:
        # Generar datos aleatorios realistas (Ej: Temperatura y Humedad)
        temperatura = round(random.uniform(18.0, 26.0), 2)
        humedad = round(random.uniform(40.0, 65.0), 2)
        
        # Estructurar el payload en JSON
        payload = {
            "temperatura": temperatura,
            "humedad": humedad,
            "estado": "operativo"
        }
        
        mensaje = json.dumps(payload)
        
        # Publicar en el tópico
        client.publish(TOPIC, mensaje)
        print(f"[->] Enviado a {TOPIC}: {mensaje}")
        
        # Esperar 3 segundos antes del siguiente envío
        time.sleep(3)
        
except KeyboardInterrupt:
    print("\nSimulación detenida por el usuario.")
    client.loop_stop()
    client.disconnect()