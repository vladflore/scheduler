from datetime import datetime, date, timedelta
from collections import defaultdict
from data import FitnessClass
from pyodide.ffi import create_proxy
from data import (
    load_classes_from_file,
    dummy_classes,
    load_classes_from_url,
    load_dummy_classes,
    CLASSES_INPUT_FILE_URL,
)
from config import (
    translations,
    LANGUAGE,
    WHATSAPP_NUMBER,
    BOOK_VIA_WHATSAPP,
    DataSourceMode,
    DATA_SOURCE_MODE,
)
import io
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from js import Uint8Array, File, URL, document
from pyodide.ffi import create_proxy
from pyscript import document, display
from pyweb import pydom
import json


def render_fitness_classes(classes: list[FitnessClass], highlighted_date: date) -> str:
    classes_by_day = defaultdict(list)
    for cls in classes:
        day = cls.start.date()
        classes_by_day[day].append(cls)

    days = sorted(classes_by_day.keys())

    if days:
        if len(days) < 7:
            last_day = days[-1]
            week_start_day = last_day - timedelta(days=last_day.weekday())
            days = [week_start_day + timedelta(days=i) for i in range(7)]
    else:
        week_start_day = highlighted_date - timedelta(days=highlighted_date.weekday())
        days = [week_start_day + timedelta(days=i) for i in range(7)]
    days = sorted(days)

    time_intervals = set()
    for cls in classes:
        time_intervals.add((cls.start.time(), cls.end.time()))
    time_intervals = sorted(time_intervals)

    class_lookup = {}
    for day in days:
        for cls in classes_by_day[day]:
            interval = (cls.start.time(), cls.end.time())
            class_lookup[(day, interval)] = cls

    html = []

    html.append('<div class="schedule-grid">')
    html.append(
        f'<div class="schedule-header">{translations[LANGUAGE]["time"]} / {translations[LANGUAGE]["date"]}</div>'
    )
    for day in days:
        week_day = day.strftime("%A")
        date_num = day.strftime("%d")
        if day == highlighted_date:
            html.append(
                f'<div class="schedule-header">'
                f"{translations[LANGUAGE]['week_days'][week_day.lower()]}<br>"
                f'<span class="schedule-today">{date_num}</span>'
                f"</div>"
            )
        else:
            html.append(
                f'<div class="schedule-header">'
                f"{translations[LANGUAGE]['week_days'][week_day.lower()]}<br>"
                f'<span style="font-size: 1.5em; font-weight: bold;">{date_num}</span>'
                f"</div>"
            )

    for interval in time_intervals:
        start_str = interval[0].strftime("%H:%M")
        end_str = interval[1].strftime("%H:%M")
        html.append(f'<div class="schedule-time">{start_str}-{end_str}</div>')
        for day in days:
            fitness_class: FitnessClass | None = class_lookup.get((day, interval))
            if fitness_class:
                config = fitness_class.render_config
                whatsapp_number = WHATSAPP_NUMBER
                message_template: str = translations[LANGUAGE]["whatsapp_message"]
                message = message_template.format(
                    class_name=fitness_class.name,
                    instructor=fitness_class.instructor,
                    date=day.strftime("%A, %d %B %Y"),
                    time=start_str,
                )
                whatsapp_url = f"https://wa.me/{whatsapp_number}?text={message.replace(' ', '%20')}"

                if BOOK_VIA_WHATSAPP:
                    book_via_whatsapp = (
                        f'<a class="whatsapp-link" href="{whatsapp_url}" target="_blank">'
                        f"{translations[LANGUAGE]['book_via_whatsapp']}"
                        f"</a>"
                    )
                else:
                    book_via_whatsapp = (
                        f'<span style="color:gray; font-style:italic; cursor:not-allowed;" '
                        f'title="Feature disabled.">'
                        f"{translations[LANGUAGE]['book_via_whatsapp']}"
                        f"</span>"
                    )

                html.append(
                    f'<div class="schedule-cell" style="color:{config.text_color}; background:{config.background_color};">'
                    f"<strong>{fitness_class.name}</strong><br>"
                    f"{translations[LANGUAGE]['instructor']}: {fitness_class.instructor}<br>"
                    f"{book_via_whatsapp}<br>"
                    "</div>"
                )
            else:
                html.append('<div class="schedule-cell schedule-cell-empty"></div>')
    html.append("</div>")
    return "\n".join(html)


