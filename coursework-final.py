import random
import threading
import time


class Timer:
    def _init_(self, seconds):
        self.seconds = seconds
        self.timer_event = threading.Event()
        self.user_answer = None

    def start_timer(self):
        for i in range(self.seconds, 0, -1):
            if self.timer_event.is_set():
                return
            print(f"Time remaining: {i} seconds", end='\r')
            time.sleep(1)
        print("\nTime's up!")

    def get_user_answer(self):
        self.user_answer = input("Your answer (A/B/C/D): ").strip().upper()
        self.timer_event.set()

    def start(self):
        self.timer_event.clear()
        timer_thread = threading.Thread(target=self.start_timer)
        timer_thread.start()
        self.get_user_answer()
        timer_thread.join()
        return self.user_answer


class Question:
    def _init_(self, text, options, answer):
        self.text = text
        self.options = options
        self.answer = answer

    def display(self):
        print(self.text)
        for option in self.options:
            print(option)


class Lifeline:
    def use(self, question):
        raise NotImplementedError("Subclasses should implement this method")


class FiftyFiftyLifeline(Lifeline):
    def use(self, question):
        correct_option = question.answer
        options = ["A", "B", "C", "D"]
        options.remove(correct_option)
        removed_options = random.sample(options, 2)
        reduced_options = [opt for opt in question.options if opt[0] not in removed_options]
        return reduced_options


class GameController:
    _instance = None

    @staticmethod
    def get_instance():
        if GameController._instance is None:
            GameController._instance = GameController()
        return GameController._instance

    def _init_(self):
        if GameController._instance is not None:
            raise Exception("This is a singleton class. Use the get_instance() method.")
        self.score = 0
        self.questions = []
        self.lifelines = [FiftyFiftyLifeline()]
        self.timer_seconds = 24
        self.prizes = [
            "$100", "$200", "$300", "$500", "$1,000",
            "$2,000", "$4,000", "$8,000", "$16,000",
            "$32,000", "$64,000", "$125,000"
        ]

    def add_question(self, question):
        self.questions.append(question)

    def use_lifeline(self, lifeline, question):
        if lifeline in self.lifelines:
            self.lifelines.remove(lifeline)
            return lifeline.use(question)
        return question.options

    def play(self):
        for index, question in enumerate(self.questions):
            timer = Timer(self.timer_seconds)
            question.display()

            use_lifeline = input("Do you want to use 50/50 lifeline? (yes/no): ").strip().lower()
            if use_lifeline == "yes" and isinstance(self.lifelines[0], FiftyFiftyLifeline):
                options = self.use_lifeline(self.lifelines[0], question)
                for option in options:
                    print(option)
            else:
                for option in question.options:
                    print(option)

            user_answer = timer.start()
            if not user_answer:
                print("Time's up! Game over!")
                break
            if user_answer == question.answer:
                self.score += 1
                print("Correct!")
                print(f"You have won {self.prizes[index]} so far!")
            else:
                print("Wrong answer. Game over!")
                break
        print(f"Your final score is: {self.score}")
        if self.score > 0:
            print(f"Your final prize is: {self.prizes[self.score - 1]}")
        else:
            print("You didn't win any prize.")



game_controller = GameController.get_instance()


questions_data = [
    {
        "question": "What is the capital of France?",
        "options": ["A: Paris", "B: London", "C: Berlin", "D: Madrid"],
        "answer": "A"
    },
    {
        "question": "Who wrote 'To Kill a Mockingbird'?",
        "options": ["A: Harper Lee", "B: Mark Twain", "C: J.K. Rowling", "D: Ernest Hemingway"],
        "answer": "A"
    },
    {
        "question": "What is the largest planet in our Solar System?",
        "options": ["A: Earth", "B: Jupiter", "C: Saturn", "D: Mars"],
        "answer": "B"
    },
    {
        "question": "What is the square root of 64?",
        "options": ["A: 6", "B: 7", "C: 8", "D: 9"],
        "answer": "C"
    },
    {
        "question": "What is the chemical symbol for gold?",
        "options": ["A: Au", "B: Ag", "C: Fe", "D: Hg"],
        "answer": "A"
    },
    {
        "question": "Who is known as the 'Father of Computers'?",
        "options": ["A: Charles Babbage", "B: Alan Turing", "C: Bill Gates", "D: Steve Jobs"],
        "answer": "A"
    },
    {
        "question": "Which element has the atomic number 1?",
        "options": ["A: Helium", "B: Oxygen", "C: Hydrogen", "D: Nitrogen"],
        "answer": "C"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["A: Venus", "B: Mars", "C: Jupiter", "D: Saturn"],
        "answer": "B"
    },
    {
        "question": "What is the capital of Japan?",
        "options": ["A: Beijing", "B: Seoul", "C: Tokyo", "D: Bangkok"],
        "answer": "C"
    },
    {
        "question": "Who painted the Mona Lisa?",
        "options": ["A: Vincent van Gogh", "B: Pablo Picasso", "C: Leonardo da Vinci", "D: Claude Monet"],
        "answer": "C"
    },
    {
        "question": "What is the hardest natural substance on Earth?",
        "options": ["A: Gold", "B: Iron", "C: Diamond", "D: Platinum"],
        "answer": "C"
    },
    {
        "question": "What is the smallest prime number?",
        "options": ["A: 1", "B: 2", "C: 3", "D: 4"],
        "answer": "B"
    }
]

for q_data in questions_data:
    question = Question(q_data["question"], q_data["options"], q_data["answer"])
    game_controller.add_question(question)


game_controller.play()