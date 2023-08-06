import setuptools

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name='pyBloxyCola',
    version='0.1.2',
    description='An Library that interacts with the Roblox API.',
    author="Illgyaz",
    license="BSD 2-clause",
    packages=['pyBloxyCola'],
    install_requires=['requests'],
    url='https://github.com/lucaytpols/pyBloxy',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.8',
    ],
)