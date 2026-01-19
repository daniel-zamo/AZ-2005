import os
import asyncio
from dotenv import load_dotenv

# [TASK] Import namespaces
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.functions.kernel_arguments import KernelArguments

# Load environment variables from .env file
load_dotenv()

async def main():
    # Retrieve configuration from environment variables
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

    # [TASK] Create a kernel with Azure OpenAI chat completion
    kernel = Kernel()
    
    # Initialize the Azure OpenAI service
    chat_completion = AzureChatCompletion(
        api_key=api_key,
        endpoint=endpoint,
        deployment_name=deployment_name
    )
    
    # Add the service to the kernel
    kernel.add_service(chat_completion)

    # [TASK] Test the chat completion service
    # We send a prompt to the model and wait for the response
    prompt = "Give me a list of 10 breakfast foods with eggs and cheese"
    
    print("User > " + prompt)
    
    response = await kernel.invoke_prompt(
        function_name="get_breakfast_suggestions",
        prompt=prompt,
        arguments=KernelArguments()
    )

    # Display the result
    print("Assistant > " + str(response))

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())