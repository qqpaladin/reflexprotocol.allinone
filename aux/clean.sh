# ./$ FOLDER NUMMACH

# this command invokes reflex and react scripts to parse
# trace files for machine NUMMACH contained in folder FOLDER
#
# all output is then contained in a subfolder within FOLDER
# so plots can be quickly regenerated without parsing traces

if [ ! -d $1 ]
then
  echo "no such directory"
  exit 0
fi

cd $1

rm -r .*

