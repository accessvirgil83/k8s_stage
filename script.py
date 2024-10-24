import os


os.system("swapoff -a && sed -i '/swap/d' /etc/fstab")
os.system("modprobe br_netfilter && sysctl net.bridge.bridge-nf-call-iptables=1 && sudo sysctl net.ipv4.ip_forward=1")
os.system('echo "net.bridge.bridge-nf-call-iptables=1" | sudo tee -a /etc/sysctl.conf')
os.system('echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf')
os.system('echo "br_netfilter" | sudo tee -a /etc/modules-load.d/k8s.conf')
os.system("modprobe br_netfilter")
os.system("curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.21.2/bin/linux/amd64/kubectl && chmod +x kubectl && sudo mv kubectl /usr/local/bin/")
os.system("curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.21.2/bin/linux/amd64/kubelet && chmod +x kubelet && mv kubelet /usr/local/bin/")
os.system("curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.21.2/bin/linux/amd64/kubeadm && chmod +x kubeadm && mv kubeadm  /usr/local/bin/")
#sudo nano /etc/systemd/system/kubelet.service
st="""
[Unit]
Description=Kubelet
After=network.target

[Service]
ExecStart=/usr/local/bin/kubelet
Restart=always
StartLimitInterval=0

[Install]
WantedBy=multi-user.target
"""
open("/etc/systemd/system/kubelet.service".'w').write(st)

#sudo apt-get install -y docker.io

os.system("apt-get install docker-ce=5:20.10.15~3-0~ubuntu-jammy docker-ce-cli=5:20.10.15~3-0~ubuntu-jammy containerd.io docker-compose-plugin -y")
os.system("systemctl enable docker")
os.system("systemctl daemon-reload && systemctl restart docker && chmod 777 /var/run/docker.sock")
os.system("kubeadm init --pod-network-cidr=10.244.0.0/16 --upload-certs")

