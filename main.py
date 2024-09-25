import chainlit as cl
from gptwrapper import GPTWrapper
from extract import ModelExtract
from chainlit.input_widget import Select, Slider
#from database.hana import Hana
from doc_extractor import DocumentTextExtractor

# Loads the initial prompt for the selected ai personality.
def load_inital_prompt():
    extractor = cl.user_session.get("extractor")
    return extractor.get_initial_prompt()

# Appends prompt to the message history
def append_prompt_to_messages(message, role):
    messages = cl.user_session.get("messages")
    messages.append({'role':role, 'content':message})
    cl.user_session.set("messages", messages)

# Appends the decoded image to the messages
def append_images_to_messages(message, images):
    messages = cl.user_session.get("messages")
    messages.append({'role':'user', 'content':[{"type":"text", "text":message}]})
    wrapper = cl.user_session.get('gptwrapper')
    for _,image in enumerate(images):
        base64_image = wrapper.encode_image(image.path)
        messages[-1]["content"].append({"type":"image_url", "image_url":{"url":f"data:image/jpeg;base64,{base64_image}"}})
    cl.user_session.set("messages",messages)

# Appends the extracted file content to the messages with the user prompt.
def append_files_to_messages(message, files):
    text = ""
    messages = cl.user_session.get("messages")
    doc_extractor = cl.user_session.get("doc_extractor")
    if not doc_extractor:
        cl.user_session.set("doc_extractor", DocumentTextExtractor())
        doc_extractor = cl.user_session.get("doc_extractor")
    for file in files:
        text += doc_extractor.extract_text(file=file)
    messages.append({'role':'user', 'content':f"User prompt: {message} , context: {text}"})
  
# Calls the wrapper's getCompletion method and appends the response to the message history
def getCompletion(messages):
    gptwrapper = cl.user_session.get("gptwrapper")
    ai_message = gptwrapper.getCompletion(messages)
    append_prompt_to_messages(ai_message, 'assistant')
    return ai_message

# Chat profile selector
@cl.set_chat_profiles
async def chat_profile():
    return [
        cl.ChatProfile(
            name="Basic ChatGPT",
            markdown_description="General knowledge for all sorts of questions.",
            #icon=''
        ),
        cl.ChatProfile(
            name="Teams post",
            markdown_description="Create engageing social media posts.",
            #icon=''
        ),
        cl.ChatProfile(
            name="Checklist",
            markdown_description="Create a checklist for event organizing.",
            #icon=''
        ),
        cl.ChatProfile(
            name="Q&A Generator",
            markdown_description="Upload a document to generate questions about it.",
            #icon=''
        ),
        cl.ChatProfile(
            name="RAG",
            markdown_description="Ask about corporate policies.",
            #icon=''
        ),

    ]
# Upload a file to generate questions and answers for it.
async def message_qa_generator():
    file = None
        # Wait for the user to upload a file
    while file is None:
        file = await cl.AskFileMessage(
            content="Please upload ONE PDF file to begin!", 
            accept=["application/pdf"],
            max_size_mb=20,
            timeout=180,
            max_files=1
        ).send()

        text = DocumentTextExtractor().extract_text_from_pdf(file[0].path)

        # Let the user know that the system is ready
        await cl.Message(
            content=f"`{file[0].name}` uploaded!"
        ).send()
        messages = cl.user_session.get("messages")
        messages.append({'role': 'user', 'content': text})
        await cl.Message(content=f"{getCompletion(messages)}").send()

