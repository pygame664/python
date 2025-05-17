import random
import time
from datetime import datetime


HISTORY_FILE = "game_history.txt"
DEFAULT_WORDS = ['dog', 'cat', 'fish', 'mouse', 'chicken', 'frog']


def save_history(mode, result, word, time_used, remaining_guesses):
    """保存游戏记录到文件"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(
            f"[{timestamp}] Mode: {mode} | Result: {result} | Word: {word} | "
            f"Time: {time_used:.1f}s | Remaining: {remaining_guesses}\n"
        )

def show_history():
    """显示历史记录"""
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            print("\n=== GAME HISTORY ===\n")
            print(f.read())
    except FileNotFoundError:
        print("\nNo history records found.\n")


class WordGame:
    def __init__(self, mode="normal", custom_words=None, guess_chances=14, rounds=1, order='random'):
        self.mode = mode
        self.words = custom_words if custom_words else DEFAULT_WORDS.copy()
        self.guess_chances = guess_chances
        self.rounds = rounds
        self.order = order
        self.current_round = 0
        

        if order == 'random':
            random.shuffle(self.words)
        elif order == 'reverse':
            self.words.reverse()

    def select_word(self):
        """根据模式选择单词"""
        if self.mode == 'creator' and len(self.words) > 0:
            return self.words.pop(0)
        return random.choice(self.words)

    def play_round(self):
        """进行一轮游戏"""
        self.current_round += 1
        word = self.select_word().lower()
        guessed = set()
        start_time = time.time()
        remaining = self.guess_chances
        
        print(f"\n=== Round {self.current_round} ===")
        print(f"Word length: {len(word)} letters")
        
        while remaining > 0:
            print(f"\nGuesses left: {remaining}")
            self.display_word(word, guessed)
            

            guess = input("Enter letter(s): ").lower()
            if not guess.isalpha():
                print("Please enter valid letters.")
                continue
                

            new_letters = {char for char in guess if char not in guessed}
            guessed.update(new_letters)
            remaining -= 1
            

            if all(c in guessed for c in word):
                time_used = time.time() - start_time
                print(f"\nCongratulations! The word was: {word}")
                print(f"Time used: {time_used:.1f}s | Guesses remaining: {remaining}")
                save_history(self.mode, "WIN", word, time_used, remaining)
                return True
                

            correct_guess = any(c in word for c in new_letters)
            if not correct_guess:
                print("No correct letters in this guess!")
        

        time_used = time.time() - start_time
        print(f"\nGame Over! The word was: {word}")
        save_history(self.mode, "LOSE", word, time_used, remaining)
        return False

    @staticmethod
    def display_word(word, guessed):
        """显示当前猜测进度"""
        display = ''.join([c if c in guessed else '-' for c in word])
        print(f"Word: {display}")


def main_menu():
    """显示主菜单"""
    while True:
        print("\n=== MAIN MENU ===")
        print("1. Normal Mode")
        print("2. Creator Mode")
        print("3. View History")
        print("4. Exit")
        
        choice = input("Select option (1-4): ").strip()
        
        if choice == '1':
            normal_mode()
        elif choice == '2':
            creator_mode()
        elif choice == '3':
            show_history()
        elif choice == '4':
            print("Goodbye!")
            return
        else:
            print("Invalid choice. Please enter 1-4.")

def normal_mode():
    """普通游戏模式"""
    game = WordGame()
    game.play_round()

def creator_mode():
    """自定义游戏模式"""
    print("\n=== CREATOR MODE ===")
    

    words = []
    while True:
        word = input("Add a word (leave blank to finish): ").strip()
        if word == "":
            if len(words) < 1:
                print("Please add at least one word.")
                continue
            break
        if not word.isalpha():
            print("Invalid word. Use letters only.")
            continue
        words.append(word.lower())
    
    chances = get_number_input("Guess chances per round: ", min_val=1)
    rounds = get_number_input("Number of rounds: ", min_val=1)
    
    print("\nSelect word order:")
    print("1. Random")
    print("2. In order")
    print("3. Reverse order")
    order_choice = input("Choice (1-3): ").strip()
    order_map = {'1':'random', '2':'sequence', '3':'reverse'}
    order = order_map.get(order_choice, 'random')
    

    game = WordGame(
        mode='creator',
        custom_words=words,
        guess_chances=chances,
        rounds=rounds,
        order=order
    )
    

    for _ in range(rounds):
        game.play_round()
        if _ != rounds-1:
            input("\nPress Enter to continue to next round...")

def get_number_input(prompt, min_val=1):
    """获取有效数字输入"""
    while True:
        try:
            value = int(input(prompt))
            if value >= min_val:
                return value
            print(f"Value must be at least {min_val}")
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    print("=== WORD GUESSING GAME ===")
    print("Developed for Python 3.12")
    main_menu()