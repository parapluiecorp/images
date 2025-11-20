from PIL import Image
import argparse


def resize_image(input_path, output_path, factor):
    """
    Redimensionne une image d'entrée en divisant sa largeur et sa hauteur par le facteur donné.
    
    Args:
        input_path (str): Chemin vers le fichier image à redimensionner.
        output_path (str): Chemin pour enregistrer l'image redimensionnée.
        factor (int): Le facteur de réduction de la taille (doit être > 0).
    """
    
    try:
        img = Image.open(input_path)
        
        new_width = img.width // factor
        new_height = img.height // factor
        
        img = img.resize((new_width, new_height))
        img.save(output_path, optimize=True)
        print(f"Image redimensionnée et enregistrée à : {output_path}")

    except FileNotFoundError:
        print(f"FICHIER INTROUVABLE: '{input_path}'")
    except ZeroDivisionError:
        print("Erreur: Le facteur ne peut pas être zéro.")
    except Exception as e:
        print(f"UNE ERREUR S'EST PRODUITE: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Réduit la taille de votre image d'entrée par FACTOR fois."
    )
    
    parser.add_argument(
        "input_path", 
        type=str, 
        help="Le chemin vers l'image que vous voulez modifier (ex: image.png)."
    )
    parser.add_argument(
        "output_path", 
        type=str, 
        help="Chemin de sortie pour l'image redimensionnée."
    )
    parser.add_argument(
        "factor", 
        type=int, 
        help="Le facteur par lequel diviser la largeur et la hauteur (doit être un entier positif)."
    )
    
    args = parser.parse_args()
    
    resize_image(args.input_path, args.output_path, args.factor)
