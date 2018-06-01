import soundfile as sf
import numpy as np

def getsnr(noisy, clean, threshold):
    nthd = np.max(noisy) * threshold
    cthd = np.max(clean) * threshold
    vadn = [samp**2 for samp in noisy if samp > nthd]
    vadn.extend([samp**2 for samp in noisy if samp > nthd])
    vadc = [samp**2 for samp in clean if samp > cthd]
    enrgn = np.mean(vadn)
    enrgc = np.mean(vadc)
    print(enrgn, enrgc)
    try:
        snr = 10*(np.log10(enrgc) - np.log10(enrgn - enrgc))
    except:
        import ipdb; ipdb.set_trace()
    return snr



