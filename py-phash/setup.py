from distutils.core import setup, Extension

pHashModule = Extension('PypHash',
                    sources = ['phashmodule.C'],
		    language='c++',
		    libraries = ['pHash'])

setup (name = 'PypHash',
       version = '0.1',
       description = 'perceptual hashing',
       ext_modules = [pHashModule])
