import qrcode

# Link da prova
link_prova = "https://forms.gle/SEU_LINK_DA_PROVA"

# Criando QR Code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)

qr.add_data(link_prova)
qr.make(fit=True)

imagem = qr.make_image(fill_color="black", back_color="white")

imagem.save("QRCode_Prova.png")

print("QR Code gerado com sucesso!")
print("Link compartilhável:", link_prova)
