import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

# Constants
SUITS = ['clubs', 'diamonds', 'hearts', 'spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'jack': 10, 'queen': 10, 'king': 10, 'ace': 11}
STARTING_CHIPS = 1000  # Starting chips for the player

# Card image path
IMAGE_PATH = r'C:\Users\llelo\OneDrive - Lynfield College\2PAD\blackjack'

# Define math questions
EASY_QUESTIONS = [
    ("5 + 3", 8),
    ("10 - 4", 6),
    ("7 * 2", 14),
    ("20 / 4", 5),
    ("9 + 6", 15),
]

MEDIUM_QUESTIONS = [
    ("15 * 4", 60),
    ("28 / 7", 4),
    ("12 + 15", 27),
    ("35 - 17", 18),
    ("9 * 7", 63),
]

HARD_QUESTIONS = [
    ("(5 + 3) * 2", 16),
    ("12 * (3 + 2)", 60),
    ("(8 - 3) * (6 + 2)", 40),
    ("18 / (3 - 1)", 9),
    ("25 + 5 * 4 - 10", 30),
]

# Card class
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = VALUES[rank]
        image_file = f'{rank}_of_{suit}.png'
        image_path = os.path.join(IMAGE_PATH, image_file)
        self.image = Image.open(image_path)
        self.image = self.image.resize((100, 150), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

# Deck class
class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

# Hand class
class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def calculate_value(self):
        value = sum(card.value for card in self.cards)
        num_aces = sum(1 for card in self.cards if card.rank == 'ace')
        while value > 21 and num_aces:
            value -= 10
            num_aces -= 1
        return value

    def __repr__(self):
        return f"Hand: {', '.join(str(card) for card in self.cards)} (Value: {self.calculate_value()})"

# Blackjack game class
class BlackjackGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack")
        self.root.geometry("1200x800")

        self.canvas = tk.Canvas(root, bg="green")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()

        self.player_chips = STARTING_CHIPS
        self.dealer_chips = STARTING_CHIPS

        self.buttons_frame = tk.Frame(root, bg="darkgreen")
        self.buttons_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.hit_button = tk.Button(self.buttons_frame, text="Hit", command=self.player_hit, font=('Arial', 18))
        self.hit_button.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        self.stay_button = tk.Button(self.buttons_frame, text="Stay", command=self.player_stay, font=('Arial', 18))
        self.stay_button.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        self.buy_chips_button = tk.Button(self.buttons_frame, text="Buy Chips", command=self.ask_math_question, font=('Arial', 18))
        self.buy_chips_button.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        self.restart_game()

    def restart_game(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()

        self.player_hand.add_card(self.deck.deal())
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())

        self.update_display()
        self.check_for_blackjack()

    def draw_card(self, hand, position):
        x = 50
        y = 200 if position == 'player' else 400
        for card in hand.cards:
            self.canvas.create_image(x, y, image=card.photo, anchor=tk.NW)
            x += 110

    def update_display(self):
        self.canvas.delete("all")
        self.draw_card(self.player_hand, 'player')
        self.draw_card(self.dealer_hand, 'dealer')

        player_value = self.player_hand.calculate_value()
        dealer_value = self.dealer_hand.calculate_value()

        self.canvas.create_text(150, 30, text=f"Your hand value: {player_value}", fill="white", font=("Arial", 16))
        self.canvas.create_text(150, 60, text=f"Dealer's hand value: {dealer_value}", fill="white", font=("Arial", 16))

        # Display chips
        self.canvas.create_text(150, 100, text=f"Your Chips: ${self.player_chips}", fill="white", font=("Arial", 16))
        self.canvas.create_text(150, 130, text=f"Dealer's Chips: ${self.dealer_chips}", fill="white", font=("Arial", 16))

    def check_for_blackjack(self):
        if self.player_hand.calculate_value() == 21:
            messagebox.showinfo("Blackjack!", "You got a Blackjack! You win!")
            self.player_chips += 50  # Award chips
            self.restart_game()
        elif self.dealer_hand.calculate_value() == 21:
            messagebox.showinfo("Blackjack!", "Dealer got a Blackjack! You lose.")
            self.dealer_chips += 50  # Award chips to dealer
            self.restart_game()

    def player_hit(self):
        self.player_hand.add_card(self.deck.deal())
        if self.player_hand.calculate_value() > 21:
            messagebox.showinfo("Busted!", "You busted! Dealer wins.")
            self.dealer_chips += 50  # Award chips to dealer
            self.restart_game()
        else:
            self.update_display()

    def player_stay(self):
        while self.dealer_hand.calculate_value() < 17:
            self.dealer_hand.add_card(self.deck.deal())

        dealer_value = self.dealer_hand.calculate_value()
        player_value = self.player_hand.calculate_value()

        if dealer_value > 21 or player_value > dealer_value:
            messagebox.showinfo("Result", "You win!")
            self.player_chips += 50  # Award chips
        elif player_value < dealer_value:
            messagebox.showinfo("Result", "Dealer wins!")
            self.dealer_chips += 50  # Award chips to dealer
        else:
            messagebox.showinfo("Result", "It's a tie!")

        self.restart_game()

    def generate_math_question(self):
        difficulty = random.choices(['easy', 'medium', 'hard'], weights=[0.4, 0.4, 0.2])[0]

        if difficulty == 'easy':
            question, answer = random.choice(EASY_QUESTIONS)
            reward = 20
        elif difficulty == 'medium':
            question, answer = random.choice(MEDIUM_QUESTIONS)
            reward = 50
        else:  # hard
            question, answer = random.choice(HARD_QUESTIONS)
            reward = 100
        
        return question, answer, reward

    def ask_math_question(self):
        question, answer, reward = self.generate_math_question()

        self.math_window = tk.Toplevel(self.root)
        self.math_window.title("Math Question")

        question_label = tk.Label(self.math_window, text=f"Solve this: {question}", font=('Arial', 18))
        question_label.pack(pady=10)

        self.answer_entry = tk.Entry(self.math_window, font=('Arial', 18))
        self.answer_entry.pack(pady=10)

        submit_button = tk.Button(self.math_window, text="Submit", command=lambda: self.check_answer(answer, reward), font=('Arial', 18))
        submit_button.pack(pady=10)

    def check_answer(self, correct_answer, reward):
        try:
            user_answer = float(self.answer_entry.get())
            if abs(user_answer - correct_answer) < 0.01:
                self.player_chips += reward
                messagebox.showinfo("Correct!", f"Correct answer! You've been awarded {reward} chips.")
            else:
                messagebox.showinfo("Incorrect!", "Incorrect answer. No chips awarded.")
        except ValueError:
            messagebox.showinfo("Error!", "Invalid input. Please enter a number.")
        finally:
            self.math_window.destroy()
            self.update_display()

if __name__ == "__main__":
    root = tk.Tk()
    game = BlackjackGame(root)
    root.mainloop()
