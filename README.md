
InfluxDB and Grafana Enterprise Setup with Docker

This guide provides step-by-step instructions to install Docker and set up InfluxDB and Grafana Enterprise using Docker containers.

---

## Step 1: Install Docker

### On Linux (Ubuntu/Debian)

1. Update your package list:
   ```bash
   sudo apt update
 

2. Install dependencies:
   ```bash
   sudo apt install apt-transport-https ca-certificates curl software-properties-common
   ```

3. Add Docker's official GPG key:
   ```bash
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
   ```

4. Add the Docker repository:
   ```bash
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```

5. Update the package list again:
   ```bash
   sudo apt update
   ```

6. Install Docker:
   ```bash
   sudo apt install docker-ce docker-ce-cli containerd.io
   ```

7. Verify Docker installation:
   ```bash
   sudo docker --version
   ```

8. Start and enable Docker:
   ```bash
   sudo systemctl start docker
   sudo systemctl enable docker
   ```


## Step 2: Pull the Docker Images

Pull the official Docker images for InfluxDB and Grafana Enterprise.

```bash
# Pull InfluxDB image
docker pull influxdb:latest

# Pull Grafana Enterprise image
docker pull grafana/grafana-enterprise:latest
```


---

## Step 3: Run the InfluxDB Container

Start the InfluxDB container and attach it to the created network.

```bash
docker run -d \
  --name influxdb \
  --network monitoring-network \
  -p 8086:8086 \
  -v influxdb-data:/var/lib/influxdb2 \
  influxdb:latest
```

### Explanation:
- `-d`: Run the container in detached mode.
- `--name`: Name the container for easy reference.
- `--network`: Attach the container to the `monitoring-network`.
- `-p`: Map port 8086 on the host to port 8086 in the container.
- `-v`: Persist InfluxDB data to a Docker volume.

---

## Step 4: Run the Grafana Enterprise Container

Start the Grafana Enterprise container and connect it to the same network.

```bash
docker run -d \
  --name grafana-enterprise \
  --network monitoring-network \
  -p 3000:3000 \
  -v grafana-data:/var/lib/grafana \
  grafana/grafana-enterprise:latest
```

### Explanation:
- `-d`: Run the container in detached mode.
- `--name`: Name the container for easy reference.
- `--network`: Attach the container to the `monitoring-network`.
- `-p`: Map port 3000 on the host to port 3000 in the container.
- `-v`: Persist Grafana data to a Docker volume.

---

## Step 5: Configure Grafana to Connect to InfluxDB

1. Open Grafana in your browser: `http://localhost:3000`.
2. Log in with the default credentials:
   - Username: `admin`
   - Password: `admin`
3. Add InfluxDB as a data source:
   - Go to **Configuration > Data Sources > Add data source**.
   - Select **InfluxDB**.
   - Set the URL to `http://influxdb:8086`.
   - Configure authentication if required.
   - Click **Save & Test** to verify the connection.

---

## Step 6: Verify the Setup

- Access InfluxDB at `http://localhost:8086` to ensure it's running.
- Access Grafana at `http://localhost:3000` and verify that the InfluxDB data source is working.

---

## Conclusion

You now have Docker installed and InfluxDB and Grafana Enterprise running in Docker containers, ready for monitoring and visualization tasks.


