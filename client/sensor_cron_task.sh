#!/bin/bash

BIN_DIR=/sensor_client/bin
BACKUP_DIR=/sensor_client/sensorBackup/to_send
PENDING_DIR=/sensor_client/sensorBackup/pending

SOUND_DATA=$BACKUP_DIR/registersound.csv
WIFI_DATA=$BACKUP_DIR/registerwifi.csv
BT_DATA=$BACKUP_DIR/registerbt.csv

#Filter wifi data files and move it
python $BIN_DIR/filter_wifi.py

#Move sound data to backup
python $BIN_DIR/move_sound_to_backup.py

#Move BT data to backup
python $BIN_DIR/move_bt_to_backup.py

#Create unique files to be sent
cat $BACKUP_DIR/registerbt_*.log > $BT_DATA
cat $BACKUP_DIR/registersound_*.log > $SOUND_DATA
rm $BACKUP_DIR/registerbt_*.log
rm $BACKUP_DIR/registersound_*.log

#Send data files to server
python $BIN_DIR/senddata.py -s $SOUND_DATA -b $BT_DATA -w $WIFI_DATA
