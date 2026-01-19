import os
import asyncio
from dotenv import load_dotenv
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

# 1. Cargar variables del archivo .env
load_dotenv()

async def main():
    # 2. Inicializar el Kernel
    kernel = sk.Kernel()

    # 3. Preparar el servicio de Azure OpenAI
    # Los valores se leen de las variables de entorno cargadas arriba
    service_id = "default"
    kernel.add_service(
        AzureChatCompletion(
            service_id=service_id,
            deployment_name=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY")
        )
    )

    print(f"Kernel configurado con el servicio: {service_id}")
    return kernel

if __name__ == "__main__":
    asyncio.run(main())