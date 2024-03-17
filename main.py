import threading
import requests

class DownloadThread(threading.Thread):
    def __init__(self, url, filename):
        threading.Thread.__init__(self)
        self.url = url
        self.filename = filename

    def run(self):
        response = requests.get(self.url)
        with open(self.filename, 'w') as file:
            file.write(response.text)

class DecryptThread(threading.Thread):
    def __init__(self, filename, decrypted_data):
        threading.Thread.__init__(self)
        self.filename = filename
        self.decrypted_data = decrypted_data

    def run(self):
        with open(self.filename, 'r') as file:
            encrypted_text = file.read()
        decrypted_text = self.caesar_decrypt(encrypted_text, 8)
        self.decrypted_data[self.filename] = decrypted_text

    @staticmethod
    def caesar_decrypt(text, shift):
        decrypted = ''
        for char in text:
            if char.isalpha():
                offset = 65 if char.isupper() else 97
                decrypted += chr((ord(char) - offset - shift) % 26 + offset)
            else:
                decrypted += char
        return decrypted

class Combiner:
    def __init__(self, decrypted_data):
        self.decrypted_data = decrypted_data

    def combine_and_save(self):
        sorted_filenames = sorted(self.decrypted_data.keys())
        with open('s_final.txt', 'w') as final_file:
            for filename in sorted_filenames:
                final_file.write(self.decrypted_data[filename] + '\n')
                final_file.write('\n')

if __name__ == "__main__":
    # Step 1: Instantiate DownloadThread
    download_threads = [
        DownloadThread("https://advancedpython.000webhostapp.com/s1.txt", "s1_enc.txt"),
        DownloadThread("https://advancedpython.000webhostapp.com/s2.txt", "s2_enc.txt"),
        DownloadThread("https://advancedpython.000webhostapp.com/s3.txt", "s3_enc.txt")
    ]

    # Step 2: Start and join each DownloadThread
    for thread in download_threads:
        thread.start()
    for thread in download_threads:
        thread.join()

    # Step 3: Instantiate DecryptThread
    decrypted_data = {}
    decrypt_threads = [
        DecryptThread("s1_enc.txt", decrypted_data),
        DecryptThread("s2_enc.txt", decrypted_data),
        DecryptThread("s3_enc.txt", decrypted_data)
    ]

    # Step 4: Start and join each DecryptThread
    for thread in decrypt_threads:
        thread.start()
    for thread in decrypt_threads:
        thread.join()

    # Step 5: Instantiate Combiner
    combiner = Combiner(decrypted_data)
    combiner.combine_and_save()

    # Step 6: Display the content of the s_final.txt file
    with open("s_final.txt", "r") as file:
        content = file.read()
        print(content)


