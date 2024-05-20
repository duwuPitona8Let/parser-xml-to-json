import xml.etree.ElementTree as ET
import json
import os




TRANSLITERATION_DICT = {
    'А': 'A', 'Б': 'B', 'В': 'V', 'О': 'O', 'М': 'M', 'Е': 'E', 'И': 'I', 'С': 'C', 'Р': 'R',
    'П': 'P', 'К': 'K',
}
WEEKDAYS_DICT = {
    'Понедельник': 1,
    'Вторник': 2,
    'Среда': 3,
    'Четверг': 4,
    'Пятница': 5,
    'Суббота': 6,
}



def transliterate(text):

    transliterated_text = ""
    for char in text:
        if char in TRANSLITERATION_DICT:
            transliterated_text += TRANSLITERATION_DICT[char]
        else:
            transliterated_text += char
    return transliterated_text


def extract_schedule(group):
    group_number = group.attrib['Number']
    schedule = []

    days = group.find('Days')
    if days is not None:
        for day in days.findall('Day'):
            day_title = day.attrib['Title']
            day_number = WEEKDAYS_DICT.get(day_title)
            group_lessons = day.find('GroupLessons')
            if group_lessons is not None:
                lessons = group_lessons.findall('Lesson')
                for lesson in lessons:
                    week_code = int(lesson.find('WeekCode').text)
                    time = lesson.find('Time').text
                    discipline = lesson.find('Discipline').text
                    classroom = lesson.find('Classroom').text

                    lecturer_element = lesson.find('Lecturers')
                    if lecturer_element is not None:
                        lecturer = lecturer_element.find('Lecturer')
                        if lecturer is not None:
                            lecturer_name = lecturer.find('ShortName').text
                        else:
                            lecturer_name = None
                    else:
                        lecturer_name = None

                    schedule.append({
                        'day': day_number,
                        'week_code': week_code,
                        'time': time,
                        'discipline': discipline,
                        'classroom': classroom,
                        'lecturer': lecturer_name
                    })

    return group_number, schedule



tree = ET.parse('schedule.xml')
root = tree.getroot()


os.makedirs('group_schedules', exist_ok=True)


for group in root.findall('Group'):
    group_number, schedule = extract_schedule(group)


    trans_group_number = transliterate(group_number)

    json_filename = f'group_schedules/{trans_group_number}.json'
    with open(json_filename, 'w', encoding='utf-8') as json_file:
        json.dump(schedule, json_file, ensure_ascii=False, indent=4)

    print(f"Расписание {group_number} сохранено  {json_filename}")
