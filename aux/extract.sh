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

if [ ! -d .$2 ]
then
  mkdir ".$2"
  python ../reflex.py reflex-out-$2.tr > .$2/plot 
  python ../react.py  reflex-stat-$2.tr >> .$2/plot
  mv .*tr .$2
  mv .*sampled .$2
  mv .*gnu .$2
  touch .$2/done
  cd .$2
  sh plot
else
  if [ ! -f .$2/done ]
  then
    rm -r .$2
    echo "cleaned previous run, please re-run command"
  else
    cd .$2
    sh plot
  fi
fi

