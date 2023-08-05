import setuptools
from pathlib import Path

setuptools.setup(
    name='gym_dofbot',
    version='0.1.1',
    author="Charles Xu",
    author_email="xuzheyuan961124@gmail.com",
    url='https://github.com/CharlesXu1124/gym-dofbot',
    description="A OpenAI Gym Env for Yahboom DOFBOT robotic arm",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include="gym_dofbot*"),
    license='GPL',
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: GNU General Public License v3.0 or later (GPL-3.0-or-later)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["gym_dofbot"],
    install_requires=['gym', 'pybullet', 'numpy']  # And any other dependencies foo needs
)