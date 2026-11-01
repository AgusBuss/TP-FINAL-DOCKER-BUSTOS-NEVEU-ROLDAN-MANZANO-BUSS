# Prueba MQTT request/reply

Todos los comandos se ejecutan desde la carpeta raíz del proyecto (PowerShell en Windows). Las herramientas `mosquitto_sub` y `mosquitto_pub` se ejecutan dentro del contenedor de Mosquitto, así que no hace falta instalarlas en la PC.

## Tópicos

- Solicitud: `lab/g1/req/lecturas.create`
- Respuesta: `lab/g1/res/lecturas/<correlation_id>`, indicado por el cliente en el campo `reply_to`.

n8n solo publica la respuesta si `reply_to` empieza con `lab/g1/res/`.

## Requisitos

- La plataforma está levantada (`docker compose up -d`).
- El workflow "MQTT - Registrar lectura" está importado y publicado en n8n.

## Mensaje de solicitud

Archivo `pruebas/mqtt.json`:

```json
{
  "correlation_id": "req-001",
  "reply_to": "lab/g1/res/lecturas/req-001",
  "data": {
    "dispositivo": "esp32-01",
    "tipo": "temperatura",
    "valor": 24.8
  }
}
```

## Procedimiento

**Terminal 1: escuchar la respuesta** (queda esperando, no cerrarla):

```powershell
docker compose exec mosquitto mosquitto_sub -h localhost -t "lab/g1/res/lecturas/req-001" -v
```

**Terminal 2: publicar la solicitud:**

```powershell
Get-Content pruebas/mqtt.json -Raw | docker compose exec -T mosquitto mosquitto_pub -h localhost -t "lab/g1/req/lecturas.create" -s
```

## Resultado esperado

En la Terminal 1 aparece la respuesta:

```
lab/g1/res/lecturas/req-001 {"ok":true,"correlation_id":"req-001","result":{"id":7,"status":"created"}}
```

- El `correlation_id` coincide con el de la solicitud.
- El `id` es el del registro realmente creado en PostgreSQL, así que varía según los registros previos.

## Verificar que el registro quedó guardado

- **Aplicación web:** http://app.lab.test:8081/lecturas. El registro nuevo aparece con origen `mqtt`.
- **pgAdmin:** http://db.lab.test:8081, tabla `lecturas`, Ver/Editar datos.
- **Terminal:**

```powershell
docker compose exec postgres psql -U admin -d plataforma -c "SELECT * FROM lecturas ORDER BY id DESC LIMIT 5;"
```

## Alternativa con las herramientas instaladas en la PC

Si `mosquitto_pub` y `mosquitto_sub` están instalados en el equipo anfitrión (Linux o Mac):

```bash
mosquitto_sub -h localhost -p 1883 -t "lab/g1/res/lecturas/req-001" -v
```

En otra terminal:

```bash
mosquitto_pub -h localhost -p 1883 -t "lab/g1/req/lecturas.create" -f pruebas/mqtt.json
```

## Cómo probar otro mensaje

Para repetir la prueba hay que cambiar el `correlation_id` y el `reply_to` (por ejemplo `req-002`) y suscribirse al nuevo tópico de respuesta.