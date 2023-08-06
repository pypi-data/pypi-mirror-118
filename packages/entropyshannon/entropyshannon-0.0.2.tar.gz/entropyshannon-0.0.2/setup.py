from setuptools import setup,find_packages


setup(
    name='entropyshannon',
    version='0.0.2',
    description='A python package for various  type of entropy calculations(Specially Shannon)',
    long_description=open('README.md',encoding='UTF-8').read(),
    long_description_content_type='text/markdown',
    author='Kalana Mihiranga',
    author_email='kalanam217@gmail.com',
    license='MIT',
    keywords=['entropy', 'shannon', 'calculator'],
    url='https://github.com/ffalpha/Entropy-Calucalator',
    packages=find_packages()
  )