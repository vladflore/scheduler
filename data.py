from dataclasses import dataclass, field
from datetime import datetime, date
import json
from datetime import timedelta
import requests
from config import LANGUAGE


@dataclass
class FitnessClassRenderConfig:
    text_color: str = "black"
    background_color: str = "white"
    font_size: int = 12


@dataclass
class FitnessClass:
    name: str
    start: datetime
    end: datetime
    instructor: str
    description: str
    render_config: FitnessClassRenderConfig = field(
        default_factory=FitnessClassRenderConfig
    )

    @staticmethod
    def from_dict(item: dict) -> "FitnessClass":
        return FitnessClass(
            name=item["name"],
            start=datetime.fromisoformat(item["start"]),
            end=datetime.fromisoformat(item["end"]),
            instructor=item["instructor"],
            description=item["description"],
            render_config=FitnessClassRenderConfig(
                text_color=item.get("render_config", {}).get("text_color", "#000000"),
                background_color=item.get("render_config", {}).get(
                    "background_color", "#FFFFFF"
                ),
                font_size=item.get("render_config", {}).get("font_size", 12),
            ),
        )


CLASSES_INPUT_FILE = "classes_{lang}.json"
CLASSES_INPUT_FILE_URL = f"https://raw.githubusercontent.com/vladflore/scheduler/refs/heads/main/classes_{LANGUAGE}.json"

today = date.today()
start_of_week = today - timedelta(days=today.weekday())

