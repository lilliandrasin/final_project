import random

# ==== Constants ====
# RANKS is ordered from strongest to weakest for hand-labeling (AKs, etc.)
RANKS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

# Map rank character to a numeric value for comparisons and sorting
RANK_TO_VALUE = {
    '2': 2, '3': 3, '4': 4, '5': 5,
    '6': 6, '7': 7, '8': 8, '9': 9,
    'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
}

# Map suit character to its full name (mainly cosmetic if you print it later)
SUIT_MAP = {'s': 'Spades', 'h': 'Hearts', 'd': 'Diamonds', 'c': 'Clubs'}


# === Calculations ===

def pot_odds(to_call, pot_size):
    """
    Pot odds is the minimum equity needed to break even on a call):

        pot_odds = to_call / (pot_size + to_call)

        - to_call is the amount you must put in to continue.
        - pot_size is the money already in the pot (before you call).
        - pot_size + to_call is the size of the pot after you call.

        If your equity (chance to win) is greater than pot_odds,
        then calling is positive expected return in the long run.
    """
    if to_call <= 0:
        # Nothing to call --> no risk --> pot odds treated as 0
        return 0.0

    # use the amount in the pot as if if hero decides to call
    # hero risks to_call amount to win pot_size + to_call
    total_after_call = pot_size + to_call
    #So the minimum equity needed to break even becomes
    odds = to_call / total_after_call
    return odds


def expected_return_call(equity, pot_size, to_call):
    """
    EXPECTED VALUE OF CALLING:

        EV(call) = equity * (pot_size + to_call)
                   - (1 - equity) * to_call

        - equity is your probability of winning at showdown 
        - pot_size is the current pot before your call
        - to_call is how much you must put in to call
    """
    if to_call <= 0:
        # Calling costs nothing; EV of the action "call" is 0 by definition.
        return 0.0

    win_value = equity * (pot_size + to_call)
    lose_value = (1.0 - equity) * to_call

    ev = win_value - lose_value
    return ev


# ==== Core helpers ====

def create_deck():
    """
    Create a standard 52-card deck.
    Each card is a 2-character string like rank + suit
    """
    deck = []
    # Loop 4 times
    for suit in SUIT_MAP.keys():
        # Loop 13 times 4x13 = 52
        for rank in RANKS:
            card = rank + suit
            deck.append(card)
    return deck


# Create a fixed player list P1, P2, ..., P3
num_players = 3
player_list = []
for i in range(num_players):
    player_id = "P" + str(i + 1)
    player_list.append(player_id)
print(player_list)


def deal_hole_cards(player_list, deck):
    """
    Shuffle the deck and deal 2 cards to each player.
    Return a dictionary mapping player IDs to their hole cards:

        { 'P1': ['As','Kd'], 'P2': [...], ... }
    """
    random.shuffle(deck)

    #Initialize a dictionary where player is key and their card as a list is the value
    hands = {}

    for p in player_list:
        hands[p] = []
        for _ in range(2):
            card = deck.pop()
            hands[p].append(card)
    return hands


def all_169_hands(RANKS):
    """
    Build all preflop hand labels/169 starting hands by iterating over ranks with indices i <= j
    and attaching the proper suffix
    """
    unique_hands = []

    i = 0
    while i < len(RANKS):
        j = i
        while j < len(RANKS):
            r1 = RANKS[i]
            r2 = RANKS[j]

            if i == j:
                # Same rank means a pocket pair, no suit suffix needed
                label = r1 + r2
                unique_hands.append(label)
            else:
                # Different ranks need suited and offsuit labels.
                suited_label = r1 + r2 + 's'
                offsuit_label = r1 + r2 + 'o'
                unique_hands.append(suited_label)
                unique_hands.append(offsuit_label)

            j += 1
        i += 1

    print(unique_hands)
    return unique_hands


