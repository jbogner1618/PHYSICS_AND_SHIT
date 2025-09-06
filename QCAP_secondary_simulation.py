#!/usr/bin/env python
"""
lab_sim.py — Pelican’s Perspective quantum-lab console  v5.0.1
(no ASCII art)
"""

from __future__ import annotations
import argparse, csv, json, importlib, pathlib, subprocess, sys, time
from dataclasses import dataclass
from typing import Dict, List, Tuple

# ──────────────────────────────────────────────────────────────
# Lazy imports (auto-install if missing)
# ──────────────────────────────────────────────────────────────
def _ensure(mod: str, pip: str | None = None):
    try:
        return importlib.import_module(mod)
    except ModuleNotFoundError:
        pkg = pip or mod
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
        return importlib.import_module(mod)

np      = _ensure("numpy")
qiskit  = _ensure("qiskit")
_       = _ensure("qiskit_aer", "qiskit-aer")
rich    = _ensure("rich")

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, phase_damping_error
from rich.console import Console
from rich.table   import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn

console = Console()

# ──────────────────────────────────────────────────────────────
# Data containers
# ──────────────────────────────────────────────────────────────
@dataclass
class Trial:
    test: str
    plv: float
    value: float
    sigma2: float

_SIM_CACHE: Dict[float, Tuple[AerSimulator, float]] = {}

def get_sim(plv: float) -> Tuple[AerSimulator, float]:
    if plv in _SIM_CACHE:
        return _SIM_CACHE[plv]
    sigma2 = 1e-6 * (1 + 5 * (plv - 0.5))
    nm = NoiseModel()
    nm.add_all_qubit_quantum_error(phase_damping_error(sigma2),
                                   ["id", "rz", "sx", "x", "u"])
    sim = AerSimulator(noise_model=nm)
    _SIM_CACHE[plv] = (sim, sigma2)
    return sim, sigma2

# ──────────────────────────────────────────────────────────────
# Physics routines
# ──────────────────────────────────────────────────────────────
_BELL = QuantumCircuit(2); _BELL.h(0); _BELL.cx(0, 1)
_CHSH = {"AB": (0.0, np.pi/8), "A'B": (np.pi/4, np.pi/8),
         "AB'": (0.0, 3*np.pi/8), "A'B'": (np.pi/4, 3*np.pi/8)}

def _corr(ct):
    tot = sum(ct.values()) or 1
    p = {k: ct.get(k,0)/tot for k in ("00","01","10","11")}
    return p["00"] + p["11"] - p["01"] - p["10"]

def _chsh(sim, shots):
    E = {}
    for k,(a,b) in _CHSH.items():
        qc = _BELL.copy(); qc.ry(2*a,0); qc.ry(2*b,1); qc.measure_all()
        ct = sim.run(transpile(qc,sim), shots=shots).result().get_counts()
        E[k] = _corr(ct)
    return E["AB"] + E["A'B"] + E["AB'"] - E["A'B'"]

def _ramsey(sim, shots, delay=1000):
    qc = QuantumCircuit(1,1)
    qc.h(0); qc.delay(delay,0,"ns"); qc.h(0); qc.measure(0,0)
    ct = sim.run(transpile(qc,sim), shots=shots).result().get_counts()
    c  = abs(ct.get("0",0)-ct.get("1",0))/shots
    c  = max(c,1e-12)
    return np.sqrt(-2*np.log(c))/(2*np.pi*delay*1e-9)

def _echo(sim, shots, tau=500):
    qc = QuantumCircuit(1,1)
    qc.h(0); qc.delay(tau,0,"ns"); qc.x(0); qc.delay(tau,0,"ns"); qc.h(0); qc.measure(0,0)
    ct = sim.run(transpile(qc,sim), shots=shots).result().get_counts()
    c = abs(ct.get("0",0)-ct.get("1",0))/shots
    return -tau/np.log(max(c,1e-12))

