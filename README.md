# Image Encryption Project

# Description

This project is a simple implementation of AES (Advanced Encryption Standard) encryption and decryption for images. It allows you to encrypt an image into an unreadable binary format and later decrypt it back into the original image. It’s a great demonstration of how cryptography can secure image data.
# How to Use  Prerequisites

`Python 3.x installed on your system.`

# Running the Program

1. Clone the repository or download the script file.
```
git clone <repository_url>
cd <repository_directory>
```
2. Install the required libraries.
```
pip install pycryptodome pillow numpy
```
3. Run the script using Python.
```
python imageencryption.py
```
Program Menu
When you run the script, you will see a menu with the following options:

1) Encrypts an image file (example.jpg) into a binary file (encrypted_image.bin).

2) Decrypts the binary file back into its original image (decrypted_image.jpg).


# Example Usage
# Encrypting an Image:
- Place your input image in the project folder (e.g., example.jpg).
- Run the script, and the encrypted image will be saved as a binary file:
- Encrypted File: encrypted_image.bin
# Decrypting an Image:
- The script reads the binary file (encrypted_image.bin) and reconstructs the original image:
- Decrypted File: decrypted_image.jpg
  - `Output Image`
    
  ![Profile](https://github.com/user-attachments/assets/3c5686eb-d1da-4395-9185-89f5f655f089)

# File
- `imageencryption.py`  
  ```python
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

  ```

# Code Overview

1) `Encrypt Function`
   - Converts the image into byte data.
   - Encrypts the data using AES encryption in EAX mode.
2) `Decrypt Function`
   - Reads the encrypted binary file.
   - Decrypts it to reconstruct the original image.

3) `Main Program Loop`
   - Handles encryption, decryption, and file saving.

# License
This project is licensed under the MIT License - see the LICENSE file for details.

# Acknowledgments
This project demonstrates a basic implementation of AES encryption for images. It's an excellent way to learn about cryptography and image processing.
# Author 
`Umar Farooq`
