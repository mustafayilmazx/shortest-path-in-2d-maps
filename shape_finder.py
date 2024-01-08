import cv2
import numpy as np

# Resmi oku
img = cv2.imread('floor.jpg')

# BGR'dan HSV'ye dönüştür
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Kırmızı renk aralığını tanımla
lower_red1 = np.array([0, 120, 70])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 120, 70])
upper_red2 = np.array([180, 255, 255])

# Sadece kırmızı renkli alanları maskele
mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
mask = mask1 + mask2

# Maskelenmiş görüntüyü orijinal görüntü ile birleştir
red_only = cv2.bitwise_and(img, img, mask=mask)

# Maskelenmiş görüntüde kontur bulma
contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:
    # Konturun yaklaşık şeklini hesapla
    approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)

    # Konturun merkezini bul
    M = cv2.moments(contour)
    if M['m00'] != 0.0:
        x = int(M['m10']/M['m00'])
        y = int(M['m01']/M['m00'])

    # Şekil adını belirle ve yazdır
    if len(approx) == 3:
        cv2.putText(red_only, 'Triangle', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    elif len(approx) == 4:
        cv2.putText(red_only, 'Quadrilateral', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

# Sonucu göster
cv2.imshow('Red Shapes', red_only)
cv2.waitKey(0)
cv2.destroyAllWindows()
