# `Easyunfold` Documentation

![build](https://github.com/SMTG-UCL/easyunfold/actions/workflows/ci.yaml/badge.svg)
[![docs](https://github.com/SMTG-UCL/easyunfold/actions/workflows/docs.yaml/badge.svg)](https://smtg-ucl.github.io/easyunfold/)
[![codecov](https://codecov.io/gh/SMTG-UCL/easyunfold/branch/main/graph/badge.svg?token=XLLWWU5UM2)](https://codecov.io/gh/SMTG-UCL/easyunfold)
[![PyPI](https://img.shields.io/pypi/v/easyunfold)](https://pypi.org/project/easyunfold)
[![Downloads](https://img.shields.io/pypi/dm/easyunfold)](https://smtg-ucl.github.io/easyunfold/)
<!--- When JOSS submitted, add this: [![JOSS](https://joss.theoj.org/papers/10.21105/joss.04817/status.
svg)](https://doi.org/10.21105/joss.)--->

This package is intended for obtaining the effective band structure of a supercell for a certain _k_-point
path of the primitive cell. It was originally based on 
[PyVaspwfc](https://github.com/QijingZheng/VaspBandUnfolding) for reading VASP wavefunction outputs, 
with a notable improvement being that symmetry-breaking is properly accounted for by sampling necessary 
additional _k_-points and averaging accordingly.

Our goal is to implement the band structure unfolding workflow in a robust and user-friendly software 
package.

For the methodology of supercell band unfolding, see 
[here](https://link.aps.org/doi/10.1103/PhysRevB.85.085201).

## Usage

To generate an unfolded band structure, one typically needs to perform the following steps:

1. Create a primitive unit cell, and generate a band structure _k_-point path corresponding to this 
   primitive cell.
2. Create a supercell (e.g. disordered, defective, surface slab etc.), and obtain its optimised structure.
3. Generate a series of _k_-points for the supercell to be calculated.
4. Perform a band structure calculation with the supercell, and save its wavefunction output to file.
5. Post-process the supercell wavefunction to obtain the unfolded band structure in the _k_-point path 
   of the primitive unit cell.

These generation and analysis steps are automated in `easyunfold`, with only the primitive unit cell and 
supercell structures required as inputs from the user.

Typically, the supercell comprises some form of symmetry-breaking relative to the primitive cell, such 
as defects, disorder (e.g. special quasi-random structures (SQS) for site disorder – other forms of 
disorder such as magnetic, dynamic/vibrational, polar, elastic etc. also possible), or a surface/interface 
slab.
In all cases, the supercell symmetry is lowered compared to the pristine primitive cell.
Hence, for a given _k_-point path in the primitive cell Brillouin Zone, additional _k_-points are 
required to be sampled for the supercell, and the extracted spectral weights need to be appropriately 
averaged to obtain the correct effective band structure (EBS).
<!-- when JOSS submitted, add link to paper (discussion of theory) here! -->
<!--- When JOSS submitted, add 'License and Citation' section here --->

## Studies using `easyunfold`

We'll add papers that use `easyunfold` to this list as they come out!

- Y. T. Huang & S. R. Kavanagh et al. [_Nature Communications_](https://www.nature.com/articles/s41467-022-32669-3) 2022
- A. T. J. Nicolson et al. [_Journal of the Americal Chemical Society_](https://doi.org/10.1021/jacs.2c13336) 2023
- Y. Wang & S. R. Kavanagh et al. [_Nature Photonics_](https://www.nature.com/articles/s41566-021-00950-4) 2022 (early version)

## DFT code support

At the moment, easyunfold supports [VASP](https://www.vasp.at) and [CASTEP](http://www.castep.org), but most of the routines are abstracted from the code specific details.
In principle, support for other plane wave DFT code can be added by:

- Implementing a subclass of `WaveFunction` that handles reading the wave function output.
- Implementing functions for reading/writing _k_-points.
- Adding branches for dispatching based on the `dft_code` attribute of the `UnfoldKSet` object in 
  various places within the code.

The Atomic Simulation Environment ([ASE](https://wiki.fysik.dtu.dk/ase/)) is used by `easyunfold` for 
reading in structures, so structure file IO is natively supported for essentially all public DFT codes.

### Code Compatibility Notes
- Atom-projected band structures are currently only supported for `VASP` calculation outputs.
- Gamma-only and non-collinear spin calculations are not supported for `CASTEP`. 

## Contributors
- [Bonan Zhu](https://github.com/zhubonan)  
- [Seán Kavanagh](https://github.com/kavanase)  
- [Adair Nicolson](https://github.com/adair-nicolson)  

And those who helped in the development:
- [Joe Willis](https://github.com/joebesity)  
- [David O. Scanlon](http://davidscanlon.com/?page_id=5)  

## Contributing
## Bugs reports and feature requests
Bug reports and feature requests are well come.
If you found any bug or missing features please report it on the 
[Issue Tracker](https://github.com/SMTG-UCL/easyunfold/issues).

## Code contributions
We welcome your help in improving and extending the package with your
own contributions. This is managed through GitHub pull requests;
for external contributions, we prefer the
[fork and pull](https://guides.github.com/activities/forking/)
workflow while core developers use branches in the main repository:

1. First open an [Issue](https://github.com/SMTG-UCL/easyunfold/issues) to discuss the proposed 
   contribution. This discussion might include how the changes fit `easyunfold`'s scope and a
  general technical approach.
2. Make your own project fork and implement the changes
  there. Please keep your code style compliant and use the `pre-commit` hooks.
3. Open a pull request to merge the changes into the main
  project. A more detailed discussion can take place there before
  the changes are accepted.


```{toctree}
  :hidden:
  :maxdepth: 2

installation.md
guide.md
examples.md
theory.md
references.md
publications.md
cli.rst
apidocs/index
```