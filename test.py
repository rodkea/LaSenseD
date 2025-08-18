import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # o CAP_V4L2
print("Brillo actual:", cap.get(cv2.CAP_PROP_SHARPNESS))

# Probar varios valores
for val in [-10, -1, 0, 0.25, 0.5, 10,14, 1850, 1900, 1956, 1960, 1990, 1999]:
    ok = cap.set(cv2.CAP_PROP_SHARPNESS, val)
    print(f"Set {val} ->", ok, " | Actual:", cap.get(cv2.CAP_PROP_SHARPNESS))

cap.release()