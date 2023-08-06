from setuptools import setup

# setup para enviar o pacote para pypi

setup(

	name="my-tube",
	version="1.0.0",
	license="MIT license",
	author="lucas-Dk",
	long_description="Olá, esté pacote te permite baixar videos do youtube",
	author_email="lucas2000bss@gmail.com",
	keywords="pacotes",
	description="my_tube",
	packages=["mytube"],
	install_requires=["pytube"]

	)