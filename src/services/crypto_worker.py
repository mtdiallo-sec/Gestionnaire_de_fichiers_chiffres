import os
import keyring
import argparse
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes, hmac

####
#
# Ajouter les imports manquants pour compléter le TP.
# Il s'agit de classes de la librairie cryptography.
# Vous n'avez rien à installer de plus. Tout devrait déjà
# être fait si vous avez réalisé correctement les étapes
# de configuration du TP (voir README.md)
#
# Exemple :
# from cryptography.hazmat.<...> import <...>
#
####

####
# Constantes pour keyring
# Vous ne devez pas modifier ces valeurs.
####
SERVICE_NAME = "UQAC-8INF333"
ACCOUNT_NAME = "TP1-APP"


class CryptoWorker:
    """
    Classe de gestion des opérations cryptographiques.

    Consigne générale : compléter les fonctions
    marquées d'un "TODO" sans utiliser de dépendances
    supplémentaires en vous aidant des "docstrings".
    """
    def __init__(self) -> None:
        self.aes_key = None
        self.hmac_key = None

    def _clean_memory(self) -> None:

        if self.aes_key is not None:
            for i in range(len(self.aes_key)):
                self.aes_key[i] = 0
        
        if self.hmac_key is not None:
            for i in range(len(self.hmac_key)):
                self.hmac_key[i] = 0
        
        #liberation des references
        self.aes_key = None
        self.hmac_key = None

        print("DEBUG: Nettoyage mémoire (fonction à implémenter pour le TP)")


    def _load_keys(self) -> None:

        #Recuperation des cles depuis le stockage securisé
        cles_recupere = keyring.get_password(SERVICE_NAME, ACCOUNT_NAME)

        if not cles_recupere:
            raise RuntimeError("Aucune cle n'est trouvee dans le stockage securise")
        
        aes_hexa, hmac_hexa = cles_recupere.split(":")

        #Conversion des cles en tableau d'octets
        self.aes_key = bytearray.fromhex(aes_hexa)
        self.hmac_key = bytearray.fromhex(hmac_hexa)

        print("DEBUG: Chargement des clés (fonction à implémenter pour le TP)")


    def check_key(self):

        #Recuperation des cles aes et hmac depuis le stockage securisé
        cles_recupere = keyring.get_password(SERVICE_NAME, ACCOUNT_NAME)

        #Verification
        is_key = cles_recupere is not None
 
        print(json.dumps({"exists": bool(is_key)}))


    def generate_key(self) -> None:

        #Generation des cles de 256 bits (32 octets) en tableau d'octets
        self.aes_key = bytearray(os.urandom(32))
        self.hmac_key = bytearray(os.urandom(32))

        #Conversion des cles en hexadecimal
        aes_hexa = self.aes_key.hex()
        hmac_hexa = self.hmac_key.hex()

        cles = f"{aes_hexa}:{hmac_hexa}"

        #Stockage des cles dans le stockage securisé
        keyring.set_password(SERVICE_NAME, ACCOUNT_NAME, cles)
        
        print("DEBUG: Génération de clé (fonction à implémenter pour le TP)")


    def encrypt(self, input_path: str, output_path: str) -> None:

        #Chargement des clés
        self._load_keys()

        #Lecture du fichier à chiffrer
        with open(input_path, "rb") as fichier:
            donnees = fichier.read()

        #Application du padding PKCS#7 (block AES = 16 octets = 128 bits)
        appliquer_pad = padding.PKCS7(128).padder()
        donnees_padder = appliquer_pad.update(donnees) + appliquer_pad.finalize()

        #Generation de l'IV aleatoirement - Il doit être sur 16 octets
        IV = os.urandom(16)

        #Chiffrement avec AES-256-CBC
        chiffrement = Cipher(
            algorithms.AES(self.aes_key),
            modes.CBC(IV)
        )

        chiffreur = chiffrement.encryptor()
        donnees_chiffrees = chiffreur.update(donnees_padder) + chiffreur.finalize()

        #Calcul du HMAC sur IV + ciphertext
        hmac_cal = hmac.HMAC(self.hmac_key, hashes.SHA256())
        hmac_cal.update(IV + donnees_chiffrees)
        signature = hmac_cal.finalize()

        #Écrirure IV + ciphertext + HMAC dans le fichier de sortie
        with open(output_path, "wb") as fichier:
            fichier.write(IV + donnees_chiffrees + signature)

        #Nettoyage de la memoire
        self._clean_memory()

        print(f"DEBUG: Chiffrement de {input_path} vers {output_path} (fonction à implémenter pour le TP)")


    def decrypt(self, input_path: str, output_path: str) -> None:

        #Chargement des cles
        self._load_keys()

        #Lecture du fichier chiffré
        with open(input_path, "rb") as fichier:
            contenu = fichier.read()

        #Verification de la validité du fichier (taille minimale)
        #on verifie si la taille minimale du fichier > taille IV (16) + taille HMAC (32)
        if len(contenu) < 16 + 32:
            raise RuntimeError("Fichier invalide")
        
        #Decoupage des donnnes 
        IV = contenu[:16] #Vecteur d'initialisation
        signature = contenu[-32:] #Signature HMAC
        donnees_chiffrees = contenu[16:-32] #Données chiffrées

        #Verification du HMAC
        hmac_verif = hmac.HMAC(self.hmac_key, hashes.SHA256())
        hmac_verif.update(IV + donnees_chiffrees)

        try:
            hmac_verif.verify(signature)
        except Exception:
            raise RuntimeError("HMAC invalide - fichier corrompu ou modifie")
        
        #Déchiffrement avec AES-256-CBC
        dechiffrement = Cipher(
            algorithms.AES(self.aes_key),
            modes.CBC(IV)
        )

        dechiffreur = dechiffrement.decryptor()
        donnees_padder = dechiffreur.update(donnees_chiffrees) + dechiffreur.finalize()

        #Depadding avec PKCS#7
        depadder = padding.PKCS7(128).unpadder()
        donnees = depadder.update(donnees_padder) + depadder.finalize()

        #Écriture des données déchiffrée dans le fichier de sortie
        with open(output_path, "wb") as fichier:
            fichier.write(donnees)

        #Nettoyage de la memoire
        self._clean_memory()

        print(f"DEBUG: Déchiffrement de {input_path} vers {output_path} (fonction à implémenter pour le TP)")


