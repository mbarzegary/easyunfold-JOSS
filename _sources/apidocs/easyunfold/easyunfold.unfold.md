# {py:mod}`easyunfold.unfold`

```{py:module} easyunfold.unfold
```

```{autodoc2-docstring} easyunfold.unfold
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`UnfoldKSet <easyunfold.unfold.UnfoldKSet>`
  - ```{autodoc2-docstring} easyunfold.unfold.UnfoldKSet
    :summary:
    ```
* - {py:obj}`Unfold <easyunfold.unfold.Unfold>`
  - ```{autodoc2-docstring} easyunfold.unfold.Unfold
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`get_symmetry_dataset <easyunfold.unfold.get_symmetry_dataset>`
  - ```{autodoc2-docstring} easyunfold.unfold.get_symmetry_dataset
    :summary:
    ```
* - {py:obj}`find_K_from_k <easyunfold.unfold.find_K_from_k>`
  - ```{autodoc2-docstring} easyunfold.unfold.find_K_from_k
    :summary:
    ```
* - {py:obj}`rotate_kpt <easyunfold.unfold.rotate_kpt>`
  - ```{autodoc2-docstring} easyunfold.unfold.rotate_kpt
    :summary:
    ```
* - {py:obj}`expand_K_by_symmetry <easyunfold.unfold.expand_K_by_symmetry>`
  - ```{autodoc2-docstring} easyunfold.unfold.expand_K_by_symmetry
    :summary:
    ```
* - {py:obj}`LorentzSmearing <easyunfold.unfold.LorentzSmearing>`
  - ```{autodoc2-docstring} easyunfold.unfold.LorentzSmearing
    :summary:
    ```
* - {py:obj}`GaussianSmearing <easyunfold.unfold.GaussianSmearing>`
  - ```{autodoc2-docstring} easyunfold.unfold.GaussianSmearing
    :summary:
    ```
* - {py:obj}`remote_duplicated_kpoints <easyunfold.unfold.remote_duplicated_kpoints>`
  - ```{autodoc2-docstring} easyunfold.unfold.remote_duplicated_kpoints
    :summary:
    ```
* - {py:obj}`write_kpoints <easyunfold.unfold.write_kpoints>`
  - ```{autodoc2-docstring} easyunfold.unfold.write_kpoints
    :summary:
    ```
* - {py:obj}`read_kpoints <easyunfold.unfold.read_kpoints>`
  - ```{autodoc2-docstring} easyunfold.unfold.read_kpoints
    :summary:
    ```
* - {py:obj}`read_kpoints_line <easyunfold.unfold.read_kpoints_line>`
  - ```{autodoc2-docstring} easyunfold.unfold.read_kpoints_line
    :summary:
    ```
* - {py:obj}`make_kpath <easyunfold.unfold.make_kpath>`
  - ```{autodoc2-docstring} easyunfold.unfold.make_kpath
    :summary:
    ```
* - {py:obj}`clean_latex_string <easyunfold.unfold.clean_latex_string>`
  - ```{autodoc2-docstring} easyunfold.unfold.clean_latex_string
    :summary:
    ```
* - {py:obj}`spectral_function_from_weight_sets <easyunfold.unfold.spectral_function_from_weight_sets>`
  - ```{autodoc2-docstring} easyunfold.unfold.spectral_function_from_weight_sets
    :summary:
    ```
* - {py:obj}`spectral_weight_multiple_source <easyunfold.unfold.spectral_weight_multiple_source>`
  - ```{autodoc2-docstring} easyunfold.unfold.spectral_weight_multiple_source
    :summary:
    ```
* - {py:obj}`concatenate_scf_kpoints <easyunfold.unfold.concatenate_scf_kpoints>`
  - ```{autodoc2-docstring} easyunfold.unfold.concatenate_scf_kpoints
    :summary:
    ```
* - {py:obj}`create_white_colormap <easyunfold.unfold.create_white_colormap>`
  - ```{autodoc2-docstring} easyunfold.unfold.create_white_colormap
    :summary:
    ```
