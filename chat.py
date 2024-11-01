# * import libraries
import time, yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_authenticator import Authenticate

# * import agent
from agent import AgentCRUD

with open('account.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Pre-hashing all plain text passwords once
# stauth.Hasher.hash_passwords(config['credentials'])

authentication_status = None

try:
    authenticator.login("main")
    authentication_status = st.session_state['authentication_status']
    roles = st.session_state['roles'][0]
except Exception as e:
    st.error(e)

def stream_data(response):
    for word in response.split(" "):
        yield word + " "
        time.sleep(0.05)

print(st.session_state)

if authentication_status:
    authenticator.logout('Se déconnecter', 'sidebar')
    st.title("🤖 Bot Crudo le rigolo")
    st.write(f'Bienvenue *{st.session_state["name"]}*')

    # init agent
    agent = AgentCRUD()

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Que puis-je faire pour toi ? "):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with st.spinner("Loading response..."):
                docs = agent.similarityFilter(prompt, roles)
                response = agent.chat(docs, st.session_state.messages)
            st.write_stream(stream_data(response))

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