def main() -> None:
    """
    Point d'entrée CLI du worker.

    Utilise argparse pour gérer les opérations :
    - check: vérifier existence clé
    - generate: générer clé AES/HMAC
    - encrypt: chiffrer un fichier
    - decrypt: déchiffrer un fichier

    Vous n'avez pas à modifier cette fonction.
    """

    parser = argparse.ArgumentParser(
        description="Worker des opérations cryptographiques"
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-c", "--check", action="store_true")
    group.add_argument("-g", "--generate", action="store_true")
    group.add_argument("-e", "--encrypt", action="store_true")
    group.add_argument("-d", "--decrypt", action="store_true")

    parser.add_argument("--input", "-i", type=str)
    parser.add_argument("--output", "-o", type=str)

    args = parser.parse_args()

    worker = CryptoWorker()

    if args.check:
        if args.input or args.output:
            parser.error("Les paramètres input et output ne sont pas requis")
        worker.check_key()

    elif args.generate:
        if args.input or args.output:
            parser.error("Les paramètres input et output ne sont pas requis")
        worker.generate_key()

    elif args.encrypt:
        if not args.input or not args.output:
            parser.error("Les paramètres input et output sont requis")
        worker.encrypt(args.input, args.output)

    elif args.decrypt:
        if not args.input or not args.output:
            parser.error("Les paramètres input et output sont requis")
        worker.decrypt(args.input, args.output)


if __name__ == "__main__":
    main()
