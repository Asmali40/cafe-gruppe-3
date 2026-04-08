"""Funktionen für E-Mails."""

from email.mime.text import MIMEText
from email.utils import make_msgid
from smtplib import SMTP, SMTPServerDisconnected
from socket import gaierror
from typing import Final
from uuid import uuid4

from loguru import logger

from cafe.config import (
    mail_enabled,
    mail_host,
    mail_port,
    mail_timeout,
)
from cafe.service.cafe_dto import CafeDTO

__all__ = ["send_mail"]

# Mail-Client konfigurieren
MAILSERVER: Final = mail_host
PORT: Final = mail_port
SENDER: Final = "Python Server <python.server@acme.com>"
RECEIVERS: Final = ["Buchhaltung <buchhaltung@acme.com>"]
TIMEOUT: Final = mail_timeout


def send_mail(cafe_dto: CafeDTO) -> None:
    """Funktion, um eine E-Mail zu senden.

    :param cafe_dto: Café-Daten
    """
    logger.debug("{}", cafe_dto)
    if not mail_enabled:
        logger.warning("send_mail: Der Mailserver ist deaktiviert")
        return

    # Body und Subject
    msg: Final = MIMEText(f"Neues Café: <b>{cafe_dto.name}</b>")
    msg["Subject"] = f"Neues Café: ID={cafe_dto.id}"
    msg["Message-ID"] = make_msgid(idstring=str(uuid4()))

    try:
        logger.debug("mailserver={}, port={}", MAILSERVER, PORT)
        with SMTP(host=MAILSERVER, port=PORT, timeout=TIMEOUT) as smtp:
            # ggf. TLS verwenden und einloggen
            # smtp.starttls()
            # smtp.login("my_username", "my_password")
            smtp.sendmail(from_addr=SENDER, to_addrs=RECEIVERS, msg=msg.as_string())
            logger.debug("msg={}", msg)
    except ConnectionRefusedError:
        logger.warning("ConnectionRefusedError")
    except SMTPServerDisconnected:
        # z.B. bei Timeout
        logger.warning("SMTPServerDisconnected")
    except gaierror:
        # gai = getaddrinfo()  # NOSONAR
        logger.warning("socket.gaierror: Laeuft der Mailserver im virtuellen Netzwerk?")
