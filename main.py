"""
Module main.py

Модуль тестирования знаний. Загружает из файла вопросы с ответами в специальном
формате и формирует тестовые вопросы с проверкой ответов.
"""
from random import randint
from reportlab.pdfgen import canvas  # Для формирования PDF-файлов
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


# Путь к файлу с вопросами
FILE_PATH = 'questions2.txt'


def load_questions(file):
    """
    Загружает вопросы и ответы из файла.
    Файл должен быть в формате:
    Вопрос $вариант ответа $Вариант ответа $@Вариант правильного ответа
    $Вариант ответа $Вариант ответа
    """
    questions = []
    questions_list = []

    # Открываем файл и читаем его
    with open(file, 'r', encoding='utf-8') as qfile:
        for list_item in qfile:
            questions_list.append(
                list_item.strip())  # Очищаем строки от лишних пробелов

    # Проверим содержимое файла
    if not questions_list:
        print("Файл пустой или не содержит строк.")
        return []

    # Выведем первые 5 строк файла для проверки
    # print("Прочитанные строки файла:")
    # for line in questions_list[:5]:  # Покажем только первые 5 строк для проверки
    #     print(line)

    # Обрабатываем все строки в файле (убираем проверку на 20 случайных вопросов)
    for line in questions_list:
        parts = line.split(' $')  # Разделяем строку по символу '$'

        if len(parts) > 1:  # Убедимся, что строка содержит хотя бы один вариант ответа
            question = parts[0].replace('$',
                                        '').strip()  # Извлекаем вопрос, удаляя лишние '$'

            # Найдем правильный ответ, который начинается с '$@'
            correct_answer = None
            answers = []

            # Обрабатываем каждый вариант ответа
            for part in parts[1:]:
                part = part.strip()  # Убираем лишние пробелы

                if part.startswith('@'):
                    correct_answer = part[
                                     1:].strip()  # Убираем символ '@' у правильного ответа
                    answers.append(
                        correct_answer)  # Добавление правильного ответа в список ответов
                else:
                    answers.append(
                        part.strip('-').strip('+'))  # Очищаем от лишних знаков

            # Проверка на наличие правильного ответа
            if correct_answer is None:
                print(f"Отсутствует правильный ответ в вопросе: {question}")
                continue  # Если правильный ответ не найден, пропускаем этот вопрос

            questions.append({
                'question': question,
                'correct_answer': correct_answer,
                'answers': answers
            })

    return questions


def ask_question(question_data):
    """
    Выводит вопрос и варианты ответов, принимает ответ пользователя и проверяет
     его.
    """
    print(question_data['question'])
    for i, answer in enumerate(question_data['answers'], 1):
        print(f"{i}. {answer}")

    user_answer = int(input("Выберите номер правильного ответа: "))

    # Проверка, правильный ли ответ
    return question_data['answers'][user_answer - 1] == question_data[
        'correct_answer']


def run_quiz(file):
    """
    Запускает викторину, загружает вопросы из файла, задает их пользователю,
    проверяет ответы и подсчитывает количество правильных.
    """
    questions = load_questions(file)
    correct_answers = 0

    if not questions:
        print("Вопросы не загружены. Проверьте файл.")
        return

    # Ограничение по количеству вопросов
    number_of_questions = int(input('Введите количество вопросов для теста: '))
    # Первый вопрос это случайный от 0 до общего количества вопросов минус
    # желаемое количество вопросов
    start_question = randint(0, len(questions)-number_of_questions)
    # Срез массива вопросов из общего списка
    questions = questions[start_question:start_question + number_of_questions]

    order_number = 1
    for question_data in questions:
        # Нумерация вопросов
        print(f"Вопрос № {order_number} из {len(questions)}")
        if ask_question(question_data):
            print("Правильный ответ! \n")
            correct_answers += 1
        else:
            print("Неправильный ответ. \n")
        order_number += 1

    print(
        f"Вы ответили правильно на {correct_answers} из {len(questions)} "
        f"вопросов. {(correct_answers/len(questions)*100):.1f}%")

    pdf_task = input("Выгрузить файл pdf с результатом тестирования? (д/н)")
    yes_list = ['да', 'д', 'yes', 'y']
    if pdf_task.lower() in yes_list:
        #region Блок формирования pdf-отчёта.
        # Создаём объект canvas
        pdf_file = "output.pdf"
        c = canvas.Canvas(pdf_file, pagesize=letter)

        # Регистрируем шрифт OTF
        pdfmetrics.registerFont(
            TTFont('CaviarDreams', 'caviar-dreams.ttf'))

        # Устанавливаем шрифт и размер текста
        c.setFont("CaviarDreams", 14)

        # Добавляем текст на страницу (x, y) — это координаты на странице
        c.drawString(100, 750, f"Вы ответили правильно на "
                               f"{correct_answers} из {len(questions)} вопросов. "
                               f"{(correct_answers/len(questions)*100):.1f}%")

        # Сохраняем PDF
        c.save()
        #endregion

    print("Завершение тестирования.")


if __name__ == '__main__':
    run_quiz(FILE_PATH)
