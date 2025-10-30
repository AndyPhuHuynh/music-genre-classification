genre_labels = {
    "blues": 0,
    "classical": 1,
    "country": 2,
    "disco": 3,
    "hiphop": 4,
    "jazz": 5,
    "metal": 6,
    "pop": 7,
    "reggae": 8,
    "rock": 9,
}

def get_label(genre: str) -> int:
    if genre in genre_labels:
        return genre_labels[genre]
    else:
        raise ValueError(f"No label found, invalid genre: {genre}")