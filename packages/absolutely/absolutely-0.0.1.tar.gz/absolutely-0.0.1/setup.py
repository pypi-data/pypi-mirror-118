from setuptools import setup, find_packages

with open('README.md', 'r') as readme_file:
    readme = readme_file.read()

requirements = ['numpy', 'pandas']

setup(
    name='absolutely',
    version='0.0.1',
    author='Fusion Power AI',
    author_email='admin@fusionpower.ai',
    description='A/B testing complete experimentation arena in Python',
    long_description=readme,
    long_description_content_type='text/markdown',
    keywords=[],
    url='https://github.com/fpai/absolutely',
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
    # package_data={'datasets': ['absolutely/resources/*']},
    classifiers=[
        'Programming Language :: Python :: 3.9',
    ],
)
