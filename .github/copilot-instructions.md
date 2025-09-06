# AI Agent Instructions for Theoretical Physics Research Workspace

This workspace contains **theoretical physics research** presented as sophisticated thought experiments for academic engagement. The repository explores novel approaches to fundamental physics through the lens of a proposed Coherence-Modulated Ψ-Field theory framework.

## Project Overview

The repository is organized as a professional academic research collection focusing on speculative theoretical physics. The core hypothesis explores whether observer coherence might influence physical systems through modulation of underlying field structures. All work is framed as theoretical speculation requiring rigorous validation.

**Repository Structure:**
1. **`theory/`** - LaTeX theoretical frameworks (field equations, mathematical models)
2. **`simulations/`** - Python quantum simulations and computational models  
3. **`docs/`** - Project briefings and documentation
4. **`supporting-materials/`** - Transcripts, notes, and supplementary materials
5. **`archive/`** - Working drafts and historical development materials

## Critical Concepts

- **Ψ-Field**: A hypothetical scalar field that forms the substrate of reality
- **Observer Coherence (ρobs)**: A quantifiable measure of structured informational activity
- **Coherence-Modulation**: How observer coherence alters physical systems via the Ψ-field
- **Solitons**: Particle-like stable excitations in the Ψ-field
- **Hypercausal Dynamics**: Signal propagation faster than light speed (c ≪ C)

## Critical Concepts

- **Ψ-Field**: Hypothetical scalar field proposed as substrate for physical phenomena
- **Observer Coherence (ρ_obs)**: Quantifiable measure of structured informational activity
- **Coherence-Modulation**: Proposed mechanism for observer influence on field dynamics
- **Soliton Excitations**: Particle-like stable excitations in the Ψ-field substrate
- **Hypercausal Dynamics**: Theoretical signal propagation faster than light speed (c ≪ C)

## Code Structure and Patterns

### Python Simulations
- `simulations/coherence_quantum_simulation.py`: Primary quantum coherence simulation using Qiskit 2.x
- `simulations/extended_lab_simulation.py`: Extended laboratory simulation framework with Rich interface

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
- Each theoretical component has its own directory in `theory/` with `main.tex`
- Organized by theoretical focus: field theory, ontology, participatory physics, etc.
- Mathematical notation follows established physics conventions

## Development Workflow

1. **Running Simulations**: 
   ```bash
   python simulations/coherence_quantum_simulation.py    # Primary CHSH test simulation
   python simulations/extended_lab_simulation.py        # Extended lab framework
   ```

2. **Editing Theory Documents**:
   - LaTeX files organized in `theory/` subdirectories by topic
   - Follow mathematical notation conventions established in existing documents
   - Maintain theoretical coherence across interconnected frameworks

3. **Documentation Access**:
   - Start with `README.md` for overview and navigation
   - Consult `FILE_INDEX.md` for comprehensive file descriptions
   - Review `docs/nexus_briefing_main.md` for theoretical introduction

## Key Integration Points

1. **Theory to Simulation**: Mathematical models from LaTeX documents inform simulation parameters
2. **Coherence Parameter**: Central to all models - connects observer effects to physical systems
3. **Academic Framing**: All work presented as theoretical speculation requiring validation
4. **Cross-project References**: Theoretical frameworks reference concepts across multiple documents

## Academic Engagement Guidelines

This repository is structured for safe academic engagement:

1. **Theoretical Context**: All proposals framed as speculative thought experiments
2. **Professional Safety**: Clear disclaimers and academic framing throughout  
3. **Rigorous Standards**: Emphasis on falsifiability and experimental validation requirements
4. **Scholarly Discussion**: Designed to stimulate academic conversation without career risk

## Specific Conventions

1. **File Organization**: Logical grouping by content type (theory, simulations, docs, etc.)
2. **Professional Naming**: Consistent kebab-case for directories, descriptive filenames
3. **Unicode in Code**: Use unicode mathematical symbols appropriately (ρ, Ψ, α)
4. **Documentation Style**: Comprehensive docstrings explaining both implementation and theory
5. **Academic Tone**: Professional presentation suitable for academic review

## External Dependencies

- Python 3.9+
- Qiskit 2.x+ and qiskit-aer (auto-installed by simulations)
- NumPy (auto-installed)
- Rich (for enhanced console output in extended simulations)
- LaTeX with AMS packages (for theory documents)

## Navigation and File Structure

- **`README.md`** - Main repository overview and navigation guide
- **`FILE_INDEX.md`** - Comprehensive index of all files with descriptions
- **`theory/`** - Organized theoretical frameworks by topic
- **`simulations/`** - Quantum simulation implementations
- **`docs/`** - Project documentation and briefings
- **`supporting-materials/`** - Transcripts, notes, implementation details
- **`archive/`** - Historical development materials and working files

When extending or modifying this codebase:
1. Maintain the theoretical integrity of the research concepts
2. Follow established file organization patterns
3. Preserve academic framing and professional presentation
4. Ensure new contributions connect appropriately to existing frameworks
5. Update FILE_INDEX.md when adding new files
