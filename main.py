from datetime import date


assignments = []


# 마감일까지 며칠 남았는지 계산하는 함수
def calculate_d_day(deadline):
    parts = deadline.split("-")
    year = int(parts[0])
    month = int(parts[1])
    day = int(parts[2])

    deadline_date = date(year, month, day)
    today = date.today()

    return (deadline_date - today).days


# 난이도를 점수로 바꾸는 함수
def difficulty_score(difficulty):
    if difficulty == "상":
        return 3
    elif difficulty == "중":
        return 2
    else:
        return 1


# 과제 종류를 점수로 바꾸는 함수
def type_score(assignment_type):
    if assignment_type == "코딩" or assignment_type == "문제풀이" or assignment_type == "발표":
        return 2
    else:
        return 1


# 우선순위를 계산하는 함수
# 남은 날짜가 적을수록, 난이도와 종류 점수가 높을수록 먼저 보여준다.
def priority_score(assignment):
    days_left = calculate_d_day(assignment["deadline"])
    difficulty = difficulty_score(assignment["difficulty"])
    assignment_type = type_score(assignment["type"])

    return days_left * 10 - difficulty - assignment_type


# 새 과제를 추가하는 함수
def add_assignment():
    print("\n[과제 추가]")
    title = input("과제명: ")
    subject = input("과목명: ")
    deadline = input("마감일(예: 2026-06-10): ")
    assignment_type = input("과제 종류(발표/보고서/코딩/문제풀이/강의/기타): ")
    difficulty = input("난이도(상/중/하): ")

    assignment = {
        "title": title,
        "subject": subject,
        "deadline": deadline,
        "type": assignment_type,
        "difficulty": difficulty,
    }

    assignments.append(assignment)
    print("과제가 추가되었습니다.")


# 과제 하나를 출력하는 함수
def show_assignment(assignment, number):
    days_left = calculate_d_day(assignment["deadline"])

    if days_left > 0:
        d_day = str(days_left) + "일 남음"
    elif days_left == 0:
        d_day = "오늘 마감"
    else:
        d_day = str(abs(days_left)) + "일 지남"

    print(str(number) + ". " + assignment["title"])
    print("   과목명: " + assignment["subject"])
    print("   마감일: " + assignment["deadline"] + " / " + d_day)
    print("   종류: " + assignment["type"] + " / 난이도: " + assignment["difficulty"])


# 전체 과제 목록을 출력하는 함수
def show_all_assignments():
    print("\n[전체 과제 목록]")

    if len(assignments) == 0:
        print("등록된 과제가 없습니다.")
    else:
        for i in range(len(assignments)):
            show_assignment(assignments[i], i + 1)


# 우선순위 순서로 과제를 출력하는 함수
def show_priority_assignments():
    print("\n[우선순위 과제 목록]")

    if len(assignments) == 0:
        print("등록된 과제가 없습니다.")
    else:
        sorted_assignments = sorted(assignments, key=priority_score)

        for i in range(len(sorted_assignments)):
            show_assignment(sorted_assignments[i], i + 1)


# 메뉴를 출력하는 함수
def show_menu():
    print("\n=== D-day 과제 처리기 ===")
    print("1. 과제 추가")
    print("2. 전체 과제 보기")
    print("3. 우선순위 보기")
    print("4. 종료")


# 프로그램 시작 부분
def main():
    while True:
        show_menu()
        choice = input("메뉴 선택: ")

        if choice == "1":
            add_assignment()
        elif choice == "2":
            show_all_assignments()
        elif choice == "3":
            show_priority_assignments()
        elif choice == "4":
            print("프로그램을 종료합니다.")
            break
        else:
            print("1~4 중에서 선택해주세요.")


main()
