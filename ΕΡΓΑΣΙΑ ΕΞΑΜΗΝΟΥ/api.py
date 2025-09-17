from fastapi import FastAPI, Query
import json
from typing import List

app = FastAPI()

# Φόρτωση των δεδομένων από το JSON αρχείο
def load_quotes():
    try:
        with open("quotes.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:    #Διαχείριση Λαθών με την δομη try-except σε περίπτωση που δεν βρέθηκε το αρχείο  
        return []                

@app.get("/quotes", response_model=List[str])
def get_quotes(author: str = Query(..., title="Author Name", description="Το όνομα του συγγραφέα")):
    quotes = load_quotes()
    author_quotes = [q["quote"] for q in quotes if q["author"].lower() == author.lower()]
    return author_quotes
   



