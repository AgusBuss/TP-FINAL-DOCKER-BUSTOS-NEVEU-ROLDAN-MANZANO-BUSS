# Prueba del webhook HTTP

Todos los comandos se ejecutan desde la carpeta raíz del proyecto (PowerShell en Windows).

## Requisitos

- La plataforma está levantada (`docker compose up -d`).
- El workflow "Webhook HTTP" está importado y publicado en n8n.
- El archivo `hosts` tiene la línea `127.0.0.1 n8n.lab.test`.

## 1. Solicitud válida

Datos enviados (`pruebas/valida.json`):

```json
{"dispositivo":"esp32-02","tipo":"humedad","valor":55.2}
```

Comando:

```powershell
curl.exe -i -X POST http://n8n.lab.test:8081/webhook/lecturas -H "Content-Type: application/json" -d "@pruebas/valida.json"
```

Resultado esperado: `HTTP/1.1 201 Created` y un cuerpo similar a:

```json
{"ok":true,"result":{"id":6,"status":"created"}}
```

El `id` es el del registro realmente creado en PostgreSQL, así que varía según los registros previos.

## 2. Solicitud inválida

Datos enviados (`pruebas/invalida.json`), sin `tipo` y con `valor` como texto:

```json
{"dispositivo":"esp32-03","valor":"abc"}
```

Comando:

```powershell
curl.exe -i -X POST http://n8n.lab.test:8081/webhook/lecturas -H "Content-Type: application/json" -d "@pruebas/invalida.json"
```

Resultado esperado: `HTTP/1.1 400 Bad Request` y el cuerpo:

```json
{"ok":false,"error":"Datos inválidos: se requieren dispositivo, tipo y valor numérico"}
```

## 3. Verificar que el registro quedó guardado

- **Aplicación web:** abrir http://app.lab.test:8081/lecturas. El registro nuevo aparece con origen `http`.
- **pgAdmin:** abrir http://db.lab.test:8081, ir a la tabla `lecturas` y elegir Ver/Editar datos → Todas las filas.
- **Terminal:**

```powershell
docker compose exec postgres psql -U admin -d plataforma -c "SELECT * FROM lecturas ORDER BY id DESC LIMIT 5;"
```

## Si no se configuró el archivo hosts

Se puede probar igual indicando a curl dónde está el nombre:

```powershell
curl.exe -i --resolve n8n.lab.test:8081:127.0.0.1 -X POST http://n8n.lab.test:8081/webhook/lecturas -H "Content-Type: application/json" -d "@pruebas/valida.json"
```