def standardizeMyHand(my_cards):
    """
    Convert hero cards from list to a standard label
    """
    # Index hero cards to pull card 1 and 2
    card1 = my_cards[0]
    card2 = my_cards[1]

    # Pull the rank from the first character in card
    rank1 = card1[0]
    rank2 = card2[0]

    # Pull the suit from the second character in card
    suit1 = card1[1]
    suit2 = card2[1]

    # compare to dictionary to assign a numerical value
    val1 = RANK_TO_VALUE[rank1]
    val2 = RANK_TO_VALUE[rank2]

    # Order ranks so the higher rank comes first in the label.
    if val1 >= val2:
        high_rank = rank1
        low_rank = rank2
        s_high = suit1
        s_low = suit2
    else:
        high_rank = rank2
        low_rank = rank1
        s_high = suit2
        s_low = suit1

    # Pocket pair
    if high_rank == low_rank:
        label = high_rank + low_rank
        print(label)
        return label

    # Suited when both suits are the same
    if s_high == s_low:
        suffix = 's'
    else:
        # Offsuit when suits are different
        suffix = 'o'

    label = high_rank + low_rank + suffix
    print(label)
    return label


# ==== PREFLOP RANGES ====

def build_preflop_ranges(all_hands):
    """
    Build preflop ranges using 6 color-based categories given by poker ranges chart:
    all_hands: output of all_169_hands
    """
    # 1) TIGHT_HANDS: strongest “red” hands.
    TIGHT_RED = [
        "AA", "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A4s", "A3s", "A2s",
        "AKo", "KK", "KQs", "KJs", "KTs",
        "AQo", "KQo", "QQ", "QJs", "QTs",
        "AJo", "JJ", "JTs",
        "ATo", "TT", "T9s",
        "99",
        "88",
        "77",
        "66", "65s",
        "55",
        "44"
    ]

    # 2. STRONG_ORANGE: strong but slightly below red
    STRONG_ORANGE = [
        "K9s", "K8s",
        "Q9s",
        "KJo", "QJo", "J9s",
        "98s",
        "87s",
        "76s",
        "54s",
        "44"
    ]

    # 3.MEDIUM_YELLOW: good but not great
    MEDIUM_YELLOW = [
        "K7s", "K6s", "K5s",
        "Q8s",
        "J8s",
        "KTo", "QTo", "JTo", "T8s",
        "97s",
        "86s",
        "75s",
        "33",
        "22"
    ]

    # 4. LOOSE_GREEN: not great but playable
    LOOSE_GREEN = [
        "K4s", "K3s", "K2s",
        "Q7s", "Q6s", "Q5s",
        "J7s",
        "T7s", "T6s",
        "A9o", "K9o", "Q9o", "J9o", "T9o", "96s",
        "A8o", "98o", "85s",
        "A6o", "64s",
        "A5o", "53s",
        "A4o", "43s"
    ]

    # 5. SPECULATIVE_BLUE: very loose rarely played
    SPECULATIVE_BLUE = [
        "Q4s", "Q3s", "Q2s",
        "J6s", "J5s", "J4s", "J3s", "J2s",
        "T5s", "T4s", "T2s",
        "95s", "94s",
        "K8o", "Q8o", "J8o", "T8o", "84s",
        "K7o", "Q7o", "J7o", "T7o", "97o", "87o", "74s", "73s",
        "K6o", "86o", "76o", "63s",
        "K5o", "75o", "65o", "52s",
        "64o", "54o", "42s",
        "A3o", "32s", "A2o"
    ]

    # Build set of all explicitly assigned hands so far
    assigned = set(
        TIGHT_RED +
        STRONG_ORANGE +
        MEDIUM_YELLOW +
        LOOSE_GREEN +
        SPECULATIVE_BLUE
    )

    # 6. JUNK_GREY = any hand in all_hands that was not assigned
    JUNK_GREY = []
    for hand in all_hands:
        if hand not in assigned:
            JUNK_GREY.append(hand)

   # Build dictionary for ranges
    ranges = {
        "Tight": TIGHT_RED,
        "Orange": STRONG_ORANGE,
        "Medium": MEDIUM_YELLOW,
        "Loose": LOOSE_GREEN,
        "Speculative": SPECULATIVE_BLUE,
        "Junk": JUNK_GREY
    }

    return ranges


# ==== BETTING ROUNDS ====

