# Reto Técnico AppSec / GenAI – Mercado Libre

Este repositorio documenta el desarrollo y análisis de una prueba técnica para el equipo de AppSec / GenAI de Mercado Libre. El objetivo fue construir un agente conversacional conectado a un MCP (Mail Control Point), evaluar su seguridad, y aplicar buenas prácticas de protección contra ataques comunes en entornos de IA generativa.

## Descripción del Reto

El desafío consistió en:

- Desarrollar una aplicación de línea de comandos que interactúe con un servidor MCP.
- El MCP expone dos herramientas básicas:
  - `list_emails`: listar todos los correos.
  - `get_email_by_id`: obtener un correo por ID.
- El sistema contiene una variable de entorno secreta (una "bandera") que debe mantenerse protegida.
- El reto incluye simular un ataque que permita exfiltrar esta bandera mediante un correo malicioso y herramientas vulnerables.

## Solución Propuesta

Se desarrollaron dos versiones del agente:

### 1. Agente Vulnerable

- Implementado con `FastMCP`.
- Herramientas adicionales habilitadas:
  - `list_emails`
  - `get_email`
  - `send_email`
  - `run_shell_command`
- Permite que un correo malicioso contamine el flujo del agente y ejecute comandos para extraer la bandera secreta.
- Utiliza `Strands Agents` y `OpenAI GPT-4`.

### 2. Agente Protegido

Se aplicaron múltiples controles de seguridad inspirados en principios OWASP y AppSec:

- **Principio de mínimo privilegio**: se eliminó la herramienta `run_shell_command`.
- **Trazabilidad**: se habilitaron logs para auditar acciones del agente.
- **Human-in-the-loop**: se requiere autorización explícita del usuario para ejecutar herramientas de modificación (como `send_email`).
- **Validación de entradas/salidas**:
  - Se integró la API de moderación de OpenAI como sistema de guardrails.
  - Evalúa tanto el prompt de entrada como la respuesta generada antes de ejecutar herramientas.

## Logros Alcanzados

- Se logró simular exitosamente un ataque de prompt injection en el agente vulnerable.
- Se implementó un flujo de protección que incluye validación, autorización y trazabilidad.
- Se documentó el proceso de exfiltración de prompts de sistema de modelos GPT, disponible en la carpeta `red_teaming`.


## Observaciones y Mejoras Futuras

### MCP

- Actualmente el MCP tiene acceso irrestricto a todos los correos.
- Se recomienda implementar autenticación con `Auth0`, `OAuth 2.0`, `PKCE` y `JWT` para filtrar correos por usuario.
- Posible integración de filtros de spam y sanitización de contenido (e.g. imágenes, caracteres especiales).

### Agente

- Los guardrails pueden ser extendidos para evaluar también las herramientas activadas.
- Se sugiere usar sistemas más robustos para detección de prompt injection y prompt hacking.
- Diseño transversal del agente para limitar capacidades a lo estrictamente necesario.

## Estructura de repositorio

~~~bash
.
├── agent
│   ├── guardrails.py
│   ├── __init__.py
│   ├── protected_hook.py
│   ├── protected.py
│   ├── protected_telemetry.py
│   ├── __pycache__
│   │   └── guardrails.cpython-312.pyc
│   └── vulnerable.py
├── data
│   └── sample_base.json
├── logs
│   ├── strands_agents_sdk.log
│   └── strands_telemetry.jsonl
├── Makefile
├── mcp
│   ├── client.py
│   ├── __init__.py
│   ├── mail_client.py
│   ├── main.py
│   └── __pycache__
│       └── mail_client.cpython-312.pyc
├── pyproject.toml
├── README.md
├── .env.example
├── red_teaming
│   ├── gpt_prompt_extraction.md
│   ├── MELIGPT_Easy.pdf
│   └── MELIGPT_Hard.pdf
└── uv.lock
~~~

## Uso

Para ejecutar la solución se debe agregar un archivo .env con las siguientes características:
~~~bash
OPENAI_API_KEY = "sk-123"
SECRET_KEY="sk_live_mock_123"
~~~

Luego ejecutar los siguientes componentes:
1. Ejecutar MCP server
~~~bash
make mcp-v
~~~

2. Ejecutar agente vulnerable
~~~bash
make run-v-agent
~~~

3. Ejecutar agente protegido
~~~bash
make run-p-agent
~~~