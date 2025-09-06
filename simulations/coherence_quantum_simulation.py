#!/usr/bin/env python
"""qcap_autorun.py — turnkey runner for **Qiskit ≥ 2.x** (no venv needed)

Run it with any CPython ≥3.9 and it will:
  • Auto‑install *numpy*, *qiskit*, and *qiskit‑aer* if missing.
  • Build a phase‑damping noise model tied to a synthetic PLV.
  • Simulate a CHSH test & single‑qubit Ramsey fringe at two PLV levels.

It now targets Qiskit 2.x’s API (the old `execute` helper is gone) using
`AerSimulator().run()` plus `transpile()`.
"""
from __future__ import annotations
import importlib, subprocess, sys, textwrap

# ---------------------------------------------------------------------------
# Helper: import a module, installing via pip first if it’s missing
# ---------------------------------------------------------------------------

def ensure(mod: str, pip_name: str | None = None):
    try:
        return importlib.import_module(mod)
    except ModuleNotFoundError:
        pkg = pip_name or mod
        print(f"[setup] installing '{pkg}'…", file=sys.stderr)
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
        return importlib.import_module(mod)

np = ensure("numpy")
qiskit = ensure("qiskit")           # meta‑package (Terra ≥ 2.0)
_ = ensure("qiskit_aer", "qiskit-aer")

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, phase_damping_error

# ---------------------------------------------------------------------------
# Synthetic coherence proxy (Phase‑Locking Value)
# ---------------------------------------------------------------------------

def generate_plv(duration: float = 1.0, fs: int = 250, coherence: float = 0.5) -> float:
    t = np.linspace(0.0, duration, int(fs * duration))
    s1 = np.sin(2 * np.pi * 10 * t)
    s2 = np.sin(2 * np.pi * 10 * t + np.random.uniform(0, 2 * np.pi * (1 - coherence)))
    return float(np.abs(np.mean(np.exp(1j * (np.angle(s1) - np.angle(s2))))))

# ---------------------------------------------------------------------------
# Build a phase‑damping noise model scaled by PLV
# ---------------------------------------------------------------------------

def build_noise_model(plv: float) -> tuple[NoiseModel, float]:
    sigma2 = 1e-7 * (1 + 5 * (plv - 0.5))
    nm = NoiseModel()
    nm.add_all_qubit_quantum_error(phase_damping_error(sigma2), ["id", "rz", "sx", "x", "u"])
    return nm, sigma2

# ---------------------------------------------------------------------------
# Quantum circuits
# ---------------------------------------------------------------------------
chsh = QuantumCircuit(4, 4)
chsh.h(0); chsh.cx(0, 1)
chsh.h(2); chsh.cx(2, 3)
chsh.ry(np.pi / 4, [0, 2])
chsh.ry(-np.pi / 4, [1, 3])
chsh.measure(range(4), range(4))

ramsey = QuantumCircuit(1, 1)
ramsey.h(0)
ramsey.delay(100, unit="ns")
ramsey.h(0)
ramsey.measure(0, 0)

# ---------------------------------------------------------------------------
# Main simulation routine
# ---------------------------------------------------------------------------

def run():
    for plv in (0.3, 0.8):
        nm, sigma2 = build_noise_model(plv)
        sim = AerSimulator(noise_model=nm)

        # CHSH
        counts = sim.run(transpile(chsh, sim), shots=10_000).result().get_counts()
        s = (counts.get("0000", 0) + counts.get("1111", 0)
             - counts.get("0011", 0) - counts.get("1100", 0)) / 10_000

        # Ramsey
        r_counts = sim.run(transpile(ramsey, sim), shots=10_000).result().get_counts()
        contrast = (r_counts.get("0", 0) - r_counts.get("1", 0)) / 10_000
        dnu = np.sqrt(max(0, -2 * np.log(np.clip(abs(contrast), 1e-12, 1)))) / (2 * np.pi * 100e-9)

        print(textwrap.dedent(f"""
            PLV = {plv:.1f}
              • CHSH S ≈ {s:.4f}
              • Ramsey Δν ≈ {dnu:.2f} Hz (σ²={sigma2:.2e})"""))

if __name__ == "__main__":
    run()
