import cv2
import numpy as np


def bi_converter(message):
    if type(message) == str:
        return ''.join([format(ord(i), "08b") for i in message])
    elif type(message) == bytes or type(message) == np.ndarray:
        return [format(i, "08b") for i in message]
    elif type(message) == int or type(message) == np.uint8:
        return format(message, "08b")
    elif type(message) == list:
        return ''.join([format(i, "08b") for i in message])
    else:
        raise TypeError("Input type not supported")


def hide_data(image, bi_msg):
    data_index = 0
    a = len(bi_msg)
    for values in image:
        for pixel in values:
            r, g, b = bi_converter(pixel)
            if data_index < a:
                pixel[0] = int(r[:-1] + bi_msg[data_index], 2)
                data_index += 1
            if data_index < a:
                pixel[1] = int(g[:-1] + bi_msg[data_index], 2)
                data_index += 1
            if data_index < a:
                pixel[2] = int(b[:-1] + bi_msg[data_index], 2)
                data_index += 1
            if data_index >= a:
                break

    return image


def list1d(array):
    lst = []
    [lst.append(ele) for column in array for row in column for ele in row]
    return lst


def array3d(lst, x, y, z):
    n = iter(lst)
    return np.array([[[next(n) for k in range(z)] for j in range(y)] for i in range(x)], dtype=np.uint8)


def show_data(image):
    binary_data = ""
    for values in image:
        for pixel in values:
            r, g, b = bi_converter(pixel)
            binary_data += r[-1]
            binary_data += g[-1]
            binary_data += b[-1]
    all_bytes = [binary_data[i: i + 8] for i in range(0, len(binary_data), 8)]
    if pin == "0000":
        decoded_data = []
        for byte in all_bytes:
            decoded_data.append(int(byte, 2))
            if decoded_data[-4:] == [115, 105, 103, 110]:
                break
        len_x, len_y = int(chr(decoded_data[-6])), int(chr(decoded_data[-5]))
        length = ''.join([format(chr(i)) for i in decoded_data[-7-len_y-len_x:-7-len_y]])
        width = ''.join([format(chr(i)) for i in decoded_data[-7-len_y:-7]])
        height = chr(decoded_data[-7])
        return decoded_data[:-7-len_y-len_x], int(length), int(width), int(height)

    else:
        decoded_data = ""
        for byte in all_bytes:
            decoded_data += chr(int(byte, 2))
            if decoded_data[-4:] == pin:
                break
        if decoded_data[-4:] != pin:
            raise ValueError("Error the pin was incorrect")

        return decoded_data[:-4]


def encode_text():
    image = cv2.imread(input("Enter image name(with extension): "))
    cv2.imwrite(input("Enter the name of new encoded image(with extension): "), hide_data(image, bi_converter(input("Enter data to be encoded : ")+pin)))


def decode_text():
    image = cv2.imread(input("Enter the name of the Encoded image that you want to decode (with extension) :"))
    return show_data(image)


def encode_image():
    container_image = cv2.imread(input("Enter image name(with extension): "))
    image_hide = cv2.imread(input("Enter image name you want to hide(with extension): "))
    if np.prod(image_hide.shape)*8 > np.prod(container_image.shape):
        raise OverflowError("Please input a bigger container image or a smaller image to hide")
    x, y, z = [str(i) for i in image_hide.shape]
    bi_str = bi_converter(list1d(image_hide)) + bi_converter(x+y+z+str(len(x))+str(len(y))+"sign")
    cv2.imwrite(input("Enter the name of new encoded image(with extension): "), hide_data(container_image, bi_str))


def decode_image():
    image_name = input("Enter the name of the encrypted image that you want to decode (with extension) :")
    image = cv2.imread(image_name)
    lst, x_axis, y_axis, z_axis = show_data(image)
    cv2.imwrite(input("Enter the name you want decoded image to be saved as (with extension) :"), array3d(lst, x_axis, y_axis, z_axis))


def steganography():
    if pin == "0000":
        a = int(input("Image Steganography\n 1. Encode Image\n 2. Decode Image\n Your input is: "))
        if a == 1:
            print("\nEncoding....")
            encode_image()
        elif a == 2:
            print("\nDecoding....")
            decode_image()
        else:
            raise Exception("Enter correct input")
    else:
        a = int(input("Image Steganography\n 1. Encode text\n 2. Decode text\n Your input is: "))
        if a == 1:
            print("\nEncoding....")
            encode_text()
        elif a == 2:
            print("\nDecoding....")
            print("Decoded message is: " + decode_text())
        else:
            raise Exception("Enter correct input")


pin = input("please input the security pin (0000 for image encryption mode):")
steganography()
