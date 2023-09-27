from __future__ import annotations

import json
from difflib import get_close_matches
import os


def load_knowledge_base(file_path: str) -> dict:
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            try:
                data: dict = json.load(file)
            except Exception as e:
                print(f"Warning: Error loading json file > {file_path}.\nError Reason: {e}")
                return {}
        return data
    else:
        print(f"Warning: file name > {file_path} doesn't exist")
        return {}


def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file)


def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None


def get_answers_for_questions(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["question"]:
        if q["question"] == question:
            return q["answer"]


def chat_bot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    while True:
        try:
            user_input: str = input("You:")

            if user_input.lower() == 'quit':
                break
            
            if knowledge_base:
                best_match: str | None = find_best_match(user_input, [q['question'] for q in knowledge_base["question"]])

                if best_match:
                    answer: str = get_answers_for_questions(best_match, knowledge_base)
                    print(f'Bot: {answer}')
                else:
                    print('Bot: i don\'t know the answer . can you teach me ? ')
                    new_answer: str = input('Type the answer of "skip" to skip:')

                    if new_answer.lower() != 'skip':
                        knowledge_base['question'].append({"question": user_input, "answer": new_answer})
                        save_knowledge_base('knowledge_base.json', knowledge_base)
                        print('Bot Thank you i learned new response!')
            else:
                print('Bot: i don\'t know the answer . can you teach me ? ')
                new_answer: str = input('Type the answer of "skip" to skip:')

                if new_answer.lower() != 'skip':
                    knowledge_base['question'] = []
                    knowledge_base['question'].append({"question": user_input, "answer": new_answer})
                    save_knowledge_base('knowledge_base.json', knowledge_base)
                    print('Bot Thank you i learned new response!')
        except:
            response = input("\n\nare you sure, you want to terminate me sir/ma?")

            for i in ['y', 'yes', 'sure', 'okay', 'ok', 'yeah', 'yh']:
                if i in response:
                    print("Program terminated!!!")
                    return

if __name__ == '__main__':
    chat_bot()
