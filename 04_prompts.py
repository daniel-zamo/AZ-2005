import os
import asyncio
from dotenv import load_dotenv

# Importar namespaces de Semantic Kernel
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from semantic_kernel.contents import ChatHistory
from semantic_kernel.functions import KernelArguments
from semantic_kernel.prompt_template import KernelPromptTemplate, PromptTemplateConfig, HandlebarsPromptTemplate

load_dotenv()

async def main():
    # --- CONFIGURACIÓN DEL KERNEL ---
    kernel = Kernel()
    
    # Asegúrate de que en tu .env el nombre del despliegue sea el correcto (ej. gpt-4o)
    chat_completion = AzureChatCompletion(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    )
    kernel.add_service(chat_completion)

    # --- TAREA: CREAR EL HISTORIAL DE CHAT ---
    # Esto permite que la IA "recuerde" lo que dijimos antes
    chat_history = ChatHistory()

    # Función auxiliar para obtener respuesta y guardarla en el historial
    async def get_reply():
        reply = await chat_completion.get_chat_message_content(
            chat_history=chat_history,
            kernel=kernel,
            settings=AzureChatPromptExecutionSettings()
        )
        print(f"\nAssistant: {reply}")
        chat_history.add_assistant_message(str(reply))

    # --- TAREA: PROMPT TEMPLATE (FORMATO SEMANTIC KERNEL) ---
    # Usamos {{$variable}} para definir huecos que rellenaremos luego
    sk_prompt_template = KernelPromptTemplate(
        prompt_template_config=PromptTemplateConfig(
            template="""
            You are a helpful career advisor. Based on the users's skills and interest, suggest up to 5 suitable roles.
            Return the output as JSON in the following format:
            "Role Recommendations":
            {
            "recommendedRoles": [],
            "industries": [],
            "estimatedSalaryRange": ""
            }

            My skills are: {{$skills}}. My interests are: {{$interests}}. What are some roles that would be suitable for me?
            """,
            name="recommend_roles_prompt",
            template_format="semantic-kernel",
        )
    )

    # Renderizar el prompt con argumentos específicos
    print("\n--- Generando Recomendaciones de Carrera ---")
    sk_rendered_prompt = await sk_prompt_template.render(
        kernel,
        KernelArguments(
            skills="Software Engineering, C#, Python, Drawing, Guitar, Dance",
            interests="Education, Psychology, Programming, Helping Others"
        )
    )

    # Enviar al historial e invocar
    chat_history.add_user_message(sk_rendered_prompt)
    await get_reply()

    # --- TAREA: PROMPT TEMPLATE (FORMATO HANDLEBARS) ---
    # Handlebars permite usar etiquetas tipo XML y lógica más compleja ({{variable}})
    hb_prompt_template = HandlebarsPromptTemplate(
        prompt_template_config=PromptTemplateConfig(
            template="""
            <message role="system">
            Instructions: You are a career advisor. Analyze the skill gap between 
            the user's current skills and the requirements of the target role.
            </message>
            <message role="user">Target Role: {{targetRole}}</message>
            <message role="user">Current Skills: {{currentSkills}}</message>

            <message role="assistant">
            "Skill Gap Analysis":
            {
                "missingSkills": [],
                "coursesToTake": [],
                "certificationSuggestions": []
            }
            </message>
            """,
            name="missing_skills_prompt",
            template_format="handlebars",
        )
    )

    print("\n--- Analizando Brecha de Habilidades (Skill Gap) ---")
    hb_rendered_prompt = await hb_prompt_template.render(
        kernel,
        KernelArguments(
            targetRole="Game Developer",
            currentSkills="Software Engineering, C#, Python, Drawing, Guitar, Dance"
        )
    )

    chat_history.add_user_message(hb_rendered_prompt)
    await get_reply()

    # --- TAREA: INTERACCIÓN CONTINUA ---
    print("\nAssistant: How can I help you?")
    user_input = input("User: ")
    
    chat_history.add_user_message(user_input)
    await get_reply()

if __name__ == "__main__":
    asyncio.run(main())