dummy_classes = [
    FitnessClass(
        name="Dummy Yoga Flow",
        start=datetime.combine(start_of_week, datetime.min.time()).replace(hour=9),
        end=datetime.combine(start_of_week, datetime.min.time()).replace(hour=10),
        instructor="Alice Smith",
        description="A gentle yoga class to start your week.",
        render_config=FitnessClassRenderConfig(
            text_color="#FFFFFF",
            background_color="#800080",
            font_size=14,  # white, purple
        ),
    ),
    FitnessClass(
        name="Dummy Power Yoga",
        start=datetime.combine(start_of_week, datetime.min.time()).replace(hour=17),
        end=datetime.combine(start_of_week, datetime.min.time()).replace(hour=18),
        instructor="Alice Smith",
        description="Dynamic yoga for strength and flexibility.",
        render_config=FitnessClassRenderConfig(
            text_color="#FFFFFF",
            background_color="#4B0082",
            font_size=13,
        ),
    ),
    FitnessClass(
        name="Dummy HIIT Blast",
        start=datetime.combine(
            start_of_week + timedelta(days=1), datetime.min.time()
        ).replace(hour=18),
        end=datetime.combine(
            start_of_week + timedelta(days=1), datetime.min.time()
        ).replace(hour=19),
        instructor="Bob Johnson",
        description="High intensity interval training for all levels.",
        render_config=FitnessClassRenderConfig(
            text_color="#000000",
            background_color="#FFFF00",
            font_size=12,  # black, yellow
        ),
    ),
    FitnessClass(
        name="Dummy Morning HIIT",
        start=datetime.combine(
            start_of_week + timedelta(days=1), datetime.min.time()
        ).replace(hour=7),
        end=datetime.combine(
            start_of_week + timedelta(days=1), datetime.min.time()
        ).replace(hour=8),
        instructor="Bob Johnson",
        description="Kickstart your day with HIIT.",
        render_config=FitnessClassRenderConfig(
            text_color="#000000",
            background_color="#FFD700",
            font_size=12,
        ),
    ),
    FitnessClass(
        name="Dummy Pilates Core",
        start=datetime.combine(
            start_of_week + timedelta(days=2), datetime.min.time()
        ).replace(hour=7),
        end=datetime.combine(
            start_of_week + timedelta(days=2), datetime.min.time()
        ).replace(hour=8),
        instructor="Carol Lee",
        description="Strengthen your core with Pilates.",
        render_config=FitnessClassRenderConfig(
            text_color="#000000",
            background_color="#ADD8E6",
            font_size=13,  # black, lightblue
        ),
    ),
    FitnessClass(
        name="Dummy Pilates Stretch",
        start=datetime.combine(
            start_of_week + timedelta(days=2), datetime.min.time()
        ).replace(hour=19),
        end=datetime.combine(
            start_of_week + timedelta(days=2), datetime.min.time()
        ).replace(hour=20),
        instructor="Carol Lee",
        description="Evening pilates for flexibility.",
        render_config=FitnessClassRenderConfig(
            text_color="#000000",
            background_color="#B0E0E6",
            font_size=13,
        ),
    ),
    FitnessClass(
        name="Dummy Spin Class",
        start=datetime.combine(
            start_of_week + timedelta(days=4), datetime.min.time()
        ).replace(hour=17),
        end=datetime.combine(
            start_of_week + timedelta(days=4), datetime.min.time()
        ).replace(hour=18),
        instructor="Dan Miller",
        description="Cardio spin session with energetic music.",
        render_config=FitnessClassRenderConfig(
            text_color="#FFFFFF",
            background_color="#00008B",
            font_size=12,  # white, darkblue
        ),
    ),
    FitnessClass(
        name="Dummy Morning Spin",
        start=datetime.combine(
            start_of_week + timedelta(days=4), datetime.min.time()
        ).replace(hour=7),
        end=datetime.combine(
            start_of_week + timedelta(days=4), datetime.min.time()
        ).replace(hour=8),
        instructor="Dan Miller",
        description="Start your day with a spin workout.",
        render_config=FitnessClassRenderConfig(
            text_color="#FFFFFF",
            background_color="#4682B4",
            font_size=12,
        ),
    ),
    FitnessClass(
        name="Dummy Zumba",
        start=datetime.combine(
            start_of_week + timedelta(days=5), datetime.min.time()
        ).replace(hour=11),
        end=datetime.combine(
            start_of_week + timedelta(days=5), datetime.min.time()
        ).replace(hour=12),
        instructor="Eva Gomez",
        description="Dance your way to fitness with Zumba.",
        render_config=FitnessClassRenderConfig(
            text_color="#000000",
            background_color="#FFC0CB",
            font_size=15,  # black, pink
        ),
    ),
    FitnessClass(
        name="Dummy Zumba Party",
        start=datetime.combine(
            start_of_week + timedelta(days=5), datetime.min.time()
        ).replace(hour=18),
        end=datetime.combine(
            start_of_week + timedelta(days=5), datetime.min.time()
        ).replace(hour=19),
        instructor="Eva Gomez",
        description="Evening Zumba with party vibes.",
        render_config=FitnessClassRenderConfig(
            text_color="#000000",
            background_color="#FF69B4",
            font_size=15,
        ),
    ),
    FitnessClass(
        name="Dummy Stretch & Relax",
        start=datetime.combine(
            start_of_week + timedelta(days=6), datetime.min.time()
        ).replace(hour=10),
        end=datetime.combine(
            start_of_week + timedelta(days=6), datetime.min.time()
        ).replace(hour=11),
        instructor="Grace Lin",
        description="Gentle stretching and relaxation.",
        render_config=FitnessClassRenderConfig(
            text_color="#000000",
            background_color="#E0FFFF",
            font_size=13,
        ),
    ),
    FitnessClass(
        name="Dummy Sunday Bootcamp",
        start=datetime.combine(
            start_of_week + timedelta(days=6), datetime.min.time()
        ).replace(hour=16),
        end=datetime.combine(
            start_of_week + timedelta(days=6), datetime.min.time()
        ).replace(hour=17),
        instructor="Mike Brown",
        description="Full body bootcamp to end your week strong.",
        render_config=FitnessClassRenderConfig(
            text_color="#FFFFFF",
            background_color="#228B22",
            font_size=14,
        ),
    ),
]


def read_data(data) -> list[FitnessClass]:
    classes: list[FitnessClass] = []
    for fitness_class in data["fitness_classes"]:
        start = datetime.fromisoformat(fitness_class["start"])
        end = datetime.fromisoformat(fitness_class["end"])
        render_config = FitnessClassRenderConfig(
            text_color=fitness_class["render_config"].get("text_color", "black"),
            background_color=fitness_class["render_config"].get(
                "background_color", "white"
            ),
            font_size=fitness_class["render_config"].get("font_size", 12),
        )
        fitness_class = FitnessClass(
            name=fitness_class["name"],
            start=start,
            end=end,
            instructor=fitness_class["instructor"],
            description=fitness_class["description"],
            render_config=render_config,
        )
        classes.append(fitness_class)
    return classes


def load_classes_from_file(language: str = "en") -> list[FitnessClass]:
    with open(CLASSES_INPUT_FILE.format(lang=language), "r") as file:
        data = json.load(file)
        return read_data(data)


def load_classes_from_url(url: str) -> list[FitnessClass]:
    response = requests.get(url)
    data = response.json()
    return read_data(data)


if __name__ == "__main__":
    # classes = load_classes_from_file()
    # print(classes)
    classes = load_classes_from_url(
        "https://raw.githubusercontent.com/vladflore/scheduler/refs/heads/main/classes_en.json"
    )
    print(classes)
