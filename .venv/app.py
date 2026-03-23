import requests
import streamlit as st

# =============================
# CONFIG
# =============================
API_BASE = "http://127.0.0.1:8000"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# =============================
# STYLES (minimal modern)
# =============================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

/* Animated Dynamic Background */
.stApp {
    background: linear-gradient(-45deg, #0f172a, #1e1b4b, #09090b, #171717);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
    color: #f8fafc;
}

@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1400px;
}

/* Typography Enhancements */
h1, h2, h3, h4, .hero-title {
    letter-spacing: -0.02em;
}

.small-muted { 
    color: #94a3b8; 
    font-size: 0.95rem; 
    font-weight: 300;
}

/* Movie Poster Styles & Hover Animations */
img {
    border-radius: 12px;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -2px rgba(0, 0, 0, 0.3);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

img:hover {
    transform: scale(1.05) translateY(-5px);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.7), 0 10px 10px -5px rgba(0, 0, 0, 0.5);
}

.movie-title {
    font-size: 0.95rem;
    font-weight: 600;
    line-height: 1.25rem;
    min-height: 2.5rem;
    overflow: hidden;
    margin-top: 0.6rem;
    color: #e2e8f0;
    text-align: center;
    transition: color 0.2s ease;
}

/* Glassmorphism Cards */
.card {
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 24px;
    background: rgba(15, 23, 42, 0.4);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    transition: all 0.3s ease;
}

.card:hover {
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Hero Section */
.hero {
    position: relative;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 24px;
    background: linear-gradient(135deg, rgba(79, 70, 229, 0.2) 0%, rgba(15, 23, 42, 0.8) 100%);
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    overflow: hidden;
    box-shadow: 0 20px 40px -10px rgba(0,0,0,0.5);
}

.hero::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(circle at top right, rgba(99, 102, 241, 0.15), transparent 50%);
    pointer-events: none;
}