def _t1(sim, shots, wait=2000):
    qc = QuantumCircuit(1,1)
    qc.x(0); qc.delay(wait,0,"ns"); qc.measure(0,0)
    ct = sim.run(transpile(qc,sim), shots=shots).result().get_counts()
    p1 = ct.get("1",0)/shots
    return -wait/np.log(max(p1,1e-12))

def _purity(sim, shots):
    vals=[]
    for p in ("x","y","z"):
        qc=QuantumCircuit(1,1)
        if p=="x": qc.h(0)
        if p=="y": qc.sdg(0); qc.h(0)
        qc.measure(0,0)
        ct = sim.run(transpile(qc,sim), shots=shots).result().get_counts()
        vals.append((ct.get("0",0)-ct.get("1",0))/shots)
    return np.linalg.norm(vals)

_TESTS = {
    "chsh":   ("CHSH S",        _chsh),
    "ramsey": ("Δν (Hz)",       _ramsey),
    "echo":   ("T₂_echo (ns)",  _echo),
    "t1":     ("T₁ (ns)",       _t1),
    "purity": ("Bloch |r|",     _purity),
}

# ──────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────
def run_tests(plv: float, shots: int, choice: List[str]) -> List[Trial]:
    sim, sigma2 = get_sim(plv); rows=[]
    with Progress(SpinnerColumn(), TextColumn("[cyan]PLV {task.fields[plv]:.2f}"),
                  BarColumn(), TimeElapsedColumn(),
                  console=console, transient=True) as prog:
        task = prog.add_task("", total=len(choice), plv=plv)
        for k in choice:
            label, fn = _TESTS[k]; val = fn(sim, shots)
            rows.append(Trial(label, plv, val, sigma2))
            prog.advance(task)
    return rows

def table(rows: List[Trial]):
    t = Table(header_style="bold magenta")
    t.add_column("PLV", justify="right")
    t.add_column("Test")
    t.add_column("Value", justify="right")
    t.add_column("σ²", justify="right")
    for r in rows:
        t.add_row(f"{r.plv:.2f}", r.test, f"{r.value:.3g}", f"{r.sigma2:.1e}")
    console.print(t)

def save(rows: List[Trial], path: pathlib.Path):
    if path.suffix.lower()==".csv":
        new = not path.exists()
        with path.open("a", newline="") as f:
            w = csv.writer(f); 
            if new: w.writerow(["test","plv","value","sigma2"])
            for r in rows: w.writerow([r.test,r.plv,r.value,r.sigma2])
    elif path.suffix.lower()==".json":
        data=[r.__dict__ for r in rows]
        if path.exists(): data=json.loads(path.read_text())+data
        path.write_text(json.dumps(data,indent=2))

# ──────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────
def parse():
    p = argparse.ArgumentParser(description="Pelican’s Perspective quantum-lab")
    p.add_argument("--plv", nargs="*", type=float)
    p.add_argument("--range", nargs=3, type=float, metavar=("START","STOP","STEP"))
    p.add_argument("--test", nargs="*", choices=list(_TESTS)+["all"])
    p.add_argument("--shots", type=int, default=4096)
    p.add_argument("--out", type=pathlib.Path)
    p.add_argument("--list", action="store_true")
    p.add_argument("--clear-cache", action="store_true")
    return p.parse_args()

def main():
    args=parse()
    if args.list:
        for k,(lbl,_) in _TESTS.items(): console.print(f"{k:<7} {lbl}")
        return
    if args.clear_cache: _SIM_CACHE.clear()
    plvs=[]
    if args.plv: plvs+=args.plv
    if args.range:
        s,e,step=args.range; plvs+=list(np.arange(s,e+1e-9,step))
    if not plvs: plvs=[float(console.input("PLV (0-1) [0.5]: ") or 0.5)]
    tests=list(_TESTS) if not args.test or "all" in args.test else args.test
    rows=[]
    for p in plvs: rows+=run_tests(p,args.shots,tests)
    table(rows)
    if args.out: save(rows,args.out); console.print(f"Logged to {args.out}")

if __name__=="__main__":
    main()
