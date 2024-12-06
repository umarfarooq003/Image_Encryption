from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from PIL import Image
import numpy as np

def image_to_bytes(image_path):
    with Image.open(image_path) as img:
        img = img.convert("RGB")  # Ensure it's in RGB format
        data = np.array(img)
        return data.tobytes(), img.size

def encrypt_image(data, key):
    cipher = AES.new(key, AES.MODE_EAX)  # EAX mode provides confidentiality and integrity
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return cipher.nonce, ciphertext, tag

def save_encrypted_image(filepath, nonce, ciphertext, tag):
    with open(filepath, 'wb') as file:
        file.write(nonce + ciphertext + tag)

def decrypt_image(filepath, key, size):
    with open(filepath, 'rb') as file:
        nonce = file.read(16)  # First 16 bytes are the nonce
        file_content = file.read()  # Read the rest of the file
        tag = file_content[-16:]  # Last 16 bytes are the tag
        ciphertext = file_content[:-16]  # Remaining bytes are the ciphertext

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)

    # Reconstruct the image from bytes
    array = np.frombuffer(data, dtype=np.uint8).reshape(size[1], size[0], 3)
    return Image.fromarray(array)

def main():
    image_path = "Profile.jpg"
    encrypted_path = "encrypted_image.bin"
    decrypted_path = "decrypted_image.jpg"
    key = get_random_bytes(16)  # AES requires a 16-byte key

    # Encrypt the image
    print("Encrypting the image...")
    data, size = image_to_bytes(image_path)
    nonce, ciphertext, tag = encrypt_image(data, key)
    save_encrypted_image(encrypted_path, nonce, ciphertext, tag)
    print(f"Encrypted image saved to {encrypted_path}")

    # Decrypt the image
    print("Decrypting the image...")
    decrypted_image = decrypt_image(encrypted_path, key, size)
    decrypted_image.save(decrypted_path)
    print(f"Decrypted image saved to {decrypted_path}")

if __name__ == "__main__":
    main()
