from setuptools import setup

with open("README.md", "r") as fh:
    description = fh.read()

setup(
    name="odoo_rest_framework",
    version="1.1.1",
    description="Store user access token for one-time-login",
    long_description=description,
    long_description_content_type="text/markdown",
    packages=['odoo_rest_framework'],
    author="Han Zaw Nyein",
    author_email="hanzawnyineonline@gmail.com",
    zip_safe=False,
    url='https://github.com/HanZawNyein/odoo-rest-framework.git',
    install_requires=['PyJWT', 'simplejson','requests','tzwhere','pytz']
)