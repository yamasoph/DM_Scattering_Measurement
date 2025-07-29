import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import csv

azimuth_step = 5
motor_step = 1.5
azimuth_edges = np.arange(0, 180 + azimuth_step, azimuth_step)
motor_edges = np.arange(0, 180 + motor_step, motor_step)
azimuth_bins = len(azimuth_edges) - 1
motor_bins = len(motor_edges) - 1

image_shape = (1520, 1536)  
dtype = np.uint16        
data_root = Path(r"/media/locsst/USB SKY/twenty_three")

polar_map = np.full((motor_bins, azimuth_bins), np.nan)

def extract_total_intensity(raw):
    R  = raw[0::2, 0::2]
    G1 = raw[0::2, 1::2]
    G2 = raw[1::2, 0::2]
    B  = raw[1::2, 1::2]
    return (R.astype(np.float32) + G1 + G2 + B) / 4.0

for i, az in enumerate(azimuth_edges[:-1]):
    folder_data = data_root / f"rawtrials_{az:05.1f}"
    for j, mot in enumerate(motor_edges[:-1]):
        fname = f"rawtrials_{az:05.1f}_{mot:05.1f}.raw"
        f_data = folder_data / fname
        if not f_data.exists():
            continue

        try:
            raw = np.fromfile(f_data, dtype=dtype)
            if raw.size != np.prod(image_shape):
                print(raw.shape)
                continue
            img = raw.reshape(image_shape)
            print(f"working on {fname}")
            intensity = extract_total_intensity(img)
            
            #log scale for better dynamic range visualization
            #polar_map[j, i] = np.log1p(intensity.sum())
            
            polar_map[j, i] = intensity.sum()
        except Exception as e:
            print(f"Error loading {f_data.name}: {e}")
            continue

r_edges = motor_edges - 90  
theta_edges = np.deg2rad(azimuth_edges)
theta_grid, r_grid = np.meshgrid(theta_edges, r_edges)
x_edges = r_grid * np.cos(theta_grid)
y_edges = r_grid * np.sin(theta_grid)

fig, ax = plt.subplots(figsize=(10, 10))

c = ax.pcolormesh(x_edges, y_edges, polar_map, cmap="gray", shading="auto")

ax.set_aspect("equal")
ax.set_xlim(-100, 100)
ax.set_ylim(-100, 100)
ax.set_title("Scattering Map from Unpacked RAW Data")
ax.grid(True)
fig.colorbar(c, ax=ax, label="Total Intensity (summed)")
plt.tight_layout()
plt.show()

output_csv = data_root / "scattering_map.csv"
np.savetxt(output_csv, polar_map, delimiter=",", fmt="%.2f")
print(f"Saved polar map to {output_csv}")
