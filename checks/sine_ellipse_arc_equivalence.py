#!/usr/bin/env python3
"""Cross-check a specially scaled sine period against an ellipse perimeter."""
from __future__ import annotations
import json
import mpmath as mp


def sine_period_arc_length(a, b):
    """Integrate one sine period directly; return the equivalent ellipse perimeter.

    For y=A*sin(k*x), A=sqrt(a^2-b^2), k=1/b, the full period is
    2*pi*b.  This is a constructed equivalence, not an identity for an
    arbitrarily scaled sine curve.  mpmath.ellipe uses parameter m=k^2.
    """
    with mp.workdps(50):
        a = mp.mpf(a)
        b = mp.mpf(b)
        if not a > b > 0:
            raise ValueError("This real-valued ellipse family requires a>b>0")
        amplitude = mp.sqrt(a**2 - b**2)
        wave_number = 1 / b
        slope_scale = amplitude * wave_number
        elliptic_parameter = slope_scale**2 / (1 + slope_scale**2)
        period = 2 * mp.pi / wave_number
        quarter_period = period / 4
        integrand = lambda x: mp.sqrt(1 + slope_scale**2 * mp.cos(wave_number * x)**2)
        direct = mp.quad(integrand, [0, quarter_period, 2 * quarter_period, 3 * quarter_period, period])
        ellipse = 4 * a * mp.ellipe(1 - b**2 / a**2)
        return {
            "amplitude": amplitude,
            "waveNumber": wave_number,
            "period": period,
            "directArcLength": direct,
            "ellipsePerimeter": ellipse,
            "ellipticParameter": elliptic_parameter,
            "absoluteDiscrepancy": abs(direct - ellipse),
        }


def main() -> None:
    result = sine_period_arc_length(2, 1)
    serialized = {key: float(value) for key, value in result.items()}
    print(json.dumps({
        "schemaVersion": "sine-ellipse-arc-equivalence/v1",
        "sourceId": "9547914574",
        "a": 2.0,
        "b": 1.0,
        **serialized,
        "equivalenceRequiresSpecifiedAmplitudeAndPeriod": True,
        "arbitrarySineCurveHasThisLength": False,
        "independentPhysicalTheoryEstablished": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
