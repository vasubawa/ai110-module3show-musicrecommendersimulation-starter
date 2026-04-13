# Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0** — A content-based music recommendation engine

---

## 2. Intended Use  

Recommend songs to users based on their taste profile (favorite genre, mood, and energy level). Designed for classroom exploration of how AI systems make predictions. Not intended for production use or real user deployment.

---

## 3. How the Model Works  

The system scores every song in the catalog using a weighted formula:
- **Genre Match**: +2 points if the song's genre matches the user's favorite
- **Mood Match**: +1 point if the song's mood matches the user's preference
- **Energy Similarity**: Compare how close the song's energy is to the user's target (0-1 scale)
- **Valence Similarity**: Compare how positive/upbeat the song is vs. user preference
- **Danceability Similarity**: Compare dance-ability to user preference

Final score = (genre × 2.0) + (mood × 1.0) + (energy × 0.5) + (valence × 0.25) + (danceability × 0.25)

The system ranks all songs by score and returns the top 5 recommendations.

---

## 4. Data  

- **Size**: 18 songs across 9 genres
- **Genres**: pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, electronic, metal, reggae, folk
- **Moods**: happy, chill, intense, relaxed, moody, focused, energetic, sad, uplifting, melancholic
- **Features**: genre, mood, energy, tempo, valence, danceability, acousticness
- **Missing**: Artist popularity, release recency, user listening context, cultural trends

---

## 5. Strengths  

- Correctly differentiates between distinct user types (High-Energy Pop vs. Chill Lofi vs. Intense Rock)
- Transparent scoring: Shows exactly why each song was recommended
- Handles conflicting preferences gracefully (energy vs. mood can both influence ranking)
- Works with limited data (no user-user or song-song collaboration needed)

---

## 6. Limitations and Bias 

- **Genre over-prioritization**: Genre match (+2 points) dominates, so songs from non-preferred genres rarely rank high regardless of mood/energy match
- **Dataset imbalance**: Pop songs are 22% of catalog; system may favor them despite user preferences
- **Filter bubble**: Recommendations tend toward similar songs; low diversity in top 5
- **Cold-start problem**: Requires explicit user preferences; can't learn from implicit feedback
- **Missing context**: Ignores time of day, user activity, recent listening history

---

## 7. Evaluation  

Tested three distinct user profiles:
- **High-Energy Pop**: Returns pop/electronic songs with high energy/valence ✓
- **Chill Lofi**: Returns lofi/ambient songs with low energy ✓
- **Intense Rock**: Returns rock/metal songs with high energy/low valence ✓

**Findings**: System works as intended for each profile. Different genres get different recommendations appropriately.

---

## 8. Future Work  

- Increase dataset size to improve diversity
- Add collaborative filtering to discover cross-genre recommendations
- Weight recent songs higher (recency bias)
- Allow users to rate recommendations to improve future scoring
- Implement diversity penalty to ensure top 5 don't all sound identical

---

## 9. Personal Reflection

**Biggest Learning**: How much the weight distribution matters. Doubling genre (+2.0) made it dominate the recommendations. I realized that simple numbers can create powerful biases that aren't obvious until you test them.

**AI Tool Reflection**: AI helped me structure the code quickly, but I had to verify every scoring calculation manually. AI suggested the formulas, but I needed to validate the math worked correctly for edge cases.

**What Surprised Me**: How transparent the scoring breakdowns made the system. Showing "Because: Genre match: pop (+2.0)" for every recommendation immediately revealed why the system was biased—I could see the problem in the output itself.

**Next Steps**: If I continued this project, I'd:
1. Implement a "surprise me" feature that occasionally recommends songs outside the user's usual preferences
2. Add user feedback loop so the system learns which recommendations were actually good
3. Create a visualization of how the scoring weights influence different user types
4. Test with adversarial profiles (e.g., user wants high energy BUT sad mood) to stress-test the logic  
