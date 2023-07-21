import streamlit as st
from rembg import remove
from PIL import Image


st.title('Remove fundo da Imagem')

# Recebendo a imagem
img = st.file_uploader("Insira sua imagem aqui", type=['png', 'jpg', 'jpeg'])


if st.button('Remover fundo'):
    if img:
        # manipulando a imagem em bytes
        img_bytes = Image.open(img)

        # removendo fundo
        img_sem_fundo = remove(img_bytes)
        st.image(img_sem_fundo, caption='Nova imagem')