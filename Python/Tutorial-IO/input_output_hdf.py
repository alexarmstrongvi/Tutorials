#!/usr/bin/env python
'''
HDF files form a hierarchy
* File: `file = File(path, mode)'
    * Group: `group = file['/group_key']
        * Attributes: `group.attrs`
        * Sub-groups
    * Group vs Dataset
'''
# Standard library
import os
from pathlib import Path
import logging

# 3rd party
import h5py
from numpy.lib.arraysetops import isin

log = logging.getLogger(Path(__file__).stem)
logging.basicConfig(
    level  = logging.DEBUG,
    format = '%(levelname)s :: [%(name)s] %(message)s',
)
# logging.getLogger('h5py').setLevel(logging.WARNING)

################################################################################
def main():
    pass


def module_basics() -> None:
    h5py.AttributeManager
    h5py.Dataset
    h5py.Datatype
    h5py.Empty
    h5py.ExternalLink
    h5py.File
    h5py.Group
    h5py.HLObject
    h5py.HardLink
    h5py.MultiBlockSlice
    h5py.Reference
    h5py.RegionReference
    h5py.SoftLink
    h5py.UNLIMITED
    h5py.VirtualLayout
    h5py.VirtualSource
    h5py.atexit
    h5py.check_dtype
    h5py.check_enum_dtype
    h5py.check_opaque_dtype
    h5py.check_ref_dtype
    h5py.check_string_dtype
    h5py.check_vlen_dtype
    h5py.defs
    h5py.enable_ipython_completer
    h5py.enum_dtype
    h5py.filters
    h5py.get_config
    h5py.h5
    h5py.h5a
    h5py.h5ac
    h5py.h5d
    h5py.h5ds
    h5py.h5f
    h5py.h5fd
    h5py.h5g
    h5py.h5i
    h5py.h5l
    h5py.h5o
    h5py.h5p
    h5py.h5pl
    h5py.h5py_warnings
    h5py.h5r
    h5py.h5s
    h5py.h5t
    h5py.h5z
    h5py.is_hdf5
    h5py.opaque_dtype
    h5py.ref_dtype
    h5py.regionref_dtype
    h5py.register_driver
    h5py.registered_drivers
    h5py.run_tests
    h5py.special_dtype
    h5py.string_dtype
    h5py.unregister_driver
    h5py.utils
    h5py.version
    h5py.vlen_dtype

def summarize_h5_object(h5_obj: h5py._hl.base.HLObject) -> str:
    # Attributes common to File, Group, Dataset, and all high level interface
    # objects (i.e. HLObject base class)
    return f'''H5 Object:
    attrs     = {h5_obj.attrs}
    file      = {h5_obj.file}
    id        = {h5_obj.id}
    name      = {h5_obj.name}
    parent    = {h5_obj.parent}
    '''
    # ref       = {h5_obj.ref}
    # regionref = {h5_obj.regionref}
    # '''
     
def create_example_file(path: Path) -> None:
    if path.is_file():
        log.info('Deleting previous file: %s', path)
        os.remove(path)
    
    with h5py.File(path, 'w') as ofile:
        ofile.create_dataset('mydataset', (100,), dtype='i')
        ofile.create_dataset('mygroup/mysubgroup/mysubdataset', (50,), dtype='f')
        ofile['mygroup'].attrs['myattr'] = 'myval'

if __name__ == '__main__':
    main()
    module_basics()

    path = Path('./tmp/my_hdf5.hdf5')
    create_example_file(path)
    ############################################################################ 
    # def file_basics()
    ifile =  h5py.File(path, 'r+')
    assert isinstance(ifile, h5py.File)
    assert ifile.filename      == str(path)
    assert ifile.mode          == 'r+'
    assert tuple(ifile.keys()) == ('mydataset', 'mygroup')
    
    # Attributes
    assert isinstance(ifile.id, h5py.h5f.FileID)
    print(f'''File attributes
    {ifile.driver          = },
    {ifile.libver          = },
    {ifile.meta_block_size = },
    {ifile.swmr_mode       = },
    {ifile.userblock_size  = },
    ''')
    
    # Methods
    # ifile.close
    # ifile.flush

    ############################################################################ 
    # def group_basics()
    assert isinstance(ifile, h5py.Group)
    group = ifile['mygroup']
    assert group.name == '/mygroup'
    
    # Attributes
    assert group.file == ifile
    assert group.file is not ifile and group.file is not group.file # Why is this?
    assert group.parent == ifile == ifile.parent
    assert isinstance(group.id, h5py.h5g.GroupID)
    assert ifile[group.ref] == group 

    # HDF5 Attributes
    assert isinstance(group.attrs, h5py.AttributeManager)
    attr_keysview = group.attrs.keys()
    assert isinstance(attr_keysview, h5py._hl.base.KeysViewHDF5)
    assert list(group.attrs.items()) == [('myattr','myval')]

    assert isinstance(group.ref, h5py.h5r.Reference)
    assert isinstance(group.regionref, h5py._hl.base._RegionProxy)
    
    # Access methods
    # Methods
    # group.build_virtual_dataset()
    # group.clear()
    # group.copy()
    # group.create_dataset()
    # group.create_dataset_like()
    # group.create_group()
    # group.create_virtual_dataset()
    # group.get()
    # group.items()
    # group.keys()
    # group.move()
    # group.pop()
    # group.popitem()
    # group.require_dataset()
    # group.require_group()
    # group.setdefault()
    # group.update()
    # group.values()
    # group.visit()
    # group.visititems()

    ################################################################################ 
    # def dataset_basics()
    # dset.nbytes
    # dset.size
    # dset.dtype
    # dset.len
    # dset.is_scale
    # dset.shuffle
    # dset.resize
    # dset.asstr
    # dset.make_scale
    # dset.astype
    # dset.refresh
    # dset.flush
    # dset.maxshape
    # dset.is_virtual
    # dset.scaleoffset
    # dset.virtual_sources
    # dset.chunks
    # dset.compression_opts
    # dset.external
    # dset.shape
    # dset.ndim
    # dset.fletcher32
    # dset.compression
    # dset.write_direct
    # dset.fillvalue
    # dset.iter_chunks
    # dset.read_direct
    # dset.fields
    # dset.dims
    
    ################################################################################ 
    # Object and Region References
    # regref = dset.regionref[0:10, 0:5]
    
    ################################################################################ 
    # TODO: Is reading regionrefs faster than loading all the data and filtering