def preflopRound(PREFLOP_RANGES, my_cards_S, GAME_STATE):
    """
    Look up hero standardized starting hand in the preflop ranges
    and return a text suggestion about how to play it, using the 6 ranges
    """
    if my_cards_S in PREFLOP_RANGES["Tight"]:
        my_range = my_cards_S + " is in the Tight range"
        suggest = "SUGGEST STRONG RAISE "
    elif my_cards_S in PREFLOP_RANGES["Orange"]:
        my_range = my_cards_S + " is in the Strong range"
        suggest = "SUGGEST RAISE"
    elif my_cards_S in PREFLOP_RANGES["Medium"]:
        my_range = my_cards_S + " is in the Medium range"
        suggest = "SUGGEST CALL OR SMALL RAISE"
    elif my_cards_S in PREFLOP_RANGES["Loose"]:
        my_range = my_cards_S + " is in the Loose range"
        suggest = "SUGGEST CALL OR FOLD"
    elif my_cards_S in PREFLOP_RANGES["Speculative"]:
        my_range = my_cards_S + " is in the Speculative range"
        suggest = "SUGGEST FOLD, RARELY CALL"
    elif my_cards_S in PREFLOP_RANGES["Junk"]:
        my_range = my_cards_S + " is in the Junk range"
        suggest = "SUGGEST FOLD"

    text = my_range + "\n" + suggest
    return text


"""
Each betting round:

    - The number of community cards increases (flop/turn/river).
    - GAME_STATE["betting_round"] is updated accordingly.
"""

def flopRound(deck, GAME_STATE):
    """
    Deal 3 community cards and set betting_round to Flop
    """
    GAME_STATE["betting_round"] = "Flop"

    # Deal out 3 community cards
    community_cards = []
    index = 0
    while index < 3:
        card = deck.pop()
        community_cards.append(card)
        index += 1

    return community_cards


def turnRound(deck, GAME_STATE, community_cards):
    """
    Deal 1 community card and set betting_round to Turn
    """
    GAME_STATE["betting_round"] = "Turn"
    card = deck.pop()
    community_cards.append(card)
    return community_cards


def River(deck, GAME_STATE, community_cards):
    """
    Deal 1 community card and set betting_round to River
    """
    GAME_STATE["betting_round"] = "River"
    card = deck.pop()
    community_cards.append(card)
    return community_cards


# ==== Hand evaluation and Monte Carlo equity ====

