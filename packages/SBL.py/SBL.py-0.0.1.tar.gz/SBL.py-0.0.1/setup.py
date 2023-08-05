from setuptools import setup,find_packages
import re

def get(
  arg: str
):
  with open(
    'sblpy/__init__.py'
  ) as f:
    return re.search(
      fr'^__{arg}__\s*=\s*[\'"]([^\'"]*)[\'"]',
      f.read(),
      re.MULTILINE
    ).group(
      1
    )

version = get(
  'version'
)

if version.endswith(
  (
    'a',
    'b',
    'rc'
  )
):
  # append version identifier based on commit count
  try:
    import subprocess
    p = subprocess.Popen(
      [
        'git',
        'rev-list',
        '--count',
        'HEAD'
      ],
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE
    )
    out, err = p.communicate()
    if out:
      version += out.decode(
        'utf-8'
      ).strip()
      p = subprocess.Popen(
        [
          'git',
          'rev-parse',
          '--short',
          'HEAD'
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
      )
      out, err = p.communicate()
      if out:
        version += '+g' + out.decode(
          'utf-8'
        ).strip()
  except Exception:
    pass

setup(
  name="SBL.py",
  version=version,
  description="No",
  url="https://github.com/Rishiraj0100/SBL.py",
  author=get(
    'author'
  ),
  license=get(
    'license'
  ),
  classifiers=[
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.8",
  ],
  python_requires=">=3.8",
  keywords="SBL BotList SmartBots",
  packages=find_packages()
)
