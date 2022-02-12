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


def list_int(array):
    lst = []
    for column in array:
        for row in column:
            for ele in row:
                lst.append(ele)
    return lst


def lst3d(int_lst, x, y, z):
    a_3d_list = []
    n = 0
    for i in range(x):
        a_3d_list.append([])
        for j in range(y):
            a_3d_list[i].append([])
            for k in range(z):
                a_3d_list[i][j].append(int_lst[n])
                n += 1
    return a_3d_list


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
    image_name = input("Enter image name(with extension): ")
    image = cv2.imread(image_name)
    data = input("Enter data to be encoded : ")
    if len(data) == 0:
        raise ValueError('Data is empty')
    filename = input("Enter the name of new encoded image(with extension): ")
    data += pin
    encoded_image = hide_data(image, bi_converter(data))
    cv2.imwrite(filename, encoded_image)


def decode_text():
    image_name = input(
        "Enter the name of the Encoded image that you want to decode (with extension) :")
    image = cv2.imread(image_name)
    text = show_data(image)
    return text


def encode_image():
    container_name = input("Enter image name(with extension): ")
    container_image = cv2.imread(container_name)
    image_hide_name = input("Enter image name you want to hide(with extension): ")
    image_hide = cv2.imread(image_hide_name)
    filename = input("Enter the name of new encoded image(with extension): ")
    x, y, z = [str(i) for i in image_hide.shape]
    if np.prod(image_hide.shape)*8 > np.prod(container_image.shape):
        OverflowError("Please input a bigger container image or a smaller image to hide")
    bi_str = bi_converter(list_int(image_hide)) + bi_converter(x+y+z+str(len(x))+str(len(y))+"sign")
    encoded_image = hide_data(container_image, bi_str)
    cv2.imwrite(filename, encoded_image)


def decode_image():
    image_name = input("Enter the name of the encrypted image that you want to decode (with extension) :")
    image = cv2.imread(image_name)
    lst, x_axis, y_axis, z_axis = show_data(image)
    array = np.array(lst3d(lst, x_axis, y_axis, z_axis), dtype=np.uint8)
    decoded_image_name = input("Enter the name you want decoded image to be saved as (with extension) :")
    cv2.imwrite(decoded_image_name, array)


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
