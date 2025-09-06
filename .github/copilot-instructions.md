# AI Agent Instructions for Physics & Theoretical Research Workspace

This workspace contains theoretical physics research, computational implementations, and documentation related to a novel framework called the Coherence-Modulated Ψ-Field theory. The work spans multiple interconnected projects that explore consciousness, quantum physics, field theory, and cosmological models.

## Project Overview

The core hypothesis is that a fundamental scalar field (Ψ-field) underlies reality, which can be modulated by observer coherence. This leads to a "Physics of Participation" where observer coherence influences physical systems through modulation of soliton-like excitations in this field.

Major components:
1. **Theoretical frameworks** in LaTeX (mathematical models, field equations, Lagrangians)
2. **Python simulations** (quantum system models, coherence effects)
3. **Documentation** (briefing documents, notes, transcripts)

## Critical Concepts

- **Ψ-Field**: A hypothetical scalar field that forms the substrate of reality
- **Observer Coherence (ρobs)**: A quantifiable measure of structured informational activity
- **Coherence-Modulation**: How observer coherence alters physical systems via the Ψ-field
- **Solitons**: Particle-like stable excitations in the Ψ-field
- **Hypercausal Dynamics**: Signal propagation faster than light speed (c ≪ C)

## Code Structure and Patterns

### Python Simulations
- `QCAP_main_simulation.py`: Primary quantum simulation using Qiskit 
- `QCAP_secondary_simulation.py`: Extended lab simulation framework

Key patterns:
```python
# Lazy imports with auto-installation
def ensure(mod: str, pip_name: str | None = None):
    try:
        return importlib.import_module(mod)
    except ModuleNotFoundError:
        pkg = pip_name or mod
        print(f"[setup] installing '{pkg}'…", file=sys.stderr)
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
        return importlib.import_module(mod)
```

### Quantum Circuits
The project uses Qiskit (≥2.x) for quantum simulations:
```python
# Example circuit construction pattern
chsh = QuantumCircuit(4, 4)
chsh.h(0); chsh.cx(0, 1)
chsh.h(2); chsh.cx(2, 3)
chsh.ry(np.pi / 4, [0, 2])
chsh.ry(-np.pi / 4, [1, 3])
chsh.measure(range(4), range(4))
```

### LaTeX Structure
- Each theoretical component has its own directory with `main.tex`
- Mathematical notation follows specific conventions (see `Hyperchronal Ontology-Inversion/main.tex`)

## Development Workflow

1. **Running Simulations**: 
   ```bash
   python QCAP_main_simulation.py  # Basic CHSH test simulation
   python QCAP_secondary_simulation.py  # Extended lab simulation
   ```

2. **Editing Theory Documents**:
   - LaTeX files in their respective project directories
   - Follow mathematical notation conventions established in existing files

3. **Project Integration**:
   - New theoretical components should connect to the core Ψ-Field framework
   - Python simulations should reference theoretical parameters

## Key Integration Points

1. **Theory to Simulation**: Mathematical models from LaTeX documents inform simulation parameters
2. **Coherence Parameter**: Central to all models - connects observer effects to physical systems
3. **Cross-project References**: Many documents reference concepts from other components

## Specific Conventions

1. **Unicode in Code**: Use full unicode where appropriate for mathematical symbols
2. **Documentation Style**: Detailed docstrings that explain both implementation and theoretical foundation
3. **Variable Naming**: Physics notation (ρ, Ψ, α) when representing the corresponding physical quantities

## External Dependencies

- Python 3.9+
- Qiskit 2.x+ and qiskit-aer
- NumPy
- LaTeX with AMS packages
- Rich (for console output in lab simulations)

When extending or modifying code, maintain the theoretical integrity of the research concepts while improving implementation quality.