def evaluate_7_card_hand(cards):
    """
    Evaluate 7 cards. This will give numeric rank values for comparing winning hand patterns that depend on numeric value of card and winning hand patterns that depend on suit
    """
    # Split into numeric ranks and suit characters in order 
    ranks = []
    suits = []
    for card in cards:
        rank_char = card[0]
        suit_char = card[1]
        # Compare rank letter to a numver using RANK_TO_VALUE
        rank_val = RANK_TO_VALUE[rank_char]
        ranks.append(rank_val)
        suits.append(suit_char)

    # Sort ranks from high to low for easier evaluation
    ranks.sort(reverse=True)

    # Count occurrences of each rank from list above
    rank_counts = {}
    for r in ranks:
        if r not in rank_counts:
            rank_counts[r] = 0
        rank_counts[r] += 1

    # Convert rank_counts dict into a list of (count, rank) pairs.
    # sort by count descending, then rank descending.
    count_rank_list = []
    for r in rank_counts:
        pair = (rank_counts[r], r)
        count_rank_list.append(pair)
    count_rank_list.sort(reverse=True)
    #This runs however many times is specified in the monte carlo simulation call
    #print(count_rank_list)

    # FLUSH DETECTION (same suit, not a sequence)
    # Count occurrences of each suit, from list created earlier
    suit_counts = {}
    for s in suits:
        if s not in suit_counts:
            suit_counts[s] = 0
        suit_counts[s] += 1


    #If any suit appears more that 5 times, it records a flush suit and stops
    flush_suit = None
    for s in suit_counts:
        if suit_counts[s] >= 5:
            #Stop looking
            flush_suit = s
            break

    # If a flush suit is found, a list of ranks belonging to flush suit is built
    flush_ranks = []
    #If no suit has <5 cards, skip everything because no flush possible
    if flush_suit is not None:
        for card in cards:
            if card[1] == flush_suit:
                rank_val = RANK_TO_VALUE[card[0]]
                flush_ranks.append(rank_val)
        # Make it descending to check for a straight flush
        flush_ranks.sort(reverse=True)

    #find the best straight high card from a list of high to low ranks.
    def best_straight(high_to_low_ranks):
        """
        By temporarily assigning the Ace a dual value (14 for high, 1 for low), the function runs the single, unified consecutive rank check to find both standard straights and the special Ace-low straight
        If low straight sequence is found, it confirms the "Wheel" straight, and the highest card of that run, 5, is recorded as the best straight
        """
        uniq = []
        # Removing duplicate ranks so hands like a pair don't break a straight sequence check.
        for r in high_to_low_ranks:
            if r not in uniq:
                uniq.append(r)

        # Handle wheel straight, where an ace is also considered a low card
        # Track if a hand contains an Ace (rank 14)
        has_ace = False
        for u in range(len(uniq)):
            # Check if rank at index is Ace 
            if uniq[u] == 14:
                has_ace = True
                break

        if has_ace:
            uniq.append(1)

        # Sort descending again after possibly adding 1 because adding the value 1 may have broken the original sort order
        uniq.sort(reverse=True)

        #Initialize a variable to store highest rank of best 5 card straight
        best = None
        # Initialize a list run to track the current sequence of consecutive cards, starting at highest card
        run = [uniq[0]]
        # Start the check at second card
        k = 1
        while k < len(uniq):
            # Checks for a straight continuation
            if uniq[k] == uniq[k - 1] - 1:
                # Continue the straight run
                run.append(uniq[k])
                if len(run) >= 5:
                    # Track highest straight found
                    best = run[0]
            k += 1
        return best

    # Compute a straight of any suits
    straight_high = best_straight(ranks)

    # Compute straight flush (only flush suit ranks)
    straight_flush_high = None
    if flush_suit is not None:
        straight_flush_high = best_straight(flush_ranks)

    # Hand classification using category order.

    # Straight flush
    if straight_flush_high is not None:
        return (8, straight_flush_high)

    # Four of a kind
    # Extract first element of tuple in count_rank_list to check if the count is 4
    if count_rank_list[0][0] == 4:
        # set four_rank = to the rank that appears 4 times
        four_rank = count_rank_list[0][1]
        for r in ranks:
            if r != four_rank:
                # The kicker is the card that is not in the 4 rank, this will set break the tie >1 opponent has a 4 rank
                kicker = r
                break
        return (7, four_rank, kicker)

    # Full house (3 of a kind + pair)
    # Extract first element of tuple in count_rank_list to check if the count is 4
    if count_rank_list[0][0] == 3:
        trips_rank = count_rank_list[0][1]
        #pair_rank = None
        for i in range(len(count_rank_list)):
            cnt = count_rank_list[i][0]
            r = count_rank_list[i][1]
            if cnt >= 2:
                pair_rank = r
                break
        if pair_rank == r:
            return (6, trips_rank, pair_rank)

    # Logic for if flush exists
    if flush_suit is not None:
        top5 = flush_ranks[:5]
        return (5, top5)

    # Straight.
    if straight_high is not None:
        return (4, straight_high)

    # Three of a kind 
    # Extract first element of tuple in count_rank_list to check if the count is 4
    if count_rank_list[0][0] == 3:
        # Extract rank 
        trips_rank = count_rank_list[0][1]
        # The other two cards will be the kickers, deciding any possible tie break necessary
        kickers = []
        for r in ranks:
            if r != trips_rank and r not in kickers:
                #Ranks is sorted high to low previously, so the highest two cards are automatically appended
                kickers.append(r)
            if len(kickers) == 2:
                break
        return (3, trips_rank, kickers[0], kickers[1])

    # Two pair
    if count_rank_list[0][0] == 2 and count_rank_list[1][0] == 2:
        high_pair = count_rank_list[0][1]
        low_pair = count_rank_list[1][1]
        # Ensure high_pair is the larger rank
        if low_pair > high_pair:
            temp = high_pair
            high_pair = low_pair
            low_pair = temp

        kicker = None
        for r in ranks:
            if r != high_pair and r != low_pair:
                kicker = r
                break
        return (2, high_pair, low_pair, kicker)

    # One pair
    if count_rank_list[0][0] == 2:
        pair_rank = count_rank_list[0][1]
        kickers = []
        for r in ranks:
            if r != pair_rank and r not in kickers:
                kickers.append(r)
            if len(kickers) == 3:
                break
        return (1, pair_rank, kickers[0], kickers[1], kickers[2])

    # High card: top 5 ranks.
    top5 = ranks[:5]
    return (0, top5)


