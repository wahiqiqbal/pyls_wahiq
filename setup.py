from setuptools import setup, find_packages

setup(
    name="pyls",
    version="0.2",
    description="An executable of pyls command",
    author="Wahiq Iqbal",
    author_email="jigarwahiq@gmail.com",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pyls=pyls:main',  # This tells setuptools to use the `main` function in the `pyls` module
        ],
    },
    python_requires='>=3.6',  # Adjust this if needed
)
