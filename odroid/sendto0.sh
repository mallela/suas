#! /bin/bash
if [ "$1" == 'admin-pc' ];then
	nextSystemPath="/home/admin-pc/suas/System0/targets1/"
	user='sony'
	ip = "23"
elif [ "$1" == 'user' ];then
	nextSystemPath="/home/user/suas/System0/targets1/"
	user="user"
	ip = "83"
elif [ "$1" == 'praneeta' ]; then
	nextSystemPath="/home/praneeta/suas/System0/targets1/"
	ip = "33"
	user='praneeta'
elif [ "$1" == 'ghost' ]; then
	nextSystemPath="/home/ghost/suas/System0/targets1/"
	user='ghost'
	ip = "70"
elif [ "$1" == 'sony' ]; then
	nextSystemPath="/home/sony/suas/System0/targets1/"
	user='sony'
	ip = "20"
else
	echo "invalid parameter"
	exit 1
fi

if [ $2 -ne 0 ];then
	ip=$2
fi
LOCATION="/home/odroid/imageFolder" #don't add / at the end
PREVCOUNT=0
echo "rsync -avzhe ssh /home/odroid/imageFolder/ $user@10.42.0.$ip:$nextSystemPath/"
#rsync -avzhe ssh /home/odroid/imageFolder/ $user@10.42.0.$ip:$nextSystemPath/ # keep the/ at end
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
	rsync -avzhe ssh /home/odroid/imageFolder/ $user@10.42.0.$ip:$nextSystemPath/ # keep the/ at end change it back to 10.42.0 this is for testing.
	#rsync -avzh allcrops/ junk2
	PREVCOUNT=$FILECOUNT
	
fi
sleep 3 # check cpu itilization and add sleep. 
done

