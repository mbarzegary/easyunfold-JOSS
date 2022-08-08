#!/usr/bin/env python
# -*- coding: utf-8 -*-

############################################################
import os
import multiprocessing

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from monty.json import MSONable

from vaspwfc import vaspwfc

############################################################


def find_K_from_k(k, M):
    '''
    Get the K vector of the supercell onto which the k vector of the primitive
    cell folds. The unfoliding vector G, which satisfy the following equation,
    is also returned.

        k = K + G

    where G is a reciprocal space vector of supercell
    '''

    M = np.array(M)
    Kc = np.dot(k, M.T)
    G = np.array(
        np.round(Kc), dtype=int)
    KG = Kc - np.round(Kc)

    return KG, G


def rotate_kpt(k, latt, rec, opt):
    """Apply rotation to a kpoint"""
    #rot = k @ rec @ opt.T @ latt
    rot =  k @ opt
    return rot - np.rint(rot)

def expand_K_by_symmetry(k, rec_pc, opts_pc, opts_sc):
    """
    Expend the sampling of the PC kpoints due to symmetry breaking of the SC
    """
    k = np.asarray(k)
    latt_pc = np.linalg.inv(rec_pc)

    # Find distinct images of the kpoints in the PC
    pc_distinct = [k]
    for opt in opts_pc:
        k_equiv = rotate_kpt(k, latt_pc, rec_pc, opt)
        found = False
        for k_ in pc_distinct:
            if np.allclose(k_equiv, k_):
                found = True
        if not found:
            pc_distinct.append(k_equiv)
    weights = np.ones(len(pc_distinct))
    # Now each for uniqueness in the supercell
    for i, k in enumerate(pc_distinct):
        if weights[i] == 0:
            continue

        for opt in opts_sc:
            k_equiv = rotate_kpt(k, latt_pc, rec_pc, opt)
            for j, k_ in enumerate(pc_distinct):
                # Skip if it is the same point, or the other point has been taken
                if i == j or weights[j] == 0:
                    continue
                if np.allclose(k_equiv, k_):
                    weights[i] += weights[j]
                    weights[j] = 0

    out_points = []
    out_weights = []
    for i, k in enumerate(pc_distinct):
        if weights[i] != 0:
            out_points.append(k)
            out_weights.append(weights[i])
    assert sum(out_weights) == len(pc_distinct)
    out_weights = np.array(out_weights) / sum(out_weights)
    return out_points, out_weights


