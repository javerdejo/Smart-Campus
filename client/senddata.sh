#!/bin/bash
# Use:
# ./senddata.sh sound.log bluetooth.log wifi.log

SOUND=${1}
BLUETOOTH=${2}
WIFI=${3}

ADD_SOUND="http://150.214.214.19:3000/add/sound"
ADD_BLUETOOTH="http://150.214.214.19:3000/add/bluetooth"
ADD_WIFI="http://150.214.214.19:3000/add/wifi"

# Add sound
echo "Uploading sound data ..."
tail -n +2 $SOUND > .$SOUND.tmp
while read LINE ;
do
   SENSOR_ID=`echo $LINE | cut -d"," -f 1 `
   NOISE=`echo $LINE | cut -d"," -f 3 `
   PEAK=`echo $LINE | cut -d"," -f 4 `
   DATE_TIME=`echo $LINE | cut -d"," -f 2 `
   JSON='{
      "sensor_id":"'$SENSOR_ID'",
      "noise":"'$NOISE'",
      "peak":"'$PEAK'",
      "date_time":"'$DATE_TIME'"
   }'
   curl -X POST \
   -H 'Content-Type: application/json' \
   -d "$JSON" \
   $ADD_SOUND
done < .$SOUND.tmp
rm -f .$SOUND.tmp

# Add bluetooth
echo "Uploading bluetooth data ..."
tail -n +2 $BLUETOOTH > .$BLUETOOTH.tmp
while read LINE ;
do
   SENSOR_ID=`echo $LINE | cut -d"," -f 1 `
   MAC_ADDRESS=`echo $LINE | cut -d"," -f 3 `
   DURATION=`echo $LINE | cut -d"," -f 4 `
   DATE_TIME=`echo $LINE | cut -d"," -f 2 `

   MAC_ADDRESS="$(echo -e "${MAC_ADDRESS}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
   DURATION="$(echo -e "${DURATION}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
   DATE_TIME="$(echo -e "${DATE_TIME}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"

   JSON='{
      "sensor_id":"'$SENSOR_ID'",
      "mac_address":"'$MAC_ADDRESS'",
      "duration":"'$DURATION'",
      "date_time":"'$DATE_TIME'"
   }'
   curl -X POST \
   -H 'Content-Type: application/json' \
   -d "$JSON" \
   $ADD_BLUETOOTH
done < .$BLUETOOTH.tmp
rm -f .$BLUETOOTH.tmp

# Add wifi
echo "Uploading wifi data ..."
tail -n +2 $WIFI > .$WIFI.tmp
while read LINE ;
do
   if [ `echo $LINE | wc -c` -ge 65 ] && [ `echo $LINE | grep "BSSID" | wc -c` -eq 0 ] ; then
      #SENSOR_ID=`echo $LINE | cut -d"," -f 1 `
      SENSOR_ID=1
      MAC_ADDRESS=`echo $LINE | cut -d"," -f 1 `
      FIRST_TIME=`echo $LINE | cut -d"," -f 2 `
      LAST_TIME=`echo $LINE | cut -d"," -f 3 `

      MAC_ADDRESS="$(echo -e "${MAC_ADDRESS}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
      FIRST_TIME="$(echo -e "${FIRST_TIME}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
      LAST_TIME="$(echo -e "${LAST_TIME}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"

      JSON='{
         "sensor_id":"'$SENSOR_ID'",
         "mac_address":"'$MAC_ADDRESS'",
         "first_time":"'$FIRST_TIME'",
         "last_time":"'$LAST_TIME'"
      }'
      curl -X POST \
      -H 'Content-Type: application/json' \
      -d "$JSON" \
      $ADD_WIFI
   fi
done < .$WIFI.tmp
rm -f .$WIFI.tmp

echo "Done :)"
