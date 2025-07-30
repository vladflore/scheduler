from dataclasses import dataclass, field
from datetime import datetime, date
import json


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


CLASSES_INPUT_FILE = "classes.json"


def load_classes_from_file() -> list[FitnessClass]:
    classes: list[FitnessClass] = []

    with open(CLASSES_INPUT_FILE, "r") as file:
        data = json.load(file)
        for fitness_class in data["fitness_classes"]:
            start = datetime.fromisoformat(fitness_class["start"])
            end = datetime.fromisoformat(fitness_class["end"])
            render_config = FitnessClassRenderConfig(
                text_color=fitness_class["render_config"].get("text_color", "black"),
                background_color=fitness_class["render_config"].get("background_color", "white"),
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


if __name__ == "__main__":
    classes = load_classes_from_file()
    print(classes)