def monte_carlo_equity(my_cards, community_cards, betting_round, trials=200):
    """
    Estimate hero's equity vs ALL opponents at the table using Monte Carlo simulation.

    - Use num_players to determine number of villains: num_opponents = num_players - 1

    Equity is approximated as:
        equity ≈ (wins + 0.5 * ties) / trials
    """
    # Number of opponents = all players at table except hero (P1)
    num_opponents = num_players - 1

    # counters for outcomes
    wins = 0
    losses = 0
    ties= 0

    for trials in range(trials+1):
        #1. Build a fresh full deck for this trial 
        deck = create_deck()
        # 2. Remove known cards: hero hole cards and current community cards 
        for card in my_cards:
            if card in deck:
                deck.remove(card)
        for card in community_cards:
            if card in deck:
                deck.remove(card)

        # Shuffle remaining deck
        random.shuffle(deck)

        # 3. Redeal random cards to villains for the purpose of monte carlo simulation
        # Initialize a list of [card1, card2] for each villain
        villains = []  
        for _ in range(num_opponents):
            for _ in range(2):
                v_hand = []
                # first card
                v_hand.append(deck.pop()) 
                # second card 
                v_hand.append(deck.pop())  
                villains.append(v_hand)

        # 4. Complete the community board to 5 cards total 
        board = []
        for c in community_cards:
            board.append(c)

        # Number of community cards still needed to deal
        cards_needed = 5 - len(board)
        for _ in range(cards_needed):
            board.append(deck.pop())
  
        # 5. Evaluate hero score
        hero_score = evaluate_7_card_hand(my_cards + board)

        # Track the best villain hand score
        best_villain_score = None
        num_best_villains = 0  

        for v_hand in villains:
            v_score = evaluate_7_card_hand(v_hand + board)
        
            if best_villain_score is None:
                best_villain_score = v_score
                num_best_villains = 1
            else:
                if v_score > best_villain_score:
                    best_villain_score = v_score
                    num_best_villains = 1
                elif v_score == best_villain_score:
                    num_best_villains += 1

        # 6. Compare hero to the BEST villain hand 
        if hero_score > best_villain_score:
            wins +=1
        elif hero_score == best_villain_score:
            ties+=1
        else: 
            losses+=1

    print("=== Monte Carlo Simulation Summary ===")
    print(f"Wins:   {wins}")
    print(f"Losses: {losses}")
    print(f"Ties:   {ties}")
    print(f"Total Trials: {trials}")
    print("---------------------------------------")

    #7. Convert counts into equity (probability hero wins at showdown)
    total = float(trials)
    equity = (wins + 0.5 * ties) / total
    return equity
   

def simulate_equity_and_hand_probs(my_cards, community_cards, betting_round, trials=200):
    """
    Monte Carlo simulation that estimates hero's probability of
    finishing with each hand category 
    Hand categories 
        8: straight flush
        7: four of a kind
        6: full house
        5: flush
        4: straight
        3: three of a kind
        2: two pair
        1: one pair
        0: high card
    """
    # Count how often hero gets each category 

    hand_type_counts = {}
    category = 0
    while category <= 8:
        hand_type_counts[category] = 0
        category += 1

    # How many more community cards that are still needed in community cards  based on current actual betting round
    if betting_round == "Pre-Flop":
        cards_to_add = 5 
    elif betting_round == "Flop":
        cards_to_add = 2                         
    elif betting_round == "Turn":
        cards_to_add = 1                          
    else:
        cards_to_add = 0

    for trial in range(trials+1):
        #Build a fresh deck for this trial
        deck = create_deck()

        # Remove hero's cards and current community cards from the deck
        for card in my_cards:
            if card in deck:
                deck.remove(card)
        for card in community_cards:
            if card in deck:
                deck.remove(card)

        # Shuffle remaining unknown cards.
        random.shuffle(deck)

        # Start board as a fresh copy of the current community cards for THIS trial
        board = []
        for c in community_cards:
            board.append(c)

        # Deal the remaining community cards needed to get to 5 total
        #Initialize a counter to track how many cards have been added
        extra = 0
        while extra < cards_to_add:
            board.append(deck.pop())
            extra += 1

        # Evaluate hero's final 7-card hand
        hero_score = evaluate_7_card_hand(my_cards + board)

        # hero_score[0] is the category code 0..8.
        hero_cat = hero_score[0]
        hand_type_counts[hero_cat] += 1

    # Convert raw counts into probabilities for each category.
    total = float(trials)
    # This prints the probability to user later
    hand_type_probs = {}
    for cat in hand_type_counts:
        hand_type_probs[cat] = hand_type_counts[cat] / total

    return hand_type_probs



