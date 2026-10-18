#!/usr/bin/env python3
"""Deterministic finite checks for the written analytical results.

The script validates explicit matrices and spectra. It does not prove the
universal inequalities, asymptotic optimality, or absence of prior results.
"""

from __future__ import annotations

import math
import numpy as np


ATOL = 2e-10
RNG = np.random.default_rng(20261018)
COUNTS: dict[str, int] = {}


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    COUNTS[name] = COUNTS.get(name, 0) + 1


def close(name: str, actual, expected, atol: float = ATOL) -> None:
    check(name, bool(np.allclose(actual, expected, atol=atol, rtol=atol)))


def basis(d: int) -> list[np.ndarray]:
    out = []
    for j in range(d):
        for k in range(j + 1, d):
            a = np.zeros((d, d), dtype=complex)
            a[j, k] = a[k, j] = 1 / math.sqrt(2)
            out.append(a)
            a = np.zeros((d, d), dtype=complex)
            a[j, k], a[k, j] = -1j / math.sqrt(2), 1j / math.sqrt(2)
            out.append(a)
    for k in range(1, d):
        diagonal = np.zeros(d)
        diagonal[:k], diagonal[k] = 1, -k
        out.append(np.diag(diagonal / math.sqrt(k * (k + 1))).astype(complex))
    return out


def gap_matrix(states, weights) -> np.ndarray:
    d = len(states[0])
    b = basis(d)
    q = np.zeros((d * d - 1, d * d - 1), dtype=complex)
    for p, psi in zip(weights, states):
        complement = np.eye(d) - np.outer(psi, psi.conj())
        w = np.column_stack([complement @ a @ psi for a in b])
        q += p * w.conj().T @ w
    return q


def survival_errors(kraus, states) -> np.ndarray:
    return np.array([
        1 - sum(abs(np.vdot(psi, k @ psi)) ** 2 for k in kraus)
        for psi in states
    ])


def risk(kraus) -> float:
    d = len(kraus[0])
    return float(1 - (d + sum(abs(np.trace(k)) ** 2 for k in kraus)) / (d * (d + 1)))


def sqrt_psd(a: np.ndarray) -> np.ndarray:
    w, v = np.linalg.eigh(a)
    if w.min() < -ATOL:
        raise AssertionError("positive square root input")
    return (v * np.sqrt(np.maximum(w, 0))) @ v.conj().T


def random_channel(d: int, rank: int = 3) -> list[np.ndarray]:
    z = RNG.normal(size=(rank * d, d)) + 1j * RNG.normal(size=(rank * d, d))
    q, _ = np.linalg.qr(z)
    return [q[j * d:(j + 1) * d] for j in range(rank)]


def random_states(d: int, count: int) -> list[np.ndarray]:
    states = []
    for _ in range(count):
        v = RNG.normal(size=d) + 1j * RNG.normal(size=d)
        states.append(v / np.linalg.norm(v))
    return states


def simplex(d: int) -> list[np.ndarray]:
    return [np.exp(2j * np.pi * k * np.arange(d) / (d + 1)) / math.sqrt(d)
            for k in range(d + 1)]


def union_probability(z) -> float:
    z = np.asarray(z, dtype=float)
    if np.any(z >= 1):
        return 1.0
    return float(-np.expm1(np.log1p(-z).sum()))