* - {py:obj}`create_white_colormap_from_existing <easyunfold.unfold.create_white_colormap_from_existing>`
  - ```{autodoc2-docstring} easyunfold.unfold.create_white_colormap_from_existing
    :summary:
    ```
* - {py:obj}`parse_atoms_idx <easyunfold.unfold.parse_atoms_idx>`
  - ```{autodoc2-docstring} easyunfold.unfold.parse_atoms_idx
    :summary:
    ```
* - {py:obj}`process_projection_options <easyunfold.unfold.process_projection_options>`
  - ```{autodoc2-docstring} easyunfold.unfold.process_projection_options
    :summary:
    ```
````

### API

````{py:function} get_symmetry_dataset(atoms: ase.Atoms, symprec: float = 1e-05)
:canonical: easyunfold.unfold.get_symmetry_dataset

```{autodoc2-docstring} easyunfold.unfold.get_symmetry_dataset
```
````

````{py:function} find_K_from_k(k: numpy.ndarray, M: numpy.ndarray)
:canonical: easyunfold.unfold.find_K_from_k

```{autodoc2-docstring} easyunfold.unfold.find_K_from_k
```
````

````{py:function} rotate_kpt(k: numpy.ndarray, opt: numpy.ndarray)
:canonical: easyunfold.unfold.rotate_kpt

```{autodoc2-docstring} easyunfold.unfold.rotate_kpt
```
````

````{py:function} expand_K_by_symmetry(kpt: typing.Union[list, numpy.ndarray], opts_pc: numpy.ndarray, opts_sc: numpy.ndarray, time_reversal: bool = True)
:canonical: easyunfold.unfold.expand_K_by_symmetry

```{autodoc2-docstring} easyunfold.unfold.expand_K_by_symmetry
```
````