def create_pdf(classes: list[FitnessClass]) -> FPDF:
    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=10)

    page_width = 297  # A4 landscape width in mm
    page_height = 210  # A4 landscape height in mm
    steps = 100
    for i in range(steps):
        r1, g1, b1 = (
            int(153 * 0.7 + 255 * 0.3),
            int(94 * 0.7 + 255 * 0.3),
            int(10 * 0.7 + 255 * 0.3),
        )
        r2, g2, b2 = (255, 255, 255)
        ratio = i / steps
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        y = (page_height / steps) * i
        pdf.set_fill_color(r, g, b)
        pdf.rect(0, y, page_width, page_height / steps, "F")

    pdf.set_y(4)
    pdf.set_font("Helvetica", "B", 18)
    title = translations[LANGUAGE].get("schedule_title", "Classes Schedule")
    pdf.set_text_color(40, 40, 80)
    pdf.cell(0, 12, title, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 14)

    classes_by_day = defaultdict(list)
    for cls in classes:
        day = cls.start.date()
        classes_by_day[day].append(cls)
    days = sorted(classes_by_day.keys())
    if days:
        if len(days) < 7:
            last_day = days[-1]
            week_start_day = last_day - timedelta(days=last_day.weekday())
            days = [week_start_day + timedelta(days=i) for i in range(7)]
    else:
        week_start_day = date.today() - timedelta(days=date.today().weekday())
        days = [week_start_day + timedelta(days=i) for i in range(7)]
    days = sorted(days)

    time_intervals = set()
    for cls in classes:
        time_intervals.add((cls.start.time(), cls.end.time()))
    time_intervals = sorted(time_intervals)

    class_lookup = {}
    for day in days:
        for cls in classes_by_day[day]:
            interval = (cls.start.time(), cls.end.time())
            class_lookup[(day, interval)] = cls

    cell_height = 15
    cell_width_time = 35
    cell_width_day = (
        277 - cell_width_time
    ) / 7  # 277mm is printable width in landscape A4

    pdf.set_fill_color(220, 220, 220)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(
        cell_width_time,
        cell_height,
        f"{translations[LANGUAGE]['time']} / {translations[LANGUAGE]['date']}",
        border=1,
        align="C",
        fill=True,
    )
    for day in days:
        week_day = day.strftime("%A")
        date_num = day.strftime("%d")
        pdf.set_font("Helvetica", "B", 11)
        week_label = translations[LANGUAGE]["week_days"][week_day.lower()]
        date_label = date_num
        label = f"{week_label}\n{date_label}"
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.set_fill_color(220, 220, 220)
        pdf.multi_cell(
            cell_width_day, cell_height / 2, label, border=1, align="C", fill=True
        )
        pdf.set_xy(x + cell_width_day, y)
    pdf.ln(cell_height)

    for interval in time_intervals:
        start_str = interval[0].strftime("%H:%M")
        end_str = interval[1].strftime("%H:%M")
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(0, 0, 0)
        pdf.set_fill_color(255, 255, 255)
        pdf.cell(
            cell_width_time,
            cell_height,
            f"{start_str}-{end_str}",
            border=1,
            align="C",
            fill=True,
        )
        for day in days:
            fitness_class = class_lookup.get((day, interval))
            if fitness_class:
                config = fitness_class.render_config
                font_family = (
                    config.font_family
                    if hasattr(config, "font_family")
                    else "Helvetica"
                )
                font_style = config.font_style if hasattr(config, "font_style") else ""
                try:
                    hex_color = config.text_color.lstrip("#")
                    r, g, b = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
                    pdf.set_text_color(r, g, b)
                except Exception:
                    pdf.set_text_color(0, 0, 0)
                try:
                    hex_bg = config.background_color.lstrip("#")
                    br, bg, bb = tuple(int(hex_bg[i : i + 2], 16) for i in (0, 2, 4))
                    pdf.set_fill_color(br, bg, bb)
                except Exception:
                    pdf.set_fill_color(255, 255, 255)
                text = f"{fitness_class.name}"

                font_size = 11
                pdf.set_font(font_family, font_style, font_size)
                text_width = pdf.get_string_width(text)
                while text_width > (cell_width_day - 2) and font_size > 6:
                    font_size -= 1
                    pdf.set_font(font_family, font_style, font_size)
                    text_width = pdf.get_string_width(text)
                pdf.cell(
                    cell_width_day,
                    cell_height,
                    text,
                    border=1,
                    align="C",
                    fill=True,
                )
            else:
                pdf.set_font("Helvetica", "", 11)
                pdf.set_text_color(0, 0, 0)
                pdf.set_fill_color(255, 255, 255)
                pdf.cell(cell_width_day, cell_height, "", border=1, fill=True)
        pdf.ln(cell_height)

        logo_path = "logo-nobg.png"
        logo_diameter = 15
        x_logo = 0
        y_logo = page_height - logo_diameter
        pdf.image(
            logo_path,
            x=x_logo,
            y=y_logo,
            w=logo_diameter,
            h=logo_diameter,
            type="",
            link="",
        )

    return pdf


