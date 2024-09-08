# LangchainFastAPIDocker

Prueba técnica de Nunsys: integración de Langchain, vectorStore, FastAPI, Docker y Vue3

Este proyecto implementa un chatbot utilizando OpenAI GPT-3.5 y OpenWeatherMap. El chatbot puede consultar información meteorológica a través de OpenWeatherMap o responder preguntas basadas en documentos que contienen la experiencia y currículum de Ricardo Montaner.

## Tecnologías utilizadas
- **Langchain**: Para la gestión del flujo conversacional y los agentes.
- **ChromaDB**: Como base de datos de vectores para gestionar el almacenamiento de documentos.
- **FastAPI**: Para servir la API del chatbot.
- **Docker**: Para contener y desplegar la aplicación.
- **Vue3**: Para la interfaz de usuario.
- **OpenWeatherMap**: Para la obtención de datos meteorológicos.

## Requisitos
- API key de OpenAI (ChatGPT 3.5).
- API key de OpenWeatherMap.
- Python 3.8+.

## Instalación

### 1. Crear entorno virtual (recomendado)
Se recomienda crear un entorno virtual para aislar las dependencias del proyecto:

```bash
python -m venv venv
source venv/bin/activate  # En Linux/MacOS
venv\Scripts\activate  # En Windows
```

### 2. Configurar API keys
Crea un archivo .env en la raíz del proyecto con las siguientes claves:
```bash
OPENAI_API_KEY=your_openai_api_key
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key
```

### 3. Instalar dependencias
Ejecuta el siguiente comando para instalar todas las dependencias necesarias:

```bash
pip install -r requirements.txt
```

### Ejecución de la API con FastAPI
Para iniciar el servidor FastAPI en modo desarrollo, ejecuta:
```fastapi dev main.py```

### Pruebas via Cli
Ejecutar la clase ChatBot.py con 
```
cd ./app
python ChatBot.py
```


### Uso de Docker
Este proyecto está preparado para ejecutarse en un contenedor Docker. Para construir y ejecutar la imagen, sigue estos pasos:
1. Construir la imagen Docker:
```docker build -t langchain-fastapi .```
2. Ejecutar el contenedor:
```docker run -p 8000:8000 langchain-fastapi```

Con estos comandos, tendrás la aplicación corriendo y accesible en http://localhost:8000.

### Autor
Nombre: Ricardo Montaner Lopez
Email: ricardo.montanet135@gmail.com
LinkedIn: https://www.linkedin.com/in/ricardo-montaner-lopez-13b09456/
GitHub: https://github.com/Ygeth?tab=repositories
Este proyecto es parte de una prueba técnica para Nunsys, creada para demostrar las capacidades de integración entre Langchain, ChromaDB, FastAPI y Docker. Si tienes preguntas o sugerencias, no dudes en ponerte en contacto.