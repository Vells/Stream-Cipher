"""
Author: Vela Dimitrova Mineva
Date: 02/20/2015
"""
import random
import sys


class Cipher(object):
    """
    A Cipher class that, given a passcode, can encrypt or decrypt a text
    """

    ACTIONS = ['--encrypt', '--decrypt']

    def __init__(self, passcode):
        self.passcode = passcode

    def perform_action(self, action, filename):
        """
        A function that given an action, calls the appropriate Cipher function
        or displays a message if the requested action is not available
        :param action: type(action) is a string with len(action) > 0
        :param filename: type(filename) is a string; len(filename) > 0
        :return: None
        """
        if action == self.ACTIONS[0]:
            encrypted_text = self.encrypt(filename)
            sys.stdout.write(encrypted_text)
        elif action == self.ACTIONS[1]:
            decrypted_text = self.decrypt(filename)
            sys.stdout.write(decrypted_text)
        else:
            sys.stdout.write("Action {0} not available!".format(action))
        sys.stdout.write("\n")

    @staticmethod
    def get_content(filename):
        """
        A method that given a filename returns the content of the file.
        If the file is not successfully opened, a message is printed and
        the program is terminated.
        :param filename: type(filename) is a string; len(filename) > 0
        :return type(cleartext) is a string
        """
        try:
            with open(filename) as file:
                cleartext = file.read()
                return cleartext
        except IOError:
            sys.stdout.write("Could not open file!\n")
            sys.exit(0)

    def get_stream_cipher(self, length):
        """
        A method that given a length, generates a list of random numbers
        with that length and returns it.
        :param length: type(length) is int, length > 0
        :return: type(stream_cipher) is a list
        """
        stream_cipher = []
        random.seed(self.passcode)
        while length > len(stream_cipher):
            stream_cipher.append(random.randrange(256))
        return stream_cipher

    @staticmethod
    def display_invalid_ciphertext_message():
        """
        A static method that displays an error message when
        the provided ciphertext is not in valid format.
        :param: None
        :return: None
        """
        sys.stdout.write("Error! Invalid format of the provided ciphertext!\n"
                         "Ciphertext must be a sequence of integers separated by commas!\n")

    def parse_ciphertext(self, ciphertext):
        """
        A method that converts the provided ciphertext as a string into a list
        of integers and returns it. If the operation fails, a message is displayed
        and the program is terminated.
        :param ciphertext: type(ciphertext) is string, len(ciphertext) > 0
        :return: type(parsed_cipher) is a list of integers
        """
        parsed_ciphertext = filter(lambda x: x, ciphertext.split(","))
        parsed_cipher = []
        for item in parsed_ciphertext:
            try:
                parsed_cipher.append(int(item))
            except ValueError:
                self.display_invalid_ciphertext_message()
                sys.exit(0)
        return parsed_cipher

    def encrypt(self, filename):
        """
        A method that given a filename, encrypts the content of the file
        and writes it to standard output
        :param filename: type(filename) is a string; len(filename) > 0
        :return:
        """
        cleartext = self.get_content(filename)
        stream_cipher = self.get_stream_cipher(len(cleartext))
        ciphertext = ""

        for index, letter in enumerate(cleartext):
            code = ord(letter) ^ stream_cipher[index]
            ciphertext += str(code) + ", "

        return ciphertext[:len(ciphertext)-2]

    def decrypt(self, filename):
        """
        A method that given a filename, decrypts the content of the file
        and writes it to standard output.
        :param filename: type(filename) is a string; len(filename) > 0
        :return:
        """
        ciphertext = self.get_content(filename)
        parsed_cipher = self.parse_ciphertext(ciphertext)
        stream_cipher = self.get_stream_cipher(len(parsed_cipher))
        decrypted_text = ""

        for index, code in enumerate(parsed_cipher):
            letter = chr(code ^ stream_cipher[index])
            decrypted_text += letter

        return decrypted_text