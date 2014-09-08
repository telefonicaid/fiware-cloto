error=`python fiware-pep8.py . | wc -l`
echo "checkstyle is :"
ans=$(( 100 - (100,00 * error / 14000) ))
echo $ans

