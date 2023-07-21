import streamlit as st
from PIL import Image


st.title('Remove cores da imagem')

# Recebendo a imagem
img = st.file_uploader("Insira sua imagem aqui", type=['png', 'jpg', 'jpeg'])


if st.button('Remover cores'):
    if img:
        # manipulando a imagem em bytes
        img_bytes = Image.open(img)

        # removendo cores
        img_preto_branco = img_bytes.convert('L')
        st.image(img_preto_branco, caption='Nova imagem')