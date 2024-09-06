# LangchainFastAPIDocker
Prueba tecnica de nunsys, integra Langchain, vectorStore, FastAPI, Docker y Vue3

Este proyecto utiliza OpenAI ChatGPT3.5 como LLM y OpenWeatherMap como herramienta para extraer datos metereologicos. Sera necesario las api keys de ambas aplicaciones


## Instalacion
* __Recomendado crear un entorno venv__ ya sea via cli ```py -m venv ./``` o via vsCode (recomendado)
* Introducir API KEYS en el archivo .env
## Instalar dependencias
``` pip -r requirements.txt ```

## Servidor API via FastAPI
```fastapi dev main.py```

## Pruebas via Cli
Ejecutar la clase ChatBot.py con ```python.exe ./ChatBot.py```

