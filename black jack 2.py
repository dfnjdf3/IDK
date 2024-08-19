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
IMAGE_PATH = r'C:\Users\llelo\OneDrive - Lynfield College\2PAD\PNG-cards-1.3'

# Card class
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = VALUES[rank]
        # Construct the image file path based on suit and rank
        image_file = f'{rank}_of_{suit}.png'
        image_path = os.path.join(IMAGE_PATH, image_file)
        # Load and resize the image
        self.image = Image.open(image_path)
        self.image = self.image.resize((100, 150), Image.LANCZOS)  # Resize image using LANCZOS
        self.photo = ImageTk.PhotoImage(self.image)

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

# Deck class
class Deck:
    def __init__(self, difficulty=0):
        self.difficulty = difficulty
        self.cards = self.create_deck()
        random.shuffle(self.cards)

    def create_deck(self):
        # Create a basic deck
        basic_deck = [Card(suit, rank) for suit in SUITS for rank in RANKS] * 1  # Standard 52 cards deck
        modified_deck = basic_deck.copy()  # Make a copy to modify for difficulty

        if self.difficulty > 0:
            # Modify deck composition based on difficulty
            for _ in range(self.difficulty * 2):  # Add more high-value cards
                high_value_cards = [Card(suit, rank) for suit in SUITS for rank in RANKS if VALUES[rank] > 10]
                modified_deck.append(random.choice(high_value_cards))
            for _ in range(self.difficulty * 2):  # Remove some low-value cards
                low_value_cards = [card for card in modified_deck if VALUES[card.rank] <= 5]
                if low_value_cards:
                    modified_deck.remove(random.choice(low_value_cards))
        
        return modified_deck

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

        self.difficulty = 0  # Start with the easiest difficulty
        self.player_chips = STARTING_CHIPS
        self.dealer_chips = STARTING_CHIPS

        self.buttons_frame = tk.Frame(root, bg="darkgreen")
        self.buttons_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.hit_button = tk.Button(self.buttons_frame, text="Hit", command=self.player_hit, font=('Arial', 18), width=10, height=2)
        self.hit_button.pack(side=tk.LEFT, padx=10)

        self.stay_button = tk.Button(self.buttons_frame, text="Stay", command=self.player_stay, font=('Arial', 18), width=10, height=2)
        self.stay_button.pack(side=tk.RIGHT, padx=10)

        self.restart_game()

    def restart_game(self):
        self.difficulty += 1  # Increase difficulty for the next game
        self.deck = Deck(difficulty=self.difficulty)
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

if __name__ == "__main__":
    root = tk.Tk()
    game = BlackjackGame(root)
    root.mainloop()
