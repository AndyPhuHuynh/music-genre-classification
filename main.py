import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"]  = "2"

import subprocess
from tqdm import tqdm

import src.paths as paths
from src.setup.soundfonts import download_soundfonts
from src.music_generation.generate_music import Song

# from src.features.labels import get_effect_from_label
# from src.features.mfcc import extract_mfcc_from_dataset
# from src.models.model1 import train_model1
#
# from src.music_generation.generate_music import *

NUM_SONGS: int = 10

def generate_songs():
    os.makedirs(paths.DIATONIC_DIR, exist_ok=True)
    for i in tqdm(range(NUM_SONGS), desc="Generating songs"):
        midi = paths.DIATONIC_DIR/f"diatonic_{i:03}.mid"
        wave = paths.DIATONIC_DIR/f"diatonic_{i:03}.wav"

        happy_song = Song()
        happy_song.write(midi)
        subprocess.run([
            "fluidsynth", "-ni",
            "-F", wave,
            "-r", "44100",
            paths.FLUID_SF_PATH,
            midi
        ], check=True, stdout=subprocess.DEVNULL)
        midi.unlink()
        print(f"Progression for {midi}:")
        for phrase in happy_song.phrases:
            print(f"\t{phrase.progression}")


download_soundfonts()
generate_songs()
# scaler, dataset = extract_mfcc_from_dataset(SAMPLE_RATE)

# model, history, ratios = train_model1(dataset)
# for effect, accuracy in ratios.items():
#     print(f"Accuracy for {get_effect_from_label(effect):<10} is {100 * accuracy:.2f}%")