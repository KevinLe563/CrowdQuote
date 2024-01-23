### CrowdQuote

Web application that uses computer vision to allow uses to check the population in tracked locations.


rm -rf datasets; rm -rf runs; rm *.out; rm yolo*.pt;


python ./CrowdQuote/ComputerVision-Subsystem/training/train.py --data ./VisDrone.yaml --weights yolov8s.pt --epochs 100 --img-size 640


$ scp -r ece_498_fydp4@ece-nebula07.eng.uwaterloo.ca:/slurm_nfs/ece_498_fydp4/runs/detect/train* .