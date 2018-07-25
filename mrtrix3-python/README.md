1. install: 
    - awscli
	- fsl
	- mrtrix 
	
2. config 
    - awscli  
	    - run "aws configure"
	    - enter the AWS Access Key ID and Secret Access Key provided by HCP 
			
			
3. You may be able to edit out/configure hcpDTI.getenv() to you fsl/mrtrix/aws bin/libs. My editor wasn't loading personal .bashrc so I manually loaded paths. Last script we added some code at the beginning to load fsl, that should go in .bashrc

4. "python hcpDTI.py --subNum '100307' --subsDir '/media/richard/camcan/Projects/LLNL_DTI'"


Haven't run all the way through yet and needs better logging and handling of failed steps. 