# ==== Display ====

def displayAnalysis(my_cards_S, my_cards, GAME_STATE, all_hands, PREFLOP_RANGES, community_cards):
    
    print("=" * 60, "\n")
    print("Your Hand:", my_cards, " → ", my_cards_S, "\n")
    print("ROUND:", GAME_STATE["betting_round"], "\n")
    print("You have $", GAME_STATE["my_stack"], "in your stack")
    print("The pot size is $", GAME_STATE["pot_size"], "\n")
    print("You must put in $", GAME_STATE["to_call"], "to call", "\n")
    

    # Pot odds are the break-even equity threshold: to_call / (pot + to_call).
    current_pot_odds = pot_odds(GAME_STATE["to_call"], GAME_STATE["pot_size"])
    print("Pot odds to call: {:.3f}  ({:.1f}%)".format(current_pot_odds, current_pot_odds * 100))
    print()

    # Preflop range recommendation (only on Pre-Flop).
    if GAME_STATE["betting_round"] == "Pre-Flop":
        text = preflopRound(PREFLOP_RANGES, my_cards_S, GAME_STATE)
        print(text)
        print("=" * 30)

    # ---- Monte Carlo equity vs ALL opponents + probabilities for every betting ro ----
    trials = 1000  

    # Equity vs all villains at the table 
    equity = monte_carlo_equity(
        my_cards,
        community_cards,
        GAME_STATE["betting_round"],
        trials=trials
    )

    # Hero's distribution over final hand categories at showdown
    hand_type_probs = simulate_equity_and_hand_probs(
        my_cards,
        community_cards,
        GAME_STATE["betting_round"],
        trials=trials
    )

    # EV(Call) uses equity, current pot, and to_call
    ev_call = expected_return_call(
        equity,
        GAME_STATE["pot_size"],
        GAME_STATE["to_call"]
    )

    print("Equity vs opponents: {:.1f}%".format(equity * 100))
    print("EV(Call): {:.2f}".format(ev_call))

    # Map category code  to descriptive name for printing
    category_names = {
        8: "Straight Flush",
        7: "Four of a Kind",
        6: "Full House",
        5: "Flush",
        4: "Straight",
        3: "Three of a Kind",
        2: "Two Pair",
        1: "One Pair",
        0: "High Card"
    }

    print("\nProbability of each final hand type for Hero (at showdown):")
    # Print from strongest to weakest.
    cat = 8
    while cat >= 0:
        name = category_names[cat]
        prob = hand_type_probs.get(cat, 0.0)
        print("  {:16s}: {:5.1f}%".format(name, prob * 100))
        cat -= 1

    print()

    # Show community cards on all post-flop betting rounds
    if GAME_STATE["betting_round"] in ["Flop", "Turn", "River"]:
        print("Community cards:", community_cards)


# ==== Decision ====

def mydecision(GAME_STATE):
    """
    Ask the user what action they want to take. GAME_STATE will updated accordingly.
    Returns action_string, amount_invested_by_hero
    """
    while True:
        # Not enough chips to call so hero can no longer play
        if GAME_STATE["to_call"] > GAME_STATE["my_stack"] and GAME_STATE["to_call"] > 0:
            print("You do not have enough chips to call. Game over.")
            return "FOLD", 0

        action = input("Enter your action (FOLD, CALL, RAISE): ").strip().upper()

        if action == "FOLD":
            print("Game over")
            return "FOLD", 0

        if action == "CALL":
            call_amount = GAME_STATE["to_call"]

            if call_amount > GAME_STATE["my_stack"]:
                print("You do not have enough chips to call. Game over.")
                return "FOLD", 0

            GAME_STATE["pot_size"] += call_amount
            GAME_STATE["to_call"] = 0
            GAME_STATE["my_stack"] -= call_amount
            return "CALL", call_amount

        if action == "RAISE":
            while True:
                raise_num = int(input("How much do you want to raise? "))

                # Raise must be within hero's stack
                if raise_num > GAME_STATE["my_stack"]:
                    print("Enter a raise value within your stack amount.")
                    continue

                # Total put in this action = call + raise
                total_put_in = GAME_STATE["to_call"] + raise_num

                # Cannot exceed stack
                if total_put_in > GAME_STATE["my_stack"]:
                    print("You do not have enough chips to make this raise.")
                    continue

                # Apply valid raise
                GAME_STATE["pot_size"] += total_put_in
                GAME_STATE["my_stack"] -= total_put_in
                GAME_STATE["to_call"] = raise_num

                return "RAISE", total_put_in

        #  INVALID CHOICE 
        print("Invalid. Use FOLD, CALL, or RAISE.")



