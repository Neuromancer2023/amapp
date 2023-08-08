import streamlit as st
import pandas as pd
import numpy as np
from babel.numbers import format_currency
import locale

# Configuration de Streamlit
st.set_page_config(layout="wide")

# Configuration de la locale pour les montants en euros
locale.setlocale(locale.LC_ALL, 'fr_FR.utf8')

# Fonction de formatage pour les montants en euros
def format_currency_custom(value):
    if pd.notna(value):
        try:
            numeric_value = float(value)
            return f"{numeric_value:,.2f} €".replace(",", " ").replace(".", ",").replace(" ", " ")
        except ValueError:
            return value
    else:
        return ""

# Champ de texte pour le login
login = st.sidebar.text_input("Entrez votre login:")

# Menu dans la barre latérale avec "Disponibles" comme option par défaut
option = st.sidebar.selectbox(
    'Choisissez une page:',
    ('Articles Extraordinaires', 'Articles Ordinaires', 'Bon de commande', 'Modification budgétaire', 'Budget', 'Conseiller RGPD'),
    index=1  # L'index de l'option par défaut (0-based)
)

# Fonction pour formater les montants en euros avec espace comme séparateur de milliers
def format_currency_fr(value):
    return locale.currency(value, symbol=True, grouping=True)

# Fonction pour formater les pourcentages
def format_percentage(value):
    return f"{value:.2%}" if not pd.isna(value) else ""

# Fonction pour afficher les données disponibles
def afficher_disponibles(sheet):
    # Lit le fichier Excel
    file_path = "Y:/Taxes-Finances/MEUNIER Fred 2023/plateforme/data.xlsx"
    df = pd.read_excel(file_path, sheet_name=sheet)

    formatted_columns = [2020, 2021, 2022, 2023, 'engagements', 'quart', 'disponible']
    for col in formatted_columns:
        df[col] = df[col].apply(lambda x: format_currency_fr(x) if not pd.isna(x) else "")

    df['util'] = df['util'].apply(format_percentage)  # Appliquer le format de pourcentage à la colonne 'util'

    st.title('Disponibles')
    st.dataframe(df)
def afficher_extra(sheet):
    st.title("SERVICE EXTRAORDINAIRE")
    st.title("Programmes d'investissement et voies et moyens de financement")
    file_path = 'Y:/Taxes-Finances/MEUNIER Fred 2023/plateforme/TABLEAU DES VOIES ET MOYENS.xlsx'
    df = pd.read_excel(file_path, engine='openpyxl')

    # Remplacer les valeurs numpy.nan et 'nan' par des cellules vides
    df = df.replace([np.nan, 'nan'], "")

    # Formater les colonnes "Dépenses" et autres en euros monétaires
    cols_to_format = ['Dépenses', 'Empts commune', 'Empts état./R.W.', 'Subsides', 'Sinistre', 'Fonds Réserves']
    df[cols_to_format] = df[cols_to_format].applymap(format_currency_custom)

    # Afficher la table
    st.table(df)

# Dictionnaire pour mapper les logins aux onglets
login_mapping = {
    "didier": "env",
    "superjojo": "ht",
    # ... autres logins
}

# Vérifie si le login est dans le dictionnaire
if login in login_mapping:
    sheet = login_mapping[login]

    if option == 'Bon de commande':
        st.write("Contenu de la page Bon de commande.")
    elif option == 'Articles Extraordinaires':
        afficher_extra(sheet)
    elif option == 'Articles Ordinaires':
        afficher_disponibles(sheet)
    elif option == 'Modification budgétaire':
        st.write("Contenu de la page Modification budgétaire.")
    elif option == 'Budget':
        st.write("Contenu de la page Budget.")
    elif option == 'Conseiller RGPD':
        st.write("Posez votre question RGPD.")
else:
    st.warning("Login incorrect. Veuillez réessayer.")