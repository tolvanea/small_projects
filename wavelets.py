# Minimal working example of image compression with wavelets.
# Compression works by dropping frecuencies that are near zero.
# This is not based on any course or assignment on university, just curiosity.
# Coded this while drunk, no quality assurances. Do whatever you want with it.

# I scimmed following sources to get some grasp what wavelets are
# https://pywavelets.readthedocs.io/en/latest/index.html
# https://dsp.stackexchange.com/questions/10675/difference-between-a-wavelet-transform-and-a-wavelet-decomposition
# https://mil.ufl.edu/nechyba/www/eel6562/course_materials/t5.wavelets/intro_dwt.pdf

# Documentation of 2d-wavelets with PyWavelets
# https://pywavelets.readthedocs.io/en/latest/ref/2d-dwt-and-idwt.html#ref-dwt2


import numpy as np
import matplotlib.pyplot as plt

import pywt  # pip3 install PyWavelets
import pywt.data

# Some source said that bior2.6 mother wavelet is the best for compression
wavelet = 'bior2.6'

def compress_image(image, crop_data_fraction=0.15):
    # Compress black and white image with wavelets

    def reduce_to_fraction_of_indices(matrix_2d, crop_to_fraction):
        # Drop those wave packet indices that are near to zero.
        # max image resolution is 65 535 due to the uint16
        flat = matrix_2d.flatten()
        ids_of_sorted = np.argsort(flat)
        l = int(len(ids_of_sorted) * (crop_data_fraction / 2))
        low_bound = flat[ids_of_sorted[l]]
        high_bound = flat[ids_of_sorted[-l]]
        nonzero_wavelets = np.logical_or(
            flat > high_bound,
            flat < low_bound
        )
        bitpack = np.packbits(nonzero_wavelets)
        values = flat[nonzero_wavelets].astype(np.float16)
        return (bitpack, values, matrix_2d.shape)

    compression_size = 0
    coeffs = pywt.wavedec2(image, wavelet)
    packed_coeffs = [coeffs[0]]
    compression_size += size(coeffs[0])
    # i iterates through pixel frequencies with power of 2
    for i in range(1, len(coeffs)):
        hori, vert, diag = coeffs[i]
        hori_pack = reduce_to_fraction_of_indices(hori, crop_data_fraction)
        vert_pack = reduce_to_fraction_of_indices(vert, crop_data_fraction)
        diag_pack = reduce_to_fraction_of_indices(diag, crop_data_fraction)
        packed_coeffs.append((hori_pack, vert_pack, diag_pack))

        compression_size += 3*(size(hori_pack[0]) + size(hori_pack[1] + 16))
    return (packed_coeffs, image.shape), compression_size

def decompress_image(pack):
    # Decompress black and white image with wavelets
    def construct_from_indices(pack):
        bitpack, values, shape = pack
        flat = np.zeros(shape[0]*shape[1])
        nonzero_wavelets = np.unpackbits(bitpack, count=len(flat))
        flat[np.nonzero(nonzero_wavelets)] = values
        mat = np.reshape(flat, shape)
        return mat

    packed_coeffs, shape = pack
    coeffs = [packed_coeffs[0]]

    # i iterates through pixel frequencies with power of 2
    for i in range(1, len(packed_coeffs)):
        hori_pack, vert_pack, diag_pack = packed_coeffs[i]
        hori = construct_from_indices(hori_pack)
        vert = construct_from_indices(vert_pack)
        diag = construct_from_indices(diag_pack)
        coeffs.append((hori, vert, diag))

    constructed_image = pywt.waverec2(coeffs, wavelet)
    constructed_image = np.clip(constructed_image, 0, 255)
    return constructed_image


def size(arr):
    return arr.size * arr.itemsize

def main():
    # Load image
    original = pywt.data.camera()

    # Lower values of crop_data_fraction means greater compression
    pack, size_compress = compress_image(original, crop_data_fraction=0.15)
    print(
        "Original size {:.1f}, ".format(size(original)/1024),
        "Compressed size {:.1f}".format(size_compress/1024))
    decomp = decompress_image(pack)

    fig = plt.figure(figsize=(6, 5))
    fig.suptitle("Dropping wavelets below weakest 85% presentile")

    h,l,s = 210, 100, 64

    plots = [
        ("Original, {:.1f} kB".format(size(original)/1024), original),
        ("Compressed, {:.1f} kB".format(size_compress/1024),decomp),
        ("Original, zoom",     original[l:l+s, h:h+s]),
        ("Compressed, zoom",   decomp[l:l+s, h:h+s]),
    ]

    for i, (label, image) in enumerate(plots):
        ax = fig.add_subplot(2, 2, i + 1)
        ax.imshow(image, interpolation="nearest", cmap=plt.cm.gray)
        ax.set_title(label, fontsize=10)
        ax.set_xticks([])
        ax.set_yticks([])

    fig.tight_layout()
    plt.show()

main()
