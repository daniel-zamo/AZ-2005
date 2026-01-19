import os
import asyncio
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.functions import KernelArguments

load_dotenv()

async def main():
    # 1. Configurar el Kernel (lo que ya sabías hacer)
    kernel = Kernel()
    kernel.add_service(AzureChatCompletion(
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY")
    ))

    # 2. CARGAR EL PLUGIN DESDE EL DIRECTORIO
    # "plugins" es la carpeta padre, "Prompts" es el nombre del plugin
    prompts_plugin = kernel.add_plugin(
        plugin_name="Prompts",
        parent_directory="./plugins" # Aquí buscará subcarpetas dentro de plugins
    )

    # 3. PREPARAR EL TEXTO DE PRUEBA
    texto_largo = """
    Semantic Kernel es un SDK de código abierto que permite a los desarrolladores 
    combinar servicios de IA como OpenAI, Azure OpenAI y Hugging Face con 
    lenguajes de programación convencionales como C#, Python y Java. 
    Al usar Semantic Kernel, los desarrolladores pueden crear aplicaciones 
    que son capaces de razonar, resolver problemas y ejecutar tareas complejas 
    mediante la orquestación de funciones y plugins.
    """

    # 4. INVOCAR LA FUNCIÓN DEL PLUGIN
    # Notarás que llamamos a "Summarize", que es el nombre de la carpeta
    print("\n--- Procesando Resumen ---")
    result = await kernel.invoke(
        prompts_plugin["Summarize"], 
        KernelArguments(input=texto_largo)
    )

    print(result)

if __name__ == "__main__":
    asyncio.run(main())