`````{py:class} UnfoldKSet(M: numpy.ndarray, kpts_pc: list, pc_latt: numpy.ndarray, pc_opts: numpy.ndarray, sc_opts: numpy.ndarray, time_reversal: bool = True, expand: bool = True, metadata: typing.Union[None, dict] = None, expansion_results: typing.Union[None, dict] = None, calculated_quantities: typing.Union[None, dict] = None, kpoint_labels: typing.Union[None, list] = None)
:canonical: easyunfold.unfold.UnfoldKSet

Bases: {py:obj}`monty.json.MSONable`

```{autodoc2-docstring} easyunfold.unfold.UnfoldKSet
```

```{rubric} Initialization
```

```{autodoc2-docstring} easyunfold.unfold.UnfoldKSet.__init__
```

````{py:attribute} _VERSION
:canonical: easyunfold.unfold.UnfoldKSet._VERSION
:value: >
   '0.1.0'

```{autodoc2-docstring} easyunfold.unfold.UnfoldKSet._VERSION
```

````

````{py:property} is_calculated
:canonical: easyunfold.unfold.UnfoldKSet.is_calculated
:type: bool

```{autodoc2-docstring} easyunfold.unfold.UnfoldKSet.is_calculated
```

````

````{py:property} has_averaged_spectral_weights
:canonical: easyunfold.unfold.UnfoldKSet.has_averaged_spectral_weights
:type: bool

```{autodoc2-docstring} easyunfold.unfold.UnfoldKSet.has_averaged_spectral_weights
```

````

````{py:method} from_atoms(M: numpy.ndarray, kpts_pc: list, pc: ase.Atoms, sc: ase.Atoms, time_reversal: bool = True, expand=True, symprec: float = 1e-05)
:canonical: easyunfold.unfold.UnfoldKSet.from_atoms
:classmethod:

```{autodoc2-docstring} easyunfold.unfold.UnfoldKSet.from_atoms
```

````

````{py:method} from_file(fname: str)
:canonical: easyunfold.unfold.UnfoldKSet.from_file
:classmethod:

```{autodoc2-docstring} easyunfold.unfold.UnfoldKSet.from_file
```

````

````{py:method} expand_pc_kpoints() -> None
:canonical: easyunfold.unfold.UnfoldKSet.expand_pc_kpoints

```{autodoc2-docstring} easyunfold.unfold.UnfoldKSet.expand_pc_kpoints
```

````

````{py:method} __repr__() -> str
:canonical: easyunfold.unfold.UnfoldKSet.__repr__

````

````{py:property} nsymm_orig
:canonical: easyunfold.unfold.UnfoldKSet.nsymm_orig
:type: int

```{autodoc2-docstring} easyunfold.unfold.UnfoldKSet.nsymm_orig
```

````

````{py:property} nsymm_expand
:canonical: easyunfold.unfold.UnfoldKSet.nsymm_expand
:type: int

```{autodoc2-docstring} easyunfold.unfold.UnfoldKSet.nsymm_expand
```

````

````{py:property} nkpts_orig
:canonical: easyunfold.unfold.UnfoldKSet.nkpts_orig
:type: int

```{autodoc2-docstring} easyunfold.unfold.UnfoldKSet.nkpts_orig
```

````

````{py:property} nkpts_expand
:canonical: easyunfold.unfold.UnfoldKSet.nkpts_expand
:type: int

```{autodoc2-docstring} easyunfold.unfold.UnfoldKSet.nkpts_expand
```

````

````{py:method} generate_sc_kpoints() -> None
:canonical: easyunfold.unfold.UnfoldKSet.generate_sc_kpoints

```{autodoc2-docstring} easyunfold.unfold.UnfoldKSet.generate_sc_kpoints
```

````

````{py:method} write_sc_kpoints(file: str, nk_per_split: typing.Union[None, list] = None, scf_kpoints_and_weights: typing.Union[None, list] = None)
:canonical: easyunfold.unfold.UnfoldKSet.write_sc_kpoints

```{autodoc2-docstring} easyunfold.unfold.UnfoldKSet.write_sc_kpoints
```

````

````{py:method} write_pc_kpoints(file: str, expanded: bool = False)
:canonical: easyunfold.unfold.UnfoldKSet.write_pc_kpoints

```{autodoc2-docstring} easyunfold.unfold.UnfoldKSet.write_pc_kpoints
```

````

````{py:method} _read_weights(wavecar: typing.Union[str, typing.List[str]], gamma: bool, ncl: bool, gamma_half: str)
:canonical: easyunfold.unfold.UnfoldKSet._read_weights

```{autodoc2-docstring} easyunfold.unfold.UnfoldKSet._read_weights
```

````

````{py:method} load_procar(procar: typing.Union[str, typing.List[str]], force: bool = False)
:canonical: easyunfold.unfold.UnfoldKSet.load_procar

```{autodoc2-docstring} easyunfold.unfold.UnfoldKSet.load_procar
```

````

````{py:method} _construct_procar_kmap() -> list
:canonical: easyunfold.unfold.UnfoldKSet._construct_procar_kmap

```{autodoc2-docstring} easyunfold.unfold.UnfoldKSet._construct_procar_kmap
```

````

````{py:property} procars
:canonical: easyunfold.unfold.UnfoldKSet.procars
:type: typing.Union[None, easyunfold.procar.Procar]

```{autodoc2-docstring} easyunfold.unfold.UnfoldKSet.procars
```

````

````{py:property} procar_kmaps
:canonical: easyunfold.unfold.UnfoldKSet.procar_kmaps

```{autodoc2-docstring} easyunfold.unfold.UnfoldKSet.procar_kmaps
```

````

````{py:method} _get_spectral_weights(wavecar, npoints=2000, sigma=0.01, emin=None, emax=None, gamma=False, ncl=False, gamma_half='x', also_spectral_function=False, atoms_idx=None, orbitals=None, symm_average=True)
:canonical: easyunfold.unfold.UnfoldKSet._get_spectral_weights

```{autodoc2-docstring} easyunfold.unfold.UnfoldKSet._get_spectral_weights
```

````

````{py:method} get_band_weight_sets(atoms_idx: typing.List[int], orbitals: typing.List[typing.Union[typing.List[str], str]], procars: typing.Union[None, typing.List[str], str] = None) -> list
:canonical: easyunfold.unfold.UnfoldKSet.get_band_weight_sets

```{autodoc2-docstring} easyunfold.unfold.UnfoldKSet.get_band_weight_sets
```

````

````{py:method} get_spectral_function(wavecar: typing.Union[None, easyunfold.wavecar.Wavecar] = None, npoints: int = 2000, sigma: float = 0.1, gamma: bool = False, ncl: bool = False, gamma_half: str = 'x', symm_average: bool = True, atoms_idx: typing.Union[None, typing.List[int]] = None, orbitals: typing.Union[None, str, typing.List[str]] = None)
:canonical: easyunfold.unfold.UnfoldKSet.get_spectral_function

```{autodoc2-docstring} easyunfold.unfold.UnfoldKSet.get_spectral_function
```

````

````{py:method} get_spectral_weights(wavecar=None, gamma: bool = False, ncl: bool = False, gamma_half: str = 'x', symm_average: bool = True)
:canonical: easyunfold.unfold.UnfoldKSet.get_spectral_weights

```{autodoc2-docstring} easyunfold.unfold.UnfoldKSet.get_spectral_weights
```

````

````{py:method} as_dict() -> dict
:canonical: easyunfold.unfold.UnfoldKSet.as_dict

```{autodoc2-docstring} easyunfold.unfold.UnfoldKSet.as_dict
```

````

````{py:method} get_kpoint_distances()
:canonical: easyunfold.unfold.UnfoldKSet.get_kpoint_distances

```{autodoc2-docstring} easyunfold.unfold.UnfoldKSet.get_kpoint_distances
```

````

`````

