import json
import discord
from discord.ext import commands
import music
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from config import API_KEY, ASSISTANT_ID, BASE_URL, IMAGE_CHANNEL, PREFIX, TOKEN, GOOGLE_API, CHANNEL_ID

def send_message(assistant, session_id, assistant_id, message):
    response = assistant.message(
        assistant_id=assistant_id,
        session_id=session_id,
        input={
            'message_type': 'text',
            'text': message
        }
    ).get_result()

    return response['output']['generic'][0]['text'] if 'text' in response['output']['generic'][0] else ''

def connectBot():
    cogs = [music]
    client = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())

    for i in range(len(cogs)):
        cogs[i].setup(client)

    client.run(TOKEN)


authenticator = IAMAuthenticator(API_KEY)
assistant = AssistantV2(
    version='2021-06-14',
    authenticator=authenticator
)
assistant.set_service_url(BASE_URL)
# session
session = assistant.create_session(
    assistant_id=ASSISTANT_ID
).get_result()
session_json = json.dumps(session, indent=2)
session_dict = json.loads(session_json)
session_id = session_dict['session_id']

Client = commands.Bot(command_prefix=PREFIX)

cogs = [music]

for i in range(len(cogs)):
    cogs[i].setup(Client)

@Client.listen('on_message')
async def msg(message):
    if message.content.startswith(PREFIX):
        return
    if message.author == Client.user:
        return
    if message.content != 'exit':
        await message.channel.send(send_message(assistant, session_id, ASSISTANT_ID, message.content))
    if message.content == 'exit':
        assistant.delete_session(ASSISTANT_ID, session_id).get_result()
        await message.channel.send('Shutting down..')

Client.run(TOKEN)
