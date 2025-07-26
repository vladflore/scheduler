from datetime import datetime, date
from dataclasses import dataclass, field
from collections import defaultdict
from pyweb import pydom
from js import Uint8Array, File, URL, document
from pyodide.ffi.wrappers import add_event_listener
from pyscript import document, display
import io


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
    # Saturday
    FitnessClass(
        name="Yoga",
        start=datetime(2025, 7, 26, 9, 0),
        end=datetime(2025, 7, 26, 10, 0),
        instructor="Alice Smith",
        description="A relaxing yoga session to start your day.",
        render_config=FitnessClassRenderConfig(
            text_color="white",
            background_color="#4CAF50",  # Green
            font_size=14,
        ),
    ),
    FitnessClass(
        name="HIIT",
        start=datetime(2025, 7, 26, 10, 30),
        end=datetime(2025, 7, 26, 11, 30),
        instructor="Bob Johnson",
        description="High-intensity interval training to boost your fitness.",
        render_config=FitnessClassRenderConfig(
            text_color="white",
            background_color="#FF5722",  # Red
            font_size=14,
        ),
    ),
    FitnessClass(
        name="Pilates",
        start=datetime(2025, 7, 27, 12, 0),
        end=datetime(2025, 7, 27, 13, 0),
        instructor="Cathy Lee",
        description="Strengthen your core with Pilates exercises.",
        render_config=FitnessClassRenderConfig(
            text_color="black",
            background_color="#2196F3",  # Blue
            font_size=14,
        ),
    ),
    FitnessClass(
        name="Zumba",
        start=datetime(2025, 7, 27, 13, 30),
        end=datetime(2025, 7, 27, 14, 30),
        instructor="David Brown",
        description="Dance your way to fitness with Zumba.",
        render_config=FitnessClassRenderConfig(
            text_color="white",
            background_color="#FF9800",  # Orange
            font_size=14,
        ),
    ),
    FitnessClass(
        name="Spin",
        start=datetime(2025, 7, 28, 15, 0),
        end=datetime(2025, 7, 28, 16, 0),
        instructor="Eva Green",
        description="An energetic spin class to get your heart racing.",
        render_config=FitnessClassRenderConfig(
            text_color="white",
            background_color="#9C27B0",  # Purple
            font_size=14,
        ),
    ),
    # Monday
    FitnessClass(
        name="Morning Yoga",
        start=datetime(2025, 7, 28, 7, 0),
        end=datetime(2025, 7, 28, 8, 0),
        instructor="Alice Smith",
        description="Start your week with gentle yoga.",
        render_config=FitnessClassRenderConfig(
            text_color="white",
            background_color="#388E3C",
            font_size=14,
        ),
    ),
    FitnessClass(
        name="Cardio Blast",
        start=datetime(2025, 7, 29, 9, 0),
        end=datetime(2025, 7, 29, 10, 0),
        instructor="Bob Johnson",
        description="Cardio workout for all levels.",
        render_config=FitnessClassRenderConfig(
            text_color="white",
            background_color="#D32F2F",
            font_size=14,
        ),
    ),
    FitnessClass(
        name="Pilates",
        start=datetime(2025, 7, 29, 12, 0),
        end=datetime(2025, 7, 29, 13, 0),
        instructor="Cathy Lee",
        description="Midday Pilates session.",
        render_config=FitnessClassRenderConfig(
            text_color="black",
            background_color="#1976D2",
            font_size=14,
        ),
    ),
    # Tuesday
    FitnessClass(
        name="Spin",
        start=datetime(2025, 7, 30, 8, 0),
        end=datetime(2025, 7, 30, 9, 0),
        instructor="Eva Green",
        description="Morning spin class.",
        render_config=FitnessClassRenderConfig(
            text_color="white",
            background_color="#8E24AA",
            font_size=14,
        ),
    ),
    FitnessClass(
        name="Zumba",
        start=datetime(2025, 7, 30, 10, 0),
        end=datetime(2025, 7, 30, 11, 0),
        instructor="David Brown",
        description="Dance fitness fun.",
        render_config=FitnessClassRenderConfig(
            text_color="white",
            background_color="#FBC02D",
            font_size=14,
        ),
    ),
    # Wednesday
    FitnessClass(
        name="Yoga",
        start=datetime(2025, 7, 31, 7, 30),
        end=datetime(2025, 7, 31, 8, 30),
        instructor="Alice Smith",
        description="Midweek yoga flow.",
        render_config=FitnessClassRenderConfig(
            text_color="white",
            background_color="#43A047",
            font_size=14,
        ),
    ),
    FitnessClass(
        name="HIIT",
        start=datetime(2025, 7, 31, 18, 0),
        end=datetime(2025, 7, 31, 19, 0),
        instructor="Bob Johnson",
        description="Evening HIIT session.",
        render_config=FitnessClassRenderConfig(
            text_color="white",
            background_color="#E64A19",
            font_size=14,
        ),
    ),
    # Thursday
    FitnessClass(
        name="Pilates",
        start=datetime(2025, 8, 1, 9, 0),
        end=datetime(2025, 8, 1, 10, 0),
        instructor="Cathy Lee",
        description="Morning Pilates.",
        render_config=FitnessClassRenderConfig(
            text_color="black",
            background_color="#64B5F6",
            font_size=14,
        ),
    ),
    FitnessClass(
        name="Spin",
        start=datetime(2025, 8, 1, 17, 0),
        end=datetime(2025, 8, 1, 18, 0),
        instructor="Eva Green",
        description="Evening spin ride.",
        render_config=FitnessClassRenderConfig(
            text_color="white",
            background_color="#7B1FA2",
            font_size=14,
        ),
    ),
    FitnessClass(
        name="Zumba",
        start=datetime(2025, 8, 1, 18, 30),
        end=datetime(2025, 8, 1, 19, 30),
        instructor="David Brown",
        description="Dance party workout.",
        render_config=FitnessClassRenderConfig(
            text_color="white",
            background_color="#FFA726",
            font_size=14,
        ),
    ),
    # Friday
    FitnessClass(
        name="Yoga",
        start=datetime(2025, 8, 2, 8, 0),
        end=datetime(2025, 8, 2, 9, 0),
        instructor="Alice Smith",
        description="Friday morning yoga.",
        render_config=FitnessClassRenderConfig(
            text_color="white",
            background_color="#388E3C",
            font_size=14,
        ),
    ),
    FitnessClass(
        name="HIIT",
        start=datetime(2025, 8, 2, 12, 0),
        end=datetime(2025, 8, 2, 13, 0),
        instructor="Bob Johnson",
        description="Lunchtime HIIT.",
        render_config=FitnessClassRenderConfig(
            text_color="white",
            background_color="#D84315",
            font_size=14,
        ),
    ),
    # Saturday
    FitnessClass(
        name="Pilates",
        start=datetime(2025, 8, 3, 9, 0),
        end=datetime(2025, 8, 3, 10, 0),
        instructor="Cathy Lee",
        description="Saturday Pilates.",
        render_config=FitnessClassRenderConfig(
            text_color="black",
            background_color="#1E88E5",
            font_size=14,
        ),
    ),
    FitnessClass(
        name="Spin",
        start=datetime(2025, 8, 3, 10, 30),
        end=datetime(2025, 8, 3, 11, 30),
        instructor="Eva Green",
        description="Weekend spin session.",
        render_config=FitnessClassRenderConfig(
            text_color="white",
            background_color="#8E24AA",
            font_size=14,
        ),
    ),
    FitnessClass(
        name="Zumba",
        start=datetime(2025, 8, 3, 12, 0),
        end=datetime(2025, 8, 3, 13, 0),
        instructor="David Brown",
        description="Saturday Zumba party.",
        render_config=FitnessClassRenderConfig(
            text_color="white",
            background_color="#FB8C00",
            font_size=14,
        ),
    ),
]


