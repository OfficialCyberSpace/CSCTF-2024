import json


def check_answer(question, answer):
    if "alternatives" in question and answer.lower() in [
        alt.lower() for alt in question["alternatives"]
    ]:
        return True
    else:
        return question["answer"].lower() == answer.lower()


def main():
    with open("answers.json", "r") as f:
        data = json.load(f)

    questions = data["questions"]
    flag = data["flag"]
    correct_answers = 0

    for i, question in enumerate(questions, start=1):
        print(f"\nQuestion {i}:")
        print(question["question"])
        user_answer = input("Your answer: ").strip()

        if check_answer(question, user_answer):
            print("Correct!")
            correct_answers += 1
        else:
            print("Incorrect! Exiting...")
            return

    if correct_answers == len(questions):
        print(f"\nCongratulations! Here's your flag: {flag}")
    else:
        print("\nSorry, you didn't answer all questions correctly.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"\nAn error occurred. Exiting...")
