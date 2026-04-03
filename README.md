# Ghid Setup Server Lineage 2 Interlude pe NVIDIA Jetson (ARM64)

Acest ghid te ajută să configurezi un server L2J stabil pe hardware NVIDIA Jetson.

## 📋 Cerințe Sistem
- **Hardware**: NVIDIA Jetson Orin/Xavier/Nano (Min. 4GB RAM recomandați).
- **OS**: JetPack (Ubuntu 기반).
- **Stocare**: Minim 10GB spațiu liber pe SSD/NVMe.

## 🛠️ Pași de Instalare

### 1. Actualizare și Dependențe
Rulează aceste comenzi în terminalul Jetson-ului:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git wget zip unzip curl openjdk-11-jdk mariadb-server
```

### 2. Configurare Bază de Date (MariaDB)
```bash
sudo mysql_secure_installation
# Setup DB pentru L2
sudo mysql -u root -p
CREATE DATABASE l2jdb;
CREATE USER 'l2j'@'localhost' IDENTIFIED BY 'parola_serverului';
GRANT ALL PRIVILEGES ON l2jdb.* TO 'l2j'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Server Files (Java)
Pentru "Classic Interlude", recomandăm un pack bazat pe Java.
1. Download-ează pack-ul (`L2J_Server.zip`).
2. Dezarhivează-l pe Jetson.
3. Configurează `config/loginserver.properties` și `config/gameserver.properties` cu IP-ul tău local.

## 🚀 Optimizări Performanță
Jetson împarte RAM-ul între CPU și GPU. Vom limita memoria Java pentru a nu bloca sistemul:
- În scriptul de start (`gs.sh`): Setează `-Xms512m -Xmx2g` (pentru Jetson de 4GB).
