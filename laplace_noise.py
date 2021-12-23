import numpy as np
import matplotlib.pyplot as plt
#from scipy.signal import convolve2d, deconvolve2d
from scipy import fftpack
from skimage import data

img = data.camera()
skip = max(img.shape[0], img.shape[0]) // 64
img = img[::skip,::skip]
print(np.max(img), np.min(img))
(m,n) = img.shape
noise = np.random.randn(m,n)

laplace_operator = np.zeros((m,n,m,n), dtype=noise.dtype)

for i in range(m):
    for j in range(n):
        laplace_operator[i,j,i,j] = 4
        laplace_operator[i, j, (i-1)%m, j] = -1
        laplace_operator[i, j, i, (j-1)%n] = -1
        laplace_operator[i, j, (i+1)%m, j] = -1
        laplace_operator[i, j, i, (j+1)%n] = -1


W = np.resize(laplace_operator, (m*n, m*n))
z1 = noise.flatten()
z2 = img.flatten()

deconvoluted_noise = np.resize(np.linalg.solve(W, z1), (m,n))
convoluted_noise = np.resize(W @ z1, (m,n))

deconvoluted_img = np.resize(np.linalg.solve(W, z2), (m,n))
convoluted_img = np.resize(W @ z2, (m,n))

fig, ((ax1,ax2,ax3), (ax4,ax5,ax6)) = plt.subplots(2,3)

diff = np.max(img) - np.min(img)
mi = np.min(img) - diff/2
ma = np.max(img) + diff/2
ax1.imshow(deconvoluted_img, cmap=plt.cm.gray)
ax1.set_title("deconvoluted image")
ax2.imshow(img, cmap=plt.cm.gray, vmin=mi, vmax=ma)
ax2.set_title("$\\leftarrow$ image $\\rightarrow$")
ax3.imshow(convoluted_img, cmap=plt.cm.gray, vmin=mi, vmax=ma)
ax3.set_title("convoluted image")
fig.suptitle("(De)convolution with Laplace kernel [[0 -1 0] [-1 4 -1] [0 -1 0]]")

ax4.imshow(deconvoluted_noise, cmap=plt.cm.gray)
ax4.set_title("deconvoluted noise")
ax5.imshow(noise, cmap=plt.cm.gray, vmin=-2, vmax=2)
ax5.set_title("$\\leftarrow$ (white) noise $\\rightarrow$")
ax6.imshow(convoluted_noise, cmap=plt.cm.gray, vmin=-2, vmax=2)
ax6.set_title("convoluted noise")

plt.show()
