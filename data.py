from dataclasses import dataclass, field
from datetime import datetime, date


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


classes: list[FitnessClass] = [
    # Monday (2025-07-28)
    FitnessClass(
        name="Morning Yoga",
        start=datetime(2025, 7, 28, 7, 0),
        end=datetime(2025, 7, 28, 8, 0),
        instructor="Alice Smith",
        description="Start your week with gentle yoga.",
        render_config=FitnessClassRenderConfig(
            text_color="white",
            background_color="#388E3C",
            font_size=12,
        ),
    ),
    FitnessClass(
        name="HIIT",
        start=datetime(2025, 7, 28, 8, 30),
        end=datetime(2025, 7, 28, 9, 15),
        instructor="Bob Johnson",
        description="High intensity interval training.",
        render_config=FitnessClassRenderConfig(
            text_color="white",
            background_color="#FBC02D",
            font_size=12,
        ),
    ),
    FitnessClass(
        name="Evening Stretch",
        start=datetime(2025, 7, 28, 18, 0),
        end=datetime(2025, 7, 28, 19, 0),
        instructor="Eva Green",
        description="Relaxing stretch to end Monday.",
        render_config=FitnessClassRenderConfig(
            text_color="black",
            background_color="#B2DFDB",
            font_size=12,
        ),
    ),
    # Tuesday (2025-07-29)
    FitnessClass(
        name="Cardio Blast",
        start=datetime(2025, 7, 29, 9, 0),
        end=datetime(2025, 7, 29, 10, 0),
        instructor="Bob Johnson",
        description="Cardio workout for all levels.",
        render_config=FitnessClassRenderConfig(
            text_color="white",
            background_color="#D32F2F",
            font_size=12,
        ),
    ),
    FitnessClass(
        name="Core Strength",
        start=datetime(2025, 7, 29, 10, 30),
        end=datetime(2025, 7, 29, 11, 15),
        instructor="Cathy Lee",
        description="Strengthen your core muscles.",
        render_config=FitnessClassRenderConfig(
            text_color="black",
            background_color="#FFD54F",
            font_size=12,
        ),
    ),
    FitnessClass(
        name="Zumba",
        start=datetime(2025, 7, 29, 18, 0),
        end=datetime(2025, 7, 29, 19, 0),
        instructor="Alice Smith",
        description="Dance your way to fitness.",
        render_config=FitnessClassRenderConfig(
            text_color="white",
            background_color="#F06292",
            font_size=12,
        ),
    ),
    # Wednesday (2025-07-30)
    FitnessClass(
        name="Spin",
        start=datetime(2025, 7, 30, 8, 0),
        end=datetime(2025, 7, 30, 9, 0),
        instructor="Eva Green",
        description="Morning spin class.",
        render_config=FitnessClassRenderConfig(
            text_color="white",
            background_color="#8E24AA",
            font_size=12,
        ),
    ),
    FitnessClass(
        name="Pilates",
        start=datetime(2025, 7, 30, 9, 30),
        end=datetime(2025, 7, 30, 10, 30),
        instructor="Cathy Lee",
        description="Strengthen and tone with Pilates.",
        render_config=FitnessClassRenderConfig(
            text_color="black",
            background_color="#64B5F6",
            font_size=12,
        ),
    ),
    FitnessClass(
        name="Boxing Basics",
        start=datetime(2025, 7, 30, 18, 0),
        end=datetime(2025, 7, 30, 19, 0),
        instructor="Bob Johnson",
        description="Learn boxing fundamentals.",
        render_config=FitnessClassRenderConfig(
            text_color="white",
            background_color="#212121",
            font_size=12,
        ),
    ),
    # Thursday (2025-07-31)
    FitnessClass(
        name="Yoga",
        start=datetime(2025, 7, 31, 7, 30),
        end=datetime(2025, 7, 31, 8, 30),
        instructor="Alice Smith",
        description="Midweek yoga flow.",
        render_config=FitnessClassRenderConfig(
            text_color="white",
            background_color="#43A047",
            font_size=12,
        ),
    ),
    FitnessClass(
        name="Strength Training",
        start=datetime(2025, 7, 31, 9, 0),
        end=datetime(2025, 7, 31, 10, 0),
        instructor="Bob Johnson",
        description="Build muscle and strength.",
        render_config=FitnessClassRenderConfig(
            text_color="white",
            background_color="#FFA726",
            font_size=12,
        ),
    ),
    FitnessClass(
        name="Dance Fitness",
        start=datetime(2025, 7, 31, 18, 30),
        end=datetime(2025, 7, 31, 19, 30),
        instructor="Eva Green",
        description="Fun dance workout.",
        render_config=FitnessClassRenderConfig(
            text_color="black",
            background_color="#E1BEE7",
            font_size=12,
        ),
    ),
    # Friday (2025-08-01)
    FitnessClass(
        name="Pilates",
        start=datetime(2025, 8, 1, 9, 0),
        end=datetime(2025, 8, 1, 10, 0),
        instructor="Cathy Lee",
        description="Morning Pilates.",
        render_config=FitnessClassRenderConfig(
            text_color="black",
            background_color="#64B5F6",
            font_size=12,
        ),
    ),
    FitnessClass(
        name="Functional Training",
        start=datetime(2025, 8, 1, 10, 30),
        end=datetime(2025, 8, 1, 11, 15),
        instructor="Bob Johnson",
        description="Improve everyday movement.",
        render_config=FitnessClassRenderConfig(
            text_color="white",
            background_color="#388E3C",
            font_size=12,
        ),
    ),
    FitnessClass(
        name="Evening Yoga",
        start=datetime(2025, 8, 1, 18, 0),
        end=datetime(2025, 8, 1, 19, 0),
        instructor="Alice Smith",
        description="Relaxing yoga to end the week.",
        render_config=FitnessClassRenderConfig(
            text_color="white",
            background_color="#43A047",
            font_size=12,
        ),
    ),
    # Saturday (2025-08-02)
    FitnessClass(
        name="Yoga",
        start=datetime(2025, 8, 2, 8, 0),
        end=datetime(2025, 8, 2, 9, 0),
        instructor="Alice Smith",
        description="Saturday morning yoga.",
        render_config=FitnessClassRenderConfig(
            text_color="white",
            background_color="#388E3C",
            font_size=12,
        ),
    ),
    FitnessClass(
        name="Bootcamp",
        start=datetime(2025, 8, 2, 9, 30),
        end=datetime(2025, 8, 2, 10, 30),
        instructor="Bob Johnson",
        description="Outdoor bootcamp session.",
        render_config=FitnessClassRenderConfig(
            text_color="white",
            background_color="#D32F2F",
            font_size=12,
        ),
    ),
    FitnessClass(
        name="Stretch & Mobility",
        start=datetime(2025, 8, 2, 11, 0),
        end=datetime(2025, 8, 2, 12, 0),
        instructor="Eva Green",
        description="Improve flexibility and mobility.",
        render_config=FitnessClassRenderConfig(
            text_color="black",
            background_color="#B2DFDB",
            font_size=12,
        ),
    ),
    # Sunday (2025-08-03)
    FitnessClass(
        name="Pilates",
        start=datetime(2025, 8, 3, 9, 0),
        end=datetime(2025, 8, 3, 10, 0),
        instructor="Cathy Lee",
        description="Sunday Pilates.",
        render_config=FitnessClassRenderConfig(
            text_color="black",
            background_color="#1E88E5",
            font_size=12,
        ),
    ),
    FitnessClass(
        name="Family Fitness",
        start=datetime(2025, 8, 3, 10, 30),
        end=datetime(2025, 8, 3, 11, 15),
        instructor="Alice Smith",
        description="Fun workout for all ages.",
        render_config=FitnessClassRenderConfig(
            text_color="white",
            background_color="#FBC02D",
            font_size=12,
        ),
    ),
    FitnessClass(
        name="Meditation",
        start=datetime(2025, 8, 3, 18, 0),
        end=datetime(2025, 8, 3, 18, 45),
        instructor="Eva Green",
        description="Guided meditation session.",
        render_config=FitnessClassRenderConfig(
            text_color="black",
            background_color="#E1BEE7",
            font_size=12,
        ),
    ),
    # Monday (2025-08-04)
    FitnessClass(
        name="Morning Yoga",
        start=datetime(2025, 8, 4, 7, 0),
        end=datetime(2025, 8, 4, 8, 0),
        instructor="Alice Smith",
        description="Start your week with gentle yoga.",
        render_config=FitnessClassRenderConfig(
            text_color="white",
            background_color="#388E3C",
            font_size=12,
        ),
    ),
    FitnessClass(
        name="HIIT",
        start=datetime(2025, 8, 4, 8, 30),
        end=datetime(2025, 8, 4, 9, 15),
        instructor="Bob Johnson",
        description="High intensity interval training.",
        render_config=FitnessClassRenderConfig(
            text_color="white",
            background_color="#FBC02D",
            font_size=12,
        ),
    ),
    FitnessClass(
        name="Evening Stretch",
        start=datetime(2025, 8, 4, 18, 0),
        end=datetime(2025, 8, 4, 19, 0),
        instructor="Eva Green",
        description="Relaxing stretch to end Monday.",
        render_config=FitnessClassRenderConfig(
            text_color="black",
            background_color="#B2DFDB",
            font_size=12,
        ),
    ),
    FitnessClass(
        name="Advanced Yoga",
        start=datetime(2025, 8, 15, 18, 0),
        end=datetime(2025, 8, 15, 19, 0),
        instructor="Jane Doe",
        description="Advanced yoga techniques for experienced practitioners.",
        render_config=FitnessClassRenderConfig(
            text_color="red",
            background_color="#9B34AF",
            font_size=12,
        ),
    ),
]
