import numpy as np

def beta_pert_parameters(mode: float, min_val: float, max_val: float, scale:float=4.0) -> tuple[float, float]:
    """
    Calculate alpha and beta parameters for a Beta-PERT distribution.

    Source: https://prevalence.cbra.be/?main=functions&sub=betaPERT
    """
    if not (min_val < mode < max_val):
        raise ValueError("mode must be between min and max")
    
    m = mode
    a = min_val
    b = max_val
    k = scale

    mean = (a + k * m + b) / (k + 2)
    std_dev = (b - a) / (k + 2)
    alpha = ( (mean - a) / (b - a) ) * ( (mean - a) * (b - mean) / std_dev**2 - 1 )
    beta = alpha * (b - mean) / (mean - a)

    return alpha, beta

def beta_pert_sample(alpha, beta, min_val, max_val, rng: np.random.Generator) -> float:
    """
    Sample from a Beta-PERT distribution defined by min, max, alpha and beta.
    """
    sample = rng.beta(alpha, beta, size=1)
    # Scale sample back to [min_val, max_val]
    scaled_sample = sample * (max_val - min_val) + min_val
    return scaled_sample


if __name__ == "__main__":
    # Example usage
    concentration = 4.0

    min_val = 2.0
    mode = 5.0
    max_val = 10.0

    import matplotlib.pyplot as plt
    from scipy.stats import beta

    # Take 1000 beta_pert_samples and plot histogram
    alpha_param, beta_param = beta_pert_parameters(mode, min_val, max_val, concentration)
    rng = np.random.default_rng()
    samples = [beta_pert_sample(alpha_param, beta_param, min_val, max_val, rng)[0] for _i in range(10000)]
    
    # Plot the PDF of the Beta distribution along with the histogram of samples
    x = np.linspace(0, 1, 100)
    y = beta.pdf(x, alpha_param, beta_param) / 2.0 * 0.25
    # Scale x back to [min_val, max_val]
    x_scaled = x * (max_val - min_val) + min_val

    plt.plot(x_scaled, y)
    plt.hist(samples, bins=30, density=True)
    plt.title('Histogram of Beta-PERT Samples')
    plt.xlabel('Value')
    plt.ylabel('Density')
    plt.grid()
    plt.savefig("samples_histogram.png")