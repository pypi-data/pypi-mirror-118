from setuptools import setup

setup(name='schema_learn',
      version='0.1.5.3',
      description='Metric learning based synthesis of heterogeneous modalities',
      
      long_description='Schema is a Python library for the synthesis and integration of multi-modal data. It offers support for the incorporation of more than two modalities and can also simultaneously handle batch effects. Schema is based on a metric learning approach and formulates the modality synthesis problem as a quadratic programming problem.',
      
      url='http://github.com/rs239/schema',
      author='Rohit Singh',
      author_email='rsingh@alum.mit.edu',
      license='MIT',
      packages=['schema', 'schema.datasets'],
      install_requires = 'numpy,scipy,pandas,sklearn,cvxopt,tqdm,scanpy'.split(','),
      zip_safe=False)
