import streamlit as st
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain.chat_models import ChatOpenAI
from elevenlabs import generate, play, set_api_key
from elevenlabs.api.error import UnauthenticatedRateLimitError, RateLimitError
import os
# from dotenv import load_dotenv
# load_dotenv()

API_KEY = os.getenv("ELEVENLABS_API_KEY")
# os.environ["OPENAI_API_KEY"] = st.secrets("OPENAI_API_KEY")
# API_KEY = st.secrets["ELEVENLABS_API_KEY"]

set_api_key(API_KEY)

os.environ['OPRNAI_API_KEY'] = st.secrets("OPERAI_API_KEY")

st.title('🏃‍♂️ Generate your Workout Podcast!')

topic_name = st.text_input("Enter the topic name:")
time = st.number_input("Enter the length of the podcast in minutes:", min_value=0.5, max_value=3.0, value=0.5, step=0.5,format="%.1f")
voice = st.radio(
        label="Choose a voice", options=['Rachel', 'Adam'], index=0, horizontal=True)

if st.button("Make my clip!"):
    system_template = "Generate content for a podcast monologue on {topic_name} for an approx length of {time} minutes."
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

    human_template="{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    formatted_prompt = chat_prompt.format_prompt(topic_name=topic_name, time=time, text="").to_messages()

    chat = ChatOpenAI(model_name="gpt-3.5-turbo",temperature=0.3)
    response = chat(formatted_prompt)

    # st.text_area("Generated Content:", value=response.content, height=200)

    transcript = response.content

    try:
        audio = generate(text=transcript, voice=voice, model='eleven_monolingual_v1',
                         )
        st.write("Here's your podcast clip! ")
        st.audio(data=audio)
    except UnauthenticatedRateLimitError:
        e = UnauthenticatedRateLimitError("Unauthenticated Rate Limit Error")
        st.exception(e)

    except RateLimitError:
        e = RateLimitError('Rate Limit')
        st.exception(e)

    with st.expander("Transcript"):
        st.write(transcript)


