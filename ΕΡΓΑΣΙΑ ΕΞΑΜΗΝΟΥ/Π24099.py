import requests
from bs4 import BeautifulSoup   
import json
import os

def fetch_quote_ids(student_id):
    """
    Ανάκτηση των Quote IDs από τη δυναμική ιστοσελίδα.
   
    """
    url = f"https://tma111.netlify.app/.netlify/functions/generate?id={student_id}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Σφάλμα κατά τη λήψη δεδομένων: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    numbers = set()  #  set για να αποφύγουμε διπλότυπα

    # Αναζήτηση αριθμών σε διάφορα HTML tags
    for tag in soup.find_all(["p", "span", "div", "li", "td"]):
        text = tag.get_text(strip=True)
        words = text.split()  # Διαχωρισμός με βάση τα κενά
        
        for word in words:
            if word.isdigit():  # Κρατάμε μόνο αριθμούς
                numbers.add(int(word))

    return sorted(numbers)[:50]  # Επιστροφή των πρώτων 50 μοναδικών, ταξινομημένων IDs


def fetch_quotes(quote_ids):
    """
    Ανάκτηση των αποφθεγμάτων από το API.
    """
    quotes = []
    
    for qid in quote_ids:
        url = f"https://dummyjson.com/quotes/{qid}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            quote_data = response.json()
            
            if isinstance(quote_data, dict) and "id" in quote_data and "quote" in quote_data and "author" in quote_data:
                quotes.append({
                    "id": quote_data["id"],
                    "quote": quote_data["quote"],
                    "author": quote_data["author"]
                })
        except requests.RequestException as e:
            print(f"Σφάλμα κατά την ανάκτηση του quote με ID {qid}: {e}")

    return sorted(quotes, key=lambda x: x['id'])


def save_quotes_to_json(quotes, filename="quotes.json"):
    """
    Αποθήκευση των αποφθεγμάτων σε αρχείο JSON.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(quotes, f, indent=4, ensure_ascii=False)
        print(f"Τα αποφθέγματα αποθηκεύτηκαν επιτυχώς στο {filename}")
    except IOError as e:
        print(f"Σφάλμα κατά την αποθήκευση των αποφθεγμάτων: {e}")


def fetch_color_scheme(student_id):
    """
    Ανάκτηση του χρωματικού συνδυασμού από τη δυναμική σελίδα.
    """
    url = f"https://tma111.netlify.app/.netlify/functions/generate?id={student_id}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Σφάλμα κατά τη λήψη δεδομένων χρωμάτων: {e}")
        return "000000", "FFFFFF"  # Προεπιλεγμένα χρώματα

    soup = BeautifulSoup(response.text, 'html.parser')
    color_div = soup.find("div", id="colors")

    if color_div:
        bg_color = color_div.get("data-bg", "#000000").replace("#", "")  # Αφαιρούμε το #
        text_color = color_div.get("data-color", "#FFFFFF").replace("#", "")
    else:
        bg_color, text_color = "000000", "FFFFFF"  # Προεπιλεγμένα χρώματα

    return bg_color, text_color


def generate_quote_images(quotes, bg_color, text_color):
    """
    Δημιουργία εικόνων PNG για κάθε απόφθεγμα.
    """
    os.makedirs("quotes", exist_ok=True)

    for quote in quotes:
        image_url = (f"https://dummyjson.com/image/1200x200/{bg_color}/{text_color}?text="
                     f"{quote['quote'].replace(' ', '%20')}&fontSize=18")

        try:
            image_data = requests.get(image_url).content
            with open(f"quotes/{quote['id']}.png", "wb") as img_file:
                img_file.write(image_data)
            print(f"Εικόνα {quote['id']}.png δημιουργήθηκε.")
        except requests.RequestException as e:
            print(f"Σφάλμα κατά τη δημιουργία εικόνας για το quote {quote['id']}: {e}")


def main():
    student_id = input("Εισάγετε τον Α.Μ. σας: ").strip()   #Για διαχείριση απο το τερματικό
    
    # 1. Εξαγωγή Quote IDs
    quote_ids = fetch_quote_ids(student_id)
    if not quote_ids:
        print("Δεν βρέθηκαν έγκυρα Quote IDs. Ελέγξτε τον Α.Μ. σας.")
        return

    print("Ανακτήθηκαν τα ακόλουθα Quote IDs:", quote_ids)

    # 2. Ανάκτηση Quotes από το API
    quotes = fetch_quotes(quote_ids)
    if quotes:
        save_quotes_to_json(quotes)
    else:
        print("Δεν ανακτήθηκαν αποφθέγματα. Ελέγξτε τα quote IDs και την επικοινωνία με το API.")
        return

    # 3. Ανάκτηση και εφαρμογή του Χρωματικού Σχήματος
    bg_color, text_color = fetch_color_scheme(student_id)

    # 4. Δημιουργία και αποθήκευση εικόνων
    generate_quote_images(quotes, bg_color, text_color)

    print("Η διαδικασία ολοκληρώθηκε! Οι εικόνες αποθηκεύτηκαν στο φάκελο quotes/.")


if __name__ == "__main__":
    main()
