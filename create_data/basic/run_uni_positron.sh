#!/bin/bash
source ../setup.sh

source ${TAOOFFLINE}/quick_setup.sh
energy=${1}
version=${2}
seed=$[$version+7]
root_file_name=${DATAPATH}/uni_ibd/ibd_${energy}MeV_v${version}.root

python ${TAOOFFLINE}/Simulation/DetSim/TaoSim/share/run.py \
--output ${root_file_name} --particles e+ --momentums ${energy} \
--evtmax 2000 --seed $[${version}+7] \
--volume GdLS_phys \
--momentums-interp KineticEnergy \
--run ${CREATEDATAPATH}/mac/run.mac 
