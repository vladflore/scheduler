from enum import Enum, auto

LANGUAGE = "en"

WHATSAPP_NUMBER = "+34613429288"

BOOK_VIA_WHATSAPP = False


class DataSourceMode(Enum):
    LOCAL = auto()
    URL = auto()
    DUMMY = auto()


DATA_SOURCE_MODE = DataSourceMode.URL

translations: dict[str, dict[str, str | dict[str, str]]] = {
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
    },
}
