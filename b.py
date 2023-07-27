import cv2
import pytesseract

# Tesseract OCR konfigürasyonu (Tesseract kurulu olmalıdır)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Video yakalama nesnesini oluşturun
kamera = cv2.VideoCapture(0)

while True:
    # Kameradan bir kare alın
    ret, kare = kamera.read()

    # Kare alınamazsa döngüden çıkın
    if not ret:
        break

    # Görüntüyü gri tonlamaya dönüştürün (Tesseract OCR için)
    gri_tonlama = cv2.cvtColor(kare, cv2.COLOR_BGR2GRAY)

    # Plakaları bulmak için OCR kullanarak metni tespit edin
    plakalar = pytesseract.image_to_data(gri_tonlama, output_type=pytesseract.Output.DICT)

    for i, rec_num in enumerate(plakalar["text"]):
        if rec_num.isnumeric():
            # Plaka koordinatlarını alın
            x, y, w, h = plakalar["left"][i], plakalar["top"][i], plakalar["width"][i], plakalar["height"][i]

            # Plaka değerini ve koordinatları bir dosyaya yazın
            with open("plakalar.txt", "a") as dosya:
                dosya.write(f"Plaka: {rec_num}, Koordinatlar: x={x}, y={y}, w={w}, h={h}\n")

            # Plakayı çerçeveleyin
            cv2.rectangle(kare, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(kare, rec_num, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Çerçevelenmiş görüntüyü gösterin
    cv2.imshow("Plaka Algılama", kare)

    # Çıkış için 'q' tuşuna basın
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kaynakları serbest bırakın ve pencereleri kapatın
kamera.release()
cv2.destroyAllWindows()