.hero-title {
    color: #ffffff;
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
    background: repeating-linear-gradient(to right, #6366f1, #a855f7, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline-block;
}

.hero-sub {
    color: #cbd5e1;
    font-size: 1.1rem;
    max-width: 600px;
    line-height: 1.6;
}

/* Premium Buttons */
button[kind="secondary"] {
    border-radius: 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    background: rgba(30, 41, 59, 0.5) !important;
    color: #f8fafc !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
    padding: 0.5rem 1rem !important;
}

button[kind="secondary"]:hover {
    background: rgba(79, 70, 229, 0.8) !important;
    border-color: rgba(99, 102, 241, 0.5) !important;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

/* Inputs / Selectors */
.stTextInput > div > div > input {
    border-radius: 12px;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #fff;
    padding: 0.75rem 1rem;
    transition: border-color 0.2s;
}

.stTextInput > div > div > input:focus {
    border-color: #6366f1;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
}

.stSelectbox > div > div > div {
    border-radius: 12px;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Cast List */
.cast-container {
    display: flex;
    overflow-x: auto;
    gap: 15px;
    padding-bottom: 10px;
    margin-top: 10px;
}
.cast-card {
    min-width: 90px;
    text-align: center;
}
.cast-img {
    width: 70px;
    height: 70px;
    border-radius: 50%;
    object-fit: cover;
    margin-bottom: 5px;
    border: 2px solid rgba(255,255,255,0.2);
}
.cast-name {
    font-size: 0.8rem;
    font-weight: 600;
    color: #f8fafc;
}
.cast-character {
    font-size: 0.7rem;
    color: #94a3b8;
}

/* Sidebar Customization */
[data-testid="stSidebar"] {
    background-color: rgba(10, 15, 30, 0.6) !important;
    backdrop-filter: blur(20px) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}

[data-testid="stSidebar"] button[kind="secondary"] {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    justify-content: flex-start !important;
    text-align: left !important;
    padding: 0.75rem 1.25rem !important;
    margin-bottom: 0.5rem !important;
}

[data-testid="stSidebar"] button[kind="secondary"]:hover {
    background: rgba(99, 102, 241, 0.2) !important;
    border-color: rgba(129, 140, 248, 0.5) !important;
    transform: translateX(4px);
    box-shadow: none !important;
}

.sidebar-title {
    font-size: 1.3rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
    background: linear-gradient(90deg, #a78bfa, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 0.5px;
}

.sidebar-section {
    font-size: 0.85rem;
    font-weight: 600;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 2rem;
    margin-bottom: 1rem;
}
</style>
""",
    unsafe_allow_html=True,
)

# =============================
# STATE + ROUTING (single-file pages)
# =============================
if "view" not in st.session_state:
    st.session_state.view = "home"  # home | details | favorites | actor
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None
if "selected_actor_id" not in st.session_state:
    st.session_state.selected_actor_id = None
if "selected_actor_name" not in st.session_state:
    st.session_state.selected_actor_name = ""
if "favorites" not in st.session_state:
    st.session_state.favorites = {}

qp_view = st.query_params.get("view")
qp_id = st.query_params.get("id")
qp_actor_id = st.query_params.get("actor_id")
qp_actor_name = st.query_params.get("actor_name")

if qp_view in ("home", "details", "favorites", "actor"):
    st.session_state.view = qp_view
if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except:
        pass
if qp_actor_id:
    try:
        st.session_state.selected_actor_id = int(qp_actor_id)
        st.session_state.selected_actor_name = qp_actor_name or "Actor"
        st.session_state.view = "actor"
    except:
        pass


def goto_home():
    st.session_state.view = "home"
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()


def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()


# =============================
# API HELPERS
# =============================
@st.cache_data(ttl=30)  # short cache for autocomplete
def api_get_json(path: str, params: dict | None = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except Exception as e:
        return None, f"Request failed: {e}"


def poster_grid(cards, cols=6, key_prefix="grid"):
    if not cards:
        st.info("No movies to show.")
        return

    rows = (len(cards) + cols - 1) // cols
    idx = 0
    for r in range(rows):
        colset = st.columns(cols)
        for c in range(cols):
            if idx >= len(cards):
                break
            m = cards[idx]
            idx += 1

            tmdb_id = m.get("tmdb_id")
            title = m.get("title", "Untitled")
            poster = m.get("poster_url")

            with colset[c]:
                if poster:
                    st.image(poster, use_column_width=True)
                else:
                    st.write("🖼️ No poster")

                if st.button("✨ Open", key=f"{key_prefix}_{r}_{c}_{idx}_{tmdb_id}"):
                    if tmdb_id:
                        goto_details(tmdb_id)

                st.markdown(
                    f"<div class='movie-title'>{title}</div>", unsafe_allow_html=True
                )


def to_cards_from_tfidf_items(tfidf_items):
    cards = []
    for x in tfidf_items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append(
                {
                    "tmdb_id": tmdb["tmdb_id"],
                    "title": tmdb.get("title") or x.get("title") or "Untitled",
                    "poster_url": tmdb.get("poster_url"),
                }
            )
    return cards


# =============================
# IMPORTANT: Robust TMDB search parsing
# Supports BOTH API shapes:
# 1) raw TMDB: {"results":[{id,title,poster_path,...}]}
# 2) list cards: [{tmdb_id,title,poster_url,...}]
# =============================
def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24):
    """
    Returns:
      suggestions: list[(label, tmdb_id)]
      cards: list[{tmdb_id,title,poster_url}]
    """
    keyword_l = keyword.strip().lower()

    # A) If API returns dict with 'results'
    if isinstance(data, dict) and "results" in data:
        raw = data.get("results") or []
        raw_items = []
        for m in raw:
            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster_path = m.get("poster_path")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": f"{TMDB_IMG}{poster_path}" if poster_path else None,
                    "release_date": m.get("release_date", ""),
                }
            )

    # B) If API returns already as list
    elif isinstance(data, list):
        raw_items = []
        for m in data:
            # might be {tmdb_id,title,poster_url}
            tmdb_id = m.get("tmdb_id") or m.get("id")
            title = (m.get("title") or "").strip()
            poster_url = m.get("poster_url")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": poster_url,
                    "release_date": m.get("release_date", ""),
                }
            )
    else:
        return [], []

    # Word-match filtering (contains)
    matched = [x for x in raw_items if keyword_l in x["title"].lower()]

    # If nothing matched, fallback to raw list (so never blank)
    final_list = matched if matched else raw_items

    # Suggestions = top 10 labels
    suggestions = []
    for x in final_list[:10]:
        year = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))

    # Cards = top N
    cards = [
        {"tmdb_id": x["tmdb_id"], "title": x["title"], "poster_url": x["poster_url"]}
        for x in final_list[:limit]
    ]
    return suggestions, cards


# =============================
# SIDEBAR (clean)
# =============================
with st.sidebar:
    st.markdown("<div class='sidebar-title'>🎬 Navigation</div>", unsafe_allow_html=True)
    
    if st.button("🏠 Explore Home", use_container_width=True):
        goto_home()
    if st.button("⭐ My Favorites", use_container_width=True):
        st.session_state.view = "favorites"
        st.query_params["view"] = "favorites"
        st.rerun()

    st.markdown("<div class='sidebar-section'>Home Feed Settings</div>", unsafe_allow_html=True)
    home_category = st.selectbox(
        "Category",
        ["trending", "popular", "top_rated", "now_playing", "upcoming"],
        index=0,
    )
    
    # Hardcode grid columns to keep the layout consistent
    grid_cols = 6

# =============================
# HEADER
# =============================
st.markdown(
        """
        <div class='hero'>
            <div class='hero-title'>🎬 Movie Recommender</div>
            <div class='hero-sub'>Search any movie, explore rich details, and discover similar titles instantly.</div>
        </div>
        """,
    unsafe_allow_html=True,
)
st.caption("Type a keyword → pick a suggestion → open details → browse recommendations")
st.divider()

# ==========================================================
# VIEW: HOME
# ==========================================================
if st.session_state.view == "home":
    typed = st.text_input(
        "Search by movie title (keyword)", placeholder="Type: avenger, batman, love..."
    )

    st.divider()

    # SEARCH MODE (Autocomplete + word-match results)
    if typed.strip():
        if len(typed.strip()) < 2:
            st.caption("Type at least 2 characters for suggestions.")
        else:
            data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})

            if err or data is None:
                st.error(f"Search failed: {err}")
            else:
                suggestions, cards = parse_tmdb_search_to_cards(
                    data, typed.strip(), limit=24
                )

                # Dropdown
                if suggestions:
                    labels = ["-- Select a movie --"] + [s[0] for s in suggestions]
                    selected = st.selectbox("Suggestions", labels, index=0)

                    if selected != "-- Select a movie --":
                        # map label -> id
                        label_to_id = {s[0]: s[1] for s in suggestions}
                        goto_details(label_to_id[selected])
                else:
                    st.info("No suggestions found. Try another keyword.")

                st.markdown("### 🔎 Search Results")
                poster_grid(cards, cols=grid_cols, key_prefix="search_results")

        st.stop()

    # HOME FEED MODE
    st.markdown(f"### 🏠 Home — {home_category.replace('_',' ').title()}")

    home_cards, err = api_get_json(
        "/home", params={"category": home_category, "limit": 24}
    )
    if err or not home_cards:
        st.error(f"Home feed failed: {err or 'Unknown error'}")
        st.stop()

    poster_grid(home_cards, cols=grid_cols, key_prefix="home_feed")

# ==========================================================
# VIEW: DETAILS
# ==========================================================
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        st.warning("No movie selected.")
        if st.button("← Back to Home"):
            goto_home()
        st.stop()

    # Top bar
    a, b = st.columns([3, 1])
    with a:
        st.markdown("### 📄 Movie Details")
    with b:
        if st.button("← Back to Home"):
            goto_home()

    # Details (your FastAPI safe route)
    data, err = api_get_json(f"/movie/id/{tmdb_id}")
    if err or not data:
        st.error(f"Could not load details: {err or 'Unknown error'}")
        st.stop()

    title_str = data.get('title', '')
    poster_url = data.get('poster_url', '')

    # Toggle Fav logic
    is_fav = str(tmdb_id) in st.session_state.favorites
    fav_col1, fav_col2 = st.columns([4, 1])
    with fav_col2:
        if is_fav:
            if st.button("❌ Remove Fav", key="rfav", use_container_width=True):
                del st.session_state.favorites[str(tmdb_id)]
                st.rerun()
        else:
            if st.button("⭐ Add to Fav", key="afav", use_container_width=True):
                st.session_state.favorites[str(tmdb_id)] = {"title": title_str, "poster_url": poster_url}
                st.rerun()

    # Layout: Poster LEFT, Details RIGHT
    left, right = st.columns([1, 2.4], gap="large")

    with left:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        if data.get("poster_url"):
            st.image(data["poster_url"], use_column_width=True)
        else:
            st.write("🖼️ No poster")
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"## {data.get('title','')}")
        release = data.get("release_date") or "-"
        genres = ", ".join([g["name"] for g in data.get("genres", [])]) or "-"
        st.markdown(
            f"<div class='small-muted'>Release: {release}</div>", unsafe_allow_html=True
        )
        st.markdown(
            f"<div class='small-muted'>Genres: {genres}</div>", unsafe_allow_html=True
        )
        st.markdown("---")
        st.markdown("### Overview")
        st.write(data.get("overview") or "No overview available.")
        st.markdown("</div>", unsafe_allow_html=True)

    if data.get("backdrop_url"):
        st.markdown("#### Backdrop")
        st.image(data["backdrop_url"], use_column_width=True)

    # TRAILER
    trailer_id = data.get("trailer_youtube_id")
    if trailer_id:
        st.markdown("### 🍿 Official Trailer")
        st.video(f"https://www.youtube.com/watch?v={trailer_id}")
        
    # CAST
    cast_list = data.get("cast", [])
    if cast_list:
        st.markdown("### 🎭 Top Cast")
        import urllib.parse
        cast_html = "<div class='cast-container'>"
        for actor in cast_list:
            aid = actor.get("id") or 0
            img_url = actor.get("profile_url") or "https://via.placeholder.com/70x70.png?text=?"
            cname = actor.get("name") or "Unknown"
            safe_cname = urllib.parse.quote(cname)
            character = actor.get("character") or ""
            cast_html += f"<a href='?view=actor&actor_id={aid}&actor_name={safe_cname}' target='_self' style='text-decoration: none; color: inherit;'><div class='cast-card'><img src='{img_url}' class='cast-img'/><div class='cast-name'>{cname}</div><div class='cast-character'>{character}</div></div></a>"
        cast_html += "</div>"
        st.markdown(cast_html, unsafe_allow_html=True)

    st.divider()
    st.markdown("### ✅ Recommended Movies")

    # Recommendations (TF-IDF + Genre) via your bundle endpoint
    title = (data.get("title") or "").strip()
    if title:
        bundle, err2 = api_get_json(
            "/movie/search",
            params={
                "query": title,
                "tmdb_id": tmdb_id,
                "tfidf_top_n": 12,
                "genre_limit": 12,
            },
        )

        if not err2 and bundle:
            tfidf_cards = to_cards_from_tfidf_items(bundle.get("tfidf_recommendations"))
            genre_cards = bundle.get("genre_recommendations", [])
            
            # Combine and deduplicate
            seen = set()
            combined = []
            for c in tfidf_cards + genre_cards:
                tid = c.get("tmdb_id")
                if tid and tid not in seen:
                    seen.add(tid)
                    combined.append(c)
                    
            if not combined:
                st.info("No recommendations found.")
            else:
                poster_grid(combined, cols=grid_cols, key_prefix="details_recs")
        else:
            st.info("Loading fallback recommendations...")
            genre_only, err3 = api_get_json(
                "/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 18}
            )
            if not err3 and genre_only:
                poster_grid(
                    genre_only, cols=grid_cols, key_prefix="details_genre_fallback"
                )
            else:
                st.warning("No recommendations available right now.")
    else:
        st.warning("No title available to compute recommendations.")# VIEW: FAVORITES
elif st.session_state.view == 'favorites':
    st.markdown('### ⭐ My Favorites')
    st.caption('Movies you have liked will appear here.')
    
    favs = list(st.session_state.favorites.values())
    if not favs:
        st.info('You havent added any favorites yet!')
    else:
        fav_cards = [{'tmdb_id': int(k), 'title': v['title'], 'poster_url': v['poster_url']} for k,v in st.session_state.favorites.items()]
        poster_grid(fav_cards, cols=grid_cols, key_prefix='favs')


# ==========================================================
# VIEW: ACTOR
# ==========================================================
elif st.session_state.view == 'actor':
    actor_id = st.session_state.selected_actor_id
    actor_name = st.session_state.selected_actor_name
    
    a, b = st.columns([3, 1])
    with a:
        st.markdown(f"### 🌟 Starring: {actor_name}")
        st.caption("Top popular movies featuring this actor.")
    with b:
        if st.button("← Back to Home"):
            goto_home()
            
    if not actor_id:
        st.warning("No actor selected.")
        st.stop()
        
    actor_movies, err = api_get_json(f"/actor/{actor_id}/movies", params={"limit": 30})
    if err or not actor_movies:
        st.error(f"Could not load actor movies: {err or 'Unknown error'}")
        st.stop()
        
    poster_grid(actor_movies, cols=grid_cols, key_prefix="actor_feed")