# ==== RANDOM OPPONENT DECISIONS ====

def opponents_act(player_list, GAME_STATE):
    """
    Simulate random actions for all opponents (P2, P3, ...).
    """
    hero = player_list[0]
    any_raise = False

    #Loop through each play that is not the user
    for pid in player_list:
        if pid == hero:
            continue
        
        # Display each players turn 
        print("\n---", pid, "'s turn ---")
        input("Press ENTER to continue... ")

        # The choice of each each player is randomized
        action = random.choice(["FOLD", "CALL", "RAISE"])

        if action == "FOLD":
            print(pid, "FOLDS.")

        # any time a player calls, the game state changes and everyone else must match this amount
        elif action == "CALL":
            call_amount = GAME_STATE["to_call"]
            if call_amount == 0:
                print(pid, "CHECKS.")
            else:
                GAME_STATE["pot_size"] += call_amount
                print(pid, "CALLS", call_amount, ".")

        elif action == "RAISE":
            base = GAME_STATE["to_call"]
            # If no one has raised yet, force the raise to be at least one
            if base < 1:
                base = 1

            # Choose an amount for random opponent decision within reason
            raise_amount = random.randint(base, base * 3)
            # Update GAME_STATE accordingly
            total_put_in = GAME_STATE["to_call"] + raise_amount
            GAME_STATE["pot_size"] += total_put_in
            # This is the new amount players must call
            GAME_STATE["to_call"] = raise_amount
            # At this point, a raised has occured and betting is not finished
            any_raise = True
            print(pid, "RAISES to", raise_amount, ".")
    # Once all raises are matched/players fold, the betting round is continued
    return any_raise


def force_hero_match(GAME_STATE):
    """
    If there has been a raise (to_call > 0), force the hero to act again before the next card is dealt
    """
    if GAME_STATE["to_call"] > 0:
        print("\nThere has been a raise to", GAME_STATE["to_call"],
              "You must at least CALL to see the next card.\n")
        result, amount = mydecision(GAME_STATE)
        if result == "FOLD":
            return False
    return True


def resolve_showdown(GAME_STATE, my_cards, community_cards, my_cards_S, player_list, hands):
    """
    Resolve the showdown by:
        - Printing hero hand + community cards.
        - Evaluating hero's 7-card hand.
        - Evaluating ALL villain 7-card hands.
        - Finding which villain(s) have the strongest hand.
        - Comparing hero's hand strength to the best villain hand.
        - Awarding the pot accordingly.
    """

    print("\n=== SHOWDOWN ===")

    # Show hero hand and community board
    print("Your Hand:", my_cards, " → ", my_cards_S)
    print("Community cards:", community_cards)
    print("Pot size: $", GAME_STATE["pot_size"])

    # Combine hero's hole cards with community cards to form 7 cards
    hero_hand = my_cards + community_cards
    # Evaluate hero's 7-card hand strength (returns tuple for comparison)
    hero_score = evaluate_7_card_hand(hero_hand)

    # --- FIND BEST VILLAIN HAND ---
    best_villain_score = None    
    best_villains = []            

    hero_id = player_list[0]     

    # Loop through all players EXCEPT the hero
    for pid in player_list:
        if pid == hero_id:
            continue  

        # Get villain's hole cards
        v_cards = hands[pid]
        # Build full 7-card hand just like hero
        v_hand = v_cards + community_cards
        # Evaluate villain's hand strength
        v_score = evaluate_7_card_hand(v_hand)

        # First villain encountered OR stronger hand found
        if best_villain_score is None or v_score > best_villain_score:
            best_villain_score = v_score
            best_villains = [pid]     
        # Tie: another villain has the same best score
        elif v_score == best_villain_score:
            best_villains.append(pid)

    # show best villain hand
    print("\nBest villain hand:")
    for pid in best_villains:
        v_cards = hands[pid]
        v_label = standardizeMyHand(v_cards)
        print(f"{pid}: {v_cards}")

    # Compare to best villain
    if best_villain_score is None:
        # This case only happens if no villains exist (safety fallback)
        print("\nNo villains found. You win by default.")
        GAME_STATE["my_stack"] += GAME_STATE["pot_size"]

    else:
        # Hero beats strongest villain
        if hero_score > best_villain_score:
            print("\nYou win the hand!")
            print("You win the pot of $", GAME_STATE["pot_size"])
            GAME_STATE["my_stack"] += GAME_STATE["pot_size"]

        # Exact tie with best villain hand
        elif hero_score == best_villain_score:
            print("\nThe hand is a TIE with the best villain.")
            print("Pot is effectively split. (No stack change shown.)")
            # Full split logic requires tracking villain stacks, optional

        # Villain beat hero
        else:
            print("\nYou lose the hand.")
            print("The pot of $", GAME_STATE["pot_size"], "goes to an opponent.")

    # --- SHOW FINAL STACK ---
    print("Your final stack is $", GAME_STATE["my_stack"])



