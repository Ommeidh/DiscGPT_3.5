import os
import discord
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Set up OpenAI API key and model engine
openai.api_key = OPENAI_API_KEY
model_engine = "gpt-3.5-turbo"

# Set up the Discord client with all intents
intents = discord.Intents().all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    """Event handler when the bot connects to Discord."""
    print(f'{client.user} has connected to Discord!')

def generate_response(message):
    """Generate a response using OpenAI."""
    prompt = message.strip()
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=messages,
        max_tokens=2000,  # Limit each response to 2000 tokens
        n=1,
        temperature=0.5,
    )
    
    # Extract the text from the response message
    response_text = response['choices'][0]['message']['content']
    
    # Split the response into chunks of 2000 characters
    response_chunks = [response_text[i:i + 2000] for i in range(0, len(response_text), 2000)]
    
    return response_chunks

@client.event
async def on_message(message):
    """Event handler when a message is received."""
    if message.author == client.user:
        return
    if message.content.startswith('%'):
        responses = generate_response(message.content[1:])
        for response_chunk in responses:
            await message.channel.send(response_chunk)

# Run the bot
client.run(TOKEN)
