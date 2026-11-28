#!/usr/bin/env python3
"""D2 — recalcul indépendant des coefficients de la branche résistante (lecture seule, Python standard).

Formules de l'annexe D (l. 396–805) ; paramètres de référence de l'annexe F (l. 132) et w de l'annexe D (l. 50).
  m(r)   = (1+r^2)/(1+(1+λ)r^2)            m'(r), m''(r) (l. 407, 426)
  r_c    = τ_ign = sqrt((1-ζ)/(ζ(1+λ)-1))   (annexe C l. 806)
  A = √2 α/β,  B = √2 w/β                    (l. 455)
  G(x,g) = m(r(x,g)) - ζ tanh(x)/x,  r(x,g) = √2(α tanh x + g w)/β
  a_1 = m_1 B, a_2 = m_1 A, a_xx = m_2 A^2/2 + ζ/3, a_xg = m_2 A B, a_gg = m_2 B^2/2   (l. 678–700)
  c_1 = -B/A = -w/α ;  c_2 = -(a_xx c_1^2 + a_xg c_1 + a_gg)/a_2                         (l. 726–746)
Forme simplifiée : les termes en m_2 valent (m_2/2)(A c_1 + B)^2 = 0 exactement, d'où c_2 = -ζ c_1^2/(3 m_1 A).
Contrôle : racine non nulle de G(x, g_c+δ)=0 par Newton pour δ petits, comparée au développement.
Usage : python3 -I audits/G0/G0_03_crosswalk/D2_resistant_branch_check.py
"""
import math

ZETA, LAM, ALPHA, BETA, W = 0.8, 2.0, 0.45, 0.12, 0.98006


def coeffs(zeta=ZETA, lam=LAM, alpha=ALPHA, beta=BETA, w=W):
    rc = math.sqrt((1 - zeta) / (zeta * (1 + lam) - 1))
    den = 1 + (1 + lam) * rc ** 2
    m1 = -2 * lam * rc / den ** 2
    m2 = -2 * lam * (1 - 3 * (1 + lam) * rc ** 2) / den ** 3
    A = math.sqrt(2) * alpha / beta
    B = math.sqrt(2) * w / beta
    a1, a2 = m1 * B, m1 * A
    axx, axg, agg = m2 * A ** 2 / 2 + zeta / 3, m2 * A * B, m2 * B ** 2 / 2
    c1 = -B / A
    contrib = (axx * c1 ** 2, axg * c1, agg)
    c2_full = -sum(contrib) / a2
    m2part = m2 / 2 * (A * c1 + B) ** 2
    c2_simpl = -zeta * c1 ** 2 / (3 * m1 * A)
    gc = beta * rc / (math.sqrt(2) * w)
    return dict(rc=rc, m1=m1, m2=m2, A=A, B=B, a1=a1, a2=a2, axx=axx, axg=axg, agg=agg, c1=c1,
                contrib=contrib, c2_full=c2_full, c2_simpl=c2_simpl, m2part=m2part, gc=gc)


def G(x, g, zeta=ZETA, lam=LAM, alpha=ALPHA, beta=BETA, w=W):
    r = math.sqrt(2) * (alpha * math.tanh(x) + g * w) / beta
    return (1 + r * r) / (1 + (1 + lam) * r * r) - zeta * math.tanh(x) / x


def root(g, x0):
    x = x0
    for _ in range(80):
        h = 1e-9
        d = (G(x + h, g) - G(x - h, g)) / (2 * h)
        nx = x - G(x, g) / d
        if abs(nx - x) < 1e-15:
            break
        x = nx
    return x


def main():
    c = coeffs()
    print('r_c = %.15f' % c['rc'])
    print('m_1 = %.15f   m_2 = %.15f' % (c['m1'], c['m2']))
    print('A   = %.15f   B   = %.15f' % (c['A'], c['B']))
    print('g_c = %.15f' % c['gc'])
    print('c_1 = %.15f   (-w/α)' % c['c1'])
    print('a_xx = %.5f  a_xg = %.5f  a_gg = %.5f' % (c['axx'], c['axg'], c['agg']))
    print('contributions au numérateur : %.2f  %.2f  %.2f  (somme %.6f)' % (*c['contrib'], sum(c['contrib'])))
    print('partie en m_2 : (m_2/2)(A c_1 + B)^2 = %.3e  (nulle à l\'arrondi machine près)' % c['m2part'])
    print('c_2 (formule complète)   = %.15f' % c['c2_full'])
    print('c_2 (forme simplifiée)   = %.15f' % c['c2_simpl'])
    print('arrondis : c_1 = %.4f ; c_2 = %.4f' % (c['c1'], c['c2_full']))
    print('\ncontrôle par Newton (racine non nulle de G(x,g_c+δ)=0) :')
    print('   δ          x_num              c1δ+c2δ²           écart / δ³')
    for d in (1e-2, 5e-3, 2e-3, 1e-3):
        x = root(c['gc'] + d, c['c1'] * d)
        pred = c['c1'] * d + c['c2_full'] * d * d
        print('  %.0e  %.12f  %.12f  %.4f' % (d, x, pred, (x - pred) / d ** 3))
    print('\nhypothèse non vérifiée sur l\'origine des valeurs anciennes :')
    for w in (0.98, 0.98006):
        k = coeffs(w=w)
        print('  w = %.5f : c_1 = %.5f ; c_2 = %.5f' % (w, k['c1'], k['c2_full']))


if __name__ == '__main__':
    main()
