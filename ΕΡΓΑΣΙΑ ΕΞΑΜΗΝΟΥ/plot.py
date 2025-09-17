import json
import matplotlib.pyplot as plt
from collections import Counter

QUOTES_FILE = "quotes.json"

def load_quotes():
    """Φόρτωση των quotes από το JSON αρχείο."""
    try:
        with open(QUOTES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Το quotes.json δεν βρέθηκε.")
        return []

def plot_quotes_by_author():
    """Δημιουργία ιστογράμματος για τον αριθμό των quotes ανά συγγραφέα."""
    quotes = load_quotes()
    
    if not quotes:
        print("Δεν υπάρχουν διαθέσιμα quotes για ανάλυση.")
        return
    
    # Υπολογίζουμε τη συχνότητα των συγγραφέων
    author_counts = Counter(q["author"] for q in quotes)

    # Ταξινόμηση ανά αριθμό quotes
    sorted_authors = sorted(author_counts.items(), key=lambda x: x[1], reverse=True)
    authors, counts = zip(*sorted_authors)

    # Δημιουργία ιστογράμματος
    plt.figure(figsize=(10, 5))
    plt.barh(authors, counts)
    plt.xlabel("Αριθμός Quotes")
    plt.ylabel("Συγγραφέας")
    plt.title("Κατανομή Quotes ανά Συγγραφέα")
    plt.gca().invert_yaxis()  # Αναστροφή άξονα για σωστή απεικόνιση
    plt.tight_layout()

    # Αποθήκευση του γραφήματος
    plt.savefig("histogram.png")
    print("Το ιστόγραμμα αποθηκεύτηκε ως histogram.png")

if __name__ == "__main__":
    plot_quotes_by_author()
