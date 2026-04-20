import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Immobilier Maroc",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_data
def load_data():
    df = pd.read_csv("data/clean/housing_clean.csv", encoding="utf-8-sig")
    df["prix_par_m2"] = (df["new_price"] / df["surface"]).round(0)
    df = df[df["new_price"] > 100_000]
    df = df[df["surface"].between(20, 1000)]
    df = df[df["prix_par_m2"] < 50_000]
    return df

df = load_data()

# ---- SIDEBAR ----
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/2/2c/Flag_of_Morocco.svg",
    width=80
)
st.sidebar.title("Filtres")
st.sidebar.markdown("---")

toutes_villes = sorted(df["City"].unique())
ville_choisie = st.sidebar.selectbox(
    "Ville",
    options=["Toutes les villes"] + toutes_villes,
    key="filtre_ville"
)

types = sorted(df["Type"].unique())
type_choisi = st.sidebar.selectbox(
    "Type de bien",
    options=["Tous les types"] + types,
    key="filtre_type"
)

chambres = sorted(df["chambres"].unique())
chambres_choisies = st.sidebar.selectbox(
    "Chambres",
    options=["Toutes"] + [str(int(c)) for c in chambres],
    key="filtre_chambres"
)

prix_min, prix_max = st.sidebar.slider(
    "Budget (DH)",
    min_value=int(df["new_price"].min()),
    max_value=int(df["new_price"].max()),
    value=(int(df["new_price"].min()), int(df["new_price"].quantile(0.95))),
    key="filtre_budget"
)

st.sidebar.markdown("---")
st.sidebar.markdown("Données : Kaggle — Maroc Immobilier")

# ---- APPLIQUER LES FILTRES ----
df_f = df.copy()

if ville_choisie != "Toutes les villes":
    df_f = df_f[df_f["City"] == ville_choisie]

if type_choisi != "Tous les types":
    df_f = df_f[df_f["Type"] == type_choisi]

if chambres_choisies != "Toutes":
    df_f = df_f[df_f["chambres"] == int(chambres_choisies)]

df_f = df_f[df_f["new_price"].between(prix_min, prix_max)]

# ---- EN-TÊTE ----
st.title("🏠 Marché Immobilier au Maroc")
st.markdown(f"Analyse de **{len(df_f):,}** annonces · **{ville_choisie}**")
st.markdown("---")

# ---- VÉRIFIER QUE LES DONNÉES NE SONT PAS VIDES ----
if len(df_f) == 0:
    st.warning("Aucune annonce trouvée pour ces filtres. Change les filtres !")

else:
    # ---- KPIs ----
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Annonces",        f"{len(df_f):,}")
    col2.metric("Prix médian",     f"{int(df_f['new_price'].median()):,} DH")
    col3.metric("Prix/m² moyen",   f"{int(df_f['prix_par_m2'].mean()):,} DH")
    col4.metric("Surface moyenne", f"{int(df_f['surface'].mean())} m²")
    col5.metric("Chambres moy.",   f"{df_f['chambres'].mean():.1f}")

    st.markdown("---")

    # ---- GRAPHIQUES LIGNE 1 ----
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Prix médian par ville")
        prix_ville = (
            df_f.groupby("City")["new_price"]
            .median()
            .reset_index()
            .sort_values("new_price", ascending=True)
        )
        fig1 = px.bar(
            prix_ville,
            x="new_price", y="City",
            orientation="h",
            color="new_price",
            color_continuous_scale="Teal",
            labels={"new_price": "Prix médian (DH)", "City": "Ville"},
            text=prix_ville["new_price"].apply(lambda x: f"{int(x):,} DH")
        )
        fig1.update_traces(textposition="outside")
        fig1.update_layout(
            showlegend=False,
            coloraxis_showscale=False,
            plot_bgcolor="white",
            margin=dict(l=0, r=20, t=20, b=0)
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        st.subheader("Prix au m² par ville")
        fig2 = px.box(
            df_f,
            x="City", y="prix_par_m2",
            color="City",
            color_discrete_sequence=px.colors.qualitative.Set2,
            labels={"prix_par_m2": "Prix/m² (DH)", "City": "Ville"}
        )
        fig2.update_layout(
            showlegend=False,
            plot_bgcolor="white",
            margin=dict(l=0, r=0, t=20, b=0)
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ---- GRAPHIQUES LIGNE 2 ----
    col_c, col_d = st.columns(2)

    with col_c:
        st.subheader("Surface vs Prix")
        fig3 = px.scatter(
            df_f,
            x="surface", y="new_price",
            color="City",
            size="chambres",
            hover_data=["Type", "chambres", "prix_par_m2"],
            labels={
                "surface": "Surface (m²)",
                "new_price": "Prix (DH)",
                "City": "Ville"
            },
            color_discrete_sequence=px.colors.qualitative.Set2,
            opacity=0.7
        )
        fig3.update_layout(
            plot_bgcolor="white",
            margin=dict(l=0, r=0, t=20, b=0)
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col_d:
        st.subheader("Répartition par type de bien")
        type_count = df_f["Type"].value_counts().reset_index()
        type_count.columns = ["Type", "Nombre"]
        fig4 = px.pie(
            type_count,
            values="Nombre",
            names="Type",
            color_discrete_sequence=px.colors.qualitative.Set2,
            hole=0.4
        )
        fig4.update_layout(margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig4, use_container_width=True)

    # ---- GRAPHIQUE LIGNE 3 ----
    st.subheader("Distribution des prix par ville")
    fig5 = px.violin(
        df_f,
        x="City", y="new_price",
        color="City",
        box=True,
        labels={"new_price": "Prix (DH)", "City": "Ville"},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig5.update_layout(
        showlegend=False,
        plot_bgcolor="white",
        margin=dict(l=0, r=0, t=20, b=0)
    )
    st.plotly_chart(fig5, use_container_width=True)

    # ---- TABLEAU ----
    st.markdown("---")
    st.subheader("Données détaillées")
    st.dataframe(
        df_f[[
            "City", "Type", "new_price", "surface",
            "prix_par_m2", "chambres", "salles de bains",
            "ascenseur", "parking", "terrasse"
        ]].sort_values("new_price", ascending=False),
        use_container_width=True,
        height=300
    )