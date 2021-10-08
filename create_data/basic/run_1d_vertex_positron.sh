#!/bin/bash
source ../setup.sh
source ${TAOOFFLINE}/quick_setup.sh

energy=${1}
version=${2}
x=${3}
y=${4}
z=${5}
seed=$[${version}+7]
root_file_name=${DATAPATH}/1d_template/ibd_${energy}MeV_x${x}_y${y}_z${z}_v${version}.root

python ${TAOOFFLINE}/Simulation/DetSim/TaoSim/share/run.py \
--output ${root_file_name} --particles e+ \
--momentums ${energy} \
--momentums-mode Uniform \
--momentums-extra-params 4 \
--evtmax 5000 --seed $[${version}+7] \
--positions $[${x}-2450] $[${y}-2450] $[${z}-8600] \
--momentums-interp KineticEnergy \
--run ${CREATEDATAPATH}/mac/run.mac 
