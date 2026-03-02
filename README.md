# Gestionnaire_de_fichiers_chiffres

Application de gestion de fichiers chiffrés permettant de chiffrer et déchiffrer des fichiers en utilisant **AES-256 en mode CBC** et d’assurer leur intégrité grâce à un **HMAC-SHA256**.

Les opérations cryptographiques sont exécutées dans un processus séparé afin d’améliorer la sécurité, l’isolation mémoire et la robustesse de l’application.

---

## 🔐 Fonctionnalités

- Génération de clés cryptographiques (256 bits)

- Stockage sécurisé des clés

- Chiffrement de fichiers (AES-256-CBC)

- Vérification d’intégrité avec HMAC-SHA256

- Déchiffrement sécurisé

- Nettoyage des clés en mémoire après utilisation

- Interface graphique (Tkinter)

---

## 🏗 Architecture

L’application est structurée en plusieurs composants :

- Interface (processus principal) : gestion de l’UI

- Processus enfant : exécution des opérations cryptographiques

- CryptoWorker : gestion du chiffrement/déchiffrement

- Stockage sécurisé des clés : via keyring

Cette séparation permet :

- Isolation mémoire

- Principe de moindre privilège

- Meilleure robustesse

- Interface plus réactive

---

## 🛠 Technologies utilisées

- Python 3.8+
- Tkinter
- cryptography
- keyring
- multiprocessing

---

## ▶️ Test & Installation
  1. **Télécharger le projet :**
  Télécharger le fichier ZIP depuis GitHub et extraire le dossier

  1. Installer Python >= 3.8.
  2. Ouvrir une invite de commande.
   3. Se déplacer dans le dossier racine du TP :
      ```sh
         cd <your_base_path>/file_encrypt
      ```
   4. Vérifier que Python est correctement installé et que vous avez une version adéquate :
      ```sh
      # Win:
      python --version
      # Unix:
      python3 --version
      ```
      > [!WARNING]
      > Si cette commande retourne une erreur, votre installation de python n'est pas correcte !
   5. Créer un environnement virtuel :
      ```sh
      # Unix:
      python3 -m venv .venv
      # Win:
      python -m venv .venv
      ```
   6. Activer l'environnement vituel :
      ```sh
      # Unix :
      source .venv/bin/activate
      # Win :
      .\.venv\Scripts\activate
      ```
   7. Mettre à jour ```pip``` :
      ```sh
      # Unix:
      python3 -m pip install --upgrade pip
      # Win:
      python -m pip install --upgrade pip
      ```
   8. Installer les dépendances :
      ```sh
      # Unix:
      pip3 install -r requirements.txt
      # Win:
      pip install -r requirements.txt
      ```
   9. Lancer l'application :
      ```sh
      # Unix:
      python3 src/app.py
      # Win:
      python src/app.py
      ```
