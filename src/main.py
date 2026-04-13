"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs_mode


def main() -> None:
    """Run the Music Recommender Simulation with default user preferences."""
    songs = load_songs("data/songs.csv") 

    # Define three diverse user profiles
    profiles = {
        "High-Energy Pop": {
            "favorite_genres": ["pop", "electronic"],
            "favorite_mood": "happy",
            "target_energy": 0.8,
            "target_valence": 0.80,
            "target_danceability": 0.78,
            "preferred_vibes": ["uplifting", "euphoric"]
        },
        "Chill Lofi": {
            "favorite_genres": ["lofi", "ambient"],
            "favorite_mood": "chill",
            "target_energy": 0.35,
            "target_valence": 0.55,
            "target_danceability": 0.50,
            "preferred_vibes": ["peaceful", "dreamy"]
        },
        "Intense Rock": {
            "favorite_genres": ["rock", "metal"],
            "favorite_mood": "intense",
            "target_energy": 0.92,
            "target_valence": 0.40,
            "target_danceability": 0.65,
            "preferred_vibes": ["aggressive"]
        }
    }

    # Test each profile with different modes
    for profile_name, user_prefs in profiles.items():
        for mode in ["balanced", "genre_first", "mood_first"]:
            recommendations = recommend_songs_mode(user_prefs, songs, k=3, mode=mode)
            
            print(f"\n{'='*80}")
            print(f"Profile: {profile_name} | Mode: {mode.upper()}")
            print(f"{'='*80}\n")
            
            # Print as formatted table
            print(f"{'Rank':<5} {'Title':<25} {'Artist':<20} {'Score':<8}")
            print(f"{'-'*5} {'-'*25} {'-'*20} {'-'*8}")
            
            for i, rec in enumerate(recommendations, 1):
                song, score, explanation = rec
                print(f"{i:<5} {song['title']:<25} {song['artist']:<20} {score:>7.2f}")
                print(f"      [{explanation[:65]}...]")
                print()
        print()


if __name__ == "__main__":
    main()