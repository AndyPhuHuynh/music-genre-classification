genre_labels: dict[str, int] = {
    "blues":     0,
    "classical": 1,
    "country":   2,
    "disco":     3,
    "hiphop":    4,
    "jazz":      5,
    "metal":     6,
    "pop":       7,
    "reggae":    8,
    "rock":      9,
}

label_map = {v: k for k, v in genre_labels.items()}

def get_label(genre: str) -> int:
    if genre in genre_labels:
        return genre_labels[genre]
    else:
        raise ValueError(f"No label found, invalid genre: {genre}")


def get_genre_from_label(label: int) -> str:
    if label in label_map:
        return label_map[label]
    else:
        raise ValueError(f"No label found, invalid label: {label}")