def render_fitness_classes(classes: list[FitnessClass]) -> str:
    # Group classes by day
    classes_by_day = defaultdict(list)
    for cls in classes:
        day = cls.start.date()
        classes_by_day[day].append(cls)

    days = sorted(classes_by_day.keys())

    # Collect all unique time intervals across all classes
    time_intervals = set()
    for cls in classes:
        time_intervals.add((cls.start.time(), cls.end.time()))
    time_intervals = sorted(time_intervals)

    # Build a mapping: (day, time_interval) -> class
    class_lookup = {}
    for day in days:
        for cls in classes_by_day[day]:
            interval = (cls.start.time(), cls.end.time())
            class_lookup[(day, interval)] = cls

    html = [
        '<table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">'
    ]

    # Header row
    html.append("<tr>")
    html.append("<th>Time / Day</th>")
    today = date.today()
    for day in days:
        week_day = day.strftime("%A")
        date_num = day.strftime("%d")
        if day == today:
            # Highlight current day with a perfect circle and yellowish background
            html.append(
                f'<th style="text-align:center;">'
                f"{week_day}<br>"
                f'<span style="display:inline-flex; align-items:center; justify-content:center; border-radius:50%; background:#FFF59D; width:2.5em; height:2.5em; font-size: 1.5em; font-weight: bold;">{date_num}</span>'
                f"</th>"
            )
        else:
            html.append(
                f'<th style="text-align:center;">'
                f"{week_day}<br>"
                f'<span style="font-size: 1.5em; font-weight: bold;">{date_num}</span>'
                f"</th>"
            )
    html.append("</tr>")

    # Rows for each time interval
    for idx, interval in enumerate(time_intervals):
        start_str = interval[0].strftime("%H:%M")
        end_str = interval[1].strftime("%H:%M")
        # Alternate row background color for highlighting
        row_bg = "#f2f2f2" if idx % 2 == 0 else "#e0e7ff"
        html.append(f'<tr style="background-color: {row_bg};">')
        html.append(f"<td><strong>{start_str} - {end_str}</strong></td>")
        for day in days:
            fitness_class: FitnessClass | None = class_lookup.get((day, interval))
            cell_style = "padding:10px; margin:0px;"
            if fitness_class:
                config = fitness_class.render_config
                html.append(
                    f'<td style="color:{config.text_color}; background:{config.background_color}; font-size:{config.font_size}px; {cell_style}">'
                    f"<strong>{fitness_class.name}</strong><br>"
                    f"Instructor: {fitness_class.instructor}<br>"
                    f"<em>{fitness_class.description}</em>"
                    "</td>"
                )
            else:
                html.append(f'<td style="{cell_style}"></td>')
        html.append("</tr>")

    html.append("</table>")
    return "\n".join(html)


