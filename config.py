from enum import Enum, auto
import requests
from dataclasses import dataclass
import time


@dataclass
class Config:
    language: str
    whatsapp_number: str
    book_via_whatsapp: bool


class DataSourceMode(Enum):
    LOCAL = auto()
    GH_PAGES = auto()
    DUMMY = auto()


CLIENT_NAME = "generic-client"
GH_PAGES_ROOT = f"https://vladflore.github.io/{CLIENT_NAME}"

DATA_SOURCE_MODE = DataSourceMode.GH_PAGES


TRANSLATIONS: dict[str, dict[str, str | dict[str, str]]] = {
    "es": {
        "instructor": "Instructor",
        "book_via_whatsapp": "Reservar por WhatsApp",
        "date": "Fecha",
        "whatsapp_message": "Hola! Me gustaría reservar la clase '{class_name}' con {instructor} el {date} a las {time}.",
        "time": "Hora",
        "week_days": {
            "monday": "Lunes",
            "tuesday": "Martes",
            "wednesday": "Miércoles",
            "thursday": "Jueves",
            "friday": "Viernes",
            "saturday": "Sábado",
            "sunday": "Domingo",
        },
        "schedule_date_label": "Ir a la fecha",
        "schedule_title": "Horario de Clases de Fitness",
        "info_modal_title": "Información",
        "info_modal_content": "¿Te gustaría usar este programador para tu centro de fitness? Contáctame a través del botón de WhatsApp en la esquina inferior derecha.",
    },
    "en": {
        "instructor": "Instructor",
        "book_via_whatsapp": "Book via WhatsApp",
        "date": "Date",
        "whatsapp_message": "Hi! I would like to book the class '{class_name}' with {instructor} on {date} at {time}.",
        "time": "Time",
        "week_days": {
            "monday": "Monday",
            "tuesday": "Tuesday",
            "wednesday": "Wednesday",
            "thursday": "Thursday",
            "friday": "Friday",
            "saturday": "Saturday",
            "sunday": "Sunday",
        },
        "schedule_date_label": "Go to date",
        "schedule_title": "Fitness Classes Schedule",
        "info_modal_title": "Information",
        "info_modal_content": """
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; padding: 24px; background: rgba(153, 94, 10, 0.65); color: white; border-radius: 12px; text-align: center; box-shadow: 0 8px 32px rgba(0,0,0,0.1);">
    <h3 style="margin: 0 0 16px 0; font-size: 24px; font-weight: 600;">Interested in using this scheduler for your fitness center?</h3>
    
    <p style="margin: 0 0 20px 0; font-size: 16px; opacity: 0.95;">
        Contact me via the WhatsApp button in the bottom-right corner.
    </p>
    
    <div style="text-align: left; background: rgba(255,255,255,0.1); padding: 20px; border-radius: 8px; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2);">
        <h4 style="margin: 0 0 12px 0; font-size: 18px; font-weight: 500;">Features:</h4>
        <ul style="margin: 0; padding-left: 20px; line-height: 1.6;">
            <li style="margin-bottom: 8px;">Add your own classes with the information you need.</li>
            <li style="margin-bottom: 8px;">Book classes via WhatsApp.</li>
            <li style="margin-bottom: 8px;">Print the schedule as a PDF for easy sharing.</li>
            <li style="margin-bottom: 8px;">Add your own logo and colors.</li>
            <li style="margin-bottom: 0;">Languages supported: English, Spanish, and Catalan.</li>
        </ul>
    </div>
</div>
        """,
    },
    "cat": {
        "instructor": "Instructor",
        "book_via_whatsapp": "Reservar per WhatsApp",
        "date": "Data",
        "whatsapp_message": "Hola! M'agradaria reservar la classe '{class_name}' amb {instructor} el {date} a les {time}.",
        "time": "Hora",
        "week_days": {
            "monday": "Dilluns",
            "tuesday": "Dimarts",
            "wednesday": "Dimecres",
            "thursday": "Dijous",
            "friday": "Divendres",
            "saturday": "Dissabte",
            "sunday": "Diumenge",
        },
        "schedule_date_label": "Anar a la data",
        "schedule_title": "Horari de Classes de Fitness",
        "info_modal_title": "Informació",
        "info_modal_content": "Vols utilitzar aquest planificador per al teu centre de fitness? Contacta’m mitjançant el botó de WhatsApp a la cantonada inferior dreta.",
    },
}


def generate_timestamp():
    return str(int(time.time()))


def load_config() -> Config:
    try:
        response = requests.get(f"{GH_PAGES_ROOT}/config.json?v={generate_timestamp()}")
        response.raise_for_status()
        data = response.json()
        return Config(
            language=data.get("language", "en"),
            whatsapp_number=data.get("whatsapp_number", "n/a"),
            book_via_whatsapp=data.get("book_via_whatsapp", False),
        )
    except requests.RequestException as e:
        print(f"Error loading config: {e}")
        return Config(
            language="en",
            whatsapp_number="n/a",
            book_via_whatsapp=False,
        )


if __name__ == "__main__":
    config = load_config()
    print(config)
