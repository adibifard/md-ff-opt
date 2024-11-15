import os

def write_pd_to_csv(dir,file_name,pd_data):
    out_file_path =os.path.join(dir, file_name)
    try:
        pd_data.to_csv(out_file_path, index=False)
        print(f"DataFrame successfully written to {out_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")