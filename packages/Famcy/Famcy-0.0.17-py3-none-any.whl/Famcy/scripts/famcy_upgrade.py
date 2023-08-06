import subprocess
import pkg_resources
from Famcy import famcy_dir

def main(args):
	famcy_id = args[0]
	_ = subprocess.check_output(["pip3", "install", "Famcy", "--upgrade"]) 
	print("Famcy version after upgrade: ", pkg_resources.require("Famcy")[0].version)
	_ = subprocess.check_output(["bash", famcy_dir+"/scripts/bash/"+"relink.sh", famcy_dir, famcy_id]) 