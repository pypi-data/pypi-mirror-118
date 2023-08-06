import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    ld = f.read()

setuptools.setup(
    name="sanime",
    version="0.1",
    description="AniManga wrapper for Anime-Planet.",
    long_description=ld,
    url="https://github.com/centipede000",
    author="Siddhant Kumar",
    author_email="centipedemonster@gmail.com",
    license="MIT",
    packages=setuptools.find_packages(where="src"),
    zip_safe=False,
    package_dir={"":"sanime"},
    python_requires=">=3.6",
)
