from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        scored_songs = []
        for song in self.songs:
            # Calculate score based on user preferences
            score = 0.0
            
            # Genre match
            if song.genre == user.favorite_genre:
                score += 2.0
            
            # Mood match
            if song.mood == user.favorite_mood:
                score += 1.0
            
            # Energy similarity
            energy_sim = 1.0 - abs(song.energy - user.target_energy)
            score += energy_sim * 0.5
            
            # Adjust for acousticness preference
            if user.likes_acoustic and song.acousticness > 0.7:
                score += 0.5
            elif not user.likes_acoustic and song.acousticness < 0.3:
                score += 0.25
            
            scored_songs.append((song, score))
        
        # Sort by score and return top k
        ranked = sorted(scored_songs, key=lambda x: x[1], reverse=True)
        return [song for song, score in ranked[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        reasons = []
        
        if song.genre == user.favorite_genre:
            reasons.append(f"Matches your favorite genre: {song.genre}")
        
        if song.mood == user.favorite_mood:
            reasons.append(f"Matches your mood preference: {song.mood}")
        
        energy_sim = 1.0 - abs(song.energy - user.target_energy)
        reasons.append(f"Energy level ({song.energy:.2f}) is close to your preference ({user.target_energy:.2f})")
        
        if user.likes_acoustic and song.acousticness > 0.7:
            reasons.append("Has high acousticness as you prefer")
        
        return " | ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from CSV file and convert numerical values to floats."""
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert numerical values to floats
            row['id'] = int(row['id'])
            row['energy'] = float(row['energy'])
            row['tempo_bpm'] = float(row['tempo_bpm'])
            row['valence'] = float(row['valence'])
            row['danceability'] = float(row['danceability'])
            row['acousticness'] = float(row['acousticness'])
            songs.append(row)
    print(f"Loaded {len(songs)} songs.")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song against user preferences using weighted features (genre, mood, energy, valence, danceability)."""
    score = 0.0
    reasons = []
    
    # Genre match: +2.0 points
    user_genres = user_prefs.get("favorite_genres", [user_prefs.get("genre", "")])
    if isinstance(user_genres, str):
        user_genres = [user_genres]
    
    if song['genre'] in user_genres:
        score += 2.0
        reasons.append(f"Genre match: {song['genre']} (+2.0)")
    
    # Mood match: +1.0 point
    if song['mood'] == user_prefs.get("favorite_mood") or song['mood'] == user_prefs.get("mood"):
        score += 1.0
        reasons.append(f"Mood match: {song['mood']} (+1.0)")
    
    # Energy similarity: 0.5 weight
    target_energy = user_prefs.get("target_energy", 0.5)
    energy_sim = 1.0 - abs(float(song['energy']) - target_energy)
    energy_points = energy_sim * 0.5
    score += energy_points
    reasons.append(f"Energy similarity: {energy_sim:.2f} ({energy_points:.2f})")
    
    # Valence similarity: 0.25 weight
    target_valence = user_prefs.get("target_valence", 0.5)
    valence_sim = 1.0 - abs(float(song['valence']) - target_valence)
    valence_points = valence_sim * 0.25
    score += valence_points
    reasons.append(f"Valence similarity: {valence_sim:.2f} ({valence_points:.2f})")
    
    # Danceability similarity: 0.25 weight
    target_danceability = user_prefs.get("target_danceability", 0.5)
    danceability_sim = 1.0 - abs(float(song['danceability']) - target_danceability)
    danceability_points = danceability_sim * 0.25
    score += danceability_points
    reasons.append(f"Danceability similarity: {danceability_sim:.2f} ({danceability_points:.2f})")
    
    # NEW: Popularity boost (0-100 scale, normalized to 0-0.5 points)
    popularity = float(song.get('popularity', 50))
    popularity_bonus = (popularity / 100) * 0.5
    score += popularity_bonus
    reasons.append(f"Popularity bonus: {popularity_bonus:.2f}")
    
    # NEW: Vibe tag matching (if user prefers certain vibes)
    user_vibes = user_prefs.get("preferred_vibes", [])
    if user_vibes and song.get('vibe') in user_vibes:
        score += 0.3
        reasons.append(f"Vibe match: {song['vibe']} (+0.3)")
    
    return (score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank all songs by score and return top k recommendations with explanations."""
    return recommend_songs_mode(user_prefs, songs, k, mode="balanced")


def recommend_songs_mode(user_prefs: Dict, songs: List[Dict], k: int = 5, mode: str = "balanced") -> List[Tuple[Dict, float, str]]:
    """Rank songs using different scoring strategies.
    
    Modes:
    - balanced: Original weighted scoring
    - genre_first: 3x weight on genre matching
    - mood_first: 3x weight on mood matching
    """
    scored_songs = []
    
    for song in songs:
        if mode == "genre_first":
            score, reasons = score_song_genre_first(user_prefs, song)
        elif mode == "mood_first":
            score, reasons = score_song_mood_first(user_prefs, song)
        else:
            score, reasons = score_song(user_prefs, song)
        
        explanation = " | ".join(reasons)
        scored_songs.append((song, score, explanation))
    
    # Sort by score (highest first)
    ranked_songs = sorted(scored_songs, key=lambda x: x[1], reverse=True)
    
    # Apply diversity penalty: penalize if artist already in top k
    final_recs = []
    seen_artists = set()
    
    for song, score, explanation in ranked_songs:
        artist = song.get('artist', 'Unknown')
        
        if artist in seen_artists:
            penalty = 0.5
            score -= penalty
            explanation += f" | DIVERSITY PENALTY: same artist ({artist}) -0.5"
        
        final_recs.append((song, score, explanation))
        seen_artists.add(artist)
        
        if len(final_recs) >= k:
            break
    
    return final_recs[:k]


def score_song_genre_first(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Genre-first scoring: prioritize genre matching."""
    score = 0.0
    reasons = []
    
    user_genres = user_prefs.get("favorite_genres", [user_prefs.get("genre", "")])
    if isinstance(user_genres, str):
        user_genres = [user_genres]
    
    if song['genre'] in user_genres:
        score += 5.0  # Boosted from 2.0
        reasons.append(f"Genre PRIORITY: {song['genre']} (+5.0)")
    
    if song['mood'] == user_prefs.get("favorite_mood"):
        score += 0.5
        reasons.append(f"Mood: {song['mood']} (+0.5)")
    
    energy_sim = 1.0 - abs(float(song['energy']) - user_prefs.get("target_energy", 0.5))
    energy_points = energy_sim * 0.3
    score += energy_points
    reasons.append(f"Energy: {energy_points:.2f}")
    
    return (score, reasons)


def score_song_mood_first(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Mood-first scoring: prioritize mood matching."""
    score = 0.0
    reasons = []
    
    if song['mood'] == user_prefs.get("favorite_mood"):
        score += 5.0  # Boosted from 1.0
        reasons.append(f"Mood PRIORITY: {song['mood']} (+5.0)")
    
    user_genres = user_prefs.get("favorite_genres", [user_prefs.get("genre", "")])
    if isinstance(user_genres, str):
        user_genres = [user_genres]
    
    if song['genre'] in user_genres:
        score += 0.5
        reasons.append(f"Genre: {song['genre']} (+0.5)")
    
    energy_sim = 1.0 - abs(float(song['energy']) - user_prefs.get("target_energy", 0.5))
    energy_points = energy_sim * 0.3
    score += energy_points
    reasons.append(f"Energy: {energy_points:.2f}")
    
    return (score, reasons)