class UnfoldKSet(MSONable):
    """Stores the information of the kpoints in the primitive cell, and what they unfolds to in the supercell"""
    
    def __init__(self, M, kpts_pc, pc_latt, pc_opts, sc_opts, **kwargs):
        """
        Args:
            kpts_pc: A list of kpoints in the PC
            pc_lattice: A 3x3 matrix of row lattice vectors of the primitive cell
            pc_opts: Symmetry operations of the primitive cell
            sc_opts: Symmetry operations of the supercell
        """
        self.kpts_pc = kpts_pc
        self.pc_latt = pc_latt
        self.pc_opts = pc_opts
        self.sc_opts = sc_opts
        self.M = M
        self.expansion_results = None
        self.reduced_sckpts = None
        self.reduced_sckpts_map = None

        self.expand_pc_kpoints()
    
    def expand_pc_kpoints(self):
        """Comptue the pc kpoints to be unfolded into"""
        expended_k = []
        expended_weights = []
        for kpt in self.kpts_pc:
            kset, weights = expand_K_by_symmetry(kpt, np.linalg.inv(self.pc_latt), self.pc_opts, self.sc_opts)
            expended_k.append(kset)
            expended_weights.append(weights)
        self.expansion_results = {'kpoints': expended_k, 'weights': expended_weights}

    def __repr__(self) -> str:
        return f"<UnfoldKSet with {self.nkpts_expand}/{self.nkpts_orig} kpoints based on {self.nsymm_expand}/{self.nsymm_orig} symm ops"

    @property
    def nsymm_orig(self):
        """Number of symmetry operation in the original cell"""
        return self.pc_opts.shape[0]

    @property
    def nsymm_expand(self):
        """Number of symmetry operation in the original cell"""
        return self.sc_opts.shape[0]

    @property
    def nkpts_orig(self):
        """Total number of unexpanded kpoints"""
        return len(self.expansion_results['kpoints'])

    @property
    def nkpts_expand(self):
        """Total number of expanded kpoints"""
        return sum(map(len, self.expansion_results['kpoints']))

    def generate_sc_kpoints(self):
        """
        Generate the supercell kpoints to be calculated

        Returns:
            A flat list of supercell kpoints in fractional coordinates
            An indexing nested list to map expanded kpoints set to the supercell kpoints generated 
        """

        assert bool(self.expansion_results)
        expended_sc = []
        all_sc = []
        for kset in self.expansion_results['kpoints']:
            this_k = []
            for kpt in kset:
                sc_k, _ = find_K_from_k(kpt, self.M)
                this_k.append(sc_k)
            expended_sc.append(this_k)
            all_sc.extend(this_k)
        # We now have bunch of supercell kpoints for each set of expanded kpoints
        # Try to find duplicated SC kpoints
        reduced_sckpts, sc_kpts_map = removeDuplicateKpoints(all_sc, return_map=True)
        sc_kpts_map = list(sc_kpts_map)

        # Mapping between the pckpts to the redcued sckpts
        reduced_sc_map = []
        for sc_set in expended_sc:
            map_indx = []
            for _ in sc_set:
                map_indx.append(sc_kpts_map.pop(0))
            reduced_sc_map.append(map_indx)

        self.reduced_sckpts = reduced_sckpts
        # A nested list that stores the indices of the sc kpts in the reduced_sckpts list
        self.reduced_sckpts_map = reduced_sc_map
        return reduced_sckpts, reduced_sc_map



def LorentzSmearing(x, x0, sigma=0.02):
    '''
    Simulate the Delta function by a Lorentzian shape function

        \Delta(x) = \lim_{\sigma\to 0}  Lorentzian
    '''

    return 1. / np.pi * sigma**2 / ((x - x0)**2 + sigma**2)


def GaussianSmearing(x, x0, sigma=0.02):
    '''
    Simulate the Delta function by a Lorentzian shape function

        \Delta(x) = \lim_{\sigma\to 0} Gaussian
    '''

    return 1. / (np.sqrt(2*np.pi) * sigma) * np.exp(-(x - x0)**2 / (2*sigma**2))


def removeDuplicateKpoints(kpoints, return_map=False, decimals=6):
    '''
    remove duplicate kpoints in the list.
    '''


    # sorted_kpoints = np.array(
    #         sorted(kpoints, key=lambda x: (x[0], x[1], x[2]))
    #         )
    # kdiff = np.diff(sorted_kpoints, axis=0)
    # match = np.abs(np.linalg.norm(kdiff, axis=1)) > 1E-5
    #
    # reducedK = sorted_kpoints[np.r_[True, match]]

    # The simplest way to get the unique k-points is to use np.unique function,
    #
    kpoints = np.asarray(kpoints)
    uk, kid, inv_kid = np.unique(
        np.round(kpoints, decimals),
        axis=0,
        return_index=True,
        return_inverse=True,
    )
    reducedK = kpoints[kid]

    if return_map:
        return reducedK, inv_kid
    else:
        return reducedK


def save2VaspKPOINTS(kpoints):
    '''
    save to VASP KPOINTS file
    '''
    kpoints = np.array(kpoints)
    nkpts = kpoints.shape[0]

    with open('KPOINTS', 'w') as vaspkpt:
        vaspkpt.write('kpoints generated by PYVASPWFC\n')
        vaspkpt.write('%d\n' % nkpts)
        vaspkpt.write('Rec\n')
        for ik in range(nkpts):
            line = '  %12.8f %12.8f %12.8f 1.0\n' % (
                kpoints[ik, 0], kpoints[ik, 1], kpoints[ik, 2])
            vaspkpt.write(line)