def download_pdf(event):
    pdf = create_pdf(filtered_classes)
    encoded_data = pdf.output()
    my_stream = io.BytesIO(encoded_data)

    js_array = Uint8Array.new(len(encoded_data))
    js_array.assign(my_stream.getbuffer())

    file = File.new([js_array], "unused_file_name.pdf", {type: "application/pdf"})
    url = URL.createObjectURL(file)

    hidden_link = document.createElement("a")
    hidden_link.setAttribute(
        "download",
        f"plan_{current_week_start_date.strftime('%d.%m.%Y')}_{current_week_end_date.strftime('%d.%m.%Y')}_{LANGUAGE}.pdf",
    )
    hidden_link.setAttribute("href", url)
    hidden_link.click()


classes = []

if DATA_SOURCE_MODE == DataSourceMode.URL:
    classes = load_classes_from_url(CLASSES_INPUT_FILE_URL)
elif DATA_SOURCE_MODE == DataSourceMode.LOCAL:
    classes = load_classes_from_file(LANGUAGE)
else:
    classes = load_dummy_classes()


if classes:
    min_date = min(cls.start.date() for cls in classes)
    max_date = max(cls.start.date() for cls in classes)
else:
    min_date = date.today()
    max_date = date.today()

current_week_start_date = date.today() - timedelta(days=date.today().weekday())
current_week_end_date = current_week_start_date + timedelta(days=6)
filtered_classes = [
    cls
    for cls in classes
    if current_week_start_date <= cls.start.date() <= current_week_end_date
]

schedule_div = pydom["#schedule"][0]
schedule_div._js.innerHTML = render_fitness_classes(filtered_classes, date.today())
schedule_div._js.classList.remove("d-none")

pydom["#spinner"][0]._js.classList.add("d-none")

schedule_date_input = pydom["#schedule-date"][0]
schedule_date_input._js.value = datetime.now().strftime("%Y-%m-%d")
schedule_date_input._js.min = min_date.strftime("%Y-%m-%d")
schedule_date_input._js.max = max_date.strftime("%Y-%m-%d")

schedule_date_label = pydom["#schedule-date-label"][0]
schedule_date_label._js.innerHTML = translations[LANGUAGE]["schedule_date_label"]

pydom["#tools"][0]._js.classList.remove("d-none")


def on_date_change(evt):
    value = evt.target.value
    if not value:
        return
    new_date = datetime.strptime(value, "%Y-%m-%d").date()
    current_week_start_date = new_date - timedelta(days=new_date.weekday())
    current_week_end_date = current_week_start_date + timedelta(days=6)
    filtered_classes = [
        cls
        for cls in classes
        if current_week_start_date <= cls.start.date() <= current_week_end_date
    ]
    pydom["#schedule"][0]._js.innerHTML = render_fitness_classes(
        filtered_classes, new_date
    )


schedule_date_input._js.addEventListener("change", create_proxy(on_date_change))


async def upload_file_and_show(e):
    file_list = e.target.files
    first_item = file_list.item(0)

    my_bytes: bytes = await get_bytes_from_file(first_item)

    try:
        data = json.loads(my_bytes.decode("utf-8"))
        loaded_classes = [
            FitnessClass.from_dict(item) for item in data["fitness_classes"]
        ]
    except Exception as ex:
        display(f"Failed to load classes: {ex}")
        loaded_classes = []

    # TODO do something with loaded_classes


async def get_bytes_from_file(file):
    array_buf = await file.arrayBuffer()
    return array_buf.to_bytes()


# pydom["#file-upload"][0]._js.addEventListener(
#     "change", create_proxy(upload_file_and_show)
# )
