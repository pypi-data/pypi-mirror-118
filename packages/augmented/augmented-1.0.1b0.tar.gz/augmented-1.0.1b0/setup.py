from setuptools import setup, find_packages, find_namespace_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: BSD License'
]

setup(
    name='augmented',
    version='1.0.1b',
    description='Augmented reality in python made easy',
    long_description=open('README.txt').read() + '\n\n' +
    open('CHANGELOG.txt').read(),
    long_description_content_type="text/markdown",
    url='https://www.github.com/sarangt123/ar-python',
    author='Sarang T (github.com/sarangt123)',
    author_email='sarang.thekkedathpr@gmail.com',
    license='BSD-3-Clause License',
    classifiers=classifiers,
    keywords='Augmented reality',
    install_requires=["numpy==1.19.5",
                      "opencv-python==4.2.0.34", "keyboard==0.13.5"],
    packages=find_packages(),
    python_requires=">=3.6"

)
