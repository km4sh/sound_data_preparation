import soundfile as sf
import numpy as np

def getsnr(noisy, clean, threshold):
    threshold = max(clean) * threshold
    vadn = [samp**2 for samp in noisy if samp > threshold ]
    vadc = [samp**2 for samp in clean if samp > threshold ]
    enrgn = np.mean(vadn)
    enrgc = np.mean(vadc)
    snr = 10*np.log10(enrgc / (enrgn - enrgc))
    return snr

