from setuptools import setup, find_packages

setup(
    name='ktestpy',
    version='0.2',
    description='This is a common test framework support for both UI and API test with run in parallel ability.',
    author='kevin.cai',
    author_email='testertalk@outlook.com',
    zip_safe=False,
    include_package_data=True,
    install_requires=[
                    'requests',
                    'selenium'
    ],
    license='MIT',
    url='https://www.testertalk.com',
    packages=find_packages(),
    entry_points={
            'console_scripts':[
                'ktestpy = ktestpy.main:main'
            ]
         }
)