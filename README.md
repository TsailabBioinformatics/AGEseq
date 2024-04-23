# AGEseq: Analysis of Genome Editing by Sequencing

AGEseq is a robust tool designed to compare amplicon sequences with expected target sequences to detect insertion or deletion events within the amplicon sequences. Developed initially in Perl and utilizing BLAT for high-accuracy sequence alignment, AGEseq is now available both as a command-line tool, docker, and through user-friendly interfaces on Galaxy and a Streamlit app.

## Features

- Detects insertions and deletions (indels) in amplicon sequences.
- Compares amplicon sequences against expected target sequences.
- Utilizes BLAT for precise sequence alignment.
- Accessible via command-line, Galaxy, or a Streamlit app GUI.

## Getting Started

### Prerequisites

Before installing AGEseq, ensure you have the following:
- Perl (version 5.10 or higher)
- BLAT alignment tool
- Python (version 3.6 or higher) if using the Streamlit app
- Docker (optional, for containerized version)

### Installation

#### Local Installation
Clone the repository:
```bash
git clone https://github.com/your-lab/AGEseq
cd AGEseq
```
#TODO

#### Galaxy Installation
To use AGEseq on Galaxy, import it as a tool within your local Galaxy instance. Ensure your Galaxy instance is set up to handle external tools.

#### Streamlit App GUI
The Streamlit app can be run locally or deployed on a server:
```
streamlit run app.py
```

### Usage
#### Command-Line Interface
To use AGEseq from the command line:
```
perl ageseq.pl --target=target.fa --amplicon=amplicon.fa
```

#### Using Galaxy
Add AGEseq to your Galaxy toolbox and follow the interface prompts to input your sequences and run the analysis.

#### Streamlit App GUI
Navigate to the URL where your Streamlit app is hosted, and use the graphical interface to upload sequences and analyze results.

#### Contributing
We welcome contributions from the community, including bug fixes, enhancements, and documentation improvements. If you are looking to contribute:

1. Fork the repository.
2. Create a new branch for your feature (git checkout -b feature-branch).
3. Commit your changes (git commit -am 'Add some feature').
4. Push to the branch (git push origin feature-branch).
5. Open a new Pull Request.

### Support
For support and bug reports, please submit an issue on the GitHub issue tracker.

### Citation
If you use AGEseq in your research, please cite our paper:
Xue LJ, Tsai CJ. AGEseq: Analysis of Genome Editing by Sequencing. Mol Plant. 2015 Sep;8(9):1428-30. doi: 10.1016/j.molp.2015.06.001. Epub 2015 Jun 6. PMID: 26057235.
