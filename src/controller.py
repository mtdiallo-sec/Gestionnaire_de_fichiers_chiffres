import os
import tkinter as tk

from tkinter import filedialog, messagebox
from view_utils import ViewUtils
from services import WorkerRunner


class AppController:
    """
    Contrôleur de l'application Tkinter pour la gestion des fichiers chiffrés.

    Cette classe encapsule toute la logique métier liée à l'interface utilisateur.
    Elle interagit avec WorkerRunner pour les opérations cryptographiques et
    met à jour l'interface via l'objet Tkinter app.
    """
    def __init__(self, app: tk.Tk) -> None:
        """
        Initialise le contrôleur avec l'instance Tkinter de l'application.

        Paramètres
        ----------
        app : tk.Tk
            Instance de l'application Tkinter à contrôler.
        """
        self.app = app

    def check_key_status(self) -> None:
        """
        Vérifie l'existence d'une clé AES+HMAC dans le stockage sécurisé.

        Met à jour l'interface utilisateur en fonction du résultat :
            - Affiche un message de statut
            - Active/désactive les boutons de chiffrement/déchiffrement
            - Active/désactive le bouton de génération de clé
        """
        result = WorkerRunner.run("crypto_worker", "check")

        if result.get("exists"):
            self.app.key_status_label.config(
                text="Clé disponible dans le stockage sécurisé", fg="green"
            )

            self.app.generate_button.config(state="disabled")
            self.app.set_crypto_buttons(True)
        else:
            self.app.key_status_label.config(
                text="Aucune clé trouvée. Générer une nouvelle clé !", fg="red"
            )

            self.app.generate_button.config(state="normal")
            self.app.set_crypto_buttons(False)

    def generate_key(self) -> None:
        """
        Génère une nouvelle clé AES+HMAC.

        Après la génération :
            - Vérifie le statut de la clé
            - Met à jour l'interface utilisateur
            - Affiche un message d'information ou d'erreur selon le résultat
        """
        if WorkerRunner.run("crypto_worker", "generate"):
            self.check_key_status()

            messagebox.showinfo(
                "Succès",
                "Clé générée et sauvegardée dans le stockage sécurisé."
            )
        else:
            messagebox.showerror("Erreur", "Impossible de générer une clé.")

    def encrypt_file(self) -> None:
        """
        Lance le processus de chiffrement d'un fichier sélectionné par l'utilisateur.

        Étapes :
            1. Demande à l'utilisateur de sélectionner un fichier à chiffrer.
            2. Vérifie que le fichier n'est pas déjà chiffré (.dcrypt).
            3. Demande à l'utilisateur le chemin de sortie.
            4. Appelle WorkerRunner pour chiffrer le fichier.
            5. Affiche un message d'erreur ou enregistre l'opération dans le log.
        """
        input_file = filedialog.askopenfilename(title="Sélectionner un fichier à chiffrer")

        if not input_file:
            return

        if input_file.lower().endswith(".dcrypt"):
            messagebox.showerror("Erreur", "Le fichier a déjà été chiffré.")
            return

        output_file = filedialog.asksaveasfilename(
            title="Enregistrer le fichier chiffré",
            initialfile=os.path.basename(input_file) + ".dcrypt"
        )

        if not output_file:
            return

        if WorkerRunner.run("crypto_worker", "encrypt", input_file, output_file):
            ViewUtils.log_message(self.app.log_list, f"Chiffrement : {output_file}")
        else:
            messagebox.showerror("Erreur", "Impossible de chiffrer le fichier")

    def decrypt_file(self) -> None:
        """
        Lance le processus de déchiffrement d'un fichier sélectionné par l'utilisateur.

        Étapes :
            1. Demande à l'utilisateur de sélectionner un fichier chiffré (.dcrypt).
            2. Propose un nom de fichier de sortie par défaut.
            3. Appelle WorkerRunner pour déchiffrer le fichier.
            4. Affiche un message d'erreur ou enregistre l'opération dans le log.
        """
        input_file = filedialog.askopenfilename(
            title="Sélectionner un fichier à déchiffrer",
            filetypes=[("Fichiers chiffrés", "*.dcrypt")]
        )

        if not input_file:
            return

        default_name = os.path.basename(input_file).replace(".dcrypt", "")

        output_file = filedialog.asksaveasfilename(
            title="Enregistrer le fichier déchiffré",
            initialfile=default_name
        )

        if not output_file:
            return

        if WorkerRunner.run("crypto_worker", "decrypt", input_file, output_file):
            ViewUtils.log_message(self.app.log_list, f"Déchiffrement : {output_file}")
        else:
            messagebox.showerror("Erreur", "Impossible de déchiffrer le fichier")