````{py:function} LorentzSmearing(x, x0, sigma=0.02)
:canonical: easyunfold.unfold.LorentzSmearing

```{autodoc2-docstring} easyunfold.unfold.LorentzSmearing
```
````

````{py:function} GaussianSmearing(x, x0, sigma=0.02)
:canonical: easyunfold.unfold.GaussianSmearing

```{autodoc2-docstring} easyunfold.unfold.GaussianSmearing
```
````

````{py:function} remote_duplicated_kpoints(kpoints: list, return_map=False, decimals=6)
:canonical: easyunfold.unfold.remote_duplicated_kpoints

```{autodoc2-docstring} easyunfold.unfold.remote_duplicated_kpoints
```
````

````{py:function} write_kpoints(kpoints: typing.Union[numpy.ndarray, list], outpath: str = 'KPOINTS', comment: str = '', weights: typing.Union[None, typing.List[float]] = None)
:canonical: easyunfold.unfold.write_kpoints

```{autodoc2-docstring} easyunfold.unfold.write_kpoints
```
````

````{py:function} read_kpoints(path='KPOINTS')
:canonical: easyunfold.unfold.read_kpoints

```{autodoc2-docstring} easyunfold.unfold.read_kpoints
```
````

````{py:function} read_kpoints_line(content, density=20)
:canonical: easyunfold.unfold.read_kpoints_line

```{autodoc2-docstring} easyunfold.unfold.read_kpoints_line
```
````

````{py:function} make_kpath(kbound: typing.List[float], nseg=40)
:canonical: easyunfold.unfold.make_kpath

```{autodoc2-docstring} easyunfold.unfold.make_kpath
```
````

````{py:function} clean_latex_string(label: str)
:canonical: easyunfold.unfold.clean_latex_string

```{autodoc2-docstring} easyunfold.unfold.clean_latex_string
```
````

````{py:function} spectral_function_from_weight_sets(spectral_weight_sets: numpy.ndarray, kweight_sets: list, nedos: int = 4000, sigma: float = 0.02, emin=None, emax=None, band_weight_sets=None)
:canonical: easyunfold.unfold.spectral_function_from_weight_sets

