---
title: Development
summary: Tips and tricks for charm development.
author: Luca Bello
date: 2023-01-25
---
# Charm Development

## Environment

This page is a collection of ways to simply, quickly and effectively bootstrap a development environment for charming.

### Multipass

[Multipass](https://multipass.run/) allows bootstrapping VMs from YAML files holding their configuration (also called *blueprints*), through `multipass launch --cloud-init <filename>.yaml`. You can find useful blueprints and further instructions in the following resources:

* [canonical/multipass-blueprints](https://github.com/canonical/multipass-blueprints), for a minimal development environment;
* [Abuelodelanada/charm-dev-utils](https://github.com/Abuelodelanada/charm-dev-utils), for complete ready-to-go blueprints.

### LXD

[LXD](https://linuxcontainers.org/lxd/introduction/) allows creating containers or VMs from configuration *profiles*. You can write your own or customize the following one to achieve different things; this section will present an example setup.

#### Minimal Configuration

Read this profile, customize it and save it to *charm-dev.yaml*.

```yaml title="charm-dev.yaml" linenums="1"
name: charm-dev
config:
  boot.autostart: "false"
  limits.cpu: "4" # CPUs to allocate
  limits.memory: 16GiB # Memory to allocate
  security.secureboot: "false"
  # Define the VM users in cloud-config
  user.user-data: |
    #cloud-config
    users:
      - name: ubuntu
        shell: /bin/bash
        groups: lxd
        sudo: ALL=(ALL) NOPASSWD:ALL
description: Light-weight profile for charm development
devices:
  eth0:
    name: eth0
    network: lxdbr0
    type: nic
  # If you have a folder for repositories on your machine,
  # it can be useful to mount it in the VM
  repo-folder:
    path: <path/on/local/machine>
    source: /home/ubuntu/Repositories
    type: disk
  root:
    path: /
    pool: default
    size: 30GB # Disk size to allocate
    type: disk
```

The first time you create a VM, you'll need to run some commands to create the starting configuration and initialize the necessary resources:
```bash
# Create the storage pool (feel free to change its size)
lxc storage create charm-dev-pool btrfs size=100GiB
# Create your chosen profile (in this example, charm-dev)
lxc profile create charm-dev
lxc profile edit charm-dev < charm-dev.yaml
```

After the pool has been created, you'll be able to bootstrap a new VM by running:
```bash
# Launch the machine
lxc launch ubuntu:22.10 --vm charm-dev # --config limits.cpu=4 --config limits.memory=16GiB
# Set the disk size of the machine
lxc config device override charm-dev root size=30GiB
```

You can now open a shell into the VM:
```bash
lxc exec charm-dev -- su --login ubuntu
```

#### Complete Configuration

There are several ways to extend the minimal configuration above to obtain a ready-to-go development environment. One way to do so is to run the following Bash script as `./charm-dev.sh -p lxd`; please read it and adapt it your needs first!
```bash title="charm-dev.sh" linenums="1"
#!/usr/bin/env bash
# Parse arguments
available_profiles="lxd"
usage="Usage: $0 -p <profile>
Available profiles: ${available_profiles}"
profile=""
while getopts p: flag
do
  case "${flag}" in
    p) profile=${OPTARG};;
    ?) echo "${usage}"; exit 1;;
  esac
done
## Check if a profile has been specified
if [[ -z "${profile}" ]]; then echo "(using default profile)" && profile="lxd"; fi
if grep -wqv "${profile}" <<< "${available_profiles}"; then
  echo "The profile doesn't exist!"; echo "${usage}"; exit 3;
fi


# Configuration
## Packages to install
### apt
apt_packages="""
  btop
  git
  jq
  neovim
  python-is-python3
  python3
  ranger
  sshuttle
  tox
  tree
  vim
  zsh
"""
### pip
pip_packages="""
  yq
"""
### snap
snap_commands=(
  "snap install yq"
  "snap install microk8s --channel 1.25-strict/stable"
  "snap alias microk8s.kubectl kubectl"
  "snap install juju --channel=3.0/stable"
  "snap install charmcraft --classic"
  "snap install jhack"
  "snap connect jhack:dot-local-share-juju snapd"
)


# Ask for confirmation
## Summarize changes
echo "---
Profile: ${profile}
---"
echo "The following packages will be installed:"
case "${profile}" in
  lxd) 
    printf "+ apt +\n%s---\n" "${apt_packages}"
    printf "+ pip +\n%s---\n" "${pip_packages}"
    printf "+ snap commands +\n---\n"
    printf "%s\n" "${snap_commands[@]}" && echo "---";;
esac

## Confirmation question
read -p "Continue (y/n)? " choice
case "${choice}" in 
  y|Y ) true;;
  * ) echo "Exiting!"; exit 4;;
esac


# Preliminary operations
## Set passwords
read -p "Set user and root passwords (y/n)? " choice
case "${choice}" in
  y|Y )
    echo "Changing the password for user $USER" && sudo passwd $USER || exit 5
    echo "Changing the password for root" && sudo passwd root || exit 5;;
esac


# Install packages
case "${profile}" in
  lxd)
    echo "+ Installing apt packages +"
    sudo apt update
    sudo apt install ${apt_packages}
    echo "+ Installing pip packages +"
    pip install --user ${pip_packages}
    echo "+ Installing snap packages +"
    for snap_cmd in "${snap_commands[@]}"; do
      eval "sudo $snap_cmd"
    done
    ;;
esac


# Common operations
## Change shell to zsh
read -p "Change default shell to zsh (y/n)? " choice
case "${choice}" in 
  y|Y )
    chsh -s /usr/bin/zsh
    sudo chsh -s /usr/bin/zsh
    ;;
esac
## OhMyZsh install
read -p "Install OhMyZsh (y/n)? " choice
case "${choice}" in 
  y|Y ) 
	# OhMyZsh main script
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
    # Plugins
    git clone https://github.com/zsh-users/zsh-autosuggestions ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions
	git clone https://github.com/zsh-users/zsh-completions ~/.oh-my-zsh/custom/plugins/zsh-completions
	git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting
	sed -i 's/plugins=(git)/plugins=(git zsh-autosuggestions zsh-completions zsh-syntax-highlighting virtualenv colored-man-pages juju colorize)/g' ~ubuntu/.zshrc
	# Themes
	git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ~/.oh-my-zsh/custom/themes/powerlevel10k
	ubuntu sed -i 's/ZSH_THEME="robbyrussell"/ZSH_THEME="powerlevel10k/powerlevel10k"/g' ~ubuntu/.zshrc
	;;
esac
## Charmcraft init
read -p "Do you want to initialize Charmcraft (y/n)? " choice
case "${choice}" in
  y|Y )
    lxd init --auto;;
esac
## MicroK8s init
read -p "Do you want to initialize MicroK8s (y/n)? " choice
case "${choice}" in
  y|Y )
    mkdir -p $HOME/.kube
    sudo usermod -a -G snap_microk8s $USER
    exec su -l $USER
    microk8s config > $HOME/.kube/config
    sudo chown -f -R $USER ~/.kube
    microk8s status --wait-ready
    microk8s enable dns hostpath-storage ingress
    microk8s status --wait-ready
    ;;
esac
## Juju controller bootstrap
read -p "Bootstrap juju *dev* controller (y/n)? " choice
case "${choice}" in
  y|Y )
    juju bootstrap microk8s dev;;
esac
```

### GCP (Google Cloud Platform)

Use the template and instructions provided at [sed-i/tf-gcp](https://github.com/sed-i/tf-gcp/tree/main/charm-dev).

## Tools

There are tools to make your charming experience better:

* [jhack](https://github.com/PietroPasotti/jhack) from [PietroPasotti](https://github.com/PietroPasotti), with a lot of [Discourse topics](https://discourse.charmhub.io/tag/jhack) to get you started

