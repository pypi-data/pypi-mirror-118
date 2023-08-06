from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
        name="call_useragent",
        version="0.0.1",
        author="dream-pioneer",
        author_email="dream.pioneer537@gmail.com",
        url="https://github.com/dream-pioneer/call_useragent",
        description="由于国内网络限制无法使用 fake_useragent 库而制作的替代品",
        long_description=long_description,
        packages=find_packages(),
        long_description_content_type="text/markdown"
        )
