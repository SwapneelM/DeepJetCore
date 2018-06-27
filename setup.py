import os
from setuptools import setup, Extension
from setuptools.command.install import install
# from distutils.command.build_py import build_py
from setuptools.command.build_ext import build_ext
# from setuptools.command.build_py import build_py
from subprocess import call
from multiprocessing import cpu_count

BASEPATH = os.path.dirname(os.path.abspath(__file__))
print ("\nBasepath: ", BASEPATH)

# Path to the `DeepJetCore` folder within the package
# DEEPJETCORE = os.path.join(BASEPATH, 'DeepJetCore')
DEEPJETCORE = './DeepJetCore'
print ("\nDeepjetcore: ", DEEPJETCORE)

# Path to the `compiled` folder within `DeepJetCore`
COMPILEPATH = os.path.join(DEEPJETCORE, 'compiled')
print ("\Compile Path: ", COMPILEPATH)

# Path to the `interface` folder within `DeepJetCore/compiled`
INTERFACEPATH = os.path.join(COMPILEPATH, 'interface')
print ("\Compile Path: ", INTERFACEPATH)

# Exporting the value to a variable for use to set paths
CONDA_PREFIX = os.environ['CONDA_PREFIX']

# Path to configuration files required to build some of the extensions
PYCONFIG_PATH = os.path.join(
    CONDA_PREFIX, 'lib', 'python3.6', 'config-3.6m-x86_64-linux-gnum')
'''
if os.environ['PYTHON_VERSION']:
    PYCONFIG_PATH = os.path.join(
        CONDA_PREFIX, 'lib', 'python' +
        str(os.environ['PYTHON_VERSION']), 'config')
'''

# declare command to run manual `make` using Makefile in COMPILEPATH
# --to be deprecated in DeepJetCore version 0.0.5
cmd = [
    'make',
]
try:
    cmd.append('-j%d' % cpu_count())
except NotImplementedError:
    print ('Unable to determine number of CPUs. \
    Using single threaded make.')
options = [
    '--directory=' + COMPILEPATH,
    '--makefile=Makefile',
]
cmd.extend(options)
print ("\n\n" + str(cmd) + "\n\n")


class DeepJetCoreBuildExt(build_ext):
    '''
    Override the default `build_ext` command
    to implement custom commands
    -- deprecated in DeepJetCorev0.0.5
    '''
    def run(self):
        # run original build code
        # print "\n\n\n*****running original DeepJetCore build_py*****\n\n\n"
        build_ext.run(self)
        print ("\n\n*********running custom build_py***********\n\n")
        call(cmd)


class DeepJetCoreInstall(install):
    '''
    Override the default `install` command
    to implement custom commands
    -- deprecated in DeepJetCorev0.0.5
    '''
    def run(self):
        # if BUILDFLAG==0:
        # print "\n\n\n*****running custom DeepJetCore install*****\n\n\n"
        # call(cmd, cwd=DEEPJETCORE)
        # run original install code
        # print "\n\n\n*****running original DeepJetCore install*****\n\n\n"
        install.run(self)


def retrieveReadmeContent():
    '''
    Retrieve the description for the package
    from the README.rst file in BASEPATH
    '''
    with open(os.path.join(BASEPATH, 'README.rst')) as f:
        return f.read()


quicklz = Extension(
    'quicklz',
    include_dirs=[
        os.path.join(COMPILEPATH, 'interface')
    ],
    sources=[os.path.join(COMPILEPATH, 'quicklzpy.c')])

root_flags = [
	'-pthread',
	'-std=c++11',
	'-Wno-deprecated-declarations',
	'-m64',
	'-lCore',
	'-lRIO',
	'-lNet',
	'-lHist',
	'-lGraf',
	'-lGraf3d',
	'-lGpad',
	'-lTree',
	'-lRint',
	'-lPostscript',
	'-lMatrix',
	'-lPhysics',
	'-lMathCore',
	'-lThread',
	'-lm',
	'-ldl',
	'-rdynamic',
]

cpp_compiler_flags = root_flags + ['-O2', '-fPIC', '-c']
cpp_lib_dirs = [
    os.path.join(CONDA_PREFIX, 'lib'),
    os.path.join(COMPILEPATH, 'interface'),
    '/usr/local/lib/',
]
cpp_include_dirs = [
    os.path.join(CONDA_PREFIX, 'include'),
    '/usr/local/include'
]

cpp_indata = Extension(
    'DeepJetCore.compiled.indata',
    extra_compile_args=cpp_compiler_flags,
    sources=[os.path.join(COMPILEPATH, 'src', 'indata.cpp'),
             os.path.join(INTERFACEPATH,
                          'indata_wrap.cxx')],
    include_dirs=cpp_lib_dirs,
    libraries=['python2.7'])

cpp_helper = Extension(
    'DeepJetCore.compiled.indata',
    extra_compile_args=cpp_compiler_flags,
    sources=[os.path.join(COMPILEPATH, 'src', 'helper.cpp'),
             os.path.join(INTERFACEPATH,
                          'helper_wrap.cxx')],
    include_dirs=cpp_lib_dirs,
    libraries=['python2.7'])