def run() -> None:
    zero = np.array([1, 0], dtype=complex)
    one = np.array([0, 1], dtype=complex)
    plus = (zero + one) / math.sqrt(2)
    states3 = [zero, plus, one]
    weights = np.array([0.3, 0.4, 0.3])
    ident = np.eye(2, dtype=complex)
    jump = np.array([[0, 1], [0, 1]], dtype=complex)

    # A complex coefficient vector in a Hermitian basis represents arbitrary
    # complex matrices. The gap is not restricted to Hermitian witnesses.
    close("two-ray variance spectrum",
          np.linalg.eigvalsh(gap_matrix(states3[:2], [0.5, 0.5])), [0, 0.25, 0.75])
    close("three-ray optimized gap",
          np.linalg.eigvalsh(gap_matrix(states3, weights))[0], 0.1)
    for t in [0.2, 0.05, 0.01, 0.001]:
        s = math.sqrt(1 - 2 * t)
        ks = [np.diag([1, s]).astype(complex), math.sqrt(t) * jump]
        errs = survival_errors(ks, states3)
        eps = t * t / (2 * (1 + s) ** 2)
        close("witness trace preservation", sum(k.conj().T @ k for k in ks), ident)
        close("witness individual losses", errs, [0, t * t / (1 + s) ** 2, t])
        close("exact square-root curve", risk(ks), math.sqrt(2 * eps) - 2 * eps / 3)
        close("nonunital commutator", sum(k @ k.conj().T for k in ks) - ident,
              t * (jump @ jump.conj().T - jump.conj().T @ jump))
        v = np.zeros((4, 2), dtype=complex)
        v[0, 0], v[2, 1], v[1, 1], v[3, 1] = 1, s, math.sqrt(t), math.sqrt(t)
        close("physical isometry", v.conj().T @ v, ident)
        close("physical no-jump Kraus", v[[0, 2], :], ks[0])
        close("physical jump Kraus", v[[1, 3], :], ks[1])

    # Direct diagonalization is independent of the closed eigenvalue formulas.
    for d in [2, 3, 4, 8]:
        b = basis(d)
        close("traceless basis orthonormality",
              [[np.trace(a.conj().T @ c) for c in b] for a in b], np.eye(d * d - 1))
        states = [np.eye(d, dtype=complex)[:, j] for j in range(d)]
        states.append(np.ones(d, dtype=complex) / math.sqrt(d))
        bopt = (1 + math.sqrt(d - 1)) / (d + 1 + 2 * math.sqrt(d - 1))
        for last_weight in [1 / (d + 1), bopt]:
            a = (1 - last_weight) / d
            q = gap_matrix(states, [a] * d + [last_weight])
            disc = math.sqrt((a + last_weight) ** 2 - 4 * a * last_weight / d)
            lo, hi = (a + last_weight - disc) / 2, (a + last_weight + disc) / 2
            expected = sorted([a] * ((d - 1) ** 2) + [lo] * (d - 1) + [hi] * (d - 1))
            close("basis-plus-uniform full spectrum", np.linalg.eigvalsh(q), expected)
        close("optimized weight formula", np.linalg.eigvalsh(q)[0],
              1 / (d * (d + 1 + 2 * math.sqrt(d - 1))))
        tight = simplex(d)
        close("simplex tightness", sum(np.outer(v, v.conj()) for v in tight) / (d + 1),
              np.eye(d) / d)
        close("simplex optimal gap", np.linalg.eigvalsh(gap_matrix(tight, [1 / (d + 1)] * (d + 1)))[0],
              1 / (d * d))

    # Explicit minimax mixture for a qubit trine. The Bloch vectors lie in XY.
    trine = simplex(2)
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    for t in [0.01, 0.1, 0.4]:
        ks = [math.sqrt(1 - t / 2) * ident, math.sqrt(t) * sx / 2, math.sqrt(t) * sy / 2]
        close("trine minimax trace preservation", sum(k.conj().T @ k for k in ks), ident)
        close("trine common probe error", survival_errors(ks, trine), [t / 4] * 3)
        close("trine minimax risk", risk(ks), t / 3)

    # Finite unbalanced configurations and channel samples, not a proof of the
    # universal support bound. A fixed seed makes the checks reproducible.
    for d in [2, 3, 4]:
        for _ in range(8):
            count = d + 2
            states = random_states(d, count)
            p = RNG.uniform(0.05, 1, count)
            p /= p.sum()
            q = gap_matrix(states, p)
            mu = float(np.linalg.eigvalsh(q)[0])
            cap = min((count - d) / (d * (count - 1)), 1 / (d + 1))
            check("unbalanced support inequality", mu <= cap + ATOL)
            ks = random_channel(d)
            errors = survival_errors(ks, states)
            check("CPTP linear inequality", risk(ks) <= float(p @ errors) / ((d + 1) * mu) + ATOL)
            direct = sum(np.linalg.norm(k - np.trace(k) * np.eye(d) / d, "fro") ** 2 for k in ks)
            close("Kraus risk identity", risk(ks), direct / (d + 1))

    # Approach the sharp weighted qubit ratio using the gap eigenoperator.
    eigenvalues, eigenvectors = np.linalg.eigh(gap_matrix(states3, weights))
    l = sum(c * a for c, a in zip(eigenvectors[:, 0], basis(2)))
    t = 1e-5
    ks = [sqrt_psd(ident - t * l.conj().T @ l), math.sqrt(t) * l]
    local_errors = survival_errors(ks, states3)
    local_risk = risk(ks)
    close("linear coefficient approached", local_risk / float(weights @ local_errors), 10 / 3, atol=5e-4)
    for n in [1, 2, 8, 32, 128]:
        factor = 1 / (1 + 2.0 ** (-n))
        ratio = factor * (3 / 2) * local_risk / float(weights @ local_errors)
        close("product sharp coefficient approached", ratio, 5 * factor, atol=8e-4)
        for delta in [0.1, 0.01, 0.001]:
            x_goal = -math.expm1(math.log1p(-delta / factor) / n)
            low, high = 0.0, 0.25
            for _ in range(70):
                mid = (low + high) / 2
                s = math.sqrt(1 - 2 * mid)
                x = mid / (1 + s) + mid / 4
                if x < x_goal:
                    low = mid
                else:
                    high = mid
            t = (low + high) / 2
            s = math.sqrt(1 - 2 * t)
            x = t / (1 + s) + t / 4
            eplus = t * t / (1 + s) ** 2
            bglobal = -math.expm1(n * math.log1p(-eplus))
            close("product witness calibrated risk", factor * (-math.expm1(n * math.log1p(-x))), delta)
            check("uniform witness parameter bounds", delta / n - ATOL <= t <= 8 * delta / (3 * n) + ATOL)
            check("uniform global error bound", bglobal <= 32 * delta * delta / (9 * n) + ATOL)

    for n in [1, 2, 4, 8]:
        factor = 1 / (1 + 2.0 ** (-n))
        for _ in range(12):
            xs, ys = [], []
            for j in range(n):
                raw = random_channel(2)
                mixing = [0.001, 0.05, 0.4][j % 3]
                ks = [math.sqrt(1 - mixing) * ident] + [math.sqrt(mixing) * k for k in raw]
                xs.append(1.5 * risk(ks))
                ys.append(survival_errors(ks, states3))
            ys = np.array(ys)
            global_errors = np.array([union_probability(ys[:, r]) for r in range(3)])
            global_risk = factor * union_probability(xs)
            check("nonidentical product channel bound", global_risk <= 5 * factor * float(weights @ global_errors) + ATOL)

    for name, count in COUNTS.items():
        print(f"PASS {name}: {count}")
    print(f"PASS {sum(COUNTS.values())} finite checks in {len(COUNTS)} groups")


if __name__ == "__main__":
    run()
