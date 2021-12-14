# small_projects
Random one-file self-contained codes that don't deserve own repo


## wavelets.py
Minimal working example of image compression with wavelet decomposotion. Unlike Fourier thansform, wavelets preserve locality both in spatial and frequency domains. That is, wavelets are mathematically rigorous version of spectrogram. The algorithm is home brew, and it is _very_ basic. It basically drops out the weakest 85% of local frequencies. While the 15% of the wavelets are preserved, it is no where near packing the image to 15% of the original size due to sloppy bit packing.

![wavelets](wavelets.png)
