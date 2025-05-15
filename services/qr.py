# qr.py
import qrcode
import os
import json
import cv2
from pyzbar.pyzbar import decode

QR_DIR = "qr_codes"
os.makedirs(QR_DIR, exist_ok=True)

def generate_qr(student_id):
    data = {"student_id": student_id}
    qr = qrcode.make(json.dumps(data))
    qr_path = os.path.join(QR_DIR, f"student_{student_id}.png")
    qr.save(qr_path)
    return qr_path

def scan_qr():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("Webcam not accessible")

    print("Scanning QR code... Press 'q' to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        decoded_objs = decode(frame)
        for obj in decoded_objs:
            qr_data = obj.data.decode("utf-8")
            try:
                student_data = json.loads(qr_data)
                cap.release()
                cv2.destroyAllWindows()
                return student_data.get("student_id")
            except json.JSONDecodeError:
                continue

        cv2.imshow("QR Scanner - Press 'q' to quit", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None
