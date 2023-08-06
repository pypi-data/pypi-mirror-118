from setuptools import setup, find_packages

def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]
req = parse_requirements('./requirements.txt')

setup(
name='arsr', # 패키지 명

version='2.0.1',

description='Arbitrary Scale Super resolution',

author='epsilon',

author_email='kokomong1316@gmail.com',

url='https://github.com/epsilon-deltta/arbitrary-sr/',

license='MIT', # MIT에서 정한 표준 라이센스 따른다

py_modules=[''], # 패키지에 포함되는 모듈

python_requires='>=3',

install_requires=req, # 패키지 사용을 위해 필요한 추가 설치 패키지

# packages=['arsr'] # 패키지가 들어있는 폴더들
packages=find_packages(exclude=['tests']),

long_description=open('README.md').read(),
long_description_content_type='text/markdown'
)

# setup(
#     name='mypackage',
#     version='0.0.1',
#     packages=['mypackage'],
#     install_requires=[
#         'requests',      # 최신버전 설치
#         'pandas >= 2.0', # 버전 특정
#         "pywin32 >= 1.0;platform_system=='Windows'", # 플랫폼 구분
#         'importlib; python_version >= "3.5"',
#     ],
# )