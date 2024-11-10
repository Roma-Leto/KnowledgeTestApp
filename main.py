def load_questions(file_path):
    """
    Загружает вопросы и ответы из файла.
    Файл должен быть в формате:
    Вопрос, правильный ответ, вариант 1, вариант 2, вариант 3, вариант 4.
    """
    questions = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(' ,')
            if len(parts) > 1:
                question = parts[0]
                correct_answer = parts[1].strip(
                    '+')  # Убираем "+" у правильного ответа
                answers = [answer.strip('-') for answer in parts[2:]]
                questions.append({
                    'question': question,
                    'correct_answer': correct_answer,
                    'answers': answers
                })

    return questions


def ask_question(question_data):
    """
    Выводит вопрос и варианты ответов, принимает ответ пользователя и проверяет его.
    """
    print(question_data['question'])
    for i, answer in enumerate(question_data['answers'], 1):
        print(f"{i}. {answer}")

    user_answer = int(input("Выберите номер правильного ответа: "))

    # Проверка, правильный ли ответ
    return question_data['answers'][user_answer - 1] == question_data[
        'correct_answer']


def run_quiz(file_path):
    """
    Запускает викторину, загружает вопросы из файла, задает их пользователю,
    проверяет ответы и подсчитывает количество правильных.
    """
    questions = load_questions(file_path)
    correct_answers = 0

    for question_data in questions:
        if ask_question(question_data):
            print("Правильный ответ!")
            correct_answers += 1
        else:
            print("Неправильный ответ.")

    print(
        f"Вы ответили правильно на {correct_answers} из {len(questions)} вопросов.")


# Путь к файлу с вопросами
file_path = 'questions.txt'

run_quiz(file_path)