# ============== MAIN GAME ===============

def RunHand(player_list):
    """
    Run a single hand of the game.
    """
    deck = create_deck()
    hands = deal_hole_cards(player_list, deck)

    # hero is always P1.
    me = player_list[0]
    my_cards = hands[me]
    my_cards_S = standardizeMyHand(my_cards)

    # let user imput how much they want to buy in to the game for
    initial_stack = int(input("How much money would you like to buy in for your stack? "))

    # Build preflop hand types and ranges.
    all_h = all_169_hands(RANKS)
    PREFLOP_RANGES = build_preflop_ranges(all_h)

    # Let user decide blind amounts
    small_blind = int(input("Enter small blind amount: "))
    big_blind = int(input("Enter big blind amount: "))

    # GAME_STATE updates each betting round according to actions
    GAME_STATE = {
        "betting_round": "Pre-Flop",
        "small_blind": small_blind,
        "big_blind": big_blind,
        "pot_size": small_blind + big_blind,
        "to_call": big_blind,
        "my_stack": initial_stack
    }

    community_cards = []

    # ----- Pre-Flop -----
    displayAnalysis(my_cards_S, my_cards, GAME_STATE, all_h, PREFLOP_RANGES, community_cards)
    result, amount = mydecision(GAME_STATE)
    if result == "FOLD":
        return
    raised = opponents_act(player_list, GAME_STATE)
    if raised:
        if not force_hero_match(GAME_STATE):
            return

    # ----- Flop -----
    community_cards = flopRound(deck, GAME_STATE)
    displayAnalysis(my_cards_S, my_cards, GAME_STATE, all_h, PREFLOP_RANGES, community_cards)
    result, amount = mydecision(GAME_STATE)
    if result == "FOLD":
        return
    raised = opponents_act(player_list, GAME_STATE)
    if raised:
        if not force_hero_match(GAME_STATE):
            return

    # ----- Turn -----
    community_cards = turnRound(deck, GAME_STATE, community_cards)
    displayAnalysis(my_cards_S, my_cards, GAME_STATE, all_h, PREFLOP_RANGES, community_cards)
    result, amount = mydecision(GAME_STATE)
    if result == "FOLD":
        return
    raised = opponents_act(player_list, GAME_STATE)
    if raised:
        if not force_hero_match(GAME_STATE):
            return

    # ----- River -----
    community_cards = River(deck, GAME_STATE, community_cards)
    displayAnalysis(my_cards_S, my_cards, GAME_STATE, all_h, PREFLOP_RANGES, community_cards)
    result, amount = mydecision(GAME_STATE)
    if result == "FOLD":
        return
    raised = opponents_act(player_list, GAME_STATE)
    if raised:
        if not force_hero_match(GAME_STATE):
            return

    # If hero gets here, they reached showdown.
    resolve_showdown(GAME_STATE,my_cards,community_cards, my_cards_S,player_list, hands)



# Start a single hand with the fixed player list.
RunHand(player_list)
