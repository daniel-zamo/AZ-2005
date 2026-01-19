import os
import asyncio
from dotenv import load_dotenv

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from semantic_kernel.contents import ChatHistory
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior

from plugins.NativePlugins.flight_booking_plugin import FlightBookingPlugin

load_dotenv()

async def main():
    kernel = Kernel()

    chat_service = AzureChatCompletion(
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY")
    )
    kernel.add_service(chat_service)

    # Registro del plugin
    kernel.add_plugin(FlightBookingPlugin(), plugin_name="FlightBooking")

    # --- CONFIGURACIÓN DE COMPORTAMIENTO ---
    
    # Opción 1: MODO COMPLETO (Permite buscar y reservar)
    # Usaremos esta para que funcione el "todo en uno"
    settings_full = AzureChatPromptExecutionSettings(
        function_choice_behavior=FunctionChoiceBehavior.Auto()
    )

    # Opción 2: MODO RESTRINGIDO (Solo buscar) - Descomenta para probar el bloqueo
    settings_restricted = AzureChatPromptExecutionSettings(
        function_choice_behavior=FunctionChoiceBehavior.Auto(
            filters={"included_functions": ["FlightBooking-search_flights"]}
        )
    )

    # ASIGNACIÓN: Aquí definimos cuál usará la función chat
    # Si quieres que la IA pueda reservar, usa settings_full
    active_settings = settings_full 

    history = ChatHistory()
    history.add_system_message("You are a professional travel agent. Use tools to search and book flights.")

    async def chat(user_input):
        print(f"\nUser: {user_input}")
        history.add_user_message(user_input)

        # Usamos 'active_settings' que está definida arriba
        response = await chat_service.get_chat_message_content(
            chat_history=history,
            kernel=kernel,
            settings=active_settings
        )
        
        print(f"Assistant: {response}")
        history.add_assistant_message(str(response))

    # --- PRUEBAS DE EJECUCIÓN ---

    # 1. Prueba de flujo conversacional (en dos pasos)
    print("--- PRUEBA 1: FLUJO CONVERSACIONAL ---")
    await chat("Find me a flight to Tokyo on the 2025-01-19")
    await chat("I want to book flight ID 1")

    # 2. Prueba de flujo autónomo (todo en un solo turno)
    # Nota: Para que esto funcione, el JSON debe tener vuelos disponibles para Madrid
    print("\n--- PRUEBA 2: FLUJO AUTÓNOMO (TODO EN UNO) ---")
    await chat("Find a flight to Madrid on 2025-02-10 and book it for me immediately.")

if __name__ == "__main__":
    asyncio.run(main())
