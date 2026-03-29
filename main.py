from os.path import join as join

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

from prepro import (  # import de TON fichier prpro.py
    preprocessing_modele1,
    preprocessing_modele2,
    split,
)

# ============================================================
# 1) Chargement des données
# ============================================================
df = pd.read_csv(join("data", "fichier-de-donnees-mixtes-6920344a2a6cd267411281.csv"))


# ============================================================
# 2) 🔵 Modèle SANS preprocessing (preprocessign minimal)
# ============================================================


# --- Nettoyage minimal pour modèle brut
df_raw = df.copy()

# Colonnes inutilisables (strings non numériques)
colonnes_categorical = [
    "nom",
    "prenom",
    "date_creation_compte",
    "sexe",
    "sport_licence",
    "niveau_etude",
    "region",
    "smoker",
    "nationalité_francaise",
    "situation_familiale",
    "historique_credits",
    "risque_personnel",
]

df_raw = df_raw.drop(columns=colonnes_categorical)

# Suppression des lignes avec valeurs manquantes
df_raw = df_raw.dropna()


# Séparation X / y
X_raw = df_raw.drop(columns=["montant_pret"])
y_raw = df_raw["montant_pret"]

# Split identique
X_train_raw, X_test_raw, y_train_raw, y_test_raw = split(X_raw, y_raw)

# Modèle brut
model_raw = RandomForestRegressor(random_state=42)
model_raw.fit(X_train_raw, y_train_raw)
pred_raw = model_raw.predict(X_test_raw)

mae_raw = mean_absolute_error(y_test_raw, pred_raw)
r2_raw = r2_score(y_test_raw, pred_raw)
score_raw = model_raw.score(X_test_raw, y_test_raw)

print("----------------------------------------------------")
print(
    "🔵 RÉSULTATS SANS PREPROCESSING (uniquement: supression des données nulles et non numeriques)"
)
print(f"MAE : {mae_raw:.2f}")
print(f"Coefficient de determination R²  : {r2_raw:.4f}")
print(f"Score (R²) sans preprocessing : {score_raw:.4f}")

# ============================================================
# 3) 🟢 Modèle AVEC preprocessing model 1 (via fonction)
# ============================================================

X_processed, y_processed, preprocessor = preprocessing_modele1(df)

# Split identique
X_train_prep, X_test_prep, y_train_prep, y_test_prep = split(X_processed, y_processed)

# Modèle prétraité
model_prep = RandomForestRegressor(random_state=42)
model_prep.fit(X_train_prep, y_train_prep)
pred_prep = model_prep.predict(X_test_prep)

mae_prep = mean_absolute_error(y_test_prep, pred_prep)
r2_prep = r2_score(y_test_prep, pred_prep)
score_prep = model_prep.score(X_test_prep, y_test_prep)

print("----------------------------------------------------")
print("🟢 RÉSULTATS AVEC PREPROCESSING MODELE 1")
print(f"MAE : {mae_prep:.2f}")
print(f"Coefficient de determination R²  : {r2_prep:.4f}")
print(f"Score (R²) avec preprocessing : {score_prep:.4f}")

# ============================================================
# 4) 🟢 Modèle AVEC preprocessing modele 2 (via fonction)
# ============================================================

X_processed2, y_processed2, preprocessor2 = preprocessing_modele2(df)

# Split identique
X_train_prep2, X_test_prep2, y_train_prep2, y_test_prep2 = split(
    X_processed2, y_processed2
)

# Modèle prétraité

model_prep2 = LinearRegression()
# penalty="l2", alpha=0.0001, max_iter=2000, random_state=42)

model_prep2.fit(X_train_prep2, y_train_prep2)

pred_prep2 = model_prep2.predict(X_test_prep2)

mae_prep2 = mean_absolute_error(y_test_prep2, pred_prep2)
r2_prep2 = r2_score(y_test_prep2, pred_prep2)
score_prep2 = model_prep2.score(X_test_prep2, y_test_prep2)


print("----------------------------------------------------")
print("🟢 RÉSULTATS AVEC PREPROCESSING MODELE 2")
print(f"MAE : {mae_prep2:.2f}")
print(f"Coefficient de determination R²  : {r2_prep2:.4f}")
print(f"Score (R²) avec preprocessing : {score_prep2:.4f}")


# ============================================================
# 5) ✅ Comparaison finale
# ============================================================

print("=====================================================")
print("✅ COMPARAISON (Brut vs Prétraité)")
print(f"MAE brut         : {mae_raw:.2f}")
print(f"MAE preprocess. 1: {mae_prep:.2f}")
print(f"MAE preprocess. 2: {mae_prep2:.2f}")
print("")
print(f"R² brut          : {r2_raw:.4f}")
print(f"R² preprocess.  1: {r2_prep:.4f}")
print(f"R² preprocess.  2: {r2_prep2:.4f}")
print("=====================================================")