def make_kpath(kbound, nseg=40):
    '''
    make a list of kpoints defining the path between the given kpoints. 
    '''
    kbound = np.array(kbound, dtype=float)
    kdist = np.diff(kbound, axis=0)

    # kpath = []
    # for ii in range(len(kdist)):
    #     for nk in range(nseg):
    #         kpt = kbound[ii] + kdist[ii] / nseg * nk
    #         kpath.append(kpt)

    kpath = [kbound[ii] + kdist[ii] / nseg * nk
             for ii in range(len(kdist))
             for nk in range(nseg)]
    kpath.append(kbound[-1])
    return kpath


def EBS_scatter(kpts, cell, spectral_weight,
                atomic_weights=None,
                atomic_colors=[],
                eref=0.0,
                nseg=None, save='ebs_s.png',
                kpath_label=[],
                factor=20, figsize=(3.0, 4.0),
                ylim=(-3, 3), show=True,
                color='b'):
    '''
    plot the effective band structure with scatter, the size of the scatter
    indicates the spectral weight.
    The plotting function utilizes Matplotlib package.

    inputs:
        kpts: the kpoints vectors in fractional coordinates.
        cell: the primitive cell basis
        spectral_weight: self-explanatory
    '''

    mpl.rcParams['axes.unicode_minus'] = False

    nspin = spectral_weight.shape[0]
    kpt_c = np.dot(kpts, np.linalg.inv(cell).T)
    kdist = np.r_[0, np.cumsum(
        np.linalg.norm(
            np.diff(kpt_c, axis=0),
            axis=1
        ))]
    nk = kdist.size
    nb = spectral_weight.shape[2]
    # x0 = np.outer(np.ones(nb), kdist).T
    x0 = np.tile(kdist, (nb, 1)).T

    if atomic_weights is not None:
        atomic_weights = np.asarray(atomic_weights)
        assert atomic_weights.shape[1:] == spectral_weight.shape[:-1]
        
        if not atomic_colors:
            atomic_colors = mpl.rcParams['axes.prop_cycle'].by_key()['color']

    fig = plt.figure()
    fig.set_size_inches(figsize)
    if nspin == 1:
        axes = [plt.subplot(111)]
        fig.set_size_inches(figsize)
    else:
        axes = [plt.subplot(121), plt.subplot(122)]
        fig.set_size_inches((figsize[0] * 2, figsize[1]))

    for ispin in range(nspin):
        ax = axes[ispin]
        if atomic_weights is not None:
            for iatom in range(atomic_weights.shape[0]):
                ax.scatter(x0, spectral_weight[ispin, :, :, 0] - eref,
                            s=spectral_weight[ispin, :, :, 1] * factor * atomic_weights[iatom][ispin,:,:],
                           lw=0.0, color=atomic_colors[iatom])
        else:
            ax.scatter(x0, spectral_weight[ispin, :, :, 0] - eref,
                       s=spectral_weight[ispin, :, :, 1] * factor,
                       lw=0.0, color=color)

        ax.set_xlim(0, kdist.max())
        ax.set_ylim(*ylim)
        ax.set_ylabel('Energy [eV]', labelpad=5)

        if nseg:
            for kb in kdist[::nseg]:
                ax.axvline(x=kb, lw=0.5, color='k', ls=':', alpha=0.8)

            if kpath_label:
                ax.set_xticks(kdist[::nseg])
                kname = [x.upper() for x in kpath_label]
                for ii in range(len(kname)):
                    if kname[ii] == 'G':
                        kname[ii] = r'$\mathrm{\mathsf{\Gamma}}$'
                    else:
                        kname[ii] = r'$\mathrm{\mathsf{%s}}$' % kname[ii]
                ax.set_xticklabels(kname)

    plt.tight_layout(pad=0.2)
    plt.savefig(save, dpi=360)
    if show:
        plt.show()


