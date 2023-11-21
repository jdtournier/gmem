from setuptools import setup

setup(name='gmem',
    version='0.1',
    description='simple terminal memory monitor',
    url='http://github.com/jdtournier/gmem',
    author='J-Donald Tournier',
    author_email='jdtournier@gmail.com',
    license='MIT',
    packages=['gmem'],
    install_requires=[
      'plotext',
      ],
      entry_points={
        'console_scripts': ['gmem=gmem.command_line:main'],
        },
      include_package_data=True,

      zip_safe=False)

