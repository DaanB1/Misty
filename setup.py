from distutils.core import setup

requires = [           
          'requests>=2.25.1',
          'websocket-client<=0.57.0',
          'yapf>=0.30.0'
]

setup(
  name = 'Misty-SDK',
  packages = ['mistyPy'],
  version = '0.1',
  license='apache-2.0',
  description = 'Python SDK for Misty 2 Robots',
  author = 'Misty Robotics',
  author_email = 'engineering.admin@mistyrobotics.com',
  url = 'https://www.mistyrobotics.com/',
  install_requires=requires,
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
  project_urls={'Documentation': 'https://docs.mistyrobotics.com/',
  'Source': 'https://github.com/MistyCommunity/Python-SDK',
  },
  python_requires=">=3.8",
)