def EBS_cmaps(kpts, cell, E0, spectral_function,
              eref=0.0, nseg=None,
              kpath_label=[],
              save='ebs_c.png',
              figsize=(3.0, 4.0),
              ylim=(-3, 3), show=True,
              contour_plot=False,
              cmap='jet'):
    '''
    plot the effective band structure with colormaps.  The plotting function
    utilizes Matplotlib package.

    inputs:
        kpts: the kpoints vectors in fractional coordinates.
        cell: the primitive cell basis
        spectral_weight: self-explanatory
    '''

    mpl.use('agg')

    mpl.rcParams['axes.unicode_minus'] = False

    nspin = spectral_function.shape[0]
    kpt_c = np.dot(kpts, np.linalg.inv(cell).T)
    kdist = np.r_[0, np.cumsum(
        np.linalg.norm(
            np.diff(kpt_c, axis=0),
            axis=1
        ))]
    nk = kdist.size
    xmin, xmax = kdist.min(), kdist.max()
    # ymin, ymax = E0.min() - eref, E0.max() - eref

    fig = plt.figure()
    if nspin == 1:
        axes = [plt.subplot(111)]
        fig.set_size_inches(figsize)
    else:
        axes = [plt.subplot(121), plt.subplot(122)]
        fig.set_size_inches((figsize[0] * 2, figsize[1]))

    # ax.imshow(spectral_function, extent=(xmin, xmax, ymin, ymax),
    #           origin='lower', aspect='auto', cmap=cmap)
    X, Y = np.meshgrid(kdist, E0 - eref)
    for ispin in range(nspin):
        ax = axes[ispin]
        if contour_plot:
            ax.contourf(X, Y, spectral_function[ispin], cmap=cmap)
        else:
            ax.pcolormesh(X, Y, spectral_function[ispin], cmap=cmap, shading='auto')

        ax.set_xlim(xmin, xmax)
        ax.set_ylim(*ylim)
        ax.set_ylabel('Energy [eV]', labelpad=5)

        if nseg:
            for kb in kdist[::nseg]:
                ax.axvline(x=kb, lw=0.5, color='k', ls=':', alpha=0.8)

            if kpath_label:
                tick_pos = list(kdist[::nseg])
                ax.set_xticks(tick_pos)
                kname = [x.upper() for x in kpath_label]
                for ii in range(len(kname)):
                    if kname[ii] == 'G':
                        kname[ii] = r'$\mathrm{\mathsf{\Gamma}}$'
                    else:
                        kname[ii] = r'$\mathrm{\mathsf{%s}}$' % kname[ii]
                ax.set_xticklabels(kname)

    plt.tight_layout(pad=0.2)
    plt.savefig(save, dpi=360)
    if show:
        plt.show()
############################################################


