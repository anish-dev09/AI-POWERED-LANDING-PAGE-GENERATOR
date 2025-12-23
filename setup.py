from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="landing-page-generator",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-Powered Landing Page Generator for Businesses",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/landing-page-generator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Framework :: FastAPI",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "landing-page-generator=app.main:main",
        ],
    },
)
