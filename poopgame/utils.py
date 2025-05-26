from .models import AttemptLog

def calculate_user_level(user, question_type):
    logs = AttemptLog.objects.filter(user=user, operation=question_type).order_by('-timestamp')[:100]
    if not logs:
        return 1

    correct_rate = sum(1 for log in logs if log.is_correct) / len(logs)
    streak = 0
    for log in logs:
        if log.is_correct:
            streak += 1
        else:
            break

    print("正答率, 連続正答数",correct_rate, streak)
    if correct_rate < 0.6:
        return 1
    elif correct_rate < 0.75:
        return 2
    elif streak >= 20 and correct_rate >= 0.9:
        return 5
    elif streak >= 10 and correct_rate >= 0.85:
        return 4
    elif correct_rate >= 0.8:
        return 3
    elif correct_rate >= 0.95 and streak >= 50:
        return 7
    else:
        return 2

def get_max_value_for_level(level, difficulty="default"):
    if difficulty=="default":
        table = {
            1: 5,
            2: 10,
            3: 15,
            4: 20,
            5: 50,
            6: 100,
            7: 999,
        }
    elif difficulty == "mul":
        table = {
            1: 3,
            2: 4,
            3: 5,
            4: 6,
            5: 7,
            6: 8,
            7: 9,
        }
    return table.get(level, 10)