```{autodoc2-docstring} easyunfold.unfold.spectral_function_from_weight_sets
```
````

`````{py:class} Unfold(M=None, wavecar: str = 'WAVECAR', gamma: bool = False, lsorbit: bool = False, gamma_half: str = 'x', verbose=False)
:canonical: easyunfold.unfold.Unfold

```{autodoc2-docstring} easyunfold.unfold.Unfold
```

```{rubric} Initialization
```

```{autodoc2-docstring} easyunfold.unfold.Unfold.__init__
```

````{py:method} get_vbm_cbm(thresh: float = 1e-08) -> typing.Tuple[float, float]
:canonical: easyunfold.unfold.Unfold.get_vbm_cbm

```{autodoc2-docstring} easyunfold.unfold.Unfold.get_vbm_cbm
```

````

````{py:method} get_ovlap_G(ikpt: int = 1, epsilon: float = 1e-05) -> typing.Tuple[numpy.ndarray, numpy.ndarray]
:canonical: easyunfold.unfold.Unfold.get_ovlap_G

```{autodoc2-docstring} easyunfold.unfold.Unfold.get_ovlap_G
```

````

````{py:method} find_K_index(K0: numpy.ndarray) -> int
:canonical: easyunfold.unfold.Unfold.find_K_index

```{autodoc2-docstring} easyunfold.unfold.Unfold.find_K_index
```

````

````{py:method} k2K_map(kpath) -> typing.List[int]
:canonical: easyunfold.unfold.Unfold.k2K_map

```{autodoc2-docstring} easyunfold.unfold.Unfold.k2K_map
```

````

````{py:method} spectral_weight_k(k0, whichspin=1)
:canonical: easyunfold.unfold.Unfold.spectral_weight_k

```{autodoc2-docstring} easyunfold.unfold.Unfold.spectral_weight_k
```

````

````{py:method} spectral_weight(kpoints: typing.List)
:canonical: easyunfold.unfold.Unfold.spectral_weight

```{autodoc2-docstring} easyunfold.unfold.Unfold.spectral_weight
```

````

````{py:method} spectral_function(nedos: int = 4000, sigma: float = 0.02)
:canonical: easyunfold.unfold.Unfold.spectral_function

```{autodoc2-docstring} easyunfold.unfold.Unfold.spectral_function
```

````

`````

````{py:function} spectral_weight_multiple_source(kpoints: list, unfold_objs: typing.List[easyunfold.unfold.Unfold], transform_matrix: numpy.ndarray)
:canonical: easyunfold.unfold.spectral_weight_multiple_source

```{autodoc2-docstring} easyunfold.unfold.spectral_weight_multiple_source
```
````

````{py:function} concatenate_scf_kpoints(scf_kpts: list, scf_weights: list, kpoints: list)
:canonical: easyunfold.unfold.concatenate_scf_kpoints

```{autodoc2-docstring} easyunfold.unfold.concatenate_scf_kpoints
```
````

````{py:function} create_white_colormap(color: typing.Union[str, tuple, list]) -> matplotlib.colors.ListedColormap
:canonical: easyunfold.unfold.create_white_colormap

```{autodoc2-docstring} easyunfold.unfold.create_white_colormap
```
````

````{py:function} create_white_colormap_from_existing(name: str) -> matplotlib.colors.ListedColormap
:canonical: easyunfold.unfold.create_white_colormap_from_existing

```{autodoc2-docstring} easyunfold.unfold.create_white_colormap_from_existing
```
````

````{py:function} parse_atoms_idx(atoms_idx: str) -> typing.List[int]
:canonical: easyunfold.unfold.parse_atoms_idx

```{autodoc2-docstring} easyunfold.unfold.parse_atoms_idx
```
````

````{py:function} process_projection_options(atoms_idx: str, orbitals: str) -> typing.Tuple[list, list]
:canonical: easyunfold.unfold.process_projection_options

```{autodoc2-docstring} easyunfold.unfold.process_projection_options
```
````