cpp_friendTreeInjector = Extension(
    'DeepJetCore.compiled.indata',
    extra_compile_args=cpp_compiler_flags,
    sources=[os.path.join(COMPILEPATH, 'src',
                          'friendTreeInjector.cpp'),
             os.path.join(INTERFACEPATH,
                          'friendTreeInjector_wrap.cxx')],
    include_dirs=cpp_lib_dirs,
    libraries=['python2.7'])

boost_include_dirs = [os.path.join(CONDA_PREFIX, 'include')]
module_lib_dirs = [
    os.path.join(CONDA_PREFIX, 'lib'), PYCONFIG_PATH,
    os.path.join(COMPILEPATH, 'interface'),
]
module_compiler_flags = root_flags + ['-fPIC', '-Wl', '--export-dynamic']

c_meanNormZeroPad = Extension(
    'DeepJet.compiled.c_meanNormZeroPad',
    extra_compile_args=module_compiler_flags,
    sources=[os.path.join(COMPILEPATH, 'src',
                          'c_meanNormZeroPad.c')],
    include_dirs=module_lib_dirs,
    runtime_library_dirs=[boost_include_dirs],
    libraries=['boost_python', 'python3.6m'])

c_makePlots = Extension(
    'DeepJet.compiled.c_makePlots',
    extra_compile_args=module_compiler_flags,
    sources=[os.path.join(COMPILEPATH, 'src',
                          'c_makePlots.c')],
    include_dirs=module_lib_dirs,
    runtime_library_dirs=[],
    libraries=['boost_python', 'python2.7'])

c_makeROCs = Extension(
    'DeepJet.compiled.c_makeROCs',
    extra_compile_args=module_compiler_flags,
    sources=[os.path.join(COMPILEPATH, 'src',
                          'c_makeROCs.c')],
    include_dirs=module_lib_dirs,
    runtime_library_dirs=[],
    libraries=['boost_python', 'python2.7'])

c_readArrThreaded = Extension(
    'DeepJet.compiled.c_readArrThreaded',
    extra_compile_args=module_compiler_flags,
    sources=[os.path.join(COMPILEPATH, 'src',
                          'c_readArrThreaded.c')],
    include_dirs=module_lib_dirs,
    runtime_library_dirs=[],
    libraries=['boost_python', 'python2.7'])

c_randomSelect = Extension(
    'DeepJet.compiled.c_randomSelect',
    extra_compile_args=module_compiler_flags,
    sources=[os.path.join(COMPILEPATH, 'src',
                          'c_randomSelect.c')],
    include_dirs=module_lib_dirs,
    runtime_library_dirs=[],
    libraries=['boost_python', 'python2.7'])

setup(name='DeepJetCore',
      version='0.0.5',
      description='The DeepJetCore Library: Deep Learning \
      for High-energy Physics',
      url='https://github.com/DL4J/DeepJetCore',
      author='CERN - CMS Group (EP-CMG-PS)',
      author_email='swapneel.mehta@cern.ch',
      license='Apache',
      long_description=retrieveReadmeContent(),
      packages=['DeepJetCore', 'DeepJetCore.preprocessing',
                'DeepJetCore.training', 'DeepJetCore.evaluation',
                'DeepJetCore.compiled'],
      scripts=['./DeepJetCore/bin/plotLoss.py',
               './DeepJetCore/bin/plotLoss.py',
               './DeepJetCore/bin/batch_conversion.py',
               './DeepJetCore/bin/check_conversion.py',
               './DeepJetCore/bin/convertFromRoot.py',
               './DeepJetCore/bin/predict.py',
               './DeepJetCore/bin/addPredictionLabels.py',
               './DeepJetCore/bin/convertDCtoNumpy.py',
               './DeepJetCore/bin/convertToTF.py'],
      python_requires='~=3.6',
      install_requires=[
                'absl-py==0.2.2',
		'astor==0.6.2',
		'bleach==1.5.0',
		'cycler==0.10.0',
		'funcsigs==1.0.2',
		'gast==0.2.0',
		'grpcio==1.12.1',
		'h5py==2.8.0',
		'html5lib==0.9999999',
		'keras==2.2.0',
		'keras-applications==1.0.2',
		'keras-preprocessing==1.0.1',
		'kiwisolver==1.0.1',
		'markdown==2.6.11',
		'matplotlib==2.2.2',
		'mock==2.0.0',
		'pbr==4.0.4',
		'protobuf==3.5.2.post1',
		'pyparsing==2.2.0',
		'python-dateutil==2.7.3',
		'pytz==2018.4',
		'pyyaml==3.12',
		'tables==3.4.3',
		'tensorboard==1.8.0',
		'tensorflow==1.8.0',
		'termcolor==1.1.0',
		'werkzeug==0.14.1'
      ],
      include_package_data=True,
      zip_safe=False,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: Apache Software License',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Operating System :: Unix',
          'Programming Language :: Python :: 2.7',
      ],
      keywords='deep-learning physics jets cern cms',
      project_urls={
          'Documentation': 'https://github.com/SwapneelM/DeepJetCore/wiki',
          'Source': 'https://github.com/SwapneelM/DeepJetCore',
      },
      cmdclass={
          'build_ext': DeepJetCoreBuildExt,
      },
      ext_modules=[
          quicklz,
          ])
'''
cpp_helper,
cpp_indata,
cpp_friendTreeInjector,
c_randomSelect,
c_makeROCs,
c_meanNormZeroPad,
c_makePlots,
c_readArrThreaded,
'''
