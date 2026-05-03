"""
E-posta gönderim modülü — SMTP ile resim eki gönderir.
Gmail, Yandex, Outlook vb. destekler.
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
from datetime import datetime


def send_image_email(smtp_email: str, smtp_password: str, to_email: str,
                     image_path: str, group_name: str,
                     smtp_host: str = "smtp.yandex.com",
                     smtp_port: int = 465) -> bool:
    """
    WhatsApp'tan alınan resmi e-posta olarak gönderir.

    Args:
        smtp_email:    Gönderici e-posta adresi
        smtp_password: Uygulama şifresi (App Password)
        to_email:      Alıcı e-posta adresi
        image_path:    Gönderilecek resmin dosya yolu
        group_name:    Kaynak adı (kişi/grup — e-posta konusu için)
        smtp_host:     SMTP sunucusu (varsayılan: Yandex)
        smtp_port:     SMTP portu (varsayılan: 465 SSL)

    Returns:
        True başarılı, False başarısız
    """
    try:
        msg = MIMEMultipart()
        msg["From"] = smtp_email
        msg["To"] = to_email

        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M")
        msg["Subject"] = Header(f"Yeni Resim - {group_name} ({timestamp})", "utf-8")

        filename = os.path.basename(image_path)
        body = f"""
        <html>
        <body style="font-family: 'Segoe UI', Arial, sans-serif; background: #f5f5f5; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
                <div style="background: linear-gradient(135deg, #25D366 0%, #128C7E 100%); padding: 24px 32px;">
                    <h2 style="color: #ffffff; margin: 0; font-size: 20px;">📸 WhatsApp — Yeni Resim</h2>
                </div>
                <div style="padding: 32px;">
                    <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                        <tr>
                            <td style="padding: 8px 0; color: #888; font-size: 14px;">Kaynak:</td>
                            <td style="padding: 8px 0; font-weight: 600; font-size: 14px;">{group_name}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; color: #888; font-size: 14px;">Zaman:</td>
                            <td style="padding: 8px 0; font-weight: 600; font-size: 14px;">{timestamp}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; color: #888; font-size: 14px;">Dosya:</td>
                            <td style="padding: 8px 0; font-weight: 600; font-size: 14px;">{filename}</td>
                        </tr>
                    </table>
                    <p style="color: #555; font-size: 14px; line-height: 1.6;">
                        <strong>{group_name}</strong> sohbetine yeni bir resim gönderildi.
                        Resim bu e-postaya ek olarak eklenmiştir.
                    </p>
                    <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                    <p style="color: #aaa; font-size: 12px; text-align: center;">
                        Bu bildirim <strong>WhatsApp Resim İzleyici</strong> tarafından otomatik gönderilmiştir.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        msg.attach(MIMEText(body, "html", "utf-8"))

        # Resmi ekle
        with open(image_path, "rb") as img_file:
            img_data = img_file.read()

        img = MIMEImage(img_data)
        img.add_header("Content-Disposition", "attachment", filename=filename)
        msg.attach(img)

        # SMTP ile gönder (SSL)
        with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
            server.login(smtp_email, smtp_password)
            server.sendmail(smtp_email, to_email, msg.as_string())

        try:
            print(f"  E-posta gonderildi -> {to_email}")
        except UnicodeEncodeError:
            print(f"  E-posta gonderildi -> {to_email}".encode("ascii", errors="replace").decode("ascii"))
        return True

    except Exception as e:
        try:
            print(f"  E-posta gonderilemedi: {e}")
        except UnicodeEncodeError:
            print(f"  E-posta gonderilemedi: {e}".encode("ascii", errors="replace").decode("ascii"))
        return False
