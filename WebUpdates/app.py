import streamlit as st
import os
import datetime
import time
import requests
import pandas as pd
from streamlit_js_eval import streamlit_js_eval
import shutil
import subprocess



def apply_styles_to_df(value):
    return 'background-color: #f2f2f2; color: black' if value % 2 == 0 else 'background-color: white; color: black'




def save_files(files):
    # Create a folder with the current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_path = os.path.join("/data/AGEseq/", timestamp)
    os.makedirs(folder_path)

    # Create 'reads' subfolder for .fastq files
    reads_folder_path = os.path.join(folder_path, 'reads')

    os.makedirs(reads_folder_path)


    flag_reads = 0
    flag_targets = 0
    targetFileName = ""
    # Save each uploaded file
    for file in files:
        file_path = os.path.join(folder_path, file.name)
        if file.name.endswith('.fastq') or file.name.endswith('.fa') or file.name.endswith('.fasta') or file.name.endswith('.fq'):
            file_path = os.path.join(reads_folder_path, file.name)
            flag_reads = 1
            
        if file.name.endswith('.txt'):
            targetFileName = file.name
            flag_targets = 1
            
        with open(file_path, 'wb') as f:
            f.write(file.getvalue())
            
    
    if (flag_targets==0 and flag_reads==0) or (flag_targets==0 and flag_reads==1) or (flag_targets==1 and flag_reads==0):
        st.error("Please upload both targets.txt and .fastq files")
        return 0
    else:
        st.success("Files uploaded successfully")
        return timestamp, targetFileName


#Clean way to call AGEseq in streamlit
def send_api_request(folder_name, mismatch_cutoff, min_cutoff, wt_like_report, indel_report, targetFileName):
    try:
        # 1. Define Paths
        base_path = "/data/AGEseq"
        working_dir = os.path.join(base_path, folder_name)
        reads_dir = os.path.join(base_path, folder_name,"reads")
        perl_script = os.path.join(base_path, "AGEseq.pl")
        target_file_path = os.path.join(base_path, folder_name, targetFileName)
        output_file = os.path.join(base_path, folder_name, "output.txt")
        st.success(working_dir)
        st.success(target_file_path)
        # 2. Build the Perl Command
        # Note: We pass the arguments in the order the Perl sub 'ageSeq' expects them
        # ($dat_dir, $file_design, $final_out, $mismatch, $min, $wt, $indel)
        cmd = [
            "perl", perl_script,
            reads_dir,          # $dat_dir (where the fastq files are)
            target_file_path,     # $file_design (the .txt target file)
            output_file,          # $final_out
            str(mismatch_cutoff),
            str(min_cutoff),
            str(wt_like_report),
            str(indel_report)
        ]
        
        # 3. Execute the Perl script directly
        # We run this from the base_path so the script can find its 'blat_exe' folder
        result = subprocess.run(cmd, cwd=base_path, capture_output=True, text=True)
        
        if result.returncode != 0:
            st.error(f"Perl Error: {result.stderr}")
            return False
            
        return True

    except Exception as err:
        st.error(f"System Error: {err}")
        return False
    
def read_file_content(file_name):
    prev_size = -1  # Initial size of the file
    i = 0
    
    while True:
        # Get the current size of the file
        curr_size = os.path.getsize(file_name)
    
        # If the size stops changing, start reading the file
        if curr_size == prev_size:
            try:
                data = []
                with open(file_name, 'r') as f:
                    for line in f:
                        if "Sum:" in line and "AlignedTarget" not in line:
                            data.append(line.replace("Sum:", "").replace("\n", "").split('\t'))
    
                columns = ["INPUT", "Target", "AlignedTarget", "AlignedRead", "Total Hits", "Sub Hits",	"Indel or WT Hits",	"Indel or WT rate %",	"Pattern"]
                data_rows = data[:]
                df = pd.DataFrame(data_rows, columns=columns)
                st.write("Output")
                st.write(df)
                return df
            except Exception as e:
                #st.error(f"An error occurred while reading the file: {e}")
                break
    
        prev_size = curr_size
        time.sleep(1)  # Wait for 1 second before checking the file size again
    
    
def print_output_file(folder_path):
    file_name = "/data/AGEseq/"+folder_path+"/output.txt"
    initial_file_size = os.path.getsize(file_name)
    
    #with st.spinner("Generating output..."):
    #time.sleep(5)
    while True:
        current_file_size = os.path.getsize(file_name)
        if current_file_size == initial_file_size:
            break
        else:
            initial_file_size = current_file_size
            time.sleep(1)  # Adjust the sleep duration as needed
        
    df = read_file_content(file_name)
        
    return df
            

    

# Streamlit app
def main():
    st.set_page_config(page_title="AGEseq", page_icon=":microscope:", layout="wide")
    st.markdown(
        """
        <div style="background-color:#154730;padding:10px;border-radius:10px">
            <h1 style="color:white;text-align:center;">AGEseq Analysis</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <style>
        .container-3d {
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px 0px rgba(0,0,0,0.3);
            background-color: #ffffff;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    

    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown('<h6><I>*Upload targets.txt and .fastq files only</I></h6>', unsafe_allow_html=True)
        # File upload
        uploaded_files = st.file_uploader(' ', accept_multiple_files=True)
        
    with col2:
        st.markdown('<h6><b>Mismatch Cutoff</b></h6>', unsafe_allow_html=True)
        mismatch_cutoff = st.slider("mismatch rate to filter low quality alignment, default 0.1 (10%)", min_value=0.0, max_value=1.0, value=0.1, step=0.01)
        st.markdown('<h6><b>Min Cutoff</b></h6>', unsafe_allow_html=True)
        min_cutoff = st.slider("cutoff to filter reads with low abundance, default 0", min_value=0, max_value=100, value=0)
        
    with col3:
        st.markdown('<h6><b>WT-like Report</b></h6>', unsafe_allow_html=True)
        wt_like_report = st.slider("report top xx WT like records, default 20", min_value=0, max_value=100, value=20)
        st.markdown('<h6><b>Indel Report</b></h6>', unsafe_allow_html=True)
        indel_report = st.slider("report top xx records with indel, default 50", min_value=0, max_value=100, value=50)
        #remove_files = st.checkbox("Remove Files", value=True)
        
    if st.button('Refresh'):
        streamlit_js_eval(js_expressions="parent.window.location.reload()")
    
    if uploaded_files:
        # Save files button
        if st.button('Process Files'):
        
            folder_name, targetFileName = save_files(uploaded_files)
            df = None
            if folder_name != 0:  
                with st.spinner("Generating output..."):
                    send_api_request(folder_name, mismatch_cutoff, min_cutoff, wt_like_report, indel_report, targetFileName)
                    df = print_output_file(folder_name)
                    st.success("Analysis completed!")
                    
                    
                    with open(f'/data/AGEseq/{folder_name}/output.txt', "r") as file:
                        content = file.read()
                        
                    #st.link_button(label="Download Output.txt", url=f'/data/AGEseq/{folder_name}/output.txt')
                    st.download_button(label="Download Output.txt", data=content, file_name="Output.txt", mime="text/plain")
                    st.markdown("<h6><b><I>After downloading your output.txt file, please note that the summary will no longer be visible. If you wish to view the summary again, simply click on the 'Process Files' button.</I></b></h6>", unsafe_allow_html=True)
                    
                    
                    folder_path_ = f'/data/AGEseq/{folder_name}'
                    if os.path.exists(folder_path_):
                        shutil.rmtree(folder_path_)
                    else:
                        print("Folder does not exist.")



if __name__ == '__main__':
    main()

