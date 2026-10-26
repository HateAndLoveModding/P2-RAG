import json
import re
import os
import shutil

base_dir = "kjv-chapters"
# Start from an empty folder, so files from an earlier run never get ingested with these.
shutil.rmtree(base_dir, ignore_errors=True)
os.mkdir(f"{base_dir}")

ROMAN = {"I": "1", "II": "2", "III": "3"}


def display_name(book_title):
    """The usual form of a book name: "I Samuel" -> "1 Samuel", "Revelation of John" -> "Revelation"."""
    if book_title == "Revelation of John":
        return "Revelation"
    first, _, rest = book_title.partition(" ")
    if first in ROMAN and rest:
        return f"{ROMAN[first]} {rest}"
    return book_title

with open("KJV.json") as file:
    data = json.load(file)
    books = data["books"]

old_testament = {
    "Genesis", "Exodus", "Deuteronomy", "Joshua", "Judges", "Ruth",
    "I Samuel", "II Samuel", "I Kings", "II Kings", "Esther", "Job",
    "Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon", "Isaiah",
    "Jeremiah", "Lamentations", "Ezekiel", "Daniel",
}
book_titles = list(books)
new_testament = set(book_titles[book_titles.index("Matthew"):])
keep = old_testament | new_testament

book_index = 1
for book_title in books:
    if book_title not in keep:
        continue
    name = display_name(book_title)
    file_title = str.replace(name, " ", "_")
    book = books[f"{book_title}"]
    chapters = [chapter for chapter in book]
    fulltexts = []

    chap_index = 1
    for chapter in chapters:
        verses = [verse for verse in chapter]
        indeces = [verses.index(verse) for verse in chapter]

        verses = []

        for index in indeces:
            chunks = [i for i in chapter[index]]
            verse = " ".join([chunk[0]
                              for chunk in chunks if not isinstance(chunk[0], list)])
            verse = re.sub(r'\s([?.,;!"](?:\s|$))', r'\1', verse)
            # The source puts a space before some colons and closing marks ("Christ Jesus :", "( for she died )").
            verse = re.sub(r'\s+([?.,;:!)])', r'\1', verse)
            verse = re.sub(r'\(\s+', '(', verse)
            verses.append(verse)

        with open(f"{base_dir}/{file_title}_{chap_index:02d}.md", "w") as file:
            file.write(f"---\ntitle: {name} {chap_index}\n---\n")
            verse_index = 1
            for verse in verses:
                file.write(f"{name} {chap_index}:{verse_index} {verse}\n")
                verse_index += 1
            file.write("\n")
        chap_index += 1
    book_index += 1
