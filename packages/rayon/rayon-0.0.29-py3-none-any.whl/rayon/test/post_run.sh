#!/usr/bin/env bash
# POST a FASTA file as sequence or alignment.
RUN_DOC="
Usage:
      post_run.sh  [-v] POSITIVES EMAIL TITLE [CODE]
             where
                       -v will cause the returns to be printed.
                       POSITIVES is a file containing the list of positives
                       EMAIL is the email address
                       TITLE is the title for the run
                       CODE is the expected HTTP code for this request
                            (200 if not specified).

Example:
         ./post_run.sh -v joel@generisbio.com "diabetes" diabetes.txt 200

Options:
      -v   verbose mode, shows all returns.

 Before running this script, the rayon server should be started, and the
 environmental variables RAYON_CURL_ARGS and RAYON_CURL_URL
 must be defined.
"
set -e
ARGS="$@"
error_exit() {
   >&2 echo ""
   >&2 echo "\nERROR--unexpected exit from ${BASH_SOURCE} script at line:"
   >&2 echo "   $BASH_COMMAND"
   >&2 echo "   with arguments \"${ARGS}\"."
}
#
# Parse option (verbose flag)
#
_V=0 
while getopts "v" OPTION
do
   case ${OPTION} in
     v) _V=1
	shift
        ;;
   esac
done
#
# Get environmental variables.
#
source ~/.rayon/rayon_rc
#
# Parse arguments
#
if [ "$#" -lt 3 ]; then
	>&2 echo "$RUN_DOC"
	exit 1
fi
if [ ! -f "$1" ] ; then
	>&2 echo "POSITIVES must specify a readable file of positives."
	>&2 echo "$RUN_DOC"
	exit 1
fi
if [ -z "$2" ] ; then
	>&2 echo "Must give an email address."
	>&2 echo "$RUN_DOC"
	exit 1
fi
if [ -z "$3" ] ; then
	>&2 echo "Must give a run title."
	>&2 echo "$RUN_DOC"
	exit 1
fi
if [ -z "${4}" ] ; then
   code="200"
else
   code="${4}"
fi
trap error_exit EXIT
#
# Issue the POST.
#
full_target="/calculate"
tmpfile=$(mktemp /tmp/post_run.XXX)
status=$(curl ${RAYON_CURL_ARGS} -s -o ${tmpfile} -w '%{http_code}' \
         -F "positives=@${1}" \
         -F "email=${2}" \
         -F "title=${3}"
         ${RAYON_CURL_URL}${full_target})
if [ "${status}" -eq "${code}" ]; then
   if [ "$_V" -eq 1 ]; then
      echo "POST of ${2} to ${full_target} returned HTTP code ${status} as expected."
      echo "Response is:"
      cat ${tmpfile}
      echo ""
   fi
   rm "$tmpfile"
else
   >&2 echo "ERROR--POST of ${1} to ${full_target} returned HTTP code ${status}, expected ${code}."
   >&2 echo "Full response is:"
   >&2 cat ${tmpfile}
   >&2 echo ""
   rm "$tmpfile"
   trap - EXIT
   exit 1
fi
trap - EXIT