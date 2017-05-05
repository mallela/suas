#! /bin/bash
echo "enter teammate"
read name
if [ 'odroid' == "$name" ];then
	echo 'hello'
	rsync -avzhe ssh /home/ghost/hello.py odroid@10.42.0.1:/home/$name/saurabh/
fi
if [ 'ghost' == "$name" ]; then
	echo 'path to ghost set'

fi
LOCATION="./targets1" #don't add / at the end
PREVCOUNT=0
rsync -avzhe ssh /home/praneeta/suas/System0/targets1/ $name@10.42.0.20:/home/$name/suas/System1/targetsMAIN/ # keep the/ at end
while((1))
do
FILECOUNT=0

for item in $LOCATION/*
do
if [ -f "$item" ]
    then
         FILECOUNT=$[$FILECOUNT+1]
    elif [ -d "$item" ]
        then
         DIRCOUNT=$[$DIRCOUNT+1]
fi
done
echo "File count: " $FILECOUNT
echo "PREV Count:" $PREVCOUNT
if [ "$PREVCOUNT" -lt "$FILECOUNT" ];then 
	rsync -avzhe ssh /home/praneeta/suas/System0/targets1/ $name@10.42.0.20:/home/$name/suas/System1/targetsMAIN/ # keep the/ at end
	#rsync -avzh allcrops/ junk2
	PREVCOUNT=$FILECOUNT
	
fi

done