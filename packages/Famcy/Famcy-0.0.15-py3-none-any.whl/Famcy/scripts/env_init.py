import subprocess
from Famcy import famcy_dir

def main(args):
	famcy_id = args[0]
	_ = subprocess.check_output(["bash", famcy_dir+"/scripts/bash/"+"init.sh", famcy_id]) 