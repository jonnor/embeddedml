import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.interpolate import interp1d

def gaussian_spectrum(wavelength, peak_lambda, fwhm, intensity=1.0):
    """Generate Gaussian-shaped LED spectrum"""
    sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
    return intensity * np.exp(-((wavelength - peak_lambda) ** 2) / (2 * sigma ** 2))

def photopic_luminosity_function(wavelength):
    """
    CIE 1931 photopic luminosity function V(λ) for lux calculations
    Peak at 555 nm with value of 1.0
    """
    # Key wavelengths and corresponding V(λ) values
    wl_data = np.array([380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 555, 560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 660, 670, 680, 690, 700, 710, 720, 730, 740, 750, 760, 770, 780])
    v_lambda = np.array([0.0000, 0.0001, 0.0004, 0.0012, 0.0040, 0.0116, 0.0230, 0.0380, 0.0600, 0.0910, 0.1390, 0.2080, 0.3230, 0.5030, 0.7100, 0.8620, 0.9540, 0.9950, 1.0000, 0.9950, 0.9520, 0.8700, 0.7570, 0.6310, 0.5030, 0.3810, 0.2650, 0.1750, 0.1070, 0.0610, 0.0320, 0.0150, 0.0074, 0.0033, 0.0015, 0.0007, 0.0003, 0.0001, 0.0001, 0.0000, 0.0000, 0.0000])
    
    # Interpolate for given wavelength array
    interp_func = interp1d(wl_data, v_lambda, kind='cubic', bounds_error=False, fill_value=0)
    return interp_func(wavelength)

def calculate_lux_efficiency(wavelength, spectrum):
    """Calculate luminous efficacy (lm/W) for given spectrum"""
    # Photopic luminosity function
    v_lambda = photopic_luminosity_function(wavelength)
    
    # Luminous efficacy constant: 683 lm/W at 555nm
    Km = 683  # lm/W
    
    # Calculate luminous flux (lumens) - integrate spectrum * V(λ)
    luminous_flux = np.trapz(spectrum * v_lambda, wavelength)
    
    # Calculate radiant flux (watts) - integrate spectrum
    radiant_flux = np.trapz(spectrum, wavelength)
    
    # Luminous efficacy
    if radiant_flux > 0:
        efficacy = Km * luminous_flux / radiant_flux
    else:
        efficacy = 0
    
    return efficacy

def led_spectral_response():
    """Compute spectral response for common LEDs"""
    
    # Wavelength range (nm)
    wavelength = np.linspace(350, 750, 1000)
    
    # Common LED parameters: (name, peak_wavelength, FWHM, color)
    led_types = [
        ("UV LED", 365, 15, "purple"),
        ("Blue LED", 470, 25, "blue"),
        ("Cyan LED", 505, 30, "cyan"),
        ("Green LED", 530, 35, "green"),
        ("Lime LED", 555, 30, "lime"),
        ("Yellow-Green LED", 570, 35, "yellowgreen"),
        ("Amber LED", 590, 40, "orange"),
        ("Orange LED", 605, 35, "darkorange"),
        ("Red LED", 630, 30, "red"),
        ("Deep Red LED", 660, 25, "darkred"),
        ("IR LED", 850, 50, "maroon")
    ]
    
    # AS7343
    data = {
        "Channel": ["F1", "F2", "FZ", "F3", "F4", "FY", "F5", "FXL", "F6", "F7", "F8", "NIR"],
        "Peak Wavelength (min) [nm]": [395, 415, 440, 465, 505, 545, 540, 590, 630, 680, 735, 845],
        "Peak Wavelength (typ) [nm]": [405, 425, 450, 475, 515, 555, 550, 600, 640, 690, 745, 855],
        "Peak Wavelength (max) [nm]": [415, 435, 460, 485, 525, 565, 560, 610, 650, 700, 755, 865],
        "FWHM (typ) [nm]": [30, 22, 55, 30, 40, 100, 35, 80, 50, 55, 60, 54]
    }

    # Discrete LEDs as SMD, low-cost. 0603 common. Looks possible to get these
    # 470 OK
    # 520 OK
    # 560 OK
    # 590 OK
    # 605 OK
    # 630 OK
    # 660 OK

    import pandas as pd
    df = pd.DataFrame(data)


    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Plot 1: LED spectra
    for name, peak, fwhm, color in led_types:
        spectrum = gaussian_spectrum(wavelength, peak, fwhm)
        ax1.plot(wavelength, spectrum, label=name, color=color, linewidth=2)
    
    # Add photopic luminosity function
    v_lambda = photopic_luminosity_function(wavelength)
    ax1.plot(wavelength, v_lambda, 'k--', linewidth=2, label='Photopic V(λ) - Lux Response')
    
    # Formatting for first plot
    ax1.set_xlabel('Wavelength (nm)', fontsize=12)
    ax1.set_ylabel('Relative Intensity', fontsize=12)
    ax1.set_title('LED Spectral Response vs Human Eye Sensitivity (Lux)', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax1.set_xlim(350, 750)
    ax1.set_ylim(0, 1.1)
    
    # Add visible spectrum background
    visible_colors = ['violet', 'blue', 'cyan', 'green', 'yellow', 'orange', 'red']
    visible_ranges = [(380, 450), (450, 495), (495, 520), (520, 565), (565, 590), (590, 625), (625, 750)]
    
    for i, (start, end) in enumerate(visible_ranges):
        ax1.axvspan(start, end, alpha=0.1, color=visible_colors[i])
    
    # Plot 2: Lux efficiency comparison
    led_names = []
    efficacies = []
    
    for name, peak, fwhm, color in led_types:
        spectrum = gaussian_spectrum(wavelength, peak, fwhm)
        efficacy = calculate_lux_efficiency(wavelength, spectrum)
        led_names.append(name.replace(' LED', ''))
        efficacies.append(efficacy)
        
        # Show spectrum weighted by V(λ)
        weighted_spectrum = spectrum * v_lambda
        ax2.plot(wavelength, weighted_spectrum, color=color, linewidth=2, alpha=0.7)
    
    ax2.set_xlabel('Wavelength (nm)', fontsize=12)
    ax2.set_ylabel('Lux-Weighted Intensity', fontsize=12)
    ax2.set_title('LED Spectra Weighted by Photopic Response', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(350, 750)
    
    plt.tight_layout()
    plt.show()
    

if __name__ == "__main__":
    # Run all analyses
    led_spectral_response()

