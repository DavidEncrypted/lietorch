from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension
import os.path as osp
ROOT = osp.dirname(osp.abspath(__file__))

# Common compile args
cxx_args = ['-O2', '-D_GLIBCXX_USE_CXX11_ABI=0']
nvcc_args = [
    '-O2',
    '-D_GLIBCXX_USE_CXX11_ABI=0',  # Add here too
    '-Xcompiler', '-D_GLIBCXX_USE_CXX11_ABI=0',  # This tells nvcc to pass it to the host compiler
    '-gencode=arch=compute_60,code=sm_60', 
    '-gencode=arch=compute_61,code=sm_61', 
    '-gencode=arch=compute_70,code=sm_70', 
    '-gencode=arch=compute_75,code=sm_75',
    '-gencode=arch=compute_75,code=compute_75',
]

setup(
    name='lietorch',
    version='0.2',
    description='Lie Groups for PyTorch',
    author='teedrz',
    packages=['lietorch'],
    ext_modules=[
        CUDAExtension('lietorch_backends',
            include_dirs=[
                osp.join(ROOT, 'lietorch/include'),
                osp.join(ROOT, 'eigen')],
            sources=[
                'lietorch/src/lietorch.cpp',
                'lietorch/src/lietorch_gpu.cu',
                'lietorch/src/lietorch_cpu.cpp'],
            extra_compile_args={
                'cxx': cxx_args,
                'nvcc': nvcc_args
            },
            extra_link_args=['-D_GLIBCXX_USE_CXX11_ABI=0']),  # Add to linker too
        CUDAExtension('lietorch_extras',
            sources=[
                'lietorch/extras/altcorr_kernel.cu',
                'lietorch/extras/corr_index_kernel.cu',
                'lietorch/extras/se3_builder.cu',
                'lietorch/extras/se3_inplace_builder.cu',
                'lietorch/extras/se3_solver.cu',
                'lietorch/extras/extras.cpp',
            ],
            extra_compile_args={
                'cxx': cxx_args,
                'nvcc': nvcc_args
            },
            extra_link_args=['-D_GLIBCXX_USE_CXX11_ABI=0']),  # Add to linker too
    ],
    cmdclass={ 'build_ext': BuildExtension }
