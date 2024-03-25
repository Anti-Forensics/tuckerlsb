import argparse

from PIL import Image


class TuckerLsb:
    """
    Implements steganography using the Least Significant Bit (LSB) method.

    This class provides functionality to hide a text message within the pixels of an image and to reveal a hidden
    message from an image. It uses the LSB of the pixel values to embed the message bits.

    Attributes:
    - input_image (str): Path to the input image.
    - output_image (str): Path to the output image with the message hidden in it.
    - message (str): The message to hide within the image.
    - delimeter (str): A delimiter to signify the end of the hidden message.
    """

    def __init__(self, input_image: str, output_image: str, message: str) -> None:
        """
        Initializes the TuckerLsb instance with the input image, output image, and the message to be hidden.

        Parameters:
        - input_image (str): The path to the input image file.
        - output_image (str): The path where the output image will be saved.
        - message (str): The text message to be hidden within the image.
        """
        self.input_image = input_image
        self.output_image = output_image
        self.message = message
        self.delimeter = '1111111111111110'

    def text_to_binary(self, message: str) -> str:
        """
        Converts a text message into a binary string.

        Each character of the input message is converted into its ASCII binary representation. The binary strings
        for all characters are concatenated to form a single binary string.

        Parameters:
        - message (str): The text message to convert to binary.

        Returns:
        - str: A binary string representation of the input text message.
        """
        binary_string = ''
        for char in message:
            binary_char = format(ord(char), '08b')
            binary_string += binary_char

        return binary_string

    def hide_message(self) -> None:
        """
        Hides the message within the input image using LSB steganography and saves the modified image.

        The method embeds the binary representation of the message into the least significant bits of the pixels
        in the input image. The modified image is then saved to the output image path.
        """
        image = Image.open(self.input_image)
        binary_message = self.text_to_binary(self.message) + self.delimeter
        pixels = image.load()
        message_index = 0

        for row in range(image.size[0]):
            for column in range(image.size[1]):
                if message_index < len(binary_message):
                    pixel = list(pixels[row, column])

                    bit_to_write = int(binary_message[message_index])
                    pixel[0] = (pixel[0] & ~1) | bit_to_write

                    pixels[column, row] = tuple(pixel)
                    message_index += 1
                else:
                    break
            else:
                continue
            break

        print(f'[+] Saving image to: {self.output_image}')
        image.save(self.output_image)

    def binary_to_text(self, binary_message: str) -> str:
        """
        Converts a binary string back into its textual representation.

        The binary string is divided into segments of 8 bits, each representing a single character. These segments
        are converted back to text.

        Parameters:
        - binary_message (str): The binary string to convert back to text.

        Returns:
        - str: The textual representation of the binary string.
        """
        text = ''
        for i in range(0, len(binary_message), 8):
            byte = binary_message[i:i + 8]
            text += chr(int(byte, 2))

        return text

    def reveal_message(self, input_image: str) -> str:
        """
        Reveals and returns the hidden message from the output image.

        This method scans the output image to extract the binary string hidden in the least significant bits of
        the pixels, converts it to text, and returns the text.

        Returns:
        - str: The hidden text message retrieved from the image. If no message is found or an error occurs,
          "ERROR" is returned.
        """
        image = Image.open(input_image)
        pixels = image.load()

        binary_message = ''

        for row in range(image.size[0]):
            for column in range(image.size[1]):
                pixel = pixels[column, row]
                least_significant_bit = pixel[0] & 1
                binary_message += str(least_significant_bit)

                if binary_message.endswith(self.delimeter):
                    binary_message = binary_message[:-16]  # Remove the delimiter
                    return self.binary_to_text(binary_message)

        return "ERROR"


def main():
    parser = argparse.ArgumentParser(description="Steganography with LSB (Least Significant Bit)")
    parser.add_argument('--input', '-i', required=True, type=str,
                        default=None, dest='input_image',
                        help='Specify the input image.')
    parser.add_argument('--output', '-o', required=False, type=str,
                        default=None, dest='output_image',
                        help='Specify the output image that will contain embedded message (c:\test\test.png).')
    parser.add_argument('--message', '-m', required=False, type=str,
                        default=None, dest='user_message')
    parser.add_argument('--getmessage', '-g', required=False, action="store_true",
                        help='Get a message. Use -i to provide the input file to extract the message from.')

    args = parser.parse_args()

    tucker = TuckerLsb(args.input_image, args.output_image, args.user_message)

    if args.getmessage:
        print(tucker.reveal_message(args.input_image))
    else:
        tucker.hide_message()


if __name__ == "__main__":
    main()