iframe = pydom["#schedule"][0]._js
iframe_doc = iframe.contentDocument or iframe.contentWindow.document
iframe_doc.open()
bootstrap_css = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
)
bootstrap_icons = (
    "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css"
)
custom_css = "./assets/css/styles.css"
print_script = (
    "<script>"
    "function printSchedule() {"
    "const schedule = document.getElementById('schedule').innerHTML;"
    "const printWindow = window.open('', '_blank');"
    "printWindow.document.open();"
    "printWindow.document.write('<!DOCTYPE html>');"
    "printWindow.document.write('<html><head><title>Fitness Class Schedule</title>');"
    f'printWindow.document.write(\'<link rel="stylesheet" href="{bootstrap_css}">\');'
    f'printWindow.document.write(\'<link rel="stylesheet" href="{bootstrap_icons}">\');'
    f'printWindow.document.write(\'<link rel="stylesheet" href="{custom_css}">\');'
    "printWindow.document.write('</head><body>');"
    "printWindow.document.write('<main><section>');"
    "printWindow.document.write(schedule);"
    "printWindow.document.write('</section></main>');"
    "printWindow.document.write('</body></html>');"
    "printWindow.document.close();"
    "printWindow.print();"
    "}"
    "</script>"
)
iframe_html = (
    "<!DOCTYPE html>"
    "<html>"
    "<head>"
    "<meta charset='utf-8'>"
    "<meta name='viewport' content='width=device-width, initial-scale=1'>"
    f"<link rel='stylesheet' href='{custom_css}'/>"
    f"<link href='{bootstrap_css}' rel='stylesheet'/>"
    f"<link rel='stylesheet' href='{bootstrap_icons}'/>"
    "</head>"
    "<body>"
    "<main><section>"
    "<div class='mb-3'><button class='btn btn-primary' onclick='printSchedule()'><i class='bi bi-printer fs-4'></i></button></div>"
    f"{print_script}"
    f"<div id='schedule' class=''>{render_fitness_classes(classes)}</div>"
    "</section></main>"
    "</body>"
    "</html>"
)
iframe_doc.write(iframe_html)
iframe_doc.close()


def download_iframe(event):
    encoded_data = iframe_html.encode("utf-8")
    my_stream = io.BytesIO(encoded_data)

    js_array = Uint8Array.new(len(encoded_data))
    js_array.assign(my_stream.getbuffer())

    file = File.new([js_array], "unused_file_name.html", {type: "text/html"})
    url = URL.createObjectURL(file)

    hidden_link = document.createElement("a")
    hidden_link.setAttribute(
        "download",
        f"iframe_{datetime.now().strftime('%d%m%Y_%H%M%S')}.html",
    )
    hidden_link.setAttribute("href", url)
    hidden_link.click()


add_event_listener(document.getElementById("download-iframe"), "click", download_iframe)
