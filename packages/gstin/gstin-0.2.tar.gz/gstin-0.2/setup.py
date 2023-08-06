import setuptools

# Reads the content of your README.md into a variable to be used in the setup below
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'gstin',    
  version = '0.2',        
  packages = ['gstin'],
  license='MIT',        
  description = 'Package to retrieve INDIA PAN from GSTIN',   
  author = 'Rashmi Rao',
)