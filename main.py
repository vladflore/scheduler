from datetime import datetime, date
from collections import defaultdict
from pyweb import pydom
from pyscript import display
from data import FitnessClass
from data import classes


def render_fitness_classes(classes: list[FitnessClass]) -> str:
    classes_by_day = defaultdict(list)
    for cls in classes:
        day = cls.start.date()
        classes_by_day[day].append(cls)

    days = sorted(classes_by_day.keys())

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
    html.append('<div class="schedule-header">Time / Date</div>')
    today = date.today()
    for day in days:
        week_day = day.strftime("%A")
        date_num = day.strftime("%d")
        if day == today:
            html.append(
                f'<div class="schedule-header">'
                f"{week_day}<br>"
                f'<span class="schedule-today">{date_num}</span>'
                f"</div>"
            )
        else:
            html.append(
                f'<div class="schedule-header">'
                f"{week_day}<br>"
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
                whatsapp_number = "+34613429288"
                message = (
                    f"Hi, I would like to book the class '{fitness_class.name}' with {fitness_class.instructor} "
                    f"on {day.strftime('%A, %d %B %Y')} at {start_str}."
                )
                whatsapp_url = f"https://wa.me/{whatsapp_number}?text={message.replace(' ', '%20')}"
                html.append(
                    f'<div class="schedule-cell" style="color:{config.text_color}; background:{config.background_color};">'
                    f"<strong>{fitness_class.name}</strong><br>"
                    f"Instructor: {fitness_class.instructor}<br>"
                    f'<a class="whatsapp-link" href="{whatsapp_url}" target="_blank">'
                    f"Book via WhatsApp"
                    f"</a>"
                    "</div>"
                )
            else:
                html.append('<div class="schedule-cell schedule-cell-empty"></div>')
    html.append("</div>")
    return "\n".join(html)


def print_schedule(event):
    display("Printing schedule...")


pydom["#schedule"][0]._js.innerHTML = render_fitness_classes(classes)
