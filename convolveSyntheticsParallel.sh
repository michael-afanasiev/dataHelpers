#!/bin/bash -l

#SBATCH --account=ch1
#SBATCH --job-name="convolve synthetics"
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --time=00:30:00
#SBATCH --output=../OUTPUT/slurm_output/preprocessing.%A.%a.o
#SBATCH --error=../OUTPUT/slurm_output/preprocessing.%A.%a.e

export MV2_ENABLE_AFFINITY=0
export KMP_AFFINITY=compact
export OMP_NUM_THREADS=8

if [ "$1" == '' ]; then
  echo "Usage: ./convolveSyntheticsParallel [iteration_name]"
  exit
fi

iterationDir=../$1

shopt -s nullglob

# Get event names.
array=($iterationDir/*)

# Parse name from path.
SLURM_ARRAY_TASK_ID=0
myEvent=${array[$SLURM_ARRAY_TASK_ID]}
seismo_dir=$myEvent/OUTPUT_FILES/

echo ./convolveSourceTimeFunction.py --seismogram_dir $seismo_dir --half_duration 3.805
