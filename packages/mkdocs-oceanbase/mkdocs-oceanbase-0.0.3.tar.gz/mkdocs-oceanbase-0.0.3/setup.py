from setuptools import setup, find_packages

setup(
    name="mkdocs-oceanbase",
    version='0.0.3',
    url='',
    license='',
    description='oceanbase static site theme',
    author='zhouzi',
    author_email='3222676446@qq.com',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'mkdocs.themes': [
            'oceanbase_theme = oceanbase_theme',
        ]
    },
    zip_safe=False
)
