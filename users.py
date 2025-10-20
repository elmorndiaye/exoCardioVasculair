import streamlit as st
import pandas as pd
import pickle

# ============================
# Chargement du modèle
# ============================
with open("random_forest_model.pkl", "rb") as f:
    model = pickle.load(f)

# ============================
# Barre de navigation avec st.radio
# ============================
selected = st.radio("Navigation", ["Prédiction", "Informations"], index=0, horizontal=True)

# ============================
# PAGE 1 : Prédiction
# ============================
if selected == "Prédiction":
    st.title("🩺 Prédiction du risque de maladie cardiovasculaire")
    st.write("Remplissez le formulaire ci-dessous pour estimer votre risque et recevoir des conseils.")

    with st.form("prediction_form"):
        age = st.number_input("Âge", min_value=1, max_value=120, value=30)
        gender_str = st.selectbox("Genre", ["Homme", "Femme"])
        gender = 1 if gender_str == "Homme" else 2

        height = st.number_input("Taille (cm)", 50, 250, 170)
        weight = st.number_input("Poids (kg)", 20, 300, 70)
        ap_hi = st.number_input("Pression artérielle haute", 80, 250, 120)
        ap_lo = st.number_input("Pression artérielle basse", 50, 200, 80)

        cholesterol = {"Normal":1,"Élevé":2,"Très élevé":3}[st.selectbox("Cholestérol", ["Normal","Élevé","Très élevé"])]
        gluc = {"Normal":1,"Élevé":2,"Très élevé":3}[st.selectbox("Glucose", ["Normal","Élevé","Très élevé"])]

        smoke = 0 if st.selectbox("Fumeur", ["Non","Oui"])=="Non" else 1
        alco = 0 if st.selectbox("Consommation d'alcool", ["Non","Oui"])=="Non" else 1
        active = 0 if st.selectbox("Physiquement actif", ["Non","Oui"])=="Non" else 1

        submitted = st.form_submit_button("🔍 Lancer la prédiction")

    if submitted:
        input_data = pd.DataFrame({
            'age':[age],'gender':[gender],'height':[height],'weight':[weight],
            'ap_hi':[ap_hi],'ap_lo':[ap_lo],'cholesterol':[cholesterol],
            'gluc':[gluc],'smoke':[smoke],'alco':[alco],'active':[active]
        })

        # Prédiction
        prediction = model.predict(input_data)[0]
        proba = model.predict_proba(input_data)[0]

        if prediction == 1:
            st.warning(f"⚠️ Risque élevé détecté (probabilité : {proba[1]*100:.1f}%)")
            conseils = [
                "Réduire la consommation d’alcool et arrêter de fumer.",
                "Faire au moins 30 min d’exercice physique par jour.",
                "Surveiller régulièrement la tension et le cholestérol.",
                "Avoir une alimentation équilibrée, pauvre en graisses saturées."
            ]
        else:
            st.success(f"✅ Aucun risque détecté (probabilité : {proba[0]*100:.1f}%)")
            conseils = [
                "Maintenir un mode de vie sain.",
                "Continuer l’activité physique régulière.",
                "Surveiller votre alimentation et vos habitudes.",
                "Faire des bilans de santé périodiques."
            ]

        st.subheader("🧠 Conseils :")
        for c in conseils:
            st.write(f"- {c}")

# ============================
# PAGE 2 : Informations
# ============================
else:
    st.title("ℹ️ Informations sur les maladies cardiovasculaires")
    st.markdown("""
    ### 💔 Qu’est-ce qu’une maladie cardiovasculaire ?
    Les maladies cardiovasculaires regroupent les troubles du cœur et des vaisseaux sanguins.
    Elles résultent souvent de l’accumulation de graisses dans les artères, provoquant une obstruction.

    ### ⚠️ Facteurs de risque :
    - Pression artérielle élevée
    - Cholestérol ou glucose élevés
    - Tabac, alcool
    - Manque d’activité physique
    - Obésité ou âge avancé

    ### 💪 Prévention :
    - Faire de l’exercice régulièrement
    - Avoir une alimentation équilibrée
    - Éviter le tabac et limiter l’alcool
    - Contrôler régulièrement sa tension artérielle
    """)
