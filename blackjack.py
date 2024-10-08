import random
from blackjack_art import logo

def create_deck():
    """Return a list of tuples representing a deck of cards"""
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
    deck = [(rank, suit) for suit in suits for rank in ranks]
    return deck


def shuffle_deck(deck):
    """Shuffle the deck"""
    random.shuffle(deck)


def deal_initial_cards(deck, dealt_cards):
    """Deal two cards to the player and one visible, one hidden to the dealer."""
    player_hand = []
    dealer_hand = []

    # Deal two cards to the player
    for card in range(2):
        card = random.choice(deck)  # pick a random card form the deck
        while card in dealt_cards:
            card = random.choice(deck)
        player_hand.append(card)
        dealt_cards.append(card)

    # Deal one visible card to the dealer
    card = random.choice(deck)
    while card in dealt_cards:
        card = random.choice(deck)
    dealer_hand.append(card)
    dealt_cards.append(card)

    # Deal one invisble card to the dealer
    dealer_hidden_card = random.choice(deck)
    while dealer_hidden_card in dealt_cards:
        dealer_hidden_card = random.choice(deck)
    dealt_cards.append(dealer_hidden_card)

    return player_hand, dealer_hand, dealer_hidden_card


def calculate_hand_value(hand):
    """Calculate the total value of the hand"""
    hand_value = 0
    ace_count = 0

    for card in hand:
        rank = card[0]

        if rank in ["Jack", "Queen", "King"]:
            hand_value += 10
        elif rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10']:
            hand_value += int(rank)
        elif rank == "Ace":
            hand_value += 11
            ace_count += 1
    while hand_value > 21 and ace_count > 0:
        hand_value -= 10
        ace_count -= 1

    return hand_value


def player_turn(player_hand, deck, dealt_cards):
    """Handle the player's turn"""
    while True:
        choice = input("Would you like to stick or twist?").lower()

        if choice == "twist":
            card = random.choice(deck)
            while card in dealt_cards:
                card = random.choice(deck)
            player_hand.append(card)
            dealt_cards.append(card)

            print(f"Player's hand: {player_hand}")

            player_hand_value = calculate_hand_value(player_hand)
            print(f"Player's hand value: {player_hand_value}")

            # Check for win or bust
            if player_hand_value == 21:
                print("Player wins with 21!")
                return True  # End the game
            elif player_hand_value > 21:
                print("Player busts! Dealer wins!")
                return True  # End the game
        elif choice == "stick":
            return  # End player's turn


def dealer_turn(dealer_hand, dealer_hidden_card, dealt_cards, deck):
    """Handle the dealer's turn"""
    # First, deal the hidden card (which is already added in the deal_initial_cards function)
    dealer_hand.append(dealer_hidden_card)
    dealer_hand_value = calculate_hand_value(dealer_hand)

    # Show the dealer's cards
    print(f"Dealer's cards: {dealer_hand}, Value: {dealer_hand_value}")

    while calculate_hand_value(dealer_hand) < 17:  # Dealer must hit until reaching 17 or more
        card = random.choice(deck)
        while card in dealt_cards:
            card = random.choice(deck)
        dealer_hand.append(card)
        dealt_cards.append(card)

    print(f"Dealer's hand: {dealer_hand}, Value: {calculate_hand_value(dealer_hand)}")  # Show dealer's hand


def determine_winner(player_hand, dealer_hand):
    """Determine the winner"""
    player_hand_value = calculate_hand_value(player_hand)
    dealer_hand_value = calculate_hand_value(dealer_hand)

    if player_hand_value > 21:
        return "Dealer wins!(Player busts)"
    elif dealer_hand_value > 21:
        return "Player wins!(Dealer busts)"
    elif player_hand_value > dealer_hand_value:
        return "Player wins!"
    elif dealer_hand_value > player_hand_value:
        return "Dealer wins!"
    else:
        return "Its a draw!"


def blackjack():
    """Main Game Logic"""
    print(logo)
    play_again = "yes"

    while play_again == "yes":
        deck = create_deck()
        shuffle_deck(deck)

        dealt_cards = []

        player_hand, dealer_hand, dealer_hidden_card = deal_initial_cards(deck, dealt_cards)

        player_hand_value = calculate_hand_value(player_hand)
        dealer_hand_value = calculate_hand_value(dealer_hand)

        print(f"Player's hand: {player_hand}, Value: {player_hand_value}")
        print(f"Dealer's hand: {dealer_hand}, Value: {dealer_hand_value}")

        # Player's Turn
        game_over = player_turn(player_hand, deck, dealt_cards)

        if not game_over:
            # Dealer's Turn
            dealer_turn(dealer_hand, dealer_hidden_card, dealt_cards, deck)

            # Determine the winner
            result = determine_winner(player_hand, dealer_hand)
            print(result)

        play_again = input("Do you want to play again? yes or no?").lower()


blackjack()


