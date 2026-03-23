# Franke-filtration

The Franke filtration is a descending filtration of spaces of automorphic forms on adèlic reductive groups, defined by Jens Franke in [F98], see also [F-S98]. Its main advantage is that the quotients of the filtration can be described as parabolically induced representations. See [G12], [G25].

The app Franke Filtration allows one to compute the Franke Filtration of the spaces of automorphic forms for general linear groups. The algorithm is described in detail in [G-G]. 

This code of the app in Python is written by Lovro Greganić. The same app is available on [Langlands Programs](https://langlandsprograms.com/), ported to TypeScript by Petar Bakić with the assistance of Claude Code. 

The work on this app is supported by the Croatian Science Foundation under the projects HRZZ-IP-2022-10-4615 and DOK-NPOO-2023-10-1542, and funded by the European Union NextGenerationEU under the Juraj Dobrila University of Pula institutional research projects IIP_UNIPU_010159 and IIP_UNIPU_010162.

# User interface

Alongside `Franke_filtration.py`, which contains the main algorithm implementation, there is a user interface file `Franke_filtration_user_interface.py` that handles input for the filtration process and prints out the output.

# Notation

The input to the app is the cuspidal support given by the number of non-isomorphic unitary cuspidal automorphic representations of the general linear group, the corresponding sizes of the general linear groups, and the lists of exponents (only rational exponents are allowed).

The output of the app is the inducing data for the parabolic induction of the summands in the quotients of the Franke filtration of the space of automorphic forms on the general linear group with the cuspidal support in the given input. The inducing data are presented in the form of a list of triples $\left(\frac{a+b}{2},\quad j, \quad m_j\cdot(b-a+1)\right)$ that stand for the twisted residual or cuspidal representation $J(\rho_j,b-a+1)|\det |^{\frac{a+b}{2}}$ in the notation of [G-G], where $j=1, \dots , k$, $k$ is the number of non-isomorphic unitary cuspidal automorphic representations $\rho_j$ in the input and $m_j$ is the corresponding size of the general linear group. Beware that the symmetric algebras that should appear in every summand of every quotient of the filtration are omitted in the output, because they can be easily recovered from the form of the summands.

The output also contains an indicator in case of summands for which the invariants under certain intertwining operators should be taken. The indicator is of the form $colim[t_1,\dots ,t_r]$, where $t_j$ in the list indicates that $t_j$ copies of the same triple in the list can be permuted by the intertwining operators. Besides that, in the user interface file, the user can additionally choose the detailed description option, which allows the printing of the list of partitions in Bernstein-Zelevinsky segments of the cuspidal support, as well as all the values of $\underline{z}$ and $\iota(\underline{z})$, see [G-G].


# References

[F98] J. Franke, Harmonic analysis in weighted $L_2$-spaces, Ann. Sci. École Norm. Sup. (4) 31 (1998), no. 2, 181–279.

[F-S98] J. Franke, J. Schwermer, A decomposition of spaces of automorphic forms, and the Eisenstein cohomology of arithmetic groups, Math. Ann. 311 (1998), no. 4, 765–790. 

[G12] N. Grbac, The Franke filtration of the spaces of automorphic forms supported in a maximal proper parabolic subgroup, Glas. Mat. Ser. III 47(67) (2012), no. 2, 351–372.

[G25] N. Grbac, The Franke filtration of the spaces of automorphic forms on the symplectic group of rank two, Mem. Amer. Math. Soc. 313 (2025), no. 1592, vii+85 pp. 

[G-G] N. Grbac, L. Greganić, An algorithm for explicit calculation of the Franke filtration for the general linear group, preprint, available at http://tania.unipu.hr/~negrbac/Papers.html

[G-G24] N. Grbac, H. Grobner, Some unexpected phenomena in the Franke filtration of the space of automorphic forms of the general linear group, Israel J. Math. 263 (2024), no. 1, 301–347.
