qe="/path/to/your/qe/installation/bin"
ncore=6

cwd=`pwd`

cd pp
./download_pp.sh
cd ${cwd}

cd 01scf
OMP_NUM_THREADS=1 mpirun -np ${ncore} ${qe}/pw.x    < input.in > out.o
cd ${cwd}

cd 02nscf
cp -r ../01scf/out .
OMP_NUM_THREADS=1 mpirun -np ${ncore} ${qe}/pw.x    < input.in > out.o
cd ${cwd}

cd 03bands
cp -r ../01scf/out .
OMP_NUM_THREADS=1 mpirun -np ${ncore} ${qe}/pw.x    < input.in > out.o
#OMP_NUM_THREADS=1 mpirun -np ${ncore} ${qe}/pw.x    < input_fine.in > out.o
cd ${cwd}

cd 04plotbands
cp -r ../03bands/out .
OMP_NUM_THREADS=1 mpirun -np ${ncore} ${qe}/bands.x < input.in > out.o
cd ${cwd}

python plotbands.py