class unfold():
    '''
    Unfold the band structure from Supercell calculation into a primitive cell and
    obtain the effective band structure (EBS).

    REF:
    "Extracting E versus k effective band structure from supercell
     calculations on alloys and impurities"
    Phys. Rev. B 85, 085201 (2012)
    '''

    def __init__(self, M=None, wavecar='WAVECAR', gamma=False, lsorbit=False,
                 gamma_half='x'):
        '''
        Initialization.

        M is the transformation matrix between supercell and primitive cell: 

            M = np.dot(A, np.linalg.inv(a))     

        In real space, the basis vectors of Supercell (A) and those of the
        primitive cell (a) satisfy:

            A = np.dot(M, a);      a = np.dot(np.linalg.inv(M), A)

        Whereas in reciprocal space

            b = np.dot(M.T, B);    B = np.dot(np.linalg.inv(M).T, b)    

        wavecar is the location of VASP WAVECAR file that contains the
        wavefunction information of a supercell calculation.
        '''

        # Whether the WAVECAR is a gamma-only version
        self._lgam = gamma
        self._lsoc = lsorbit

        self.M = np.array(M, dtype=float)
        assert self.M.shape == (
            3, 3), 'Shape of the tranformation matrix must be (3,3)'

        self.wfc = vaspwfc(wavecar, lsorbit=self._lsoc, lgamma=self._lgam,
                           gamma_half=gamma_half)
        # all the K-point vectors
        self.kvecs = self.wfc._kvecs
        # all the KS energies
        self.bands = self.wfc._bands

        # G-vectors within the cutoff sphere, let's just do it once for all.
        # self.allGvecs = np.array([self.wfc.gvectors(ikpt=kpt+1)
        #                           for kpt in range(self.wfc._nkpts)], dtype=int)

        # spectral weight for all the kpoints
        self.SW = None

    def get_ovlap_G(self, ikpt=1, epsilon=1E-5):
        '''
        Get subset of the reciprocal space vectors of the supercell,
        specifically the ones that match the reciprocal space vectors of the
        primitive cell.
        '''

        assert 1 <= ikpt <= self.wfc._nkpts, 'Invalid K-point index!'

        # Reciprocal space vectors of the supercell in fractional unit
        Gvecs = self.wfc.gvectors(ikpt=ikpt)
        # Gvecs = self.allGvecs[ikpt - 1]

        if self._lgam:
            nplw = Gvecs.shape[0]
            tmp = np.zeros((nplw * 2 - 1, 3), dtype=int)
            # the gvectors of Gamma version only contains half the number of a
            # normal version.
            tmp[:nplw, ...] = Gvecs
            tmp[nplw:, ...] = -Gvecs[1:, ...]            # G' = -G

            Gvecs = tmp

        # Shape of Gvecs: (nplws, 3)
        # iGvecs = np.arange(Gvecs.shape[0], dtype=int)

        # Reciprocal space vectors of the primitive cell
        gvecs = np.dot(Gvecs, np.linalg.inv(self.M).T)
        # Deviation from the perfect sites
        gd = gvecs - np.round(gvecs)
        # match = np.linalg.norm(gd, axis=1) < epsilon
        match = np.alltrue(
            np.abs(gd) < epsilon, axis=1
        )

        # return Gvecs[match], iGvecs[match]
        return Gvecs[match], Gvecs

    def find_K_index(self, K0):
        '''
        Find the index of K0.
        '''

        for ii in range(self.wfc._nkpts):
            if np.alltrue(
                np.abs(self.wfc._kvecs[ii] - K0) < 1E-5
            ):
                return ii + 1
        # the for-else
        else:
            raise ValueError(
                'Cannot find the corresponding K-points in WAVECAR!'
            )

    def k2K_map(self, kpath):
        '''
        Find the map from primitive-cell k-points to supercell k-points.
        '''

        return [
            self.find_K_index(
                find_K_from_k(k, self.M)[0]
            ) - 1 for k in kpath
        ]

    def spectral_weight_k(self, k0, whichspin=1):
        '''
        Spectral weight for a given k:

            P_{Km}(k) = \sum_n |<Km | kn>|^2

        which is equivalent to

            P_{Km}(k) = \sum_{G} |C_{Km}(G + k - K)|^2

        where {G} is a subset of the reciprocal space vectors of the supercell.
        '''

        print('Processing k-point %8.4f %8.4f %8.4f' % (k0[0], k0[1], k0[2]))

        # find the K0 onto which k0 folds
        # k0 = G0 + K0
        K0, G0 = find_K_from_k(k0, self.M)
        # find index of K0
        ikpt = self.find_K_index(K0)

        # get the overlap G-vectors
        Gvalid, Gall = self.get_ovlap_G(ikpt=ikpt)
        # Gnew = Gvalid + k0 - K0
        Goffset = Gvalid + G0[np.newaxis, :]

        # Index of the Gvalid in 3D grid
        GallIndex = Gall % self.wfc._ngrid[np.newaxis, :]
        GoffsetIndex = Goffset % self.wfc._ngrid[np.newaxis, :]

        # 3d grid for planewave coefficients
        wfc_k_3D = np.zeros(self.wfc._ngrid, dtype=np.complex)

        # if self._lsoc:
        #     # the weights and corresponding energies
        #     P_Km = np.zeros((2, self.wfc._nbands), dtype=float)
        #     E_Km = np.zeros((2, self.wfc._nbands), dtype=float)
        # else:
        #     # the weights and corresponding energies
        #     P_Km = np.zeros(self.wfc._nbands, dtype=float)
        #     E_Km = np.zeros(self.wfc._nbands, dtype=float)

        # the weights and corresponding energies
        P_Km = np.zeros(self.wfc._nbands, dtype=float)
        E_Km = np.zeros(self.wfc._nbands, dtype=float)

        for nb in range(self.wfc._nbands):
            # initialize the array to zero, which is unnecessary since the
            # GallIndex is the same for the same K-point
            # wfc_k_3D[:,:,:] = 0.0

            if self._lsoc:
                # pad the coefficients to 3D grid
                band_coeff = self.wfc.readBandCoeff(ispin=whichspin, ikpt=ikpt,
                                                    iband=nb + 1, norm=True)
                nplw = band_coeff.shape[0] // 2
                band_spinor_coeff = [band_coeff[:nplw], band_coeff[nplw:]]

                # energy
                E_Km[nb] = self.bands[whichspin-1, ikpt-1, nb]
                for Ispinor in range(2):
                    # band = band_spinor_coeff[Ispinor]
                    # band /= np.linalg.norm(band)
                    wfc_k_3D[GallIndex[:, 0], GallIndex[:, 1],
                             GallIndex[:, 2]] = band_spinor_coeff[Ispinor]

                    # spectral weight
                    P_Km[nb] += np.linalg.norm(
                        wfc_k_3D[GoffsetIndex[:, 0],
                                 GoffsetIndex[:, 1], GoffsetIndex[:, 2]]
                    )**2
            else:
                # pad the coefficients to 3D grid
                band_coeff = self.wfc.readBandCoeff(
                    ispin=whichspin, ikpt=ikpt, iband=nb + 1, norm=True)
                if self._lgam:
                    nplw = band_coeff.size
                    tmp = np.zeros((nplw * 2 - 1), dtype=band_coeff.dtype)
                    # for Gamma version, the coefficients corresponding to G \ne 0
                    # is multiplied by a factor of sqrt(2)
                    band_coeff[1:] /= np.sqrt(2.)
                    tmp[:nplw] = band_coeff
                    tmp[nplw:] = band_coeff[1:].conj()
                    band_coeff = tmp

                wfc_k_3D[GallIndex[:, 0], GallIndex[:, 1],
                         GallIndex[:, 2]] = band_coeff
                # energy
                E_Km[nb] = self.bands[whichspin-1, ikpt-1, nb]
                # spectral weight
                P_Km[nb] = np.linalg.norm(
                    wfc_k_3D[GoffsetIndex[:, 0],
                             GoffsetIndex[:, 1], GoffsetIndex[:, 2]]
                )**2

        return np.array((E_Km, P_Km), dtype=float).T

    # def spectral_weight(self, kpoints, nproc=None):
    #     '''
    #     Calculate the spectral weight for a list of kpoints in the primitive BZ.
    #     Here, we use "multiprocessing" package to parallel over the kpoints.
    #     '''
    #
    #     NKPTS = len(kpoints)
    #
    #     if nproc is None:
    #         nproc = multiprocessing.cpu_count()
    #
    #     pool = multiprocessing.Pool(processes=nproc)
    #
    #     results = []
    #     for ik in range(NKPTS):
    #         res = pool.apply_async(self.spectral_weight_k, (kpoints[ik],))
    #         results.append(res)
    #
    #     self.SW = np.array([res.get() for res in results], dtype=float)
    #
    #     pool.close()
    #     pool.join()
    #
    #     return self.SW

    def spectral_weight(self, kpoints):
        '''
        Calculate the spectral weight for a list of kpoints in the primitive BZ.
        '''

        NKPTS = len(kpoints)

        # self.SW = np.array([self.spectral_weight_k(kpoints[ik])
        #                     for ik in range(NKPTS)], dtype=float)
        sw = []
        for ispin in range(self.wfc._nspin):
            if self.wfc._nspin == 2:
                print("#" * 60)
                print("Spin component: %d" % ispin)
                print("#" * 60)
            sw.append([self.spectral_weight_k(kpoints[ik], whichspin=ispin+1)
                       for ik in range(NKPTS)])

        self.SW = np.array(sw)

        # For noncollinear calculation, nspin = 1.
        # if self._lsoc:
        #     # self.SW = np.swapaxes(self.SW, 0, 1)
        #     self.SW = np.array([self.SW[0,:,:,0,:], self.SW[0,:,:,1,]])

        return self.SW

    def spectral_function(self, nedos=4000, sigma=0.02):
        '''
        Generate the spectral function

            A(k_i, E) = \sum_m P_{Km}(k_i)\Delta(E - Em)

        Where the \Delta function can be approximated by Lorentzian or Gaussian
        function.
        '''

        assert self.SW is not None, 'Spectral weight must be calculated first!'

        # NS = 2 if self._lsoc else self.wfc._nspin
        # For noncollinear calculation, nspin = 1.
        NS = self.wfc._nspin
        # Number of kpoints
        nk = self.SW.shape[1]
        # spectral function
        SF = np.zeros((NS, nedos, nk), dtype=float)

        emin = self.SW[:, :, :, 0].min()
        emax = self.SW[:, :, :, 0].max()
        e0 = np.linspace(emin - 5 * sigma, emax + 5 * sigma, nedos)

        for ispin in range(NS):
            for ii in range(nk):
                E_Km = self.SW[ispin, ii, :, 0]
                P_Km = self.SW[ispin, ii, :, 1]

                SF[ispin, :, ii] = np.sum(
                    LorentzSmearing(
                        e0[:, np.newaxis], E_Km[np.newaxis, :],
                        sigma=sigma
                    ) * P_Km[np.newaxis, :], axis=1
                )
        return e0, SF

