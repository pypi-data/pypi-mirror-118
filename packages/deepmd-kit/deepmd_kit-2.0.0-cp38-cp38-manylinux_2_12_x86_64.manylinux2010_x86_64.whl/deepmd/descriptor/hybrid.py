import numpy as np
from typing import Tuple, List

from deepmd.env import tf
from deepmd.common import ClassArg
from deepmd.env import op_module
from deepmd.env import GLOBAL_TF_FLOAT_PRECISION
from deepmd.env import GLOBAL_NP_FLOAT_PRECISION
# from deepmd.descriptor import DescrptLocFrame
# from deepmd.descriptor import DescrptSeA
# from deepmd.descriptor import DescrptSeT
# from deepmd.descriptor import DescrptSeAEbd
# from deepmd.descriptor import DescrptSeAEf
# from deepmd.descriptor import DescrptSeR
from .se_a import DescrptSeA
from .se_r import DescrptSeR
from .se_ar import DescrptSeAR
from .se_t import DescrptSeT
from .se_a_ebd import DescrptSeAEbd
from .se_a_ef import DescrptSeAEf
from .loc_frame import DescrptLocFrame

class DescrptHybrid ():
    """Concate a list of descriptors to form a new descriptor.

    Parameters
    ----------
    descrpt_list : list
            Build a descriptor from the concatenation of the list of descriptors.
    """
    def __init__ (self, 
                  descrpt_list : list
    ) -> None :
        """
        Constructor
        """
        if descrpt_list == [] or descrpt_list is None:
            raise RuntimeError('cannot build descriptor from an empty list of descriptors.')
        # args = ClassArg()\
        #        .add('list', list, must = True)
        # class_data = args.parse(jdata)
        # dict_list = class_data['list']
        self.descrpt_list = descrpt_list
        self.numb_descrpt = len(self.descrpt_list)
        for ii in range(1, self.numb_descrpt):
            assert(self.descrpt_list[ii].get_ntypes() == 
                   self.descrpt_list[ 0].get_ntypes()), \
                   f'number of atom types in {ii}th descrptor does not match others'


    def get_rcut (self) -> float:
        """
        Returns the cut-off radius
        """
        all_rcut = [ii.get_rcut() for ii in self.descrpt_list]
        return np.max(all_rcut)


    def get_ntypes (self) -> int:
        """
        Returns the number of atom types
        """
        return self.descrpt_list[0].get_ntypes()


    def get_dim_out (self) -> int:
        """
        Returns the output dimension of this descriptor
        """
        all_dim_out = [ii.get_dim_out() for ii in self.descrpt_list]
        return sum(all_dim_out)


    def get_nlist_i(self, 
                    ii : int
    ) -> Tuple[tf.Tensor, tf.Tensor, List[int], List[int]]:
        """Get the neighbor information of the ii-th descriptor

        Parameters
        ----------
        ii : int
                The index of the descriptor

        Returns
        -------
        nlist
                Neighbor list
        rij
                The relative distance between the neighbor and the center atom.
        sel_a
                The number of neighbors with full information
        sel_r
                The number of neighbors with only radial information
        """
        return self.descrpt_list[ii].nlist, self.descrpt_list[ii].rij, self.descrpt_list[ii].sel_a, self.descrpt_list[ii].sel_r
    

    def compute_input_stats (self,
                             data_coord : list, 
                             data_box : list, 
                             data_atype : list, 
                             natoms_vec : list,
                             mesh : list, 
                             input_dict : dict
    ) -> None :
        """
        Compute the statisitcs (avg and std) of the training data. The input will be normalized by the statistics.
        
        Parameters
        ----------
        data_coord
                The coordinates. Can be generated by deepmd.model.make_stat_input
        data_box
                The box. Can be generated by deepmd.model.make_stat_input
        data_atype
                The atom types. Can be generated by deepmd.model.make_stat_input
        natoms_vec
                The vector for the number of atoms of the system and different types of atoms. Can be generated by deepmd.model.make_stat_input
        mesh
                The mesh for neighbor searching. Can be generated by deepmd.model.make_stat_input
        input_dict
                Dictionary for additional input
        """
        for ii in self.descrpt_list:
            ii.compute_input_stats(data_coord, data_box, data_atype, natoms_vec, mesh, input_dict)
    

    def build (self, 
               coord_ : tf.Tensor, 
               atype_ : tf.Tensor,
               natoms : tf.Tensor,
               box_ : tf.Tensor, 
               mesh : tf.Tensor,
               input_dict : dict, 
               reuse : bool = None,
               suffix : str = ''
    ) -> tf.Tensor:
        """
        Build the computational graph for the descriptor

        Parameters
        ----------
        coord_
                The coordinate of atoms
        atype_
                The type of atoms
        natoms
                The number of atoms. This tensor has the length of Ntypes + 2
                natoms[0]: number of local atoms
                natoms[1]: total number of atoms held by this processor
                natoms[i]: 2 <= i < Ntypes+2, number of type i atoms
        mesh
                For historical reasons, only the length of the Tensor matters.
                if size of mesh == 6, pbc is assumed. 
                if size of mesh == 0, no-pbc is assumed. 
        input_dict
                Dictionary for additional inputs
        reuse
                The weights in the networks should be reused when get the variable.
        suffix
                Name suffix to identify this descriptor

        Returns
        -------
        descriptor
                The output descriptor
        """
        with tf.variable_scope('descrpt_attr' + suffix, reuse = reuse) :
            t_rcut = tf.constant(self.get_rcut(), 
                                 name = 'rcut', 
                                 dtype = GLOBAL_TF_FLOAT_PRECISION)
            t_ntypes = tf.constant(self.get_ntypes(), 
                                   name = 'ntypes', 
                                   dtype = tf.int32)
        all_dout = []
        for idx,ii in enumerate(self.descrpt_list):
            dout = ii.build(coord_, atype_, natoms, box_, mesh, input_dict, suffix=suffix+f'_{idx}', reuse=reuse)
            dout = tf.reshape(dout, [-1, ii.get_dim_out()])
            all_dout.append(dout)
        dout = tf.concat(all_dout, axis = 1)
        dout = tf.reshape(dout, [-1, natoms[0] * self.get_dim_out()])
        return dout
        

    def prod_force_virial(self, 
                          atom_ener : tf.Tensor, 
                          natoms : tf.Tensor
    ) -> Tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
        """
        Compute force and virial

        Parameters
        ----------
        atom_ener
                The atomic energy
        natoms
                The number of atoms. This tensor has the length of Ntypes + 2
                natoms[0]: number of local atoms
                natoms[1]: total number of atoms held by this processor
                natoms[i]: 2 <= i < Ntypes+2, number of type i atoms

        Returns
        -------
        force
                The force on atoms
        virial
                The total virial
        atom_virial
                The atomic virial
        """
        for idx,ii in enumerate(self.descrpt_list):
            ff, vv, av = ii.prod_force_virial(atom_ener, natoms)
            if idx == 0:
                force = ff
                virial = vv
                atom_virial = av
            else:
                force += ff
                virial += vv
                atom_virial += av
        return force, virial, atom_virial
