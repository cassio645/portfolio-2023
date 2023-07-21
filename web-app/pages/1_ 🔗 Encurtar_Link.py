import streamlit as st
import pyshorteners


st.title('Encurtar link')

# Recebe o link
link = st.text_input("Cole o link aqui", key="link")

# Se o botão for clicado, cria o novo link, se não tiver recebido nada entra no else
if st.button("Encurtar"):
    if link:
        encurtador = pyshorteners.Shortener()

        try:
            # novo link clck.ru
            novo_link = encurtador.clckru.short(link)

            # exibe o novo link
            st.write("Link curto")
            st.code(novo_link, language="")
        except:
            st.error('Url inválida. Por favor tente novamente.', icon="🚨")
    else:
        st.write("Nenhum link foi informado!")

