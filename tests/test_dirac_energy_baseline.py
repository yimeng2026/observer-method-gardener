from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks.dirac_energy_baseline import dirac_binding_expansion, dirac_total_energy, perturbative_wavefunction_norm

ALPHA = 0.0072973525693


class DiracEnergyBaselineTest(unittest.TestCase):
    def test_standard_exact_energy_matches_displayed_expansion(self):
        exact = dirac_total_energy(2, -1, ALPHA)
        binding = exact - 1
        expanded = dirac_binding_expansion(2, 0.5, ALPHA)
        self.assertAlmostEqual(exact, 0.999993343469912, delta=1e-15)
        self.assertAlmostEqual(binding, -0.000006656530087975802, delta=1e-16)
        self.assertAlmostEqual(expanded, -0.000006656530084878909, delta=1e-16)
        self.assertLess(abs(binding - expanded), 1e-14)
        self.assertLess(binding, 0)
        self.assertGreater(exact, 0)

    def test_displayed_wavefunction_correction_requires_renormalization(self):
        norm = perturbative_wavefunction_norm(0.01, 0.1)
        self.assertAlmostEqual(norm, 0.98606775, delta=1e-7)
        self.assertNotAlmostEqual(norm, 1.0)

    def test_invalid_quantum_numbers_are_rejected(self):
        for n, k in [(0, -1), (2, 0), (1, -2)]:
            with self.assertRaises(ValueError):
                dirac_total_energy(n, k, ALPHA)


if __name__ == "__main__":
    unittest.main()
