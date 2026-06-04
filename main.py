from datetime import date
import json
import os


DATA_FILE = "assignments.json"


# 저장된 과제 목록을 불러오는 함수
def load_assignments():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("저장 파일을 읽을 수 없어 새 목록으로 시작합니다.")
        return []


# 과제 목록을 파일에 저장하는 함수
def save_assignments(assignments):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(assignments, file, ensure_ascii=False, indent=2)


# YYYY-MM-DD 형식의 문자열을 날짜로 바꾸는 함수
def parse_date(date_text):
    year, month, day = date_text.split("-")
    return date(int(year), int(month), int(day))


# 오늘 날짜와 마감일의 차이를 계산하는 함수
def calculate_d_day(deadline_text):
    deadline = parse_date(deadline_text)
    today = date.today()
    return (deadline - today).days


# 난이도를 숫자 점수로 바꾸는 함수
def difficulty_score(difficulty):
    if difficulty == "상":
        return 3
    if difficulty == "중":
        return 2
    return 1


# 마감일과 난이도를 함께 고려한 우선순위 점수
def priority_score(assignment):
    days_left = calculate_d_day(assignment["deadline"])
    score = difficulty_score(assignment["difficulty"]) * 10

    if days_left < 0:
        score += 100
    elif days_left <= 1:
        score += 50
    elif days_left <= 3:
        score += 30
    elif days_left <= 7:
        score += 10

    return score


# 새 과제를 입력받아 목록에 추가하는 함수
def add_assignment(assignments):
    print("\n[과제 추가]")
    title = input("과제명: ").strip()
    subject = input("과목명: ").strip()
    deadline = input("마감일(예: 2026-06-10): ").strip()
    assignment_type = input("과제 종류(보고서/발표/코딩/시험공부/기타): ").strip()
    difficulty = input("난이도(상/중/하): ").strip()

    if difficulty not in ["상", "중", "하"]:
        difficulty = "중"

    try:
        parse_date(deadline)
    except ValueError:
        print("마감일 형식이 올바르지 않습니다. 과제를 추가하지 않았습니다.")
        return

    assignment = {
        "title": title,
        "subject": subject,
        "deadline": deadline,
        "type": assignment_type,
        "difficulty": difficulty,
    }

    assignments.append(assignment)
    save_assignments(assignments)
    print("과제가 추가되었습니다.")


# 과제 하나를 보기 좋게 출력하는 함수
def show_assignment(assignment, number):
    days_left = calculate_d_day(assignment["deadline"])

    if days_left < 0:
        d_day_text = f"마감 {abs(days_left)}일 지남"
    elif days_left == 0:
        d_day_text = "오늘 마감"
    else:
        d_day_text = f"{days_left}일 남음"

    print(f"{number}. {assignment['title']} ({assignment['subject']})")
    print(f"   마감일: {assignment['deadline']} / {d_day_text}")
    print(f"   종류: {assignment['type']} / 난이도: {assignment['difficulty']}")


# 전체 과제 목록을 출력하는 함수
def show_all_assignments(assignments):
    print("\n[전체 과제 목록]")
    if not assignments:
        print("등록된 과제가 없습니다.")
        return

    for index, assignment in enumerate(assignments, start=1):
        show_assignment(assignment, index)


# 우선순위가 높은 순서로 과제를 출력하는 함수
def show_priority_assignments(assignments):
    print("\n[우선순위 과제 목록]")
    if not assignments:
        print("등록된 과제가 없습니다.")
        return

    sorted_assignments = sorted(assignments, key=priority_score, reverse=True)

    for index, assignment in enumerate(sorted_assignments, start=1):
        show_assignment(assignment, index)


# 메뉴를 출력하는 함수
def show_menu():
    print("\n=== D-day 과제 처리기 ===")
    print("1. 과제 추가")
    print("2. 전체 과제 보기")
    print("3. 우선순위 보기")
    print("4. 종료")


# 프로그램의 시작점
def main():
    assignments = load_assignments()

    while True:
        show_menu()
        choice = input("메뉴 선택: ").strip()

        if choice == "1":
            add_assignment(assignments)
        elif choice == "2":
            show_all_assignments(assignments)
        elif choice == "3":
            show_priority_assignments(assignments)
        elif choice == "4":
            print("프로그램을 종료합니다.")
            break
        else:
            print("1~4 중에서 선택해주세요.")


if __name__ == "__main__":
    main()
