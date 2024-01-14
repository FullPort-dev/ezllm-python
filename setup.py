from setuptools import setup, find_packages

setup(
    name='ezllm',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        # list your package dependencies here
        'requests',
        'python-dotenv'
    ],
    extras_require={
        'extra' : ['pandas']
    },
    description="Enhance your data pipelines with the power of Large Language Models. EzLLM is a developer tool that opens the door to the LLM ecosystem. Automatic webscrapers, natural language data extraction, semantic search and as little as 3 lines of code",
    author="EzLLM",
    author_email="info@fullport.dev",
    url='https://github.com/FullPort-dev/ezllm-python',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    project_urls={
        'Homepage': 'https://ezllm.io',
        'Documentation': 'https://docs.ezllm.io',
        'Source': 'https://github.com/FullPort-dev/ezllm-python',
        'Tracker': 'https://github.com/FullPort-dev/ezllm-python/issues',
        'Developer Console' : 'https://console.ezllm.io',
    },
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)