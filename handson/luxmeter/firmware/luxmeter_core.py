

# Lux calculation using CIE 1931 photopic luminosity function
# https://en.wikipedia.org/wiki/CIE_1931_color_space

import array
import math

# CIE 1931 photopic luminosity function reference data (wavelength in nm, V(λ))
CIE_1931_DATA = [
    (380, 0.000039), (385, 0.000064), (390, 0.000120), (395, 0.000217),
    (400, 0.000396), (405, 0.000640), (410, 0.001210), (415, 0.002180),
    (420, 0.004000), (425, 0.007300), (430, 0.011600), (435, 0.016840),
    (440, 0.023000), (445, 0.029800), (450, 0.038000), (455, 0.048000),
    (460, 0.060000), (465, 0.073900), (470, 0.090980), (475, 0.112600),
    (480, 0.139020), (485, 0.169300), (490, 0.208020), (495, 0.258600),
    (500, 0.323000), (505, 0.407300), (510, 0.503000), (515, 0.608200),
    (520, 0.710000), (525, 0.793200), (530, 0.862000), (535, 0.914850),
    (540, 0.954000), (545, 0.980300), (550, 0.994950), (555, 1.000000),
    (560, 0.995000), (565, 0.978600), (570, 0.952000), (575, 0.915400),
    (580, 0.870000), (585, 0.816300), (590, 0.757000), (595, 0.694900),
    (600, 0.631000), (605, 0.566800), (610, 0.503000), (615, 0.441200),
    (620, 0.381000), (625, 0.321000), (630, 0.265000), (635, 0.217000),
    (640, 0.175000), (645, 0.138200), (650, 0.107000), (655, 0.081600),
    (660, 0.061000), (665, 0.044580), (670, 0.032000), (675, 0.023200),
    (680, 0.017000), (685, 0.011920), (690, 0.008210), (695, 0.005723),
    (700, 0.004102), (705, 0.002929), (710, 0.002091), (715, 0.001484),
    (720, 0.001047), (725, 0.000740), (730, 0.000520), (735, 0.000361),
    (740, 0.000249), (745, 0.000172), (750, 0.000120), (755, 0.000085),
    (760, 0.000060), (765, 0.000042), (770, 0.000030), (775, 0.000021),
    (780, 0.000015)
]

# Spectral information. From AS7343 datasheet
AS7343_INFO = {
    "channel": ["F1", "F2", "FZ", "F3", "F4", "FY", "F5", "FXL", "F6", "F7", "F8", "NIR"],
    "peak_wavelength_min": [395, 415, 440, 465, 505, 545, 540, 590, 630, 680, 735, 845],
    "peak_wavelength": [405, 425, 450, 475, 515, 555, 550, 600, 640, 690, 745, 855], # typical (nm)
    "peak_wavelength_max": [415, 435, 460, 485, 525, 565, 560, 610, 650, 700, 755, 865],
    "FWHM": [30, 22, 55, 30, 40, 100, 35, 80, 50, 55, 60, 54], # Full Width Half Maximum (nm)
    # sensitivity info
    # counts at Ee=155 mW/m² (typical). AGAIN: 1024x, Integration Time: 27.8 ms
    "counts": [ 5749, 1756, 2169, 770, 3141, 3747, 1574, 4776, 3336, 5435, 864, 10581 ],
}

def photopic_stockman_sharpe(wavelength):
    """
    Stockman & Sharpe approximation based on L+M cone fundamentals
    Using parameters from their 2000 paper
    """
    # Parameters for L and M cone fundamentals (simplified)
    # L cone (long wavelength)
    l_peak = 564.0
    l_sigma = 45.0
    l_weight = 0.7
    
    # M cone (medium wavelength) 
    m_peak = 534.0
    m_sigma = 40.0
    m_weight = 0.3
    
    l_response = math.exp(-0.5 * ((wavelength - l_peak) / l_sigma) ** 2)
    m_response = math.exp(-0.5 * ((wavelength - m_peak) / m_sigma) ** 2)
    
    # Normalize to peak at 555nm
    normalization_wl = 555.0
    l_norm = math.exp(-0.5 * ((normalization_wl - l_peak) / l_sigma) ** 2)
    m_norm = math.exp(-0.5 * ((normalization_wl - m_peak) / m_sigma) ** 2)
    norm_factor = l_weight * l_norm + m_weight * m_norm
    
    return (l_weight * l_response + m_weight * m_response) / norm_factor

def photopic_interpolated(wavelength):
    """
    Linear interpolation of CIE 1931 standard data
    """
    # Convert to arrays for easier handling
    wavelengths = array.array('f', [data[0] for data in CIE_1931_DATA])
    values = array.array('f', [data[1] for data in CIE_1931_DATA])
    
    # Handle out of range values
    if wavelength <= wavelengths[0]:
        return values[0]
    if wavelength >= wavelengths[-1]:
        return values[-1]
    
    # Find interpolation points
    for i in range(len(wavelengths) - 1):
        if wavelengths[i] <= wavelength <= wavelengths[i + 1]:
            # Linear interpolation
            x0, y0 = wavelengths[i], values[i]
            x1, y1 = wavelengths[i + 1], values[i + 1]
            return y0 + (y1 - y0) * (wavelength - x0) / (x1 - x0)
    
    return 0.0

