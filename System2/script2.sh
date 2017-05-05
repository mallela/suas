#!/bin/bash
watch -n 60 ls -ltr	
rsync -avzhe Junk1 Junk2	
#rsync -avzhe ssh From_Camera odroid@10.42.0.1:/home/odroid/images/