############################################################


if __name__ == '__main__':
    M = [[3.0, 0.0, 0.0],
         [0.0, 3.0, 0.0],
         [0.0, 0.0, 1.0]]

    kpts = [[0.0, 0.5, 0.0],
            [0.0, 0.0, 0.0],
            [1./3, 1./3, 0.0],
            [0.0, 0.5, 0.0]]

    kpath = make_kpath(kpts, nseg=30)

    K_in_sup = []
    for kk in kpath:
        kg, g = find_K_from_k(kk, M)
        K_in_sup.append(kg)
    reducedK = removeDuplicateKpoints(K_in_sup)
    save2VaspKPOINTS(reducedK)

    # from ase.io import read, write
    #
    # pos = read('POSCAR.p', format='vasp')
    # cell = pos.cell
    cell = [[3.1850, 0.0000000000000000,  0.0],
            [-1.5925, 2.7582909110534373,  0.0],
            [0.0000, 0.0000000000000000, 35.0]]

    if os.path.isfile('spectral_function.npy'):
        sw = np.load('spectral_weight.npy')
        sf = np.load('spectral_function.npy')
        e0 = np.load('energy.npy')
    else:
        fwave = unfold(M=M, wavecar='WAVECAR')
        sw = fwave.spectral_weight(kpath)
        e0, sf = fwave.spectral_function(nedos=4000)
        np.save('spectral_weight.npy', sw)
        np.save('spectral_function.npy', sf)
        np.save('energy.npy', e0)

    EBS_scatter(kpath, cell, sw, nseg=30, eref=-4.01,
                ylim=(-3, 4), show=False,
                factor=5)
    EBS_cmaps(kpath, cell, e0, sf, nseg=30, eref=-4.01,
              show=False,
              ylim=(-3, 4))