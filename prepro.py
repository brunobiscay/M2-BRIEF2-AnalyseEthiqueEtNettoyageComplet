"""
PREPROCESSING

    ENCODAGE
        LabelEncoder: Encode target labels with value between 0 and n_classes-1.
            ex: ne traite qu'une colonne, qu'une variable
            inverse_transform permet de decoder

            Le codage des étiquettes est utile lorsque les données catégorielles ont une relation ordinale inhérente, ce qui signifie que les catégories ont un ordre ou un classement significatif.
                Niveau d'éducation      Codage des étiquettes
                École secondaire        0
                Licence                 1
                Maîtrise                2
                PhD                     3
        OrdinalEncoder: comme labelencoder mais multi variables
        LabelBinarizer: Binarize labels in a one-vs-all fashion.
            ex: on crée autant de colonne que de variables (on evite les comparaisons), cela crée des 0 et 1 ->matrices clairsemées(sparse matrix), légères à utiliser
        OneHotEncoder()
                                Color_Blue   Color_Green  Color_Red
                        0           0            0          1
                        1           0            1          0
                        2           1            0          0
                        3           0            0          1
            Pour la ligne 2 il renvoie [[1. 0. 0.]]
            ! Attention, cela peut générer bcp de nouvelles dimensions, qu'on cherchera à reduire avec l'analyse en composantes principales (ACP)

        MultiLabelBinarizer: Transform between iterable of iterables and a multilabel format

    NORMAliSATION
        KernelCenterer: Center an arbitrary kernel matrix
        MaxAbsScaler: Scale each feature by its maximum absolute value.
        MinMaxScaler:  	Transform features by scaling each feature to a given range.
            Sensible aux outliers (données aberrantes)
        Normalizer: Normalize samples individually to unit norm.
            Normalise les lignes mais pas les colonnes
        RobustScaler: Scale features using statistics that are robust to outliers.
        StandardScaler:  Standardize features by removing the mean and scaling to unit variance.
                Sensible aux outliers (données aberrantes)

    CREATION DE POLYNOMES
        PolynomialFeatures :  Generate polynomial and interaction features.
            ex: si une regression lineaire fonctionne mal, en creant une nouvelle variaible "polynomiale on peut avoir une courbe plus proche (fonction avec des ², feature engineering)

    TRANSFORMATION non lineaire
        PowerTransformer: Apply a power transform featurewise to make data more Gaussian-like.
        QuantileTransformer: Transform features using quantiles information.


    DISCRETISATION
        Binarizer: Binarize data (set feature values to 0 or 1) according to a threshold.
            ex: valeurs de 1 à 25. Totuce qui est < 18 on met 0, si >18 on met 1
        KBinsDiscretizer: Bin continuous data into intervals.
            ex: meme que au dessus mais en plus de 2 categories

    SKLEARN
            la methode fit(): permet de developper une fonction de transformation en analysant les données du train_set
            la methode transform(): permet d'appliquer cette fonction de transformation à toutes les données qu'on lui fourni (trains_set, test_set ou future)
            fit_transform(): combine les 2

            (X,y)   --> (Xtrain, Ytrain) -> [transformer / fit_transform()] -> (Xtrain, Ytrain) ->  [estimator/ fit()]
                    |_> (Xtest, Ytest)   -> [transformer / transform()] -> (Xtest, Ytest) ->  [estimator/ predict()] -> Ypred

            Xtest   -> [transformer + estimator] -> Ypred
            Xtest   -> pipeline -> Ypred
"""

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, RobustScaler


def split(X, y, test_size=0.20, random_state=42):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    return X_train, X_test, y_train, y_test


def preprocessing_modele1(df):
    """
    Fonction pour effectuer le prétraitement des données :
    - Imputation des valeurs manquantes.
    - Standardisation des variables numériques.
    - Encodage des variables catégorielles.
    """
    numerical_cols = [
        "age",
        "taille",
        "poids",
        "revenu_estime_mois",
        "score_credit",
        "loyer_mensuel",
    ]
    categorical_cols = [
        "sexe",
        "niveau_etude",
        "region",
        "nationalité_francaise",
        "smoker",
        "sport_licence",
        "situation_familiale",
        "historique_credits",
        "risque_personnel",
    ]

    # Valeurs manquantes gérées par SimpleImputer, on remplace par la moyenne ('mean', 'median', pour le numerique  'most_frequent' ou 'constant' pour categorie)
    # On normalise avec RobustScaler (moins bon que standardscaler si proche d'une distribution normale)
    num_pipeline = Pipeline(
        [("imputer", SimpleImputer(strategy="mean")), ("scaler", RobustScaler())]
    )

    # si on trouve des categories inconnues non presentes lors de l'apprentissage, on les ignore
    cat_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )

    preprocessor = ColumnTransformer(
        [("num", num_pipeline, numerical_cols), ("cat", cat_pipeline, categorical_cols)]
    )

    # Prétraitement
    X = df.drop(
        columns=[
            "nom",
            "prenom",
            "montant_pret",
        ]
    )
    y = df["montant_pret"]

    X_processed = preprocessor.fit_transform(X)
    """
    a)fit(X) : Calcule les vecteurs propres (eigenvectors) de la matrice de covariance de X en utilisant la décomposition en valeurs propres.
    Après avoir ajusté le PCA avec pca.fit(X), vous pouvez récupérer ces vecteurs propres via pca.components_.
    b)transform(X) : Convertit les données d’entrée depuis l’espace vectoriel initial vers l’espace vectoriel du PCA — c’est‑à‑dire l’espace défini par les vecteurs propres obtenus via l’algorithme PCA.
    Les données transformées sont généralement appelées composantes principales (PCs).
    c)fit_transform(X) : Combine les deux étapes : d’abord le calcul des vecteurs propres, puis la projection des données sur ceux‑ci.
    
    Scikit-learn's terminology: eigenvectors = components_
    """

    return X_processed, y, preprocessor


"""Modele 2 avec plus de suppression de colones que Modele 1"""


def preprocessing_modele2(df):
    """
    Fonction pour effectuer le prétraitement des données :
    - Imputation des valeurs manquantes.
    - Standardisation des variables numériques.
    - Encodage des variables catégorielles.
    """
    numerical_cols = [
        "age",
        "taille",
        "poids",
        "revenu_estime_mois",
        "score_credit",
        "loyer_mensuel",
    ]
    categorical_cols = [
        "sexe",
        "niveau_etude",
        "region",
        "nationalité_francaise",
        "smoker",
        "sport_licence",
        "situation_familiale",
        "historique_credits",
        "risque_personnel",
        "montant_pret",
    ]

    # Valeurs manquantes gérées par SimpleImputer, on remplace par la moyenne ('mean', 'median', pour le numerique  'most_frequent' ou 'constant' pour categorie)
    # On normalise avec RobustScaler (moins bon que standardscaler si proche d'une distribution normale)
    num_pipeline = Pipeline(
        [("imputer", SimpleImputer(strategy="mean")), ("scaler", RobustScaler())]
    )

    # si on trouve des categories inconnues non presentes lors de l'apprentissage, on les ignore
    cat_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )

    preprocessor = ColumnTransformer(
        [("num", num_pipeline, numerical_cols), ("cat", cat_pipeline, categorical_cols)]
    )

    # Prétraitement
    X = df.drop(
        columns=[
            "nom",
            "prenom",
        ]
    )
    y = df["montant_pret"]

    X_processed = preprocessor.fit_transform(X)

    return X_processed, y, preprocessor
