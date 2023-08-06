from distutils.core import setup
setup(
  name = 'basicpreprocessing',
  packages = ['basicpreprocessing'],
  version = '0.1',
  license='MIT',
  description = 'basicpreprocessing library will be used to do basic preprocessing operations on dataframe',
  author = 'Jaganathan Raja',
  author_email = 'jaganraja479@gmail.com',
  url = 'https://github.com/JaganRaja/basicpreprocessing',
  download_url = 'https://github.com/JaganRaja/basicpreprocessing/archive/refs/tags/0.1.tar.gz',
  keywords = ['eda', 'preprocessing', 'dataframe', 'pandas'],
  install_requires=[
          'numpy',
          'pandas',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)