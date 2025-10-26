import random
import os
import time

# Nettoyer le terminal
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


# Couleurs ASCII pour le terminal
class Colors:
    VERT = '\033[92m'
    ORANGE = '\033[93m'
    ROUGE = '\033[91m'
    RESET = '\033[0m'

def color_feedback(symbol):
    if symbol == '*':
        return Colors.VERT + '*' + Colors.RESET
    elif symbol == '!':
        return Colors.ORANGE + '!' + Colors.RESET
    else:
        return Colors.ROUGE + '-' + Colors.RESET



# Fonction pour afficher le tableau
def creation_tableau_mastermind(secret, code_devine,\
combi_du_joueur, nombre_utilisee, reveal=False):
    for val in secret:
        if reveal:
            print("\t" + str(val)[:3], end="")
        else:
            print("\tUNK", end="")
    print("\n")

    for index_row in reversed(range(len(code_devine))):
        print("-----------------------------------------")
        print(" ".join(color_feedback(sym)\
        for sym in combi_du_joueur[index_row]), end=" | ")

        for val in code_devine[index_row]:
            print("\t" + str(val)[:3], end="")
        print()
    print("-----------------------------------------\n")



    # Rappel des couleurs ou chiffres
    if nombre_utilisee:
        print("Rappel : chiffres de 0 à 9")
    else:
        couleurs_base = ["ROUGE", "VERT", "JAUNE", "BLEU", "NOIR", "ORANGE"]
        print("Rappel des couleurs : ", " | ".join\
              (f"{i+1}-{c}" for i, c in enumerate(couleurs_base)))
    print()



def jouer_mastermind():
    couleurs_base = ["ROUGE", "VERT", "JAUNE", "BLEU", "NOIR", "ORANGE"]
    couleurs_map = {i+1: c for i, c in enumerate(couleurs_base)}

    # Choix du mode
    while True:
        mode = input("Veux-tu deviner avec des chiffres (0-9) \
        (1) ou avec des couleurs (2) ? ").strip()

        if mode.upper() == "STOP":
            print("Partie interrompue. \
            N'hésite pas à relancer avec 'python .\main.py' !")
            return
        
        if mode in ('1','2'):
            break
        print("Réponse invalide. \
              Tape 1 pour chiffres ou 2 pour couleurs.")

    nombre_utilisee = mode == '1'
    longueur_code = 4
    vies = 10

    # Creation du mdp
    if nombre_utilisee:
        secret = [random.randint(0,9) for _ in range(longueur_code)]
    else:
        random.shuffle(couleurs_base)
        secret = couleurs_base[:longueur_code]

    code_devine = [['-'] * longueur_code for _ in range(vies)]
    combi_du_joueur = [['-'] * longueur_code for _ in range(vies)]
    tour = 0

    while tour < vies:
        print("\n\t\tM A S T E R    M I N D")
        print(f"Tour {tour+1}/{vies}")
        print()
        print()
        creation_tableau_mastermind(secret, code_devine,\
                                    combi_du_joueur, nombre_utilisee)

        try:
            valeur_joueur = input("Entre ta combinaison \
                                  (ou STOP pour quitter) : ").strip()
            if valeur_joueur.upper() == "STOP":
                print("Partie interrompue. \
                N'hésite pas à relancer avec 'python .\main.py' !")
                return

            if nombre_utilisee:
                if " " in valeur_joueur:
                    code = list(map(int, valeur_joueur.split()))
                else:
                    code = [int(ch) for ch in valeur_joueur]
                if len(code) != longueur_code or \
                    any(ch < 0 or ch > 9 for ch in code):
                    raise ValueError
            else: #Si espace
                if " " in valeur_joueur:
                    inputs = valeur_joueur.upper().split()
                else:
                    inputs = list(valeur_joueur)

                if len(inputs) != longueur_code:
                    raise ValueError

                code = []
                for item in inputs:
                    if item.isdigit():
                        chiffre = int(item)
                        if chiffre < 1 or chiffre > 6:
                            raise ValueError
                        code.append(couleurs_map[chiffre])
                    else:
                        item = item.upper()
                        if item not in couleurs_base:
                            raise ValueError
                        code.append(item)

        except ValueError:
            clear()
            print("\tAïe... Ce n’est pas bon. Essaie encore !")
            time.sleep(1.5)
            continue

        # Stocker la combinaison + victoire
        code_devine[tour] = code.copy()
        combi_du_joueur[tour] = ['-'] * longueur_code

        for idx in range(longueur_code):
            if code[idx] == secret[idx]:
                combi_du_joueur[tour][idx] = '*'

        for idx in range(longueur_code):
            if combi_du_joueur[tour][idx] == '-':
                val = code[idx]
                bonne_place_count = sum(1 for i in range(longueur_code) \
                    if secret[i]==val and combi_du_joueur[tour][i]=='*')
                total_count = secret.count(val)
                if bonne_place_count < total_count:
                    combi_du_joueur[tour][idx] = '!'

        if code_devine[tour] == secret:
            clear()
            creation_tableau_mastermind(secret, code_devine, \
                    combi_du_joueur, nombre_utilisee, reveal=True)
            print("Félicitations !! Tu as trouvé la combinaison mon champion!")
            break

        tour += 1
        clear()

    if tour == vies:
        clear()
        creation_tableau_mastermind(secret, code_devine, \
                    combi_du_joueur, nombre_utilisee, reveal=True)
        print(f"BOUHH, PERDU !! La réponse était : {secret}")



# pour rejouer
while True:
    jouer_mastermind()
    print()
    rejouer = input("Veux-tu rejouer ? (o/n) : ").strip().lower()
    if rejouer != 'o':
        print("Merci d'avoir joué loulou !")
        break
    clear()