# Sets the model parameters every time a new profile has been selected.
@cl.on_chat_start
async def start():
    init()
    chat_profile = cl.user_session.get("chat_profile")
    await cl.Message(
        content=f"Starting chat using the {chat_profile} chat profile"
        ).send()
    if chat_profile == 'RAG':    
        pass
    elif chat_profile == 'Q&A Generator':
       await message_qa_generator()
    else:
        settings = await cl.ChatSettings(
            [
                Select(
                    id="model",
                    label="OpenAI - Model",
                    values=["gpt-4o"],
                    initial_index=0,
                ),
                Slider(
                    id="temperature",
                    label="Temperature",
                    initial=0.7,
                    min=0,
                    max=1,
                    step=0.1,
                    description='This parameter controls the randomness of the output. Lower means more focused and deterministic answer.'
                ),
                Slider(
                    id="max_tokens",
                    label="Max Tokens",
                    initial=1024,
                    min=256,
                    max=4096,
                    step=32,
                    #description="This parameter determines the maximum length of the generated output.",
                ),
            ]
        ).send()
# Updates the settings of the ai model on change.
@cl.on_settings_update
async def setup_agent(settings):
    print("on_settings_update", settings)
    gptwrapper = cl.user_session.get('gptwrapper')
    gptwrapper.set_model_params(settings)
    cl.user_session.set('gptwrapper', gptwrapper)

# Loads initial prompt from the extractor when new profile is selected
def get_initial_prompt(extractor):
    if cl.user_session.get("chat_profile") == "Basic ChatGPT":
        extractor.ai_personality = 'base'
    elif cl.user_session.get("chat_profile") == "Teams post":
        extractor.ai_personality = 'teams'
    elif cl.user_session.get("chat_profile") == "Checklist":
        extractor.ai_personality = 'checklist'
    elif cl.user_session.get("chat_profile") == "Q&A Generator":
        extractor.ai_personality = 'Q&A'
    elif cl.user_session.get("chat_profile") == "RAG":
        extractor.ai_personality = 'rag'
        cl.user_session.set('extractor', extractor)
    return extractor.get_initial_prompt()
'''
First runs when starting the application.

Initializes gptwrapper, extractor, messages and calls
load_inital_prompt() to load the inital prompt into messages
'''

def init():
    cl.user_session.set("gptwrapper", GPTWrapper())
    cl.user_session.set("extractor", ModelExtract())
    #cl.user_session.set('hana', Hana())
    cl.user_session.set("doc_extractor", DocumentTextExtractor())
    initial_prompt=get_initial_prompt(cl.user_session.get("extractor"))
    messages = [{'role':'system', 'content': initial_prompt}]
    print(cl.user_session.get('extractor').ai_personality)
    cl.user_session.set("messages", messages)


'''
Runs when a message is sent from the user.

Awaits for the reply and posts it to the chat window
'''
@cl.on_message
async def main(message: cl.Message):
    images = [file for file in message.elements if "image" in file.mime]
    files = [file for file in message.elements if "application" in file.mime or "text" in file.mime]
    #if cl.user_session.get("chat_profile") == "RAG":
        #hana = cl.user_session.get('hana')
        #await cl.Message(content=f"{hana.get_conversation_chain(message.content)}",).send()
    #else:
    if cl.user_session.get('qafiles'):
            append_files_to_messages("", cl.user_session.get('qafiles'))     
    if files or images:
        if files:
            try:
                    append_files_to_messages(message.content, files)
            except ValueError as e:
                await cl.Message(content = e).send()
        if images:
            try:
                append_images_to_messages(message.content, images)
            except ValueError as e:
                await cl.Message(content = e).send()
    else:
        message_history = cl.user_session.get('messages')
        message_history.append({'role':'user', 'content':message.content})
        cl.user_session.set('messages', message_history)

        
    msg = cl.Message(content="")
    await msg.send()

    wrapper = cl.user_session.get('gptwrapper')
    stream = await wrapper.client.chat.completions.create(
        messages=cl.user_session.get('messages'), stream=True, **wrapper.settings
    )

    async for part in stream:
        try:
            print(part)
            if token := part.choices[0].delta.content or "":
                await msg.stream_token(token)
        except:
            pass

    await msg.update()
    append_prompt_to_messages(msg.content, 'assistant')
