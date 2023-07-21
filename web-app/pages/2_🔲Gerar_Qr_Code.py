import streamlit as st
from PIL import Image
import qrcode

    
st.title("Gerador de QR-Code.")

data = st.text_input("Cole o link aqui", key="link")

if st.button("Gerar Qr-Code"):

    # Instancia o objeto QRCode e informa o tamanho(box_size=6)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=6)

    # Adiciona o dado que vira qr-code
    qr.add_data(data)
    qr.make(fit = True)

    img = qr.make_image()

    # Salvando o arquivo
    img.save('QrCode.png')

    image = Image.open('QrCode.png')
    st.image(image, caption='Seu QR-Code')
    


