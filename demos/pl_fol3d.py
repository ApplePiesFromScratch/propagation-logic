"""
pl_fold3d.py — 3D Multi-Protein Folding via Propagation Logic
All P is G prior to the cut. Proteins fold as mutual gradients.
"""

from pl.calculus import CalcPattern, newton_reconfigure
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np   # only for clean 3D plotting (not used in propagation)

class PL3DCoherentFolder:
    def __init__(self, sequences: list[str] = ["HHPPHH", "PPHHPP"], initial_separation: float = 15.0):
        self.sequences = [s.upper() for s in sequences]
        self.n_chains = len(self.sequences)
        # One torsion angle per link per chain — all live in one unified field
        self.angles = [[1.0] * (len(seq) - 1) for seq in self.sequences]
        self.initial_separation = initial_separation
        print(f"✅ Loaded {self.n_chains} proteins into ONE coherence field")
        print("   → All P is G prior to any cut. Shared gradients across chains.\n")

    def _get_all_positions(self) -> list[list[tuple[float, float, float]]]:
        """3D forward kinematics — pure math, differentiable via CalcPattern."""
        all_pos = []
        for c, seq in enumerate(self.sequences):
            pos = [(float(c * self.initial_separation), 0.0, 0.0)]
            theta_x = 0.0
            theta_y = 0.0
            for angle in self.angles[c]:
                theta_x += angle * 0.8
                theta_y += angle * 0.5
                dx = 3.8 * math.cos(theta_x) * math.cos(theta_y)
                dy = 3.8 * math.sin(theta_x)
                dz = 3.8 * math.sin(theta_y)
                new_pos = (pos[-1][0] + dx, pos[-1][1] + dy, pos[-1][2] + dz)
                pos.append(new_pos)
            all_pos.append(pos)
        return all_pos

    def _global_energy_pattern(self, chain_idx: int, angle_idx: int, trial_val: float) -> CalcPattern:
        """ONE unified energy CalcPattern — every protein is gradient for every other."""
        # Temporarily apply trial angle
        original = self.angles[chain_idx][angle_idx]
        self.angles[chain_idx][angle_idx] = trial_val

        positions = self._get_all_positions()
        total = CalcPattern(0.0)

        # Intra- + inter-chain non-bonded (HP model) — full cross-propagation
        for c1 in range(self.n_chains):
            for c2 in range(c1, self.n_chains):          # symmetric but shared
                for i in range(len(positions[c1])):
                    for j in range(len(positions[c2])):
                        if c1 == c2 and abs(i - j) < 4:   # skip local backbone
                            continue
                        p1 = positions[c1][i]
                        p2 = positions[c2][j]
                        r2 = (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2
                        r = CalcPattern(max(math.sqrt(r2), 1.0))
                        lj = (1.0 / r**12) - 3.0 / r**6
                        # Strong hydrophobic attraction across chains
                        if self.sequences[c1][i] == 'H' and self.sequences[c2][j] == 'H':
                            lj -= 4.0 / r
                        total += lj

        self.angles[chain_idx][angle_idx] = original
        return total

    def fold(self, iterations: int = 20):
        print("🚀 Starting joint coherence propagation (3D multi-protein folding)...\n")
        for it in range(iterations):
            # Measure global demand
            demand = 0.0
            for c in range(self.n_chains):
                for a in range(len(self.angles[c])):
                    demand += self._global_energy_pattern(c, a, self.angles[c][a]).val
            print(f"Iter {it:2d} | Global system demand = {demand:.6f}")

            # Coordinate descent — each angle reconfigures using the full shared gradient
            for c in range(self.n_chains):
                for a in range(len(self.angles[c])):
                    def f_pattern(x: float) -> CalcPattern:
                        return self._global_energy_pattern(c, a, x)
                    new_angle = newton_reconfigure(
                        f_pattern,
                        x0=self.angles[c][a],
                        threshold=1e-9,
                        max_steps=8
                    )
                    self.angles[c][a] = new_angle

        self._render_3d()

    def _render_3d(self):
        """Beautiful interactive 3D display of the final coherent fold."""
        fig = plt.figure(figsize=(12, 9))
        ax = fig.add_subplot(111, projection='3d')
        positions = self._get_all_positions()
        colors = ['#e74c3c', '#3498db', '#2ecc71', '#f1c40f']

        for c, seq in enumerate(self.sequences):
            pos = np.array(positions[c])
            color = colors[c % len(colors)]
            ax.plot(pos[:,0], pos[:,1], pos[:,2], linewidth=5, color=color, label=f"Chain {c+1}: {seq}")
            for i, p in enumerate(pos):
                if seq[i] == 'H':
                    ax.scatter(p[0], p[1], p[2], color=color, s=180, marker='o', edgecolor='black', linewidth=1.5)
                else:
                    ax.scatter(p[0], p[1], p[2], color=color, s=100, marker='s', edgecolor='black', linewidth=1.5)

        ax.set_title("3D Coherent Protein Folding — Propagation Logic\n"
                     "All Patterns are Gradients • Joint Confluence Before Any Cut",
                     fontsize=14, pad=20)
        ax.set_xlabel("X (Å)"); ax.set_ylabel("Y (Å)"); ax.set_zlabel("Z (Å)")
        ax.legend()
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    folder = PL3DCoherentFolder(
        sequences=["HHPPHH", "PPHHPP"],   # two proteins that will attract each other
        initial_separation=18.0
    )
    folder.fold(iterations=18)
