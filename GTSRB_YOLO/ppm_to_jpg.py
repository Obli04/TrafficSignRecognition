import os
import cv2

# === PARAMETRI ===
# Directory con le immagini PPM (per train e validation)
TRAIN_PATH = '/home/xpiomba00/GTSRB/GTSRB_YOLO/train/images'
VAL_PATH = '/home/xpiomba00/GTSRB/GTSRB_YOLO/val/images'

def convert_ppm_to_jpg_and_remove(image_dir):
    """
    Converte tutte le immagini .ppm in .jpg e rimuove i file .ppm originali.
    Le dimensioni delle immagini rimangono invariate per mantenere valide le annotazioni YOLO.
    """
    for root, _, files in os.walk(image_dir):
        for file in files:
            if file.endswith('.ppm'):
                file_path = os.path.join(root, file)  # Percorso completo dell'immagine .ppm
                new_file_path = os.path.splitext(file_path)[0] + '.jpg'  # Percorso del nuovo file .jpg

                try:
                    # Leggi l'immagine in formato BGR (OpenCV usa BGR invece di RGB)
                    img = cv2.imread(file_path)
                    
                    if img is None:
                        print(f"? Impossibile leggere {file_path}")
                        continue

                    # Salva l'immagine come .jpg senza ridimensionare
                    cv2.imwrite(new_file_path, img)
                    print(f"? Immagine convertita: {file_path} ? {new_file_path}")
                    
                    # Elimina il file .ppm originale
                    os.remove(file_path)
                    print(f"??? File originale .ppm rimosso: {file_path}")
                    
                except Exception as e:
                    print(f"? Errore durante la conversione di {file_path}: {e}")

if __name__ == "__main__":
    print("?? Conversione immagini .ppm in .jpg nella directory TRAIN...")
    convert_ppm_to_jpg_and_remove(TRAIN_PATH)
    
    print("\n?? Conversione immagini .ppm in .jpg nella directory VAL...")
    convert_ppm_to_jpg_and_remove(VAL_PATH)

    print("\n? Conversione completata per tutte le immagini .ppm in TRAIN e VAL!")