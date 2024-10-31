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
Restart=always
StartLimitInterval=0
Environment="KUBELET_KUBECONFIG_ARGS=--bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf --kubeconfig=/etc/kubernetes/kubelet.conf"
Environment="KUBELET_CONFIG_ARGS=--config=/var/lib/kubelet/config.yaml"
# This is a file that "kubeadm init" and "kubeadm join" generate at runtime, populating
# the KUBELET_KUBEADM_ARGS variable dynamically
EnvironmentFile=-/var/lib/kubelet/kubeadm-flags.env
# This is a file that the user can use for overrides of the kubelet args as a last resort. Preferably,
# the user should use the .NodeRegistration.KubeletExtraArgs object in the configuration files instead.
# KUBELET_EXTRA_ARGS should be sourced from this file.
EnvironmentFile=-/etc/default/kubelet
ExecStart=/usr/local/bin/kubelet $KUBELET_KUBECONFIG_ARGS $KUBELET_CONFIG_ARGS $KUBELET_KUBEADM_ARGS $KUBELET_EXTRA_ARGS

[Install]
WantedBy=multi-user.target
"""
open("/etc/systemd/system/kubelet.service",'w').write(st)

os.system("apt-get update && apt-get install ca-certificates && apt-get install curl -y  && apt-get install gnupg  && apt-get install lsb-release")
os.system("mkdir -p /etc/apt/keyrings")
os.system("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg")
os.system('echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null')
os.system('apt-get update') #обязательно!!!
os.system("apt-get install docker-ce=5:20.10.15~3-0~ubuntu-jammy docker-ce-cli=5:20.10.15~3-0~ubuntu-jammy containerd.io docker-compose-plugin -y")
os.system("systemctl enable docker")
os.system("systemctl daemon-reload && systemctl restart docker && chmod 777 /var/run/docker.sock")
os.system("sudo apt-get install -y ethtool socat conntrack")
os.system("sudo systemctl enable kubelet.service")
os.system("kubeadm init --pod-network-cidr=10.244.0.0/16 --upload-certs")
os.system("mkdir -p $HOME/.kube")
os.system("sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config")
os.system("sudo chown $(id -u):$(id -g) $HOME/.kube/config")
#установка сетевого плагина
#kubectl apply -f https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/k8s-manifests/kube-flannel.yml"</span>)
os.system("sudo kubectl apply -f https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml")
