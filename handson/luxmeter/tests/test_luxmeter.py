
import array

import matplotlib.pyplot as plt

from luxmeter_core import photopic_interpolated, photopic_stockman_sharpe, CIE_1931_DATA


def compute_lux_from_spectral_data(spectral_data, luminosity_function):
    """
    Compute lux from spectral irradiance data using given luminosity function
    
    Args:
        spectral_data: list of (wavelength_nm, irradiance_W_per_m2_per_nm) tuples
        luminosity_function: function that takes wavelength and returns V(λ)
    
    Returns:
        Illuminance in lux
    """
    # Photopic luminous efficacy constant (lm/W)
    Km = 683.0
    
    total = 0.0
    for wavelength, irradiance in spectral_data:
        v_lambda = luminosity_function(wavelength)
        total += irradiance * v_lambda
    
    # Multiply by constant and wavelength interval (assuming 1nm intervals)
    return Km * total

# Generate comparison plot
def plot_comparison():
    """Generate comparison plot of the three methods"""
    wavelengths = array.array('f', range(380, 781, 5))  # 5nm intervals
    
    # Calculate values for each method
    stockman_values = array.array('f', [photopic_stockman_sharpe(wl) for wl in wavelengths])
    interpolated_values = array.array('f', [photopic_interpolated(wl) for wl in wavelengths])
    
    # Reference data for plotting
    ref_wavelengths = array.array('f', [data[0] for data in CIE_1931_DATA])
    ref_values = array.array('f', [data[1] for data in CIE_1931_DATA])
    
    # Create plot
    plt.figure(figsize=(12, 8))
    plt.plot(wavelengths, stockman_values, 'g-', label='Stockman & Sharpe', linewidth=2)
    plt.plot(wavelengths, interpolated_values, 'r-', label='Interpolated Standard', linewidth=2)
    plt.plot(ref_wavelengths, ref_values, 'ko', label='CIE 1931 Reference', markersize=4)
    
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Photopic Luminosity V(λ)')
    plt.title('CIE 1931 Photopic Luminosity Function - Method Comparison')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xlim(380, 780)
    plt.ylim(0, 1.1)
    
    plt.tight_layout()
    plt.show()

# Example usage
if __name__ == "__main__":
    # Example spectral data (wavelength in nm, irradiance in W/m²/nm)
    example_spectral_data = [
        (400, 0.1), (450, 0.5), (500, 1.0), (550, 1.5), (600, 1.2), (650, 0.8), (700, 0.3)
    ]
    
    # Calculate lux using each method
    lux_stockman = compute_lux_from_spectral_data(example_spectral_data, photopic_stockman_sharpe)
    lux_interpolated = compute_lux_from_spectral_data(example_spectral_data, photopic_interpolated)
    
    print(f"Lux calculations from example spectral data:")
    print(f"Stockman & Sharpe: {lux_stockman:.2f} lux") 
    print(f"Interpolated standard: {lux_interpolated:.2f} lux")
    
    # Generate comparison plot
    plot_comparison()
    
    # Test individual functions at 555nm (should be 1.0)
    print(f"\nValues at 555nm (should be 1.0):")
    print(f"Stockman & Sharpe: {photopic_stockman_sharpe(555):.6f}")
    print(f"Interpolated: {photopic_interpolated(555):.6f}")
