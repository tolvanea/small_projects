# Minimal working example of image compression with wavelets.
# Coded this while drunk, no quality assurances. Do whatever you want with it.

# I scimmed following paper to get some grasp what wavelets are
# https://mil.ufl.edu/nechyba/www/eel6562/course_materials/t5.wavelets/intro_dwt.pdf

# Documentation of 2d-wavelets with PyWavelets
# https://pywavelets.readthedocs.io/en/latest/ref/2d-dwt-and-idwt.html#ref-dwt2


import numpy as np
import matplotlib.pyplot as plt

import pywt  # pip3 install PyWavelets
import pywt.data


def compress_image(image, crop_data_fraction=0.1):
    # Compress black and white image with wavelets

    def reduce_to_fraction_of_indices(matrix_2d, crop_to_fraction):
        # max image resolution is 65 535 due to the uint16
        ids_of_sorted = np.argsort(matrix_2d.flat)
        l = int(len(ids_of_sorted) * crop_data_fraction / 2)
        low_bound = matrix_2d.flat[ids_of_sorted[l]]
        high_bound = matrix_2d.flat[ids_of_sorted[-l]]
        ids = np.nonzero(np.logical_or(matrix_2d > high_bound, matrix_2d < low_bound))
        ids = (ids[0].astype(np.uint16), ids[1].astype(np.uint16))
        values = matrix_2d[ids].astype(np.float16)
        return (ids, values, matrix_2d.shape)

    compression_size = 0
    # Some source said that bior2.6 mother wavelet
    coeffs = pywt.wavedec2(image, 'bior2.6')
    packed_coeffs = [coeffs[0]]
    compression_size += size(coeffs[0])
    # i iterates through pixel frequencies with power of 2
    for i in range(1, len(coeffs)):
        hori, vert, diag = coeffs[i]
        hori_pack = reduce_to_fraction_of_indices(hori, crop_data_fraction)
        vert_pack = reduce_to_fraction_of_indices(vert, crop_data_fraction)
        diag_pack = reduce_to_fraction_of_indices(diag, crop_data_fraction)
        packed_coeffs.append((hori_pack, vert_pack, diag_pack))

        # Calculate byte size of tuples above. Shape is 16=2*size(uint)
        compression_size += size(hori_pack[0][0])*2 + size(hori_pack[1] + 16)
        compression_size += size(vert_pack[0][0])*2 + size(vert_pack[1] + 16)
        compression_size += size(diag_pack[0][0])*2 + size(diag_pack[1] + 16)
    return (packed_coeffs, image.shape), compression_size

def decompress_image(pack):
    # Decompress black and white image with wavelets
    def construct_from_indices(pack):
        ids, values, shape = pack
        mat = np.zeros(shape)
        mat[ids] = values
        return mat

    packed_coeffs, shape = pack
    coeffs = [packed_coeffs[0]]

    # i iterates through pixel frequencies with power of 2
    for i in range(1, len(packed_coeffs)):
        hori_pack, vert_pack, diag_pack = packed_coeffs[i]
        hori = construct_from_indices(hori_pack)
        vert = construct_from_indices(vert_pack)
        diag = construct_from_indices(diag_pack)
        print("Depacking", hori.shape)
        coeffs.append((hori, vert, diag))

    constructed_image = pywt.waverec2(coeffs, 'bior2.6')
    constructed_image = np.clip(constructed_image, 0, 255)
    return constructed_image


def size(arr):
    return arr.size * arr.itemsize

def main():
    # Load image
    original = pywt.data.camera()

    pack, size_compress = compress_image(original, crop_data_fraction=0.08)
    print(
        "Original size {:.1f}, ".format(size(original)/1024),
        "Compressed size {:.1f}".format(size_compress/1024))
    decomp = decompress_image(pack)

    fig = plt.figure(figsize=(12, 3))

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
