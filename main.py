from api import fetch_data, fetch_species_data
import streamlit as st
import random

st.set_page_config(layout="wide")

st.header("Unsere Pokémon APP !")

st.write("Gib hier den Namen oder die ID ein und erhalte Infos über dein gewünschtes Pokémon!")


st.markdown(
    """
    <style>

    .stApp {
        background-color: #010a1c;
    }

    [data-testid="stSidebar"] {
        min-width: 300px !important;
        max-width: 300px !important;
        background-color: #02163d !important;
    }

    [data-testid="stSidebar"] .st-cq {
        color: #ecf0f1;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.header("Daten eingeben")

name = st.sidebar.text_input(
    "Schreib Pokémon Name oder ID", placeholder="Bulbasaur oder 1")

st.sidebar.caption(
    "⚠️ **Hinweis:** Bitte englische Namen verwenden (z.B. 'Pikachu', nicht 'Raupy')")

st.sidebar.markdown("------")
st.sidebar.subheader("🎲 Zufällige Pokémon")


random_ids=random.sample(range(1,899),3)

for poke_id in random_ids:

    try:
        poke_data=fetch_data(str(poke_id))
        poke_name=poke_data['name'].capitalize()
        poke_sprite=poke_data['sprites']['front_default']

        if poke_sprite:
            st.sidebar.image(poke_sprite)   
        st.sidebar.markdown(f"**{poke_name}**")

    except Exception: 
        continue




if name:
    result = fetch_data(name)
    species_data = fetch_species_data(name)

    if "error" in result:
        st.error(result["error"])

        with st.container():
            col1, col2 = st.columns([3, 1])

            if result.get("error_code") == 404:
                with col1:
                    st.markdown("**Mögliche Lösungen:**")
                    st.markdown("- Tippfehler überprüfen")
                    st.markdown("- Groß-/Kleinschreibung beachten")
                    st.markdown("- Pokémon-ID statt Name versuchen")
                    st.markdown(
                        "- [Offizielle Pokémon-Liste](https://www.pokemon.com/de/pokedex/)")

                with col2:
                    st.markdown("**Fehlerdetails:**")
                    st.caption(
                        f"Fehlercode: {result.get('error_code', 'N/A')}")
                    st.caption(f"Eingabe: '{name}'")

    else:
        col1, col2 = st.columns([1, 3])

        with col1:
            st.subheader(result['name'].capitalize())

            official_art = result['sprites']['other']['official-artwork']['front_default']

            image_url = official_art if official_art else result['sprites']['front_default']

            st.image(
                image_url,
                width=200
            )

            st.subheader("Charakteristik:")

            for entry in species_data.get("flavor_text_entries", []):
                if entry["language"]["name"] == "en":
                    st.text(entry["flavor_text"])
                    break

        with col2:
            st.subheader("Basisinformationen")

            m_col1, m_col2, m_col3 = st.columns(3)

            with m_col1:
                st.metric("Gewicht", f"{result['weight']/10} kg")
                st.caption(
                    "Gewicht in Kilogramm (API liefert Daten in Hectogramm)")

            with m_col2:
                st.metric("Größe", f"{result['height']/10} m")
                st.caption(
                    "Größe in Kilogramm (API liefert Daten in Dezimetr)")

            with m_col3:
                st.metric("ID", f"#{result['id']}")

            st.divider()

            st.subheader("Fähigkeiten")
            abilities = [ability['ability']['name'].capitalize()
                         for ability in result['abilities']]
            st.write(", ".join(abilities))

            st.divider()

            st.subheader("Statistiken")
            for stat in result['stats']:
                stat_name = stat['stat']['name'].replace("-", " ").capitalize()
                base_stat = stat['base_stat']

                # Normalize stat value to 0-100 scale
                max_stat_value = 255  # Max possible base stat in Pokémon games
                percentage = int((base_stat / max_stat_value) * 100)

                st.progress(
                    min(percentage, 100),  # Ensure never exceeds 100%
                    text=f"{stat_name}: {base_stat} ({percentage}%)"
                )
