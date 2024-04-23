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


# Galaxy Server Setup Guide
This guide provides instructions for setting up and configuring a Galaxy server for data analysis, workflow authoring, training, and education purposes. Galaxy is an open-source platform widely used in the scientific community, particularly in fields such as bioinformatics and genomics.

## System Requirements
To run Galaxy, ensure your system meets the following requirements:
- UNIX/Linux or Mac OSX operating system
- Python 3.8 or newer

## Installation
If you don't have a Galaxy repository yet, clone the repository using the following command: \
``` git clone -b release_23.2 https://github.com/galaxyproject/galaxy.git ```

## Starting Galaxy Server
To start the Galaxy server, follow these steps:
- Navigate to the Galaxy directory.
- Run the following command in a terminal window:
``` sh run.sh ```
This will start Galaxy on localhost using the default port 8080.

## Hosting on a Remote Server
If you want to access Galaxy from a local browser or host it on a remote server, follow these steps:
- Inside the config/ directory, locate  `galaxy.yml.sample` and rename it to `galaxy.yml`.
- Edit the `galaxy.yml` file and enable Gunicorn by setting the enable parameter to true and specifying the IP address and port to bind to:
  ```
  gunicorn:
   enable: true
   bind: 172.30.18.104:8091
  ```
- Restart Galaxy by running:
``` sh run.sh ``` \
You should now be able to access Galaxy from a browser using the specified URL. 

## Hosting on a Remote Server
To add custom tools to Galaxy, follow these steps:

- Navigate to the `tools` directory in the Galaxy installation.
- Create a new directory for your tools (e.g., myTools) and place the tool script and its XML definition file inside this directory.
- Update the `tool_conf.xml` file located in the `config/` directory to include the new tool:
```
  <section name="Custom Tools" id="myTools">
    <tool file="myTools/your_tool.xml" />
  </section>
      
```
- Restart Galaxy to apply the changes.

## Running Galaxy as a Service
To run Galaxy as a service indefinitely, follow these steps:
- Create a systemd service file by typing:
``` sudo nano /lib/systemd/system/galaxy.service ```
- Paste the following configuration into the file:
```
[Unit]
Description=Galaxy
After=multi-user.target

[Service]
User=tsai-apps
WorkingDirectory=/data/galaxy
ExecStart=sh /data/galaxy/run.sh
Restart=on-failure
KillMode=process
LimitMEMLOCK=infinity
LimitNOFILE=65535
Type=simple

[Install]
WantedBy=multi-user.target

```
- Save the file and exit the editor.
- Set appropriate permissions for the service file:
``` sudo chmod 644 /lib/systemd/system/galaxy.service  ```
- Reload systemd to recognize the new service:
``` sudo systemctl daemon-reload  ```
- Enable the Galaxy service to start on boot:
``` sudo systemctl enable galaxy.service  ```
- Start the Galaxy service:
```  sudo systemctl start galaxy.service  ```
- Check the status of the Galaxy service to ensure it's running:
```  sudo systemctl status galaxy.service ```

## Accessing Galaxy
- Galaxy is accessible via the following URL: http://tsailab.gene.uga.edu:8091/
- The Galaxy server is currently hosted on the following IP address: 172.30.18.104
- Code Location: ``` /data/galaxy  ```

## Reference documentation
- https://galaxyproject.org/admin/get-galaxy/
- https://galaxyproject.org/admin/tools/add-tool-tutorial/


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
