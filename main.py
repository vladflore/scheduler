from datetime import datetime, date, timedelta
from collections import defaultdict
from pyweb import pydom
from pyscript import display
from data import FitnessClass
from pyodide.ffi import create_proxy
from data import load_classes_from_file
from config import translations, LANGUAGE, WHATSAPP_NUMBER


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
                html.append(
                    f'<div class="schedule-cell" style="color:{config.text_color}; background:{config.background_color};">'
                    f"<strong>{fitness_class.name}</strong><br>"
                    f"{translations[LANGUAGE]['instructor']}: {fitness_class.instructor}<br>"
                    f'<a class="whatsapp-link" href="{whatsapp_url}" target="_blank">'
                    f"{translations[LANGUAGE]['book_via_whatsapp']}"
                    f"</a>"
                    "</div>"
                )
            else:
                html.append('<div class="schedule-cell schedule-cell-empty"></div>')
    html.append("</div>")
    return "\n".join(html)


def print_schedule(event): ...


classes = load_classes_from_file(language=LANGUAGE)

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

pydom["#schedule"][0]._js.innerHTML = render_fitness_classes(
    filtered_classes, date.today()
)
pydom["#schedule-date"][0]._js.value = datetime.now().strftime("%Y-%m-%d")
pydom["#schedule-date"][0]._js.min = min_date.strftime("%Y-%m-%d")
pydom["#schedule-date"][0]._js.max = max_date.strftime("%Y-%m-%d")


def on_date_change(evt):
    value = evt.target.value
    if not value:
        return
    new_date = datetime.strptime(value, "%Y-%m-%d").date()
    week_start_date = new_date - timedelta(days=new_date.weekday())
    week_end_date = week_start_date + timedelta(days=6)
    filtered_classes = [
        cls for cls in classes if week_start_date <= cls.start.date() <= week_end_date
    ]
    pydom["#schedule"][0]._js.innerHTML = render_fitness_classes(
        filtered_classes, new_date
    )


pydom["#schedule-date"][0]._js.addEventListener("change", create_proxy(on_date_change))
pydom["#schedule-date-label"][0]._js.innerHTML = translations[LANGUAGE][
    "schedule_date